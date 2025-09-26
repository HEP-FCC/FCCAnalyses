if [ "${0}" == "${BASH_SOURCE[0]}" ]; then
  echo "----> ERROR: This script is meant to be sourced!"
  exit 1
fi

unset HELP
unset LATEST
unset NIGHTLIES
unset PINNED
unset FROMBUILD
unset STACK_SELECTION_MADE

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      HELP="TRUE"
      shift
      ;;
    -l|--latest)
      LATEST="TRUE"
      STACK_SELECTION_MADE="TRUE"
      shift
      ;;
    -n|--nightlies)
      NIGHTLIES="TRUE"
      STACK_SELECTION_MADE="TRUE"
      shift
      ;;
    -p|--pinned)
      PINNED="TRUE"
      STACK_SELECTION_MADE="TRUE"
      shift
      ;;
    -b|--from-build)
      FROMBUILD="TRUE"
      STACK_SELECTION_MADE="TRUE"
      shift
      ;;
    -*)
      echo "ERROR: Unknown option ${1}"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("${1}")
      shift
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}"

if [ -n "${HELP}" ]; then
  echo "USAGE: source setup.sh [-h, -l, -n, -p, -b]"
  echo "       -h/--help           Show this help and exit"
  echo "       -l/--latest         Setup the latest release of the Key4hep stack"
  echo "       -n/--nightlies      Setup the latest nightlies version of the Key4hep stack"
  echo "       -p/--pinned         Setup the pinned version of the Key4hep stack"
  echo "       -b/--from-build     Setup the version of the Key4hep stack used for the latest local build"

  echo
  echo "The setup script defaults to using the pinned stack. If the pinned stack is not set,"
  echo "the latest stable release is used instead."

  return
fi

if [ -n "${FCCANA_LOCAL_DIR}" ]; then
  echo "----> WARNING: Local FCCAnalyses environment already set up."
  echo "               Skipping its setup..."
  return
fi

# Determining the location of this setup script
FCCANA_LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

echo "----> INFO: Setting up Key4hep stack..."
if [ -n "${KEY4HEP_STACK}" ]; then
  echo "----> INFO: Key4hep stack already set up. Skipping its setup..."
else
  # Sourcing of the stack
  if [ -n "${STACK_SELECTION_MADE}" ]; then
    if [ -n "${LATEST}" ]; then
      echo "----> INFO: Sourcing latest Key4hep stack release..."
      source /cvmfs/sw.hsf.org/key4hep/setup.sh
    fi
    if [ -n "${NIGHTLIES}" ]; then
      echo "----> INFO: Sourcing latest nightlies Key4hep stack..."
      source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
    fi
    if [ -n "${PINNED}" ]; then
      if [ -f "${FCCANA_LOCAL_DIR}/.fccana/stack_pin" ]; then
        STACK_PATH=$(<${FCCANA_LOCAL_DIR}/.fccana/stack_pin)
      # TODO: Legacy pin location, remove after Jun 2026
      elif [ -f "${FCCANA_LOCAL_DIR}/.fccana/stackpin" ]; then
        STACK_PATH=$(<${FCCANA_LOCAL_DIR}/.fccana/stackpin)
      else
        echo "----> ERROR: The Key4hep stack is not pinned! Aborting..."
        return 1
      fi
      echo "----> INFO: Sourcing pinned Key4hep stack..."
      echo "      ${STACK_PATH}"
      source ${STACK_PATH}
    fi
    if [ -n "${FROMBUILD}" ]; then
      echo "----> INFO: Sourcing Key4hep stack used for the latest build..."
      if [ -f "${FCCANA_LOCAL_DIR}/.fccana/stack_build" ]; then
        STACK_PATH=$(<${FCCANA_LOCAL_DIR}/.fccana/stack_build)
        echo "      ${STACK_PATH}"
        source ${STACK_PATH}
      else
        echo "----> ERROR: The information about the Key4hep stack used for building not found!"
        echo "             Try sourcing the Key4hep stack using other options and rebuilding"
        echo "             FCCAnalyses using 'fccanalysis build' command."
        echo "             Aborting..."
        return 1
      fi
    fi
  else
    if [ -f "${FCCANA_LOCAL_DIR}/.fccana/stack_pin" ]; then
      STACK_PATH=$(<${FCCANA_LOCAL_DIR}/.fccana/stack_pin)
      echo "----> INFO: Sourcing pinned Key4hep stack..."
      echo "      ${STACK_PATH}"
      source ${STACK_PATH}
    # TODO: Legacy pin location, remove after Jun 2026
    elif [ -f "${FCCANA_LOCAL_DIR}/.fccana/stackpin" ]; then
      STACK_PATH=$(<${FCCANA_LOCAL_DIR}/.fccana/stackpin)
      echo "----> INFO: Sourcing pinned Key4hep stack..."
      echo "      ${STACK_PATH}"
      source ${STACK_PATH}
    else
      echo "----> INFO: Sourcing latest Key4hep stack release..."
      source /cvmfs/sw.hsf.org/key4hep/setup.sh
    fi
  fi
fi

if [ -z "${KEY4HEP_STACK}" ]; then
  echo "----> ERROR: Key4hep stack not setup correctly! Aborting..."
  return 1
fi

echo "----> INFO: Setting up local FCCAnalyses environment variables..."
export FCCANA_LOCAL_DIR
export PYTHONPATH=${FCCANA_LOCAL_DIR}/python:${PYTHONPATH}
export PYTHONPATH=${FCCANA_LOCAL_DIR}/install/python:${PYTHONPATH}
export PYTHONPATH=${FCCANA_LOCAL_DIR}/install/share/examples:${PYTHONPATH}
export PATH=${FCCANA_LOCAL_DIR}/bin:${PATH}
export PATH=${FCCANA_LOCAL_DIR}/install/bin:${PATH}
export LD_LIBRARY_PATH=${FCCANA_LOCAL_DIR}/install/lib64:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${FCCANA_LOCAL_DIR}/install/lib:${LD_LIBRARY_PATH}
export CMAKE_PREFIX_PATH=${FCCANA_LOCAL_DIR}/install:${CMAKE_PREFIX_PATH}

export ROOT_INCLUDE_PATH=$(fastjet-config --prefix)/include:${ROOT_INCLUDE_PATH}
export ROOT_INCLUDE_PATH=${FCCANA_LOCAL_DIR}/install/include:${ROOT_INCLUDE_PATH}

export ONNXRUNTIME_ROOT_DIR=`python -c "import onnxruntime; print(onnxruntime.__path__[0]+'/../../../..')" 2> /dev/null`
if [ -z "${ONNXRUNTIME_ROOT_DIR}" ]; then
  echo "----> WARNING: ONNX Runtime not found! Related analyzers won't be build..."
else
  export LD_LIBRARY_PATH=${ONNXRUNTIME_ROOT_DIR}/lib:${LD_LIBRARY_PATH}
fi

export MANPATH=${FCCANA_LOCAL_DIR}/man:${MANPATH}
export MANPATH=${FCCANA_LOCAL_DIR}/install/share/man:${MANPATH}

export MYPYPATH=${FCCANA_LOCAL_DIR}/python:${MYPYPATH}

export FCCDICTSDIR=/cvmfs/fcc.cern.ch/FCCDicts:${FCCDICTSDIR}
