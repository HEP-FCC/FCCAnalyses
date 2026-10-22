#!/usr/bin/env bash

# Execute one FCCAnalyses payload after DIRAC has staged its sandbox and data.
#
# DIRAC invokes this through GenericApplication. Before this script starts, the
# DIRAC JobWrapper has created the job directory, copied the input sandbox, and
# staged the input data declared by the job. This script only activates the
# selected software and executes the already planned FCCAnalyses command.
#
# Arguments before `--` are internal job metadata:
#
#   --env inherit|clean      Preserve the current environment or re-execute a
#                            local DIRAC test payload in a minimal one.
#   --key4hep-setup PATH     Exact Key4hep setup script selected at submission.
#   --payload-archive FILE   Staged user-build archive, when one is supplied.
#   --include-archive FILE   Staged Analysis.include_paths archive, when used.
#
# Arguments after `--` are opaque FCCAnalyses arguments. The first is the
# staged analysis script; every remaining argument is forwarded unchanged to
# `fccanalysis run`. Do not add FCCAnalyses option parsing to this wrapper.
set -e -o pipefail

usage() {
  echo "Usage: $0 --env inherit|clean --key4hep-setup SETUP_SCRIPT [--payload-archive FILE] [--include-archive FILE] -- ANALYSIS_SCRIPT [RUN_ARGUMENT ...]" >&2
}

environment_mode=""
key4hep_setup=""
payload_archive=""
include_archive=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --env)
      if [ "$#" -lt 2 ]; then
        echo "--env requires inherit or clean" >&2
        exit 2
      fi
      case "$2" in
        inherit|clean)
          environment_mode="$2"
          ;;
        *)
          echo "Unknown environment mode: $2 (expected inherit or clean)" >&2
          exit 2
          ;;
      esac
      shift 2
      ;;
    --key4hep-setup)
      if [ "$#" -lt 2 ]; then
        echo "--key4hep-setup requires a path" >&2
        exit 2
      fi
      key4hep_setup="$2"
      shift 2
      ;;
    --payload-archive)
      if [ "$#" -lt 2 ]; then
        echo "--payload-archive requires a filename" >&2
        exit 2
      fi
      payload_archive="$2"
      shift 2
      ;;
    --include-archive)
      if [ "$#" -lt 2 ]; then
        echo "--include-archive requires a filename" >&2
        exit 2
      fi
      include_archive="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown wrapper option: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [ -z "${environment_mode}" ]; then
  echo "--env inherit or --env clean is required" >&2
  exit 2
fi

if [ "$#" -lt 1 ]; then
  usage
  exit 2
fi

analysis_script="$1"
shift

if [ ! -f "${analysis_script}" ]; then
  echo "Analysis script not found: ${analysis_script}" >&2
  exit 2
fi

if [ -z "${key4hep_setup}" ]; then
  echo "--key4hep-setup must name the selected Key4hep setup script" >&2
  exit 2
fi
if [ ! -r "${key4hep_setup}" ]; then
  echo "Key4hep setup script is not readable: ${key4hep_setup}" >&2
  exit 2
fi

if [ -n "${payload_archive}" ]; then
  case "${payload_archive}" in
    */*|.|..)
      echo "--payload-archive must be a staged filename" >&2
      exit 2
      ;;
  esac
fi
if [ -n "${include_archive}" ]; then
  case "${include_archive}" in
    */*|.|..)
      echo "--include-archive must be a staged filename" >&2
      exit 2
      ;;
  esac
fi

if [ "${environment_mode}" = "clean" ]; then
  # Local DIRAC execution inherits the user's client environment. DIRAC has
  # already staged the files, so rerun the payload without that environment.
  # Pass the selected stack as an argument, rather than relying on an inherited
  # Key4hep environment variable. The child selects inherited mode solely to
  # avoid another clean-environment re-execution.
  wrapper_arguments=(
    --env inherit
    --key4hep-setup "${key4hep_setup}"
  )
  if [ -n "${payload_archive}" ]; then
    wrapper_arguments+=(--payload-archive "${payload_archive}")
  fi
  if [ -n "${include_archive}" ]; then
    wrapper_arguments+=(--include-archive "${include_archive}")
  fi
  exec env -i \
    HOME="${HOME:-}" \
    USER="${USER:-}" \
    LOGNAME="${LOGNAME:-}" \
    TMPDIR="${TMPDIR:-/tmp}" \
    LANG="${LANG:-C.UTF-8}" \
    TERM="${TERM:-dumb}" \
    PATH="/usr/bin:/bin" \
    /bin/bash "$0" "${wrapper_arguments[@]}" -- "${analysis_script}" "$@"
