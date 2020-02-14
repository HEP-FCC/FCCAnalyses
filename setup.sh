#!/bin/sh -u
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh

export PATH=/cvmfs/sft.cern.ch/lcg/releases/CMake/3.11.1-773ff/x86_64-centos7-gcc8-opt/bin/:$PATH
export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include:$ROOT_INCLUDE_PATH
