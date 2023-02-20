// -*- C++ -*-
//
/** FCCAnalysis module: myAnalysis
 *
 * \file myAnalysis.cc
 * \author Perez <Emmanuel.Perez@cern.ch>
 */

#include "myAnalysis.h"
#include <iostream>

using namespace std;

namespace myAnalysis {
  void dummy_analysis() { cout << "Dummy analysis initialised." << endl; }

  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>& parts) {
    rv::RVec<float> output;
    for (size_t i = 0; i < parts.size(); ++i)
      output.emplace_back(parts.at(i).momentum.x);
    return output;
  }


 double sum_momentum_tracks(const VertexingUtils::FCCAnalysesVertex&  vertex) {
   double sum = 0;
   ROOT::VecOps::RVec< TVector3 > momenta = vertex.updated_track_momentum_at_vertex ;
   int n = momenta.size();
   for (int i=0; i < n; i++) {
      TVector3 p = momenta[i];
      double px = p[0];
      double py = p[1];
      double pt = sqrt(pow(px,2)+pow(py,2)) ;
      sum += pt;
   }
  return sum;
 }

 double tau3mu_vertex_mass( const VertexingUtils::FCCAnalysesVertex& vertex ) {
   double muon_mass = 0.1056;
   TLorentzVector tau;
   ROOT::VecOps::RVec< TVector3 > momenta = vertex.updated_track_momentum_at_vertex ;
   int n = momenta.size();
   for (int ileg=0; ileg < n; ileg++) {
     TVector3 track_momentum = momenta[ ileg ];
     TLorentzVector leg;
     leg.SetXYZM( track_momentum[0], track_momentum[1], track_momentum[2], muon_mass ) ;
     tau += leg;
   }
  return tau.M();
 }

 double tau3mu_raw_mass( const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  legs ) {
  double muon_mass = 0.1056;
  TLorentzVector tau;
  int n = legs.size();
  for (int ileg=0; ileg < n; ileg++) {
     TLorentzVector leg;
     leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, muon_mass );
     tau += leg;
  }
  return tau.M();
 }


ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in , float total_charge) {

    ROOT::VecOps::RVec< ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> >  results;
    float charge =0;
    int n = in.size();
    if ( n < 3 ) return results;

    for (int i=0; i < n; i++) {
       edm4hep::ReconstructedParticleData pi = in[i];
       float charge_i = pi.charge ;

       for (int j=i+1; j < n; j++) {
        edm4hep::ReconstructedParticleData pj = in[j];
        float charge_j = pj.charge ;

        for (int k=j+1; k < n; k++) {
          edm4hep::ReconstructedParticleData pk = in[k];
          float charge_k = pk.charge ;
          float charge_tot = charge_i + charge_j + charge_k;
          if ( charge_tot == total_charge ) {
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_triplet;
            a_triplet.push_back( pi );
            a_triplet.push_back( pj );
            a_triplet.push_back( pk );
            results.push_back( a_triplet );
          }
        }//end loop over k
      }//end loop over j
    }//end loop over i 
 return results;
}


ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(const ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets, const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks )  {
      ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex >  results;
      int ntriplets = triplets.size();
      for (int i=0; i < ntriplets; i++) {
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = triplets[i];

          ROOT::VecOps::RVec<edm4hep::TrackState> the_tracks = ReconstructedParticle2Track::getRP2TRK( legs, allTracks );
          VertexingUtils::FCCAnalysesVertex vertex = VertexFitterSimple::VertexFitter_Tk( 2, the_tracks );
          results.push_back( vertex );
      }
 return results;
}

ROOT::VecOps::RVec<  double > build_AllTauMasses(const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices) {
  ROOT::VecOps::RVec<  double >  results;
  for ( auto& v: vertices) {
     double mass =  tau3mu_vertex_mass( v );
     results.push_back( mass  );
  }
 return results;
}


selRP_Fakes::selRP_Fakes( float arg_fakeRate, float  arg_mass ) : m_fakeRate(arg_fakeRate), m_mass( arg_mass)  {
  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  std::default_random_engine generator (seed);
  m_generator = generator;
  std::uniform_real_distribution<float> flatdis(0.,1.);
  m_flat.param( flatdis.param() );
};

std::vector<edm4hep::ReconstructedParticleData> selRP_Fakes::operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in) {
  std::vector<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    float arandom =  m_flat (m_generator );
    if ( arandom <= m_fakeRate) {
      edm4hep::ReconstructedParticleData reso = p;
      // overwrite the mass:
               reso.mass = m_mass;
      result.push_back( reso );
    }
  }
  return result;
}



/*
// --- for tests...

float get_p(const edm4hep::MCParticleData& p) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    return tlv.P();
}

float get_e(const edm4hep::MCParticleData& p) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    return tlv.E();
}

float get_theta(const edm4hep::MCParticleData& p) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    return tlv.Theta();
*/



}  // namespace myAnalysis