fi

if [ -n "${include_archive}" ]; then
  if [ ! -f "${include_archive}" ]; then
    echo "Analysis include archive not found: ${include_archive}" >&2
    exit 2
  fi
  if ! command -v tar >/dev/null 2>&1; then
    echo "tar is unavailable for analysis include extraction" >&2
    exit 1
  fi
  include_members="$(tar -tzf "${include_archive}")" || {
    echo "Unable to read analysis include archive: ${include_archive}" >&2
    exit 1
  }
  if printf '%s\n' "${include_members}" | grep -Eq '(^/|(^|/)\.\.(/|$))'; then
    echo "Analysis include archive contains an unsafe path" >&2
    exit 1
  fi
  tar -xzf "${include_archive}" -C .
fi

if [ -n "${payload_archive}" ]; then
  if [ ! -f "${payload_archive}" ]; then
    echo "User-build payload archive not found: ${payload_archive}" >&2
    exit 2
  fi
  if ! command -v tar >/dev/null 2>&1; then
    echo "tar is unavailable for user-build payload extraction" >&2
    exit 1
  fi
  payload_members="$(tar -tzf "${payload_archive}")" || {
    echo "Unable to read user-build payload archive: ${payload_archive}" >&2
    exit 1
  }
  if printf '%s\n' "${payload_members}" | grep -Eq '(^/|(^|/)\.\.(/|$))'; then
    echo "User-build payload archive contains an unsafe path" >&2
    exit 1
  fi

  payload_directory="$(mktemp -d "${TMPDIR:-/tmp}/fccanalyses-payload.XXXXXX")"
  cleanup_payload() {
    local status=$?
    rm -rf -- "${payload_directory}"
    trap - EXIT
    exit "${status}"
  }
  trap cleanup_payload EXIT

  tar -xzf "${payload_archive}" -C "${payload_directory}"
  payload_root="${payload_directory}/fccanalyses-payload"
  payload_stack_record="${payload_root}/.fccana/stack_build"
  payload_setup="${payload_root}/setup.sh"
  payload_fccanalysis="${payload_root}/install/bin/fccanalysis"
  if [ ! -r "${payload_stack_record}" ] || [ ! -r "${payload_setup}" ] || \
     [ ! -x "${payload_fccanalysis}" ]; then
    echo "User-build payload is missing its required runtime files" >&2
    exit 1
  fi
  payload_stack_count="$(awk 'END { print NR }' "${payload_stack_record}")"
  payload_stack_path="$(sed -n '1p' "${payload_stack_record}")"
  if [ "${payload_stack_count}" -ne 1 ] || [ -z "${payload_stack_path}" ]; then
    echo "User-build payload has an invalid .fccana/stack_build record" >&2
    exit 1
  fi
  if [ "${payload_stack_path}" != "${key4hep_setup}" ]; then
    echo "User-build payload Key4hep stack differs from the job request" >&2
    echo "  request: ${key4hep_setup}" >&2
    echo "  payload: ${payload_stack_path}" >&2
    exit 1
  fi
fi

setup_key4hep() {
  # This no-argument function prevents sourced setup scripts from seeing the
  # analysis and FCCAnalyses arguments as their own positional arguments.
  source "${key4hep_setup}"
}
setup_key4hep

if [ -n "${payload_archive}" ]; then
  setup_user_build() {
    # A worker should not inherit a local checkout selection. The extracted
    # setup script then sets FCCANA_LOCAL_DIR to the staged payload itself.
    unset FCCANA_LOCAL_DIR
    source "${payload_setup}"
  }
  setup_user_build
  fccanalysis_command="${payload_fccanalysis}"
  runtime_description="shipped user build"
else
  if ! command -v fccanalysis >/dev/null 2>&1; then
    echo "fccanalysis is unavailable after sourcing Key4hep" >&2
    exit 1
  fi
  fccanalysis_command="$(command -v fccanalysis)"
  runtime_description="Key4hep stack"
fi

echo "Working directory: $(pwd)"
echo "Key4hep setup: ${key4hep_setup}"
echo "FCCAnalyses runtime: ${runtime_description}"
echo "fccanalysis executable: ${fccanalysis_command}"

"${fccanalysis_command}" run "${analysis_script}" "$@"
