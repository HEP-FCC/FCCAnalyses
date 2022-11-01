#!/bin/sh
if [ ! $?LD_LIBRARY_PATH ]; then
  export LD_LIBRARY_PATH=/afs/cern.ch/user/d/dimoulin/FCCAnalyses/Madgraph/MG5_aMC_v2_6_7/HEPTools/hepmc/lib
fi
if [ $?LD_LIBRARY_PATH ]; then
  export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/afs/cern.ch/user/d/dimoulin/FCCAnalyses/Madgraph/MG5_aMC_v2_6_7/HEPTools/hepmc/lib
fi
export PYTHIA8DATA=${PYTHIA8_HOME}/xmldoc
