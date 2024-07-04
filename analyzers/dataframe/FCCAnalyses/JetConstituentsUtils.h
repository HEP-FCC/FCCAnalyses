#ifndef FCCAnalyses_JetConstituentsUtils_h
#define FCCAnalyses_JetConstituentsUtils_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"
#include "edm4hep/MCParticle.h"
#include "edm4hep/Quantity.h"
#if __has_include("edm4hep/TrackerHit3DData.h")
#include "edm4hep/TrackerHit3DData.h"
#else
#include "edm4hep/TrackerHitData.h"
namespace edm4hep {
  using TrackerHit3DData = edm4hep::TrackerHitData;
}
#endif

#include "fastjet/JetDefinition.hh"

#include "TMath.h"
#include "TVector3.h"
#include "TRotation.h"
#include "TLorentzVector.h"

namespace FCCAnalyses {
  namespace JetConstituentsUtils {
    namespace rv = ROOT::VecOps;
    using FCCAnalysesJetConstituents = rv::RVec<edm4hep::ReconstructedParticleData>;
    using FCCAnalysesJetConstituentsData = rv::RVec<float>;

    /// Build the collection of constituents (mapping jet -> reconstructed particles) for all jets in event
    rv::RVec<FCCAnalysesJetConstituents> build_constituents(const rv::RVec<edm4hep::ReconstructedParticleData>&,
                                                            const rv::RVec<edm4hep::ReconstructedParticleData>&);

    rv::RVec<FCCAnalysesJetConstituents> build_constituents_cluster(const rv::RVec<edm4hep::ReconstructedParticleData>& rps,
                                                                    const std::vector<std::vector<int>>& indices);

    /// Retrieve the constituents of an indexed jet in event
    FCCAnalysesJetConstituents get_jet_constituents(const rv::RVec<FCCAnalysesJetConstituents>&, int);
    /// Retrieve the constituents of a collection of indexed jets in event
    rv::RVec<FCCAnalysesJetConstituents> get_constituents(const rv::RVec<FCCAnalysesJetConstituents>&,
                                                          const rv::RVec<int>&);


    //sorting jets
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets_sorting_on_nconst(const rv::RVec<edm4hep::ReconstructedParticleData>&);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets_sorting_on_energy(const rv::RVec<edm4hep::ReconstructedParticleData>&);


    rv::RVec<FCCAnalysesJetConstituentsData> get_Bz(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_pt(const rv::RVec<FCCAnalysesJetConstituents>&);
    rv::RVec<FCCAnalysesJetConstituentsData> get_p(const rv::RVec<FCCAnalysesJetConstituents>&);
    rv::RVec<FCCAnalysesJetConstituentsData> get_e(const rv::RVec<FCCAnalysesJetConstituents>&);
    rv::RVec<FCCAnalysesJetConstituentsData> get_theta(const rv::RVec<FCCAnalysesJetConstituents>&);
    rv::RVec<FCCAnalysesJetConstituentsData> get_phi(const rv::RVec<FCCAnalysesJetConstituents>&);
    rv::RVec<FCCAnalysesJetConstituentsData> get_type(const rv::RVec<FCCAnalysesJetConstituents>&);
    rv::RVec<FCCAnalysesJetConstituentsData> get_charge(const rv::RVec<FCCAnalysesJetConstituents>&);

    //displacement
    rv::RVec<FCCAnalysesJetConstituentsData> get_d0(const rv::RVec<FCCAnalysesJetConstituents>&,
						    const ROOT::VecOps::RVec<edm4hep::TrackState>&);

    rv::RVec<FCCAnalysesJetConstituentsData> get_z0(const rv::RVec<FCCAnalysesJetConstituents>& ,
                                                    const ROOT::VecOps::RVec<edm4hep::TrackState>&);

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						      const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_omega(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
						       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanLambda(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							   const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);


    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_dxy(const rv::RVec<FCCAnalysesJetConstituents>&,
							 const ROOT::VecOps::RVec<edm4hep::TrackState>&,
							 const TLorentzVector& V, // primary vertex
							 const float&);
    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_dz(const rv::RVec<FCCAnalysesJetConstituents>&,
							const ROOT::VecOps::RVec<edm4hep::TrackState>&,
							const TLorentzVector& V, // primary vertex
							const float&);
    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_phi(const rv::RVec<FCCAnalysesJetConstituents>&,
                                                         const ROOT::VecOps::RVec<edm4hep::TrackState>&,
                                                         const TLorentzVector& V, // primary vertex
                                                         const float&);
    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_C(const rv::RVec<FCCAnalysesJetConstituents>&,
						       const ROOT::VecOps::RVec<edm4hep::TrackState>&,
						       const float&);
    rv::RVec<FCCAnalysesJetConstituentsData> XPtoPar_ct(const rv::RVec<FCCAnalysesJetConstituents>&,
							const ROOT::VecOps::RVec<edm4hep::TrackState>&,
							const float&);

    //covariance matrix
    //diagonal
    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_cov(const rv::RVec<FCCAnalysesJetConstituents>&,
							   const ROOT::VecOps::RVec<edm4hep::TrackState>&);

    rv::RVec<FCCAnalysesJetConstituentsData> get_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>&,
							const ROOT::VecOps::RVec<edm4hep::TrackState>& );

    rv::RVec<FCCAnalysesJetConstituentsData> get_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);
    //off-diag
    rv::RVec<FCCAnalysesJetConstituentsData> get_d0_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi0_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_phi0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								   const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								 const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_tanlambda_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								 const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_tanlambda_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
								    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_phi0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_d0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							     const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_omega_z0_cov(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
							     const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);


