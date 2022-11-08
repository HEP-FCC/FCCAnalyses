#include "FCCAnalyses/JetConstituentsUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/ReconstructedParticle2MC.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/Track.h"
#include "edm4hep/TrackerHitData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/ReconstructedParticleData.h"



#include "FCCAnalyses/JetClusteringUtils.h"
//#include "FCCAnalyses/ExternalRecombiner.h"
#include "fastjet/JetDefinition.hh"
#include "fastjet/PseudoJet.hh"
#include "fastjet/Selector.hh"

/* *************************
//COMMENTS
1. Neutral particles (Clusters??)
2. units of measurement?

************************ */

namespace FCCAnalyses {
  namespace JetConstituentsUtils {
    rv::RVec<FCCAnalysesJetConstituents> build_constituents(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                            const rv::RVec<edm4hep::ReconstructedParticleData>& rps) {
      rv::RVec<FCCAnalysesJetConstituents> jcs;
      for (const auto& jet : jets) {
        auto& jc = jcs.emplace_back();
	float energy_jet = jet.energy;
	float energy_const = 0;
        for (auto it = jet.particles_begin; it < jet.particles_end; ++it) {
          jc.emplace_back(rps.at(it));
	  energy_const += rps.at(it).energy;
	}
      }
      return jcs;
    }

    rv::RVec<FCCAnalysesJetConstituents> build_constituents_cluster(const rv::RVec<edm4hep::ReconstructedParticleData>& rps,
								    const std::vector<std::vector<int>>& indices) {
      rv::RVec<FCCAnalysesJetConstituents> jcs;
      for (const auto& jet_index : indices) {
	FCCAnalysesJetConstituents jc;
	for(const auto& const_index : jet_index) {
	  jc.push_back(rps.at(const_index));
	}
	jcs.push_back(jc);
      }
      return jcs;
    }


    FCCAnalysesJetConstituents get_jet_constituents(const rv::RVec<FCCAnalysesJetConstituents>& csts, int jet) {
      if (jet < 0)
        return FCCAnalysesJetConstituents();
      return csts.at(jet);
    }

    rv::RVec<FCCAnalysesJetConstituents> get_constituents(const rv::RVec<FCCAnalysesJetConstituents>& csts,
                                                          const rv::RVec<int>& jets) {
      rv::RVec<FCCAnalysesJetConstituents> jcs;
      for (size_t i = 0; i < jets.size(); ++i)
        if (jets.at(i) >= 0)
          jcs.emplace_back(csts.at(i));
      return jcs;
    }

    /// recasting helper for jet constituents methods
    /// \param[in] jcs collection of jets constituents
    /// \param[in] meth variables retrieval method for constituents
    auto cast_constituent = [](const auto& jcs, auto&& meth) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (const auto& jc : jcs)
        out.emplace_back(meth(jc));
      return out;
    };


