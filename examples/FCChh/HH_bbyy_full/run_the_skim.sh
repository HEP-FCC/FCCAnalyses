#! /bin/sh

chunkID=$1
echo ${chunkID}

LAUNCH_FOLDER="/afs/cern.ch/user/b/bistapf/main_FCCAnalyses/FCCAnalyses/examples/FCChh/HH_bbyy_full/"

cd ${LAUNCH_FOLDER}
source /cvmfs/sw.hsf.org/key4hep/setup.sh
# source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh
python processTrees.py --ID ${chunkID}