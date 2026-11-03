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
  printf '%s\n' "${temporary_directory}/setup.sh" \
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
make_fake_payload
make_fake_include_archive
build_os="$(uname -s)"
build_arch="$(uname -m)"
# Use an equivalent spelling to exercise architecture normalization too.
case "${build_arch}" in
  arm64) build_arch=aarch64 ;;
  aarch64) build_arch=arm64 ;;
  x86_64) build_arch=amd64 ;;
  amd64) build_arch=x86_64 ;;
esac
(
  cd "${temporary_directory}"
  DIRAC_JOB_PROCESSORS=1 CONDA_PREFIX="inherited-conda" \
    "${wrapper}" --env inherit --ncpus -1 \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      --include-archive analysis-includes.tar.gz -- analysis.py \
    --input input.root --output output.root --label "two words"
)
assert_file_equals "${temporary_directory}/arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n--input\ninput.root\n--output\noutput.root\n--label\ntwo words\n'
assert_file_equals "${temporary_directory}/conda-prefix.txt" $'inherited-conda\n'
assert_file_equals "${temporary_directory}/include/functions.h" $'int answer() { return 42; }\n'

(
  cd "${temporary_directory}"
  CONDA_PREFIX="local-dirac-conda" \
    "${wrapper}" --env clean --mode local --ncpus 1 \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      --build-os "${build_os}" --build-arch "${build_arch}" \
      --payload-archive fccanalyses-payload.tar.gz -- analysis.py \
    --input input.root --output output.root --label "two words"
)
assert_file_equals "${temporary_directory}/payload-runtime.txt" $'shipped\n'
assert_file_equals "${temporary_directory}/payload-arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n--input\ninput.root\n--output\noutput.root\n--label\ntwo words\n'
assert_file_equals "${temporary_directory}/payload-conda-prefix.txt" $'unset\n'

local_cpus="$(python3 -c 'import os; print(len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count())')"
(
  cd "${temporary_directory}"
  "${wrapper}" --env clean --mode local --ncpus -1 \
    --key4hep-setup "${temporary_directory}/setup.sh" \
    -- analysis.py -- --ncpus 99
)
assert_file_equals "${temporary_directory}/arguments.txt" "$(printf 'run\nanalysis.py\n--ncpus\n%s\n--\n--ncpus\n99' "${local_cpus}")"$'\n'

# Allocation failures must stop before the analysis starts.
for allocation in missing invalid 0; do
  if (
    cd "${temporary_directory}"
    export DIRAC_JOB_PROCESSORS="${allocation}"
    if [ "${allocation}" = missing ]; then unset DIRAC_JOB_PROCESSORS; fi
    "${wrapper}" --env inherit --ncpus 2 \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      -- analysis.py > /dev/null 2> cpu-allocation.txt
  ); then
    echo "Wrapper accepted invalid CPU allocation: ${allocation}" >&2
    exit 1
  fi
  grep -q 'CPU allocation check failed' "${temporary_directory}/cpu-allocation.txt"
done
(
  cd "${temporary_directory}"
  DIRAC_JOB_PROCESSORS=1 "${wrapper}" --env inherit --ncpus 2 \
    --key4hep-setup "${temporary_directory}/setup.sh" \
    -- analysis.py > /dev/null 2> cpu-warning.txt
)
grep -q 'WARNING: Requested 2 threads' "${temporary_directory}/cpu-warning.txt"
grep -q 'limiting thread count to 1' "${temporary_directory}/cpu-warning.txt"
assert_file_equals "${temporary_directory}/arguments.txt" $'run\nanalysis.py\n--ncpus\n1\n'

for mismatch in os arch; do
  expected_os="${build_os}"
  expected_arch="${build_arch}"
  case "${mismatch}" in
    os) expected_os=UnsupportedOS ;;
    arch) expected_arch=unsupported-arch ;;
  esac
  if (
    cd "${temporary_directory}"
    "${wrapper}" --env inherit \
      --key4hep-setup "${temporary_directory}/missing-setup.sh" \
      --payload-archive fccanalyses-payload.tar.gz \
      --build-os "${expected_os}" --build-arch "${expected_arch}" \
      -- analysis.py > /dev/null 2> platform-mismatch.txt
  ); then
    echo "Wrapper accepted an incompatible build ${mismatch}" >&2
    exit 1
  fi
  grep -q 'Cannot run the shipped FCCAnalyses build' "${temporary_directory}/platform-mismatch.txt"
  grep -q "Submission/build platform: ${expected_os} ${expected_arch}" "${temporary_directory}/platform-mismatch.txt"
  grep -q "Worker platform: $(uname -s) $(uname -m)" "${temporary_directory}/platform-mismatch.txt"
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
