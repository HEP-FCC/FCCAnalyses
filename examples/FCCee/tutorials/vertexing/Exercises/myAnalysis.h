
#ifndef  MYANALYSIS_ANALYZERS_H
#define  MYANALYSIS_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/TrackState.h"

#include "VertexingUtils.h"
#include "ReconstructedParticle2Track.h"
#include "VertexFitterSimple.h"

#include <random>
#include <chrono>


namespace FCCAnalyses{

namespace myAnalysis {

 double sum_momentum_tracks( const VertexingUtils::FCCAnalysesVertex&  vertex );

 double tau3mu_vertex_mass( const VertexingUtils::FCCAnalysesVertex&  vertex );
 double tau3mu_raw_mass(  const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  legs ) ;


  ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets(
			const 	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  in , float total_charge) ;

  ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(
                        const ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets,
                        const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks ) ;

  ROOT::VecOps::RVec<  double > build_AllTauMasses( const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices ) ;


struct selRP_Fakes {
  selRP_Fakes( float arg_fakeRate, float arg_mass  );
  float m_fakeRate = 1e-3;
  float m_mass = 0.106;  // muon mass
  std::default_random_engine m_generator;
  std::uniform_real_distribution<float> m_flat;
  std::vector<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};




float get_p(const edm4hep::MCParticleData& p) ;
float get_e(const edm4hep::MCParticleData& p) ;
float get_theta(const edm4hep::MCParticleData& in) ;

}//end NS myAnalysis

}//end NS FCCAnalyses

#endif
