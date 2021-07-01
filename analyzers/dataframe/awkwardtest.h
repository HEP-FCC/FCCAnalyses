#ifndef AWKWARDTEST_ANALYZERS_H
#define AWKWARDTEST_ANALYZERS_H
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/TrackState.h"

//namespace awkwardtest{
ROOT::VecOps::RVec<float> awkwardtest(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,  
				      ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
				      ROOT::VecOps::RVec<int> recind, 
				      ROOT::VecOps::RVec<int> mcind, 
				      ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

float build_invmass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, ROOT::VecOps::RVec<int> index);

//}
#endif
