#!/bin/bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh

#export PATH=/cvmfs/sft.cern.ch/lcg/contrib/CMake/latest/Linux-x86_64/bin/:$PATH
export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH

#source ACTS env var
source /cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/acts-1.02.0-3qlgwswd5svjsvyksbzaqi2iegbx5lw2/bin/this_acts.sh
