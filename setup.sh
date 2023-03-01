if [ "${0}" != "${BASH_SOURCE}" ]; then
  if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
  else
    echo "INFO: Key4hep stack already set up."
  fi
  # Determinig the location of this setup script
  export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)

  export PYTHONPATH=${LOCAL_DIR}:${PYTHONPATH}
  export PYTHONPATH=${LOCAL_DIR}/python:${PYTHONPATH}
  export PATH=${LOCAL_DIR}/bin:${PATH}
  export LD_LIBRARY_PATH=${LOCAL_DIR}/install/lib:${LD_LIBRARY_PATH}
  export CMAKE_PREFIX_PATH=${LOCAL_DIR}/install:${CMAKE_PREFIX_PATH}
  export ROOT_INCLUDE_PATH=${LOCAL_DIR}/install/include:${ROOT_INCLUDE_PATH}

  export ONNXRUNTIME_ROOT_DIR=`python -c "import onnxruntime; print(onnxruntime.__path__[0]+'/../../../..')"`
  export LD_LIBRARY_PATH=$ONNXRUNTIME_ROOT_DIR/lib:$LD_LIBRARY_PATH
else
  echo "ERROR: This script is meant to be sourced!"
fi
