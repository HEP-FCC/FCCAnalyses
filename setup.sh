if [ "${0}" != "${BASH_SOURCE}" ]; then
  # Determinig the location of this setup script
  export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

  # Sourcing of the stack
  if [ -n "${KEY4HEP_STACK}" ]; then
    echo "INFO: Key4hep stack already set up."
  elif [ -f "${LOCAL_DIR}/.fccana/stackpin" ]; then
    STACK_PATH=$(<${LOCAL_DIR}/.fccana/stackpin)
    echo "INFO: Sourcing pinned Key4hep stack..."
    echo "      ${STACK_PATH}"
    source ${STACK_PATH}
  else
    source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
  fi

  export PYTHONPATH=${LOCAL_DIR}:${PYTHONPATH}
  export PYTHONPATH=${LOCAL_DIR}/python:${PYTHONPATH}
  export PATH=${LOCAL_DIR}/bin:${PATH}
  export LD_LIBRARY_PATH=${LOCAL_DIR}/install/lib:${LD_LIBRARY_PATH}
  export CMAKE_PREFIX_PATH=${LOCAL_DIR}/install:${CMAKE_PREFIX_PATH}
  export ROOT_INCLUDE_PATH=${LOCAL_DIR}/install/include:${ROOT_INCLUDE_PATH}

  export ONNXRUNTIME_ROOT_DIR=`python -c "import onnxruntime; print(onnxruntime.__path__[0]+'/../../../..')" 2> /dev/null`
  if [ -z "${ONNXRUNTIME_ROOT_DIR}" ]; then
    echo "WARNING: ONNX Runtime not found! Related analyzers won't be build..."
  else
    export LD_LIBRARY_PATH=${ONNXRUNTIME_ROOT_DIR}/lib:${LD_LIBRARY_PATH}
  fi
else
  echo "ERROR: This script is meant to be sourced!"
fi
