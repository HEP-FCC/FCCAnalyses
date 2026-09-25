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
(
  cd "${temporary_directory}"
  CONDA_PREFIX="inherited-conda" \
    "${wrapper}" --env inherit \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      --include-archive analysis-includes.tar.gz -- analysis.py \
    --input input.root --output output.root --label "two words"
)
assert_file_equals "${temporary_directory}/arguments.txt" $'run\nanalysis.py\n--input\ninput.root\n--output\noutput.root\n--label\ntwo words\n'
assert_file_equals "${temporary_directory}/conda-prefix.txt" $'inherited-conda\n'
assert_file_equals "${temporary_directory}/include/functions.h" $'int answer() { return 42; }\n'

(
  cd "${temporary_directory}"
  CONDA_PREFIX="local-dirac-conda" \
    "${wrapper}" --env clean \
      --key4hep-setup "${temporary_directory}/setup.sh" \
      --payload-archive fccanalyses-payload.tar.gz -- analysis.py \
    --input input.root --output output.root --label "two words"
)
assert_file_equals "${temporary_directory}/payload-runtime.txt" $'shipped\n'
assert_file_equals "${temporary_directory}/payload-arguments.txt" $'run\nanalysis.py\n--input\ninput.root\n--output\noutput.root\n--label\ntwo words\n'
assert_file_equals "${temporary_directory}/payload-conda-prefix.txt" $'unset\n'

if (
  cd "${temporary_directory}"
  "${wrapper}" --env inherit -- analysis.py > /dev/null 2> missing-stack.txt
); then
  echo "Wrapper accepted a missing Key4hep setup path" >&2
  exit 1
fi
grep -q -- "--key4hep-setup must name" "${temporary_directory}/missing-stack.txt"

echo "run_fccanalysis.sh tests passed"
