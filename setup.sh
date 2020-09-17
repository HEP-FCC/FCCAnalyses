#!/bin/bash
#source /cvmfs/fcc.cern.ch/sw/latest/setup.sh

export PATH=/cvmfs/sft.cern.ch/lcg/contrib/CMake/latest/Linux-x86_64/bin/:$PATH
export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include:$ROOT_INCLUDE_PATH

#TMP
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/8.3.0/x86_64-centos7-gcc8-opt/setup.sh
export SPACK_ROOT=/afs/cern.ch/user/h/helsens/FCCsoft/spack/
export PATH=$SPACK_ROOT/bin:$PATH
. /afs/cern.ch/work/h/helsens/FCC/soft/spack/share/spack/setup-env.sh
spack load gcc
