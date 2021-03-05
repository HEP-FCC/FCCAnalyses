#ifndef AWKWARDTEST_ANALYZERS_H
#define AWKWARDTEST_ANALYZERS_H
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackState.h"

//namespace awkwardtest{
  bool awkwardtest(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,  
		 ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
//}
#endif