    rv::RVec<FCCAnalysesJetConstituentsData> get_dndx(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                      const rv::RVec<edm4hep::Quantity>& dNdx,
						      const rv::RVec<edm4hep::TrackData>& trackdata,
						      const rv::RVec<FCCAnalysesJetConstituentsData> JetsConstituents_isChargedHad);

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dVal(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                          const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dVal_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                  const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                                  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dVal_clusterV(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& D0,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& phi0,
                                                                   const float Bz);


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip2dSig(const rv::RVec<FCCAnalysesJetConstituentsData>& Sip2dVals,
                                                          const rv::RVec<FCCAnalysesJetConstituentsData>& err2_D0);

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dVal(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                          const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);


    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dVal_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                  const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                                  const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dVal_clusterV(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& D0,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& Z0,
                                                                   const rv::RVec<FCCAnalysesJetConstituentsData>& phi0,
                                                                   const float Bz);

    rv::RVec<FCCAnalysesJetConstituentsData> get_Sip3dSig(const rv::RVec<FCCAnalysesJetConstituentsData>& Sip3dVals,
                                                          const rv::RVec<FCCAnalysesJetConstituentsData>& err2_D0,
                                                          const rv::RVec<FCCAnalysesJetConstituentsData>& err2_Z0);

    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistVal(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                            const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                            const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistVal_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                    const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                                    const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks);

    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistVal_clusterV(const rv::RVec<fastjet::PseudoJet>& jets,
                                                                     const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                                     const rv::RVec<FCCAnalysesJetConstituentsData>& D0,
                                                                     const rv::RVec<FCCAnalysesJetConstituentsData>& Z0,
                                                                     const rv::RVec<FCCAnalysesJetConstituentsData>& phi0,
                                                                     const float Bz);

    rv::RVec<FCCAnalysesJetConstituentsData> get_JetDistSig(const rv::RVec<FCCAnalysesJetConstituentsData>& JetDistVal,
                                                            const rv::RVec<FCCAnalysesJetConstituentsData>& err2_D0,
                                                            const rv::RVec<FCCAnalysesJetConstituentsData>& err2_Z0);

    rv::RVec<FCCAnalysesJetConstituentsData> get_mtof(const rv::RVec<FCCAnalysesJetConstituents>& jcs,
                                                      const rv::RVec<float>& track_L,
                                                      const rv::RVec<edm4hep::TrackData>& trackdata,
                                                      const rv::RVec<edm4hep::TrackerHit3DData>& trackerhits,
                                                      const rv::RVec<edm4hep::ClusterData>& gammadata,
                                                      const rv::RVec<edm4hep::ClusterData>& nhdata,
                                                      const rv::RVec<edm4hep::CalorimeterHitData>& calohits,
                                                      const TLorentzVector& V // primary vertex
						                                          );


    rv::RVec<FCCAnalysesJetConstituentsData> get_PIDs(const ROOT::VecOps::RVec< int > recin,
						      const ROOT::VecOps::RVec< int > mcin,
						      const rv::RVec<edm4hep::ReconstructedParticleData>& RecPart,
						      const rv::RVec<edm4hep::MCParticleData>& Particle,
						      const rv::RVec<edm4hep::ReconstructedParticleData>& Jets);

    rv::RVec<FCCAnalysesJetConstituentsData> get_PIDs_cluster(const ROOT::VecOps::RVec< int > recin,
                                                              const ROOT::VecOps::RVec< int > mcin,
                                                              const rv::RVec<edm4hep::ReconstructedParticleData>& RecPart,
                                                              const rv::RVec<edm4hep::MCParticleData>& Particle,
                                                              const std::vector<std::vector<int>>& indices);

    rv::RVec<FCCAnalysesJetConstituentsData> get_isMu(const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_isEl(const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_isChargedHad(const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_isGamma(const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_isNeutralHad(const rv::RVec<FCCAnalysesJetConstituents>& jcs);

    //countings
    int count_jets(rv::RVec<FCCAnalysesJetConstituents> jets);
    rv::RVec<int> count_consts(rv::RVec<FCCAnalysesJetConstituents> jets);
    rv::RVec<int> count_type(const rv::RVec<FCCAnalysesJetConstituentsData>& isType);



    rv::RVec<FCCAnalysesJetConstituentsData> get_erel(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
						      const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_erel_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
                                                              const rv::RVec<FCCAnalysesJetConstituents>& jcs);

    rv::RVec<FCCAnalysesJetConstituentsData> get_erel_log(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_erel_log_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
								  const rv::RVec<FCCAnalysesJetConstituents>& jcs);

    rv::RVec<FCCAnalysesJetConstituentsData> get_thetarel(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                          const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_thetarel_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
                                                              const rv::RVec<FCCAnalysesJetConstituents>& jcs);

    rv::RVec<FCCAnalysesJetConstituentsData> get_phirel(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                        const rv::RVec<FCCAnalysesJetConstituents>& jcs);
    rv::RVec<FCCAnalysesJetConstituentsData> get_phirel_cluster(const rv::RVec<fastjet::PseudoJet>& jets,
                                                              const rv::RVec<FCCAnalysesJetConstituents>& jcs);

    //residues
    rv::RVec<TLorentzVector> compute_tlv_jets(const rv::RVec<fastjet::PseudoJet>& jets);
    rv::RVec<TLorentzVector> sum_tlv_constituents(const rv::RVec<FCCAnalysesJetConstituents>& jets);
    float InvariantMass(const TLorentzVector& tlv1, const TLorentzVector& tlv2);
    
    /**
     * @brief all_invariant_masses takes an RVec of TLorentzVectors of jets and computes the invariant masses of all jet pairs, and returns an RVec with all invariant masses.
    */
    rv::RVec<double> all_invariant_masses(rv::RVec<TLorentzVector> AllJets);
    rv::RVec<double> compute_residue_energy(const rv::RVec<TLorentzVector>& tlv_jet,
					    const rv::RVec<TLorentzVector>& sum_tlv_jcs);
    rv::RVec<double> compute_residue_pt(const rv::RVec<TLorentzVector>& tlv_jet,
					const rv::RVec<TLorentzVector>& sum_tlv_jcs);
    rv::RVec<double> compute_residue_phi(const rv::RVec<TLorentzVector>& tlv_jet,
					 const rv::RVec<TLorentzVector>& sum_tlv_jcs);
    rv::RVec<double> compute_residue_theta(const rv::RVec<TLorentzVector>& tlv_jet,
					 const rv::RVec<TLorentzVector>& sum_tlv_jcs);
    rv::RVec<double> compute_residue_px(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs);
    rv::RVec<double> compute_residue_py(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs);
    rv::RVec<double> compute_residue_pz(const rv::RVec<TLorentzVector>& tlv_jet, const rv::RVec<TLorentzVector>& sum_tlv_jcs);

  }  // namespace JetConstituentsUtils
}  // namespace FCCAnalyses

#endif
