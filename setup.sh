if [ "$0" != "$BASH_SOURCE" ]; then
  source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
  export PYTHONPATH=$PWD:$PYTHONPATH
  export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
  export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH
  export LOCAL_DIR=$PWD
  export LD_LIBRARY_PATH=`python -m awkward.config --libdir`:$LD_LIBRARY_PATH
else
  echo "ERROR: This script is meant to be sourced!"
fi
