#!/bin/csh
if( ! $?LD_LIBRARY_PATH ) then
  setenv LD_LIBRARY_PATH /afs/cern.ch/user/d/dimoulin/FCCAnalyses/Madgraph/MG5_aMC_v2_6_7/HEPTools/hepmc/lib
else
  setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/afs/cern.ch/user/d/dimoulin/FCCAnalyses/Madgraph/MG5_aMC_v2_6_7/HEPTools/hepmc/lib
endif
setenv PYTHIA8DATA ${PYTHIA8_HOME}/xmldoc
