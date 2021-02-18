#!/bin/bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh

#export PATH=/cvmfs/sft.cern.ch/lcg/contrib/CMake/latest/Linux-x86_64/bin/:$PATH
export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH

#source ACTS env var
#source /cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/acts-1.02.0-3qlgwswd5svjsvyksbzaqi2iegbx5lw2/bin/this_acts.sh
#source /cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/acts-1.01.0-dk3frb6pqqi6fhyjra3x3mxxmjmag6t6/bin/this_acts.sh
#source /cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/acts-0.10.5-usyjtov2cbmq6soikqrdxrfrnwilytk6/bin/this_acts.sh

#spack install --test=all acts+unit_tests
#spack install acts
#spack install acts build_type=Debug
#spack load acts
#spack load acts build_type=Debug
#spack load acts /jpihoer
spack load acts /pwh2qmq
