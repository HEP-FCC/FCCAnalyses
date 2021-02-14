#ifndef BS2JPSIPHI_ANALYZERS_H
#define BS2JPSIPHI_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "podio/ObjectID.h"
#include "TLorentzVector.h"


#include "MCParticle.h"
#include "ReconstructedParticle2MC.h"
#include "Vertexing.h"



// the decay vertex of the Bs that decayed to mu mu KK; the indices
// of the 1 + 4 MC particles are passed as input. Take the production vertex of the mu+
edm4hep::Vector3d BsMCDecayVertex(  ROOT::VecOps::RVec<int>  mcParticles_indices, ROOT::VecOps::RVec<edm4hep::MCParticleData> in) ;

// return one MC leg corresponding to the Bs decay
// note: the sizxe of the vector is always zero or one. I return a ROOT::VecOps::RVec for convenience
struct selMC_leg{
   selMC_leg( int idx );
   int m_idx;
   ROOT::VecOps::RVec<edm4hep::MCParticleData> operator() ( ROOT::VecOps::RVec<int> list_of_indices,  ROOT::VecOps::RVec<edm4hep::MCParticleData> in) ;
};

struct selRP_leg{
   selRP_leg( int idx );
   int m_idx;
   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> BsRecoParticles );
};


struct selRP_leg_atVertex{
   selRP_leg_atVertex( int idx );
   int m_idx;
   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> BsRecoParticles,
                                Vertexing::FCCAnalysesVertex    BsDecayVertex,
                                ROOT::VecOps::RVec<edm4hep::TrackState> tracks) ;
};

#endif

