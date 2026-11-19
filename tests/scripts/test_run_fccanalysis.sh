#!/usr/bin/env bash

set -e -o pipefail

repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
wrapper="${repository_root}/scripts/dirac/run_fccanalysis.sh"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "${temporary_directory}"' EXIT

make_fake_runtime() {
  mkdir -p "${temporary_directory}/bin"
  cat > "${temporary_directory}/setup.sh" <<'EOF'
#!/usr/bin/env bash
runtime_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="${runtime_directory}/bin:${PATH}"
printf '%s\n' "$@" > setup-arguments.txt
EOF
  cat > "${temporary_directory}/bin/fccanalysis" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > arguments.txt
printf '%s\n' "${CONDA_PREFIX:-unset}" > conda-prefix.txt
EOF
  chmod +x "${temporary_directory}/bin/fccanalysis"
  : > "${temporary_directory}/analysis.py"
}

make_fake_payload() {
  local payload_root="${temporary_directory}/payload/fccanalyses-payload"
  mkdir -p "${payload_root}/install/bin" "${payload_root}/.fccana"
  cat > "${payload_root}/setup.sh" <<'EOF'
#!/usr/bin/env bash
export FCCANA_LOCAL_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="${FCCANA_LOCAL_DIR}/install/bin:${PATH}"
EOF
  cat > "${payload_root}/install/bin/fccanalysis" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' shipped > payload-runtime.txt
printf '%s\n' "$@" > payload-arguments.txt
printf '%s\n' "${CONDA_PREFIX:-unset}" > payload-conda-prefix.txt
EOF
  chmod +x "${payload_root}/install/bin/fccanalysis"
  printf '%s\n' "${build_setup}" \
    > "${payload_root}/.fccana/stack_build"
  tar -czf "${temporary_directory}/fccanalyses-payload.tar.gz" \
    -C "${temporary_directory}/payload" fccanalyses-payload
}

make_fake_include_archive() {
  mkdir -p "${temporary_directory}/include-source/include"
  printf '%s\n' 'int answer() { return 42; }' \
    > "${temporary_directory}/include-source/include/functions.h"
  tar -czf "${temporary_directory}/analysis-includes.tar.gz" \
    -C "${temporary_directory}/include-source" include/functions.h
}

assert_file_equals() {
  local path="$1"
  local expected="$2"
  if ! diff -u <(printf '%s' "${expected}") "${path}"; then
    echo "Unexpected content in ${path}" >&2
    exit 1
  fi
}

make_fake_runtime
make_fake_include_archive
build_arch="$(uname -m)"
cat > "${temporary_directory}/worker-env.sh" <<'EOF'
source() {
  local script="$1"
  shift
  if [ "${script}" = /etc/os-release ]; then
    ID=rocky
    VERSION_ID="${TEST_OS_VERSION:-9.6}"
  else
    builtin source "${script}" "$@"
  fi
}
EOF
# Use an equivalent spelling to exercise architecture normalization too.
case "${build_arch}" in
  arm64) build_arch=aarch64 ;;
  aarch64) build_arch=arm64 ;;
  x86_64) build_arch=amd64 ;;
  amd64) build_arch=x86_64 ;;
esac
build_platform="${temporary_directory}/${build_arch}-almalinux9-gcc14-opt"
mkdir -p "${build_platform}"
cp "${temporary_directory}/setup.sh" "${build_platform}/setup.sh"
build_setup="${temporary_directory}/recorded-setup.sh"
ln -s "${build_platform}/setup.sh" "${build_setup}"
make_fake_payload
(
  cd "${temporary_directory}"
  unset DIRAC_JOB_PROCESSORS
  CONDA_PREFIX="inherited-conda" \
    "${wrapper}" --env inherit \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      --include-archive analysis-includes.tar.gz -- analysis.py \
    --input input.root --output output.root --label "two words"
)
assert_file_equals "${temporary_directory}/arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n--input\ninput.root\n--output\noutput.root\n--label\ntwo words\n'
assert_file_equals "${temporary_directory}/conda-prefix.txt" $'inherited-conda\n'
assert_file_equals "${temporary_directory}/include/functions.h" $'int answer() { return 42; }\n'

