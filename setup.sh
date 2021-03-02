#!/bin/bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh

export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH

spack load acts@5.0.0 arch=linux-centos7-x86_64

#spack load acts@5.00.0 build_type=Debug
export LOCALFCCANALYSES=$PWD/install/include/FCCAnalyses
spack load py-pyyaml
