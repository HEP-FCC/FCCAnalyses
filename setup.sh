if [ "${0}" != "${BASH_SOURCE}" ]; then
  # Determinig the location of this setup script
  export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

  echo "----> Info: Setting up Key4hep stack..."
  # Sourcing of the stack
  if [ -n "${KEY4HEP_STACK}" ]; then
    echo "----> Info: Key4hep stack already set up. Skipping..."
  elif [ -f "${LOCAL_DIR}/.fccana/stackpin" ]; then
    STACK_PATH=$(<${LOCAL_DIR}/.fccana/stackpin)
    echo "----> Info: Sourcing pinned Key4hep stack..."
    echo "      ${STACK_PATH}"
    source ${STACK_PATH}
  else
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
  fi

  if [ -z "${KEY4HEP_STACK}" ]; then
    echo "----> Error: Key4hep stack not setup correctly! Aborting..."
    return 1
  fi

  echo "----> Info: Setting up environment variables..."
  export PYTHONPATH=${LOCAL_DIR}/python:${PYTHONPATH}
  export PYTHONPATH=${LOCAL_DIR}/install/python:${PYTHONPATH}
  export PYTHONPATH=${LOCAL_DIR}/install/share/examples:${PYTHONPATH}
  export PATH=${LOCAL_DIR}/bin:${PATH}
  export PATH=${LOCAL_DIR}/install/bin:${PATH}
  export LD_LIBRARY_PATH=${LOCAL_DIR}/install/lib:${LD_LIBRARY_PATH}
  export CMAKE_PREFIX_PATH=${LOCAL_DIR}/install:${CMAKE_PREFIX_PATH}

  export ROOT_INCLUDE_PATH=`fastjet-config --prefix`/include:${ROOT_INCLUDE_PATH}
  export ROOT_INCLUDE_PATH=${LOCAL_DIR}/install/include:${ROOT_INCLUDE_PATH}

  export ONNXRUNTIME_ROOT_DIR=`python -c "import onnxruntime; print(onnxruntime.__path__[0]+'/../../../..')" 2> /dev/null`
  if [ -z "${ONNXRUNTIME_ROOT_DIR}" ]; then
    echo "----> Warning: ONNX Runtime not found! Related analyzers won't be build..."
  else
    export LD_LIBRARY_PATH=${ONNXRUNTIME_ROOT_DIR}/lib:${LD_LIBRARY_PATH}
  fi

  export MANPATH=${LOCAL_DIR}/man:${MANPATH}
  export MANPATH=${LOCAL_DIR}/install/share/man:${MANPATH}

  export MYPYPATH=${LOCAL_DIR}/python:${MYPYPATH}

  export FCCDICTSDIR=/cvmfs/fcc.cern.ch/FCCDicts:${FCCDICTSDIR}
else
  echo "----> Error: This script is meant to be sourced!"
fi
