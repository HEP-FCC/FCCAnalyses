#include "Bs2JPsiPhi.h"

using namespace MCParticle;
using namespace Vertexing;


// the decay vertex of the Bs that decayed to mu mu KK; the indices
// of the 1 + 4 MC particles are passed as input

// I take the production vertex of the mu+ for example, which is the first index (after the mother Bs) in the input list

edm4hep::Vector3d BsMCDecayVertex(  ROOT::VecOps::RVec<int>  mcParticles_indices, ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {

   edm4hep::Vector3d vertex(1e12, 1e12, 1e12); 
   if ( mcParticles_indices.size() == 0 ) return vertex;

   int idx_muplus = mcParticles_indices[1];
   if ( idx_muplus < in.size() ) {
     vertex = in.at( idx_muplus ).vertex;
   }
 
 //std::cout << " in MCDecayVertex, vertex = " << vertex.x << " " << vertex.y << " " << vertex.z << std::endl;
   return vertex;

}


// To retrieve a given MC leg corresponding to the Bs decay

selMC_leg::selMC_leg( int idx ) {
  m_idx = idx;
};

// I return a vector instead of a single particle :
//   - such that the vector is empty when there is no such decay mode (instead
//     of returning a dummy particle)
//   - such that I can use the getMC_theta etc functions, which work with a
//     ROOT::VecOps::RVec of particles, and not a single particle

ROOT::VecOps::RVec<edm4hep::MCParticleData> selMC_leg::operator() ( ROOT::VecOps::RVec<int> list_of_indices,  ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData>  res;
  if ( list_of_indices.size() == 0) return res;
  if ( m_idx < list_of_indices.size() ) {
	res.push_back( sel_byIndex( list_of_indices[m_idx], in ) );
	return res;
  }
  else {
	std::cout << "   !!!  in selMC_leg:  idx = " << m_idx << " but size of list_of_indices = " << list_of_indices.size() << std::endl;
  }
  return res;
}


// Retrieve the RecoParticles associated with the Bs legs

selRP_leg::selRP_leg(int idx) {
  m_idx = idx;
};

// Below, BsRecoParticles is always of size 4 by construction
// but the RecoParticles maybe dummy ( energy set to -9999 )
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> selRP_leg::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> BsRecoParticles ) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> res;
  if ( BsRecoParticles.size() == 0) return res;
  if ( m_idx < BsRecoParticles.size() ) {
     res.push_back( BsRecoParticles[m_idx] ) ;
     return res;
  }
  else {
        std::cout << "   !!!  in selRP_leg: idx = " << m_idx << " but size of BsRecoParticles = " << BsRecoParticles.size() << std::endl;
  }
  return res;
}


// Retrieve the Reco'ed Bs legs, but now with their momentum corrected to the Bs decay vertex

selRP_leg_atVertex::selRP_leg_atVertex(int idx) {
  m_idx = idx;
};

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> selRP_leg_atVertex::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> BsRecoParticles,
				FCCAnalysesVertex    BsDecayVertex,
				ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> res;

  if ( BsRecoParticles.size() == 0 || m_idx > BsRecoParticles.size() ) {
     return res;
  }

  if ( BsDecayVertex.ntracks <= 1 ) return  res;   // no genuine vertex could be reco'ed

  // the updated momenta of the tracks used in the verte fit :
  ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex = BsDecayVertex.updated_track_momentum_at_vertex ;

  // m_idx : 1,2,3,4 = mu+, mu-, K+, K-
  // but the index in the list of tracks can be different, in case a track was not found
  std::vector<int> track_indices;
  int count = -1;
  for (auto & p: BsRecoParticles) {
    if ( p.tracks_begin>= 0 && p.tracks_begin < tracks.size() ) {  // this particle is matched to a track
	count ++;
        track_indices.push_back( count );
    }
    else {	// insert -1
	track_indices.push_back( -1 );
    }
  }

  int idx_track = track_indices[ m_idx ] ;   

  if ( idx_track < 0 )  { // no track associated to this particle, return the original particle
      res.push_back( BsRecoParticles.at( m_idx ) );
      return res;
  }
  else {	// idx_track is the track index of this particle, in the internal track array of BsDecayVertex
      TVector3 track_momentum = updated_track_momentum_at_vertex[idx_track];
      edm4hep::ReconstructedParticleData particle = BsRecoParticles[m_idx];
      particle.momentum.x = track_momentum.Px();
      particle.momentum.y = track_momentum.Py();
      particle.momentum.z = track_momentum.Pz();
      particle.referencePoint = BsDecayVertex.vertex.position ;
      res.push_back( particle );
      return res;
  }

  return res;
}






