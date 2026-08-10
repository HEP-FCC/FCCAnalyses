#!/usr/bin/env bash

# Start an ILCDIRAC submission helper from a clean, Key4hep-independent child.
# The parent launcher provides a versioned request file as explicit data. The
# request carries the Key4hep setup for the worker.

set -e -o pipefail

if (( $# != 1 )); then
  echo "Usage: $0 SUBMISSION_HELPER.py" >&2
  exit 2
fi

submission_helper="$1"
if [[ ! -r "${submission_helper}" ]]; then
  echo "Submission helper is not readable: ${submission_helper}" >&2
  exit 2
fi

if [[ -z "${FCCANALYSES_SUBMISSION_REQUEST:-}" ]]; then
  echo "FCCANALYSES_SUBMISSION_REQUEST is required" >&2
  exit 2
fi
if [[ ! -r "${FCCANALYSES_SUBMISSION_REQUEST}" ]]; then
  echo "Submission request is not readable: ${FCCANALYSES_SUBMISSION_REQUEST}" >&2
  exit 2
fi

FCC_GRID_SETUP="${FCC_GRID_SETUP:-/cvmfs/fcc.cern.ch/sw/latest/setup.sh}"
DIRAC_SETUP="${DIRAC_SETUP:-/cvmfs/clicdp.cern.ch/DIRAC/bashrc}"
DIRAC_GROUP="${DIRAC_GROUP:-fcc_user}"

for setup in "${FCC_GRID_SETUP}" "${DIRAC_SETUP}"; do
  if [[ ! -r "${setup}" ]]; then
    echo "Required setup script is not readable: ${setup}" >&2
    exit 2
  fi
done

# Source through zero-argument functions so setup scripts cannot accidentally
# inspect this script's positional arguments.
setup_fcc_grid() {
  source "${FCC_GRID_SETUP}"
}
setup_dirac() {
  source "${DIRAC_SETUP}"
}

# The FCC setup is a prerequisite for the DIRAC client. Its normal banner is
# not relevant to the worker configuration recorded in the request.
setup_fcc_grid >/dev/null
setup_dirac

echo "DIRAC submission client is ready."
echo "  DIRAC setup:         ${DIRAC_SETUP}"

if ! command -v python >/dev/null 2>&1; then
  echo "python is unavailable after sourcing DIRAC" >&2
  exit 1
fi

if ! dirac-proxy-info -m >/dev/null 2>&1; then
  echo "No valid DIRAC proxy found; creating one for group: ${DIRAC_GROUP}"
  dirac-proxy-init -g "${DIRAC_GROUP}"
else
  echo "Using an existing valid DIRAC proxy."
fi

exec python "${submission_helper}"
