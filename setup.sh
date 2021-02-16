#!/bin/bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh

#export PATH=/cvmfs/sft.cern.ch/lcg/contrib/CMake/latest/Linux-x86_64/bin/:$PATH
export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH
export LOCALFCCANALYSES=$PWD/install/include/FCCAnalyses
