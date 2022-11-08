// -*- C++ -*-
//
/** FCCAnalysis module: myAnalysis
 *
 * \file myAnalysis.h
 * \author Perez <Emmanuel.Perez@cern.ch>
 *
 * Description:
 *   [...]
 */

#ifndef myAnalysis_myAnalysis_h
#define myAnalysis_myAnalysis_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

#include "FCCAnalyses/VertexingUtils.h"

#include "TLorentzVector.h"
#include "edm4hep/ReconstructedParticleData.h"

#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/VertexFitterSimple.h"

#include <random>
#include <chrono>

using namespace FCCAnalyses;

namespace myAnalysis {
  namespace rv = ROOT::VecOps;

  void dummy_analysis();
  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>&);

double sum_momentum_tracks(const VertexingUtils::FCCAnalysesVertex&  vertex);

double tau3mu_vertex_mass(const VertexingUtils::FCCAnalysesVertex& vertex );
double tau3mu_raw_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  legs);

ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets(const   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  in , float total_charge);


 ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets, const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks) ;

ROOT::VecOps::RVec<  double > build_AllTauMasses(const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices) ;


struct selRP_Fakes {
  selRP_Fakes( float arg_fakeRate, float arg_mass );
  float m_fakeRate = 1e-3; //fake rate
  float m_mass = 0.106;  // muon mass
  std::default_random_engine m_generator;
  std::uniform_real_distribution<float> m_flat;
  std::vector<edm4hep::ReconstructedParticleData>  operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in);
};


/*
float get_p(const edm4hep::MCParticleData& p) ;
float get_e(const edm4hep::MCParticleData& p) ;
float get_theta(const edm4hep::MCParticleData& in) ;
*/

}  // namespace myAnalysis

#endif

