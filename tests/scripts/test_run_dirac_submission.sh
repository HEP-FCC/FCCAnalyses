#!/usr/bin/env bash

set -e -o pipefail

repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
runner="${repository_root}/scripts/dirac/run_dirac_submission.sh"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "${temporary_directory}"' EXIT

mkdir -p "${temporary_directory}/bin"
: > "${temporary_directory}/submission-request.json"
: > "${temporary_directory}/helper.py"

cat > "${temporary_directory}/fcc-grid-setup.sh" <<'EOF'
if (( $# != 0 )); then
  echo "FCC grid setup received unexpected arguments" >&2
  return 1
fi
export FCC_GRID_SETUP_RAN=yes
EOF

cat > "${temporary_directory}/dirac-setup.sh" <<EOF
if (( $# != 0 )); then
  echo "DIRAC setup received unexpected arguments" >&2
  return 1
fi
export DIRAC_SETUP_RAN=yes
export PATH="${temporary_directory}/bin:/usr/bin:/bin"
EOF

cat > "${temporary_directory}/bin/dirac-proxy-info" <<'EOF'
#!/usr/bin/env bash
exit 1
EOF

cat > "${temporary_directory}/bin/dirac-proxy-init" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "${TEST_OUTPUT_DIRECTORY}/proxy-arguments.txt"
EOF

cat > "${temporary_directory}/bin/python" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "${TEST_OUTPUT_DIRECTORY}/helper-arguments.txt"
printf '%s\n' "${FCCANALYSES_SUBMISSION_REQUEST}" \
  > "${TEST_OUTPUT_DIRECTORY}/request-path.txt"
printf '%s %s\n' "${FCC_GRID_SETUP_RAN:-no}" "${DIRAC_SETUP_RAN:-no}" \
  > "${TEST_OUTPUT_DIRECTORY}/setups-ran.txt"
EOF
chmod +x \
  "${temporary_directory}/bin/dirac-proxy-info" \
  "${temporary_directory}/bin/dirac-proxy-init" \
  "${temporary_directory}/bin/python"

TEST_OUTPUT_DIRECTORY="${temporary_directory}" \
FCCANALYSES_SUBMISSION_REQUEST="${temporary_directory}/submission-request.json" \
FCC_GRID_SETUP="${temporary_directory}/fcc-grid-setup.sh" \
DIRAC_SETUP="${temporary_directory}/dirac-setup.sh" \
PATH="/usr/bin:/bin" \
  "${runner}" "${temporary_directory}/helper.py" \
  > "${temporary_directory}/runner-output.txt"

diff -u \
  <(printf '%s\n' "${temporary_directory}/helper.py") \
  "${temporary_directory}/helper-arguments.txt"
diff -u \
  <(printf '%s\n' "${temporary_directory}/submission-request.json") \
  "${temporary_directory}/request-path.txt"
diff -u <(printf '%s\n' "yes yes") "${temporary_directory}/setups-ran.txt"
diff -u <(printf '%s\n' '-g' 'fcc_user') \
  "${temporary_directory}/proxy-arguments.txt"
grep -q "No valid DIRAC proxy found" \
  "${temporary_directory}/runner-output.txt"

echo "run_dirac_submission.sh tests passed"