(
  cd "${temporary_directory}"
  CONDA_PREFIX="" BASH_ENV="${temporary_directory}/worker-env.sh" \
    "${wrapper}" --env inherit \
      --key4hep-setup "${build_setup}" \
      --payload-archive fccanalyses-payload.tar.gz -- analysis.py \
    --input input.root --output output.root --label "two words"
)
assert_file_equals "${temporary_directory}/payload-runtime.txt" $'shipped\n'
assert_file_equals "${temporary_directory}/payload-arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n--input\ninput.root\n--output\noutput.root\n--label\ntwo words\n'
assert_file_equals "${temporary_directory}/payload-conda-prefix.txt" $'unset\n'

(
  cd "${temporary_directory}"
  unset DIRAC_JOB_PROCESSORS
  "${wrapper}" --env clean \
    --key4hep-setup "${temporary_directory}/setup.sh" \
    --key4hep-release 2026-04-08 \
    -- analysis.py -- --ncpus 99
)
assert_file_equals "${temporary_directory}/arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n--\n--ncpus\n99\n'
assert_file_equals "${temporary_directory}/setup-arguments.txt" $'-r\n2026-04-08\n'

printf '%s\n' false true > "${temporary_directory}/unavailable-release.sh"
if (
  cd "${temporary_directory}"
  PATH="${temporary_directory}/bin:${PATH}" \
    "${wrapper}" --env inherit --key4hep-setup "${temporary_directory}/unavailable-release.sh" \
      --key4hep-release 2026-04-08 -- analysis.py > /dev/null
); then
  echo "Wrapper continued after Key4hep setup failed" >&2
  exit 1
fi

# The worker must ignore DIRAC allocation metadata and always use one CPU.
for allocation in invalid 0 8; do
  (
    cd "${temporary_directory}"
    DIRAC_JOB_PROCESSORS="${allocation}" "${wrapper}" --env inherit \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      -- analysis.py > /dev/null
  )
  assert_file_equals "${temporary_directory}/arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n'
done

for mismatch in os arch; do
  worker_major=9
  expected_arch="${build_arch}"
  case "${mismatch}" in
    os) worker_major=10 ;;
    arch)
      case "${build_arch}" in
        x86_64|amd64) expected_arch=aarch64 ;;
        *) expected_arch=x86_64 ;;
      esac
      ;;
  esac
  test_setup="${temporary_directory}/${expected_arch}-almalinux9-gcc14-opt/setup.sh"
  mkdir -p "${test_setup%/*}"
  touch "${test_setup}"
  if (
    cd "${temporary_directory}"
    TEST_OS_VERSION="${worker_major}.0" BASH_ENV="${temporary_directory}/worker-env.sh" \
      "${wrapper}" --env inherit \
      --key4hep-setup "${test_setup}" \
      --payload-archive fccanalyses-payload.tar.gz \
      -- analysis.py > /dev/null 2> platform-mismatch.txt
  ); then
    echo "Wrapper accepted an incompatible build ${mismatch}" >&2
    exit 1
  fi
  grep -q 'Cannot run the shipped FCCAnalyses build' "${temporary_directory}/platform-mismatch.txt"
  grep -q "Build platform: el9 ${expected_arch}" "${temporary_directory}/platform-mismatch.txt"
  grep -q "Worker platform: el${worker_major} $(uname -m)" "${temporary_directory}/platform-mismatch.txt"
done

if (
  cd "${temporary_directory}"
  "${wrapper}" --env inherit -- analysis.py > /dev/null 2> missing-stack.txt
); then
  echo "Wrapper accepted a missing Key4hep setup path" >&2
  exit 1
fi
grep -q -- "--key4hep-setup must name" "${temporary_directory}/missing-stack.txt"

echo "run_fccanalysis.sh tests passed"
