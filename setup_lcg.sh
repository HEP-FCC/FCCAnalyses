#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh 

export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH
export LOCALFCCANALYSES=$PWD/install/include/FCCAnalyses