    /// This function simply applies the 2 args functions per vector of Rec Particles to a vector of vectors of Rec Particles
    auto cast_constituent_2 = [](const auto& jcs, const auto& coll, auto&& meth) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (const auto& jc : jcs) {
        out.emplace_back(meth(jc, coll));
      }
      return out;
    };

    auto cast_constituent_4 = [](const auto& jcs, const auto& coll1, const auto& coll2, const auto& coll3,auto&& meth) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (const auto& jc : jcs) {
        out.emplace_back(meth(jc, coll1, coll2, coll3));
      }
      return out;
    };
    
 
    rv::RVec<FCCAnalysesJetConstituentsData> get_Bz(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Bz);
    }
    
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_pt(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_pt);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_e(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_e);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_theta(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_theta);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_phi);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_type(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_type);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_charge(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_charge);
    }


    //sorting
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets_sorting_on_nconst(const rv::RVec<edm4hep::ReconstructedParticleData>& jets){
      ROOT::VecOps::RVec<int> nconst;
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;
      for (const auto& jet : jets) {
	nconst.push_back(jet.particles_end - jet.particles_begin);
      }
      auto indices = ROOT::VecOps::Argsort(nconst);
      for (int index = 0; index < jets.size(); ++index) {
	out.push_back( jets.at( indices.at(indices.size()-1-index) ) );
      }
      return out;
    }

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets_sorting_on_energy(const rv::RVec<edm4hep::ReconstructedParticleData>& jets){
      ROOT::VecOps::RVec<float> energy;
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;
      for (const auto& jet : jets) {
        energy.push_back(jet.energy);
      }
      auto indices = ROOT::VecOps::Argsort(energy);
      for (int index = 0; index < jets.size(); ++index) {
        out.push_back( jets.at( indices.at(indices.size()-1-index) ) );
      }
      return out;
    }

    //displacement (wrt (0,0,0))
    rv::RVec<FCCAnalysesJetConstituentsData> get_d0(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_z0(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Z0);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_omega(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_omega);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanLambda(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							   const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_tanLambda);
    }

 
    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_dxy(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							 const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
							 const TVector3& V,
							 const float& Bz) {
      
      return cast_constituent_4(jcs, tracks, V, Bz, ReconstructedParticle2Track::XPtoPar_dxy); 
    }

    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_dz(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
							const TVector3& V,
							const float& Bz) {

      return cast_constituent_4(jcs, tracks, V, Bz, ReconstructedParticle2Track::XPtoPar_dz);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_phi(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							 const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
							 const TVector3& V,
							 const float& Bz) {

      return cast_constituent_4(jcs, tracks, V, Bz, ReconstructedParticle2Track::XPtoPar_phi);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_C(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
						       const TVector3& V,
						       const float& Bz) {
      
      return cast_constituent_4(jcs, tracks, V, Bz, ReconstructedParticle2Track::XPtoPar_C);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_ct(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
							const TVector3& V,
							const float& Bz) {
      
      return cast_constituent_4(jcs, tracks, V, Bz, ReconstructedParticle2Track::XPtoPar_ct);
    }

   
    //Covariance matrix elements of tracks parameters
    //diagonal
    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							   const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_omega_cov);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                        const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Z0_cov);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi_cov);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_tanLambda_cov);
    }
    //off-diagonal
    rv::RVec<FCCAnalysesJetConstituentsData> get_d0_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							   const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_d0_z0_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							     const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_d0_phi0_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							     const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi0_z0_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_phi0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi0_tanlambda_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_d0_tanlambda_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_z0_tanlambda_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_tanlambda_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								     const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_omega_tanlambda_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_phi0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi0_omega_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							      const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_d0_omega_cov);
    }
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							      const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      return cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_omega_z0_cov);
    }
    

    //neutrals are set to 0; muons and electrons are also set to 0; 
    // only charged hads are considered (mtof used to disctriminate charged kaons and pions)
    rv::RVec<FCCAnalysesJetConstituentsData> get_dndx(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						      const rv::RVec<edm4hep::Quantity>& dNdx, //ETrackFlow_2 
						      const rv::RVec<edm4hep::TrackData>& trackdata,  //Eflowtrack
						      const rv::RVec<FCCAnalysesJetConstituentsData> JetsConstituents_isChargedHad) { 
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < jcs.size(); ++i){
	FCCAnalysesJetConstituents ct = jcs.at(i);
	FCCAnalysesJetConstituentsData isChargedHad = JetsConstituents_isChargedHad.at(i);
	FCCAnalysesJetConstituentsData tmp;
	for(int j = 0; j < ct.size(); ++j) {
	  if (ct.at(j).tracks_begin < trackdata.size() && (int)isChargedHad.at(j) == 1) {
	    tmp.push_back( dNdx.at( trackdata.at(ct.at(j).tracks_begin).dxQuantities_begin).value ); 
	  } else {
	    tmp.push_back(0.);
	  }
	}
	out.push_back(tmp);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dVal(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
							  const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      rv::RVec<FCCAnalysesJetConstituentsData> D0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
      rv::RVec<FCCAnalysesJetConstituentsData> phi0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);
      
      
      for(int i = 0; i < jets.size(); ++i){
	TVector2 p(jets[i].momentum.x, jets[i].momentum.y);
	FCCAnalysesJetConstituentsData cprojs;
	for (int j = 0; j < jcs[i].size(); ++j) {
	  if (D0.at(i).at(j) != -9) {
	    TVector2 d0( - D0.at(i).at(j) * TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j) * TMath::Cos(phi0.at(i).at(j))  );
	    cprojs.push_back( TMath::Sign(1, d0*p) * fabs(D0.at(i).at(j))  );
	  } else {
	    cprojs.push_back(-9.);
	  }
	}
	out.push_back(cprojs);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dVal_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								  const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      rv::RVec<FCCAnalysesJetConstituentsData> D0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
      rv::RVec<FCCAnalysesJetConstituentsData> phi0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);

      for(int i = 0; i < jets.size(); ++i){
        TVector2 p(jets[i].px(), jets[i].py());
        FCCAnalysesJetConstituentsData cprojs;
        for (int j = 0; j < jcs[i].size(); ++j) {
          if (D0.at(i).at(j) != -9) {
            TVector2 d0( - D0.at(i).at(j) * TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j) * TMath::Cos(phi0.at(i).at(j))  );
            cprojs.push_back( TMath::Sign(1, d0*p) * fabs(D0.at(i).at(j))  );
          } else {
            cprojs.push_back(-9.);
          }
        }
        out.push_back(cprojs);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dVal_clusterV(const rv::RVec<fastjet::PseudoJet>& jets,
								   const rv::RVec<FCCAnalysesJetConstituentsData>& D0,
								   const rv::RVec<FCCAnalysesJetConstituentsData>& phi0,
                                                                   const TVector3& V,
								   const float Bz) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;

      for(int i = 0; i < jets.size(); ++i){
        TVector2 p(jets[i].px(), jets[i].py());
        FCCAnalysesJetConstituentsData cprojs;
        for (int j = 0; j < D0[i].size(); ++j) {
          if (D0.at(i).at(j) != -9) {
            TVector2 d0( - D0.at(i).at(j) * TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j) * TMath::Cos(phi0.at(i).at(j))  );
            cprojs.push_back( TMath::Sign(1, d0*p) * fabs(D0.at(i).at(j))  );
          } else {
            cprojs.push_back(-9.);
          }
        }
        out.push_back(cprojs);
      }
      return out;
    }


    /// The functions get_Sip2dSig and get_Sip2dVal can be made independent;
    /// I passed to the former the result of the latter, avoiding the recomputation
    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dSig(const rv::RVec<FCCAnalysesJetConstituentsData>& Sip2dVals,
							  const rv::RVec<FCCAnalysesJetConstituentsData>& err2_D0) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < Sip2dVals.size(); ++i) {
	FCCAnalysesJetConstituentsData s;
	for(int j = 0; j < Sip2dVals.at(i).size(); ++j) {
	  if(err2_D0.at(i).at(j) > 0) {
	    s.push_back( Sip2dVals.at(i).at(j)/std::sqrt(err2_D0.at(i).at(j)) );
	  } else {
	    s.push_back(-9);
	  }
	}
	out.push_back(s);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dVal(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                          const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      rv::RVec<FCCAnalysesJetConstituentsData> D0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
      rv::RVec<FCCAnalysesJetConstituentsData> Z0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Z0);
      rv::RVec<FCCAnalysesJetConstituentsData> phi0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);
        
      for(int i = 0; i < jets.size(); ++i){
	TVector3 p(jets[i].momentum.x, jets[i].momentum.y, jets[i].momentum.z);
	FCCAnalysesJetConstituentsData cprojs;
        for (int j = 0; j < jcs[i].size(); ++j){
	  if(D0.at(i).at(j) != -9) {
	    TVector3 d( - D0.at(i).at(j) * TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j)*TMath::Cos(phi0.at(i).at(j)), Z0.at(i).at(j) );
	    cprojs.push_back( TMath::Sign(1, d*p) * fabs( sqrt( D0.at(i).at(j)*D0.at(i).at(j) + Z0.at(i).at(j)*Z0.at(i).at(j) ) ) );
	  } else {
	    cprojs.push_back(-9);
	  }
	}
	out.push_back(cprojs);
      } 
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dVal_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								  const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      rv::RVec<FCCAnalysesJetConstituentsData> D0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
      rv::RVec<FCCAnalysesJetConstituentsData> Z0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Z0);
      rv::RVec<FCCAnalysesJetConstituentsData> phi0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);

      for(int i = 0; i < jets.size(); ++i){
        TVector3 p(jets[i].px(), jets[i].py(), jets[i].pz());
        FCCAnalysesJetConstituentsData cprojs;
        for (int j = 0; j < jcs[i].size(); ++j){
          if(D0.at(i).at(j) != -9) {
            TVector3 d( - D0.at(i).at(j) * TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j)*TMath::Cos(phi0.at(i).at(j)), Z0.at(i).at(j) );
            cprojs.push_back( TMath::Sign(1, d*p) * fabs( sqrt( D0.at(i).at(j)*D0.at(i).at(j) + Z0.at(i).at(j)*Z0.at(i).at(j) ) ) );
          } else {
            cprojs.push_back(-9);
          }
        }
        out.push_back(cprojs);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dVal_clusterV(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& D0,
								   const rv::RVec<FCCAnalysesJetConstituentsData>& Z0,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& phi0,
                                                                   const TVector3& V,
                                                                   const float Bz) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;

      for(int i = 0; i < jets.size(); ++i){
        TVector3 p(jets[i].px(), jets[i].py(), jets[i].pz());
        FCCAnalysesJetConstituentsData cprojs;
        for (int j = 0; j < D0[i].size(); ++j){
          if(D0.at(i).at(j) != -9) {
            TVector3 d( - D0.at(i).at(j) * TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j)*TMath::Cos(phi0.at(i).at(j)), Z0.at(i).at(j) );
            cprojs.push_back( TMath::Sign(1, d*p) * fabs( sqrt( D0.at(i).at(j)*D0.at(i).at(j) + Z0.at(i).at(j)*Z0.at(i).at(j) ) ) );
          } else {
            cprojs.push_back(-9);
          }
        }
        out.push_back(cprojs);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dSig(const rv::RVec<FCCAnalysesJetConstituentsData>& Sip3dVals,
							  const rv::RVec<FCCAnalysesJetConstituentsData>& err2_D0,
							  const rv::RVec<FCCAnalysesJetConstituentsData>& err2_Z0) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < Sip3dVals.size(); ++i) {
	FCCAnalysesJetConstituentsData s;
	for(int j = 0; j < Sip3dVals.at(i).size(); ++j) {
	  if (err2_D0.at(i).at(j) > 0.) {
	    s.push_back( Sip3dVals.at(i).at(j)/sqrt( err2_D0.at(i).at(j) + err2_Z0.at(i).at(j) ) );
	  } else {
	    s.push_back(-9);
	  }
	}
	out.push_back(s);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistVal(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
							    const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      rv::RVec<FCCAnalysesJetConstituentsData> D0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
      rv::RVec<FCCAnalysesJetConstituentsData> Z0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Z0);
      rv::RVec<FCCAnalysesJetConstituentsData> phi0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);
      for(int i = 0; i < jets.size(); ++i){
	FCCAnalysesJetConstituentsData tmp;
	TVector3 p_jet(jets[i].momentum.x, jets[i].momentum.y, jets[i].momentum.z);
	FCCAnalysesJetConstituents ct = jcs.at(i);
	for(int j = 0; j < ct.size(); ++j) {
	  if (D0.at(i).at(j) != -9) { 
	    TVector3 d( - D0.at(i).at(j)* TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j)*TMath::Cos(phi0.at(i).at(j)), Z0.at(i).at(j) );
	    TVector3 p_ct(ct[j].momentum.x, ct[j].momentum.y, ct[j].momentum.z);
	    TVector3 r_jet(0.0, 0.0, 0.0);
	    TVector3 n = p_ct.Cross(p_jet).Unit(); //What if they are parallel?
	    tmp.push_back( n.Dot(d - r_jet) );
	  } else {
	    tmp.push_back(-9);
	  }
	}
	out.push_back(tmp);
      }
      return out;
    }

    
    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistVal_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								    const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      rv::RVec<FCCAnalysesJetConstituentsData> D0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_D0);
      rv::RVec<FCCAnalysesJetConstituentsData> Z0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_Z0);
      rv::RVec<FCCAnalysesJetConstituentsData> phi0 = cast_constituent_2(jcs, tracks, ReconstructedParticle2Track::getRP2TRK_phi);
      for(int i = 0; i < jets.size(); ++i){
        FCCAnalysesJetConstituentsData tmp;
        TVector3 p_jet(jets[i].px(), jets[i].py(), jets[i].pz());
        FCCAnalysesJetConstituents ct = jcs.at(i);
        for(int j = 0; j < ct.size(); ++j) {
          if (D0.at(i).at(j) != -9) {
            TVector3 d( - D0.at(i).at(j)* TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j)*TMath::Cos(phi0.at(i).at(j)), Z0.at(i).at(j) );
            TVector3 p_ct(ct[j].momentum.x, ct[j].momentum.y, ct[j].momentum.z);
            TVector3 r_jet(0.0, 0.0, 0.0);
            TVector3 n = p_ct.Cross(p_jet).Unit(); //What if they are parallel? 
            tmp.push_back( n.Dot(d - r_jet) );
          } else {
            tmp.push_back(-9);
          }
        }
        out.push_back(tmp);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistVal_clusterV(const rv::RVec<fastjet::PseudoJet>& jets,
								     const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								     const rv::RVec<FCCAnalysesJetConstituentsData>& D0,
								     const rv::RVec<FCCAnalysesJetConstituentsData>& Z0,
								     const rv::RVec<FCCAnalysesJetConstituentsData>& phi0,
								     const TVector3& V,
								     const float Bz) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;

      for(int i = 0; i < jets.size(); ++i){
        FCCAnalysesJetConstituentsData tmp;
        TVector3 p_jet(jets[i].px(), jets[i].py(), jets[i].pz());
        FCCAnalysesJetConstituents ct = jcs.at(i);
        for(int j = 0; j < ct.size(); ++j) {
          if (D0.at(i).at(j) != -9) {
            TVector3 d( - D0.at(i).at(j)* TMath::Sin(phi0.at(i).at(j)) , D0.at(i).at(j)*TMath::Cos(phi0.at(i).at(j)), Z0.at(i).at(j) );
            TVector3 p_ct(ct[j].momentum.x, ct[j].momentum.y, ct[j].momentum.z);
            TVector3 r_jet(0.0, 0.0, 0.0);
            TVector3 n = p_ct.Cross(p_jet).Unit(); //What if they are parallel?                                                                                                                             
            tmp.push_back( n.Dot(d - r_jet) );
          } else {
            tmp.push_back(-9);
          }
        }
        out.push_back(tmp);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistSig(const rv::RVec<FCCAnalysesJetConstituentsData>& JetDistVal, 
							    const rv::RVec<FCCAnalysesJetConstituentsData>& err2_D0,
							    const rv::RVec<FCCAnalysesJetConstituentsData>& err2_Z0) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < JetDistVal.size(); ++i) {
	FCCAnalysesJetConstituentsData tmp;
	for(int j = 0; j < JetDistVal.at(i).size(); ++j) {
	  if (err2_D0.at(i).at(j) > 0) {
	    float err3d = std::sqrt(err2_D0.at(i).at(j) + err2_Z0.at(i).at(j));
	    float jetdistsig = JetDistVal.at(i).at(j) / err3d;
	    tmp.push_back(jetdistsig);
	  } else {
	    tmp.push_back(-9.);
	  }
	}
	out.push_back(tmp);
      }
      return out;
    }


    //we measure L, tof; mtof in GeV
    //neutrals are set to 0; muons and electrons are set to their mass;
    // only charged hads are considered (mtof used to disctriminate charged kaons and pions)
    rv::RVec<FCCAnalysesJetConstituentsData> get_mtof(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						      const rv::RVec<float>& track_L,
						      const rv::RVec<edm4hep::TrackData>& trackdata,
						      const rv::RVec<edm4hep::TrackerHitData>& trackerhits, 
						      const rv::RVec<FCCAnalysesJetConstituentsData> JetsConstituents_Pids) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < jcs.size(); ++i){
	FCCAnalysesJetConstituents ct = jcs.at(i);
	FCCAnalysesJetConstituentsData pids = JetsConstituents_Pids.at(i);
	FCCAnalysesJetConstituentsData tmp;
	for(int j = 0; j < ct.size(); ++j) {
	  //if(ct.at(j).tracks_begin > 0 && ct.at(j).tracks_begin < trackdata.size()) { //??????????? CHECK!!!
	  if (ct.at(j).tracks_begin < trackdata.size()) {
	    if( abs(pids.at(j)) == 11) {
	      tmp.push_back(0.00051099895);
	    } else if (abs(pids.at(j)) == 13) {
	      tmp.push_back(105.65837);
	    } else {
	      float Tin = trackerhits.at(trackdata.at(ct.at(j).tracks_begin).trackerHits_begin).time;
	      float Tout = trackerhits.at(trackdata.at(ct.at(j).tracks_begin).trackerHits_end-1).time; //one track and two hits per recon. particle are assumed
	      float tof = (Tout - Tin);
	      float L = track_L.at(ct.at(j).tracks_begin) * 0.001;
	      //std::cout << "tof: " << tof << "  -  L: " << L <<  << std::endl;
	      float beta = L/(tof * 2.99792458e+8) ;
	      float p = std::sqrt( ct.at(j).momentum.x*ct.at(j).momentum.x + ct.at(j).momentum.y*ct.at(j).momentum.y + ct.at(j).momentum.z * ct.at(j).momentum.z );
	      //std::cout << "tof: " << tof << " - L: " << L << " - beta: " << beta << " - momentum: " << p << " - mtof: " << p * std::sqrt(1/(beta*beta)-1) << std::endl;
	      if (beta < 1. && beta > 0.) {
		tmp.push_back( p * std::sqrt(1/(beta*beta)-1) ); 
	      } else {
		tmp.push_back(0.13957039);
	      } 
	    }
	  } else {
	    //float E = ct.at(j).energy;
	    //tmp.pushback( E * std::sqrt(1-beta*beta) );
	    tmp.push_back(0.);
	  }
	}
	out.push_back(tmp);
      }
      return out;
    }
    

    //kinematics const/jet
    rv::RVec<FCCAnalysesJetConstituentsData> get_erel_log(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        float e_jet = jets.at(i).energy;
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          float val = (e_jet > 0.) ? jc.energy / e_jet : 1.;
          float erel_log = float(std::log10(val));
          jet_csts.emplace_back(erel_log);
        }
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_erel_log_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								  const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        float e_jet = jets.at(i).E();
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          float val = (e_jet > 0.) ? jc.energy / e_jet : 1.;
          float erel_log = float(std::log10(val));
          jet_csts.emplace_back(erel_log);
        }
      }
      return out;
    }

    
    rv::RVec<FCCAnalysesJetConstituentsData> get_erel(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        double e_jet = jets.at(i).energy;
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          float val = (e_jet > 0.) ? jc.energy / e_jet : 1.;
          float erel = val;
          jet_csts.emplace_back(erel);
        }
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_erel_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
							      const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        double e_jet = jets.at(i).E();
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          float val = (e_jet > 0.) ? jc.energy / e_jet : 1.;
          float erel = val;
          jet_csts.emplace_back(erel);
        }
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_thetarel(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        TLorentzVector tlv_jet;
        tlv_jet.SetXYZM(jets.at(i).momentum.x, jets.at(i).momentum.y, jets.at(i).momentum.z, jets.at(i).mass);
        float theta_jet = tlv_jet.Theta();
        float phi_jet = tlv_jet.Phi();
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          TLorentzVector tlv_const;
          tlv_const.SetXYZM(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.mass);
          TVector3 v_const = tlv_const.Vect();
          v_const.RotateZ(-phi_jet);
          v_const.RotateY(-theta_jet);
          float theta_rel = v_const.Theta();
          jet_csts.emplace_back(theta_rel);
        }
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_thetarel_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								  const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        TLorentzVector tlv_jet;
        tlv_jet.SetXYZM(jets.at(i).px(), jets.at(i).py(), jets.at(i).pz(), jets.at(i).E());
        float theta_jet = tlv_jet.Theta();
        float phi_jet = tlv_jet.Phi();
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          TLorentzVector tlv_const;
          tlv_const.SetXYZM(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
          TVector3 v_const = tlv_const.Vect();
          v_const.RotateZ(-phi_jet);
          v_const.RotateY(-theta_jet);
          float theta_rel = v_const.Theta();
          jet_csts.emplace_back(theta_rel);
        }
      }
      return out;
    }

    
    rv::RVec<FCCAnalysesJetConstituentsData> get_phirel(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                        const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        TLorentzVector tlv_jet;
        tlv_jet.SetXYZM(jets.at(i).momentum.x, jets.at(i).momentum.y, jets.at(i).momentum.z, jets.at(i).mass);
        float theta_jet = tlv_jet.Theta();
        float phi_jet = tlv_jet.Phi();
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          TLorentzVector tlv_const;
          tlv_const.SetXYZM(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.mass);
          TVector3 v_const = tlv_const.Vect();
          v_const.RotateZ(-phi_jet);
          v_const.RotateY(-theta_jet);
          float phi_rel = v_const.Phi();
          jet_csts.emplace_back(phi_rel);
        }
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_phirel_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (size_t i = 0; i < jets.size(); ++i) {
        auto& jet_csts = out.emplace_back();
        TLorentzVector tlv_jet;
        tlv_jet.SetXYZM(jets.at(i).px(), jets.at(i).py(), jets.at(i).pz(), jets.at(i).E());
        float theta_jet = tlv_jet.Theta();
        float phi_jet = tlv_jet.Phi();
        auto csts = get_jet_constituents(jcs, i);
        for (const auto& jc : csts) {
          TLorentzVector tlv_const;
          tlv_const.SetXYZM(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.mass);
          TVector3 v_const = tlv_const.Vect();
          v_const.RotateZ(-phi_jet);
          v_const.RotateY(-theta_jet);
          float phi_rel = v_const.Phi();
          jet_csts.emplace_back(phi_rel);
        }
      }
      return out;
    }


    
    //Identification
    
    rv::RVec<FCCAnalysesJetConstituentsData> get_PIDs(const ROOT::VecOps::RVec< int > recin,
						      const ROOT::VecOps::RVec< int > mcin,
						      const rv::RVec<edm4hep::ReconstructedParticleData>& RecPart, 
						      const rv::RVec<edm4hep::MCParticleData>& Particle,
						      const rv::RVec<edm4hep::ReconstructedParticleData>& jets) { 
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      FCCAnalysesJetConstituentsData PIDs = FCCAnalyses::ReconstructedParticle2MC::getRP2MC_pdg(recin, mcin, RecPart, Particle);
      
      for (const auto& jet : jets) {
	FCCAnalysesJetConstituentsData tmp;
        for (auto it = jet.particles_begin; it < jet.particles_end; ++it) {
          tmp.push_back(PIDs.at(it));
	}
	out.push_back(tmp);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_PIDs_cluster(const ROOT::VecOps::RVec< int > recin,
							      const ROOT::VecOps::RVec< int > mcin,
							      //const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							      const rv::RVec<edm4hep::ReconstructedParticleData>& RecPart,
							      const rv::RVec<edm4hep::MCParticleData>& Particle,
							      const std::vector<std::vector<int>>& indices) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      FCCAnalysesJetConstituentsData PIDs = FCCAnalyses::ReconstructedParticle2MC::getRP2MC_pdg(recin, mcin, RecPart, Particle);

      for (const auto& jet_index : indices) {
        FCCAnalysesJetConstituentsData tmp;
        for (const auto& const_index : jet_index) {
          tmp.push_back(PIDs.at(const_index));
        }
        out.push_back(tmp);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_isMu(const rv::RVec<FCCAnalysesJetConstituentsData>& PIDs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;      
      for(int i = 0; i < PIDs.size(); ++i) {
	FCCAnalysesJetConstituentsData is_Mu;
	for (int j = 0; j < PIDs.at(i).size(); ++j) {
	  if ( abs(PIDs.at(i).at(j)) == 13) {                                                                                         
	    is_Mu.push_back(1.);                                                                                                                                        
          } else {                                                                                                                                                   
            is_Mu.push_back(0.);                                                                                                                                                     
	  }
	}
	out.push_back(is_Mu);
      }
      return out;
    }


    rv::RVec<FCCAnalysesJetConstituentsData> get_isEl(const rv::RVec<FCCAnalysesJetConstituentsData>& PIDs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < PIDs.size(); ++i) {
        FCCAnalysesJetConstituentsData is_El;
        FCCAnalysesJetConstituentsData pids = PIDs.at(i);
	for (int j = 0; j < pids.size(); ++j) {                                                                                                                                     
	  if ( abs(pids.at(j)) == 11) {                                                                                                     
	    is_El.push_back(1.);       
	  } else {                                                                                                                                  
            is_El.push_back(0.);                                                                                                                                                     
	  }
	}
	out.push_back(is_El);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_isChargedHad(const rv::RVec<FCCAnalysesJetConstituentsData>& PIDs, 
							      const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < PIDs.size(); ++i) {
        FCCAnalysesJetConstituentsData is_ChargedHad;
        FCCAnalysesJetConstituents ct = jcs.at(i);
	FCCAnalysesJetConstituentsData pids = PIDs.at(i);
        for (int j = 0; j < pids.size(); ++j) {
	  if (ct.at(j).charge != 0 && abs(pids.at(j)) != 11 && abs(pids.at(j)) != 13) {                                                                                                       
	    is_ChargedHad.push_back(1.);                                                                                                                                        
	  } else {                                                                                                                                                 
            is_ChargedHad.push_back(0.);                                                                                                                                 
          }
	}
        out.push_back(is_ChargedHad);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_isGamma(const rv::RVec<FCCAnalysesJetConstituentsData>& PIDs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < PIDs.size(); ++i) {
        FCCAnalysesJetConstituentsData is_Gamma;
        FCCAnalysesJetConstituentsData pids = PIDs.at(i);
        for (int j = 0; j < pids.size(); ++j) {
          if ( abs(pids.at(j)) == 22) {
            is_Gamma.push_back(1.);
          } else {
            is_Gamma.push_back(0.);
          }
        }
        out.push_back(is_Gamma);
      }
      return out;
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_isNeutralHad(const rv::RVec<FCCAnalysesJetConstituentsData>& PIDs,
							      const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for(int i = 0; i < PIDs.size(); ++i) {
        FCCAnalysesJetConstituentsData is_NeutralHad;
        FCCAnalysesJetConstituents ct = jcs.at(i);
        FCCAnalysesJetConstituentsData pids = PIDs.at(i);
        for (int j = 0; j < pids.size(); ++j) {
	  if (ct.at(j).charge == 0 && abs(pids.at(j)) != 22 )                                                                                      
            is_NeutralHad.push_back(1.);                                                                                                                         
	  else                      
	    is_NeutralHad.push_back(0.);                                                                                                
	}
	out.push_back(is_NeutralHad);
      }
      return out;
    }


    //countings
    int count_jets(rv::RVec<FCCAnalysesJetConstituents> jets) {
      return jets.size();
    }
    
    rv::RVec<int> count_consts(rv::RVec<FCCAnalysesJetConstituents> jets) {
      rv::RVec<int> out;
      for(int i = 0; i < jets.size(); ++i) {
	out.push_back(jets.at(i).size());
      }
      return out;
    }

    rv::RVec<int> count_type(const rv::RVec<FCCAnalysesJetConstituentsData>& isType) {
      rv::RVec<int> out;
      for(int i = 0; i < isType.size(); ++i){
	int count = 0;
	rv::RVec<float> istype = isType.at(i);
	for(int j = 0; j < istype.size(); ++j){
	  if( (int)(istype.at(j)) == 1) count++;
	}
	out.push_back(count);
      }
      return out;
    }

    //compute residues
    rv::RVec<TLorentzVector> compute_tlv_jets(const rv::RVec<fastjet::PseudoJet>& jets) {
      rv::RVec<TLorentzVector> out;
      for(const auto& jet : jets) {
	TLorentzVector tlv_jet;
	tlv_jet.SetPxPyPzE(jet.px(), jet.py(), jet.pz(), jet.E());
	out.push_back(tlv_jet);
      }
      return out;
    }

    rv::RVec<TLorentzVector> sum_tlv_constituents(const rv::RVec<FCCAnalysesJetConstituents>& jets) {
      rv::RVec<TLorentzVector> out;
      for (int i = 0; i < jets.size(); ++i) {
	TLorentzVector sum_tlv; // initialized by (0., 0., 0., 0.)
	FCCAnalysesJetConstituents jcs = jets.at(i);
	for (const auto& jc : jcs) {
	  TLorentzVector tlv;
	  tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
	  sum_tlv += tlv;
	}
	out.push_back(sum_tlv);
      }
      return out;
    }
    
    float InvariantMass(const TLorentzVector& tlv1, const TLorentzVector& tlv2) {
      float E = tlv1.E() + tlv2.E();
      float px = tlv1.Px() + tlv2.Px();
      float py = tlv1.Py() + tlv2.Py();
      float pz = tlv1.Pz() + tlv2.Pz();
      return std::sqrt(E*E - px*px - py*py - pz*pz);
    }

    rv::RVec<double> compute_residue_energy(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
	float de = (sum_tlv_jcs.at(i).E() - tlv_jet.at(i).E())/tlv_jet.at(i).E();
	out.push_back(de);
      }
      return out;
    }

    rv::RVec<double> compute_residue_px(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
        float dpx = (sum_tlv_jcs.at(i).Px() - tlv_jet.at(i).Px())/tlv_jet.at(i).Px();
        out.push_back(dpx);
      }
      return out;
    }

    rv::RVec<double> compute_residue_py(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
        float dpy = (sum_tlv_jcs.at(i).Py() - tlv_jet.at(i).Py())/tlv_jet.at(i).Py();
        out.push_back(dpy);
      }
      return out;
    }

    rv::RVec<double> compute_residue_pz(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
        float dpz = (sum_tlv_jcs.at(i).Pz() - tlv_jet.at(i).Pz())/tlv_jet.at(i).Pz();
        out.push_back(dpz);
      }
      return out;
    }

    rv::RVec<double> compute_residue_pt(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
	double pt_jet = std::sqrt( tlv_jet.at(i).Px()*tlv_jet.at(i).Px() + tlv_jet.at(i).Py()*tlv_jet.at(i).Py() );
	double pt_jcs = std::sqrt( sum_tlv_jcs.at(i).Px()*sum_tlv_jcs.at(i).Px() + sum_tlv_jcs.at(i).Py()*sum_tlv_jcs.at(i).Py() );
	double dpt = ( pt_jcs - pt_jet)/pt_jet;
	out.push_back(dpt);
      } 
      return out;
    }

    rv::RVec<double> compute_residue_phi(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
	double phi_jet = tlv_jet.at(i).Phi();
        double phi_jcs = sum_tlv_jcs.at(i).Phi();
	double dphi = (phi_jcs - phi_jet)/phi_jet;
	out.push_back(dphi);
      }
      return out;
    }

    rv::RVec<double> compute_residue_theta(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs) {
      rv::RVec<double> out;
      for(int i = 0; i < tlv_jet.size(); ++i) {
	double theta_jet = tlv_jet.at(i).Theta();
	double theta_jcs = sum_tlv_jcs.at(i).Theta();
	double dtheta = (theta_jcs - theta_jet)/theta_jet;
	out.push_back(dtheta);
      } 
      return out;
    }


  }  // namespace JetConstituentsUtils
}  // namespace FCCAnalyses
