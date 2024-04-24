#ifndef  VERTEXFINDERLCFIPLUS_ANALYZERS_H
#define  VERTEXFINDERLCFIPLUS_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackState.h"

#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/VertexFitterSimple.h"
#include "FCCAnalyses/VertexingUtils.h"

#include "fastjet/JetDefinition.hh"

namespace FCCAnalyses{
/**
 * Primary and Seconday Vertex Finder interface using vertex fitter from
 * VertexFitterSimple.
 *
 * This represents a set functions and utilities to find vertices from a list
 * of tracks following the algorithm from LCFIPlus framework.
 */

namespace VertexFinderLCFIPlus{

  /** returns SVs reconstructed from non-primary tracks of jets
   *  non-primary separated from all tracks using isInPrimary (bool) vector
   *  currently not separating SVs by jet
   */
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>> get_SV_jets( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
											 ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
											 VertexingUtils::FCCAnalysesVertex PV,
											 ROOT::VecOps::RVec<bool> isInPrimary,
											 ROOT::VecOps::RVec<fastjet::PseudoJet> jets,
											 std::vector<std::vector<int>> jet_consti,
											 bool V0_rej=true,
											 double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5. ) ;
  
  /** returns SVs reconstructed from non-primary tracks of the event
   *  SV finding done before jet clustering
   *  non-primary separated from all tracks using isInPrimary (bool) vector
   */
  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> get_SV_event( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
								      ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
								      VertexingUtils::FCCAnalysesVertex PV,
								      ROOT::VecOps::RVec<bool> isInPrimary,
								      bool V0_rej=true,
								      double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5. ) ;

  /** returns SVs reconstructed from non-primary tracks of the event
   *  SV finding done before jet clustering
   */
  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> get_SV_event( ROOT::VecOps::RVec<edm4hep::TrackState> np_tracks,
                                                                      ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
								      VertexingUtils::FCCAnalysesVertex PV,
								      bool V0_rej=true,
								      double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5. ) ;
  
  /** returns indices of the best pair of tracks from a vector of (non-primary) tracks 
   *  default chi2 threshold is 9 and default invariant mass threshold is 10GeV
   */
  ROOT::VecOps::RVec<int> VertexSeed_best( ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
					   VertexingUtils::FCCAnalysesVertex PV,
					   double chi2_cut=9., double invM_cut=10.) ;

  /** adds index of the best track (from the remaining tracks) to the (seed) vtx 
   *  default chi2 threshold is 9 and default invariant mass threshold is 10GeV
   *  default threshold for track's chi2 contribution is 5 (?)
   */
  ROOT::VecOps::RVec<int> addTrack_best( ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
  					 ROOT::VecOps::RVec<int> vtx_tr,
  					 VertexingUtils::FCCAnalysesVertex PV,
  					 double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5.) ;

  /** V0 rejection (tight)
   *  takes all (non-primary tracks) & removes tracks coming from V0s if user chooses
   *  by default V0 rejection is done
   */
  ROOT::VecOps::RVec<edm4hep::TrackState> V0rejection_tight( ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
							     VertexingUtils::FCCAnalysesVertex PV,
							     bool V0_rej=true ) ;

  /** find SVs from a set of tracks
   *  default values of thresholds for the constraints are set
   */
  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> findSVfromTracks( ROOT::VecOps::RVec<edm4hep::TrackState> tracks_fin,
                                                                          const ROOT::VecOps::RVec<edm4hep::TrackState>& alltracks,
									  VertexingUtils::FCCAnalysesVertex PV,
									  double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5.) ;

  /** check constraints of vertex candidates
   *  default values of thresholds for the constraints are set
   *  default constraint check is that for finding vertex seed
   *  seed=true -> constraints for seed; seed=false -> constraints for adding tracks
   */
  bool check_constraints( VertexingUtils::FCCAnalysesVertex vtx,
			  ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
			  VertexingUtils::FCCAnalysesVertex PV,
			  bool seed=true,
			  double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5.) ;
  
  /** V0 rejection/identification
   *  takes all (non-primary) tracks & assigns "true" to pairs that form a V0
   *  if(tight)  -> tight constraints
   *  if(!tight) -> loose constraints
   *  by default loose constraints
   */
  ROOT::VecOps::RVec<bool> isV0( ROOT::VecOps::RVec<edm4hep::TrackState> np_tracks,
				 VertexingUtils::FCCAnalysesVertex PV,
				 bool tight = false ) ;

  ///
  
  /** returns V0s reconstructed from a set of tracks (as an FCCAnalysesV0 object)
   *  constraint thresholds can be chosen out of two sets
   */
  VertexingUtils::FCCAnalysesV0 get_V0s( ROOT::VecOps::RVec<edm4hep::TrackState> np_tracks,
					 VertexingUtils::FCCAnalysesVertex PV,
					 bool tight,
					 double chi2_cut=9. ) ;

  /** returns V0s reconstructed from a set of tracks (as an FCCAnalysesV0 object)
   *  constraint thresholds can be set manually
   */
  VertexingUtils::FCCAnalysesV0 get_V0s( ROOT::VecOps::RVec<edm4hep::TrackState> np_tracks,
					 VertexingUtils::FCCAnalysesVertex PV,
					 double Ks_invM_low=0.493, double Ks_invM_high=0.503, double Ks_dis=0.5, double Ks_cosAng=0.999,
					 double Lambda_invM_low=1.111, double Lambda_invM_high=1.121, double Lambda_dis=0.5, double Lambda_cosAng=0.99995,
					 double Gamma_invM_low=0., double Gamma_invM_high=0.005, double Gamma_dis=9, double Gamma_cosAng=0.99995,
					 double chi2_cut=9. ) ;

  /** returns V0s reconstructed in each jet of the event (as an FCCAnalysesV0 object)
   *  need to perform jet clustering before calling this function
   */
  VertexingUtils::FCCAnalysesV0 get_V0s_jet( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
					     ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
					     ROOT::VecOps::RVec<bool> isInPrimary,
					     ROOT::VecOps::RVec<fastjet::PseudoJet> jets,
					     std::vector<std::vector<int>> jet_consti,
					     VertexingUtils::FCCAnalysesVertex PV,
					     bool tight = true,
					     double chi2_cut=9. );

  /** returns invariant mass, distance from PV, and colliniarity variables for all V0 candidates
   *  [0] -> invM_Ks [GeV]
   *  [1] -> invM_Lambda1 [GeV]
   *  [2] -> invM_Lambda2 [GeV]
   *  [3] -> invM_Gamma [GeV]
   *  [4] -> r [mm]
   *  [5] -> r.p [unit vector]
   *  boolean check for if chi2 constraint needs to be checked
   *  skip the candidate with output size 0 - doesn't pass the chi2 cut
   */
  ROOT::VecOps::RVec<double> get_V0candidate( VertexingUtils::FCCAnalysesVertex &V0_vtx,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tr_pair,
					      VertexingUtils::FCCAnalysesVertex PV,
					      bool chi2,
					      double chi2_cut=9. );

  /** functions to fill constraint thresholds
   *  tight  -> tight constraints
   *  !tight -> loose constraints
   *  also an option to choose constraint threshold
   *
   *  [0] -> invariant mass lower limit [GeV]
   *  [1] -> invariant mass upper limit [GeV]
   *  [2] -> distance from PV [mm]
   *  [3] -> colinearity
   */
  ROOT::VecOps::RVec<double> constraints_Ks(bool tight) ;
  ROOT::VecOps::RVec<double> constraints_Lambda0(bool tight) ;
  ROOT::VecOps::RVec<double> constraints_Gamma(bool tight) ;
  //
  ROOT::VecOps::RVec<double> constraints_Ks(double invM_low, double invM_high, double dis, double cosAng) ;
  ROOT::VecOps::RVec<double> constraints_Lambda0(double invM_low, double invM_high, double dis, double cosAng) ;
  ROOT::VecOps::RVec<double> constraints_Gamma(double invM_low, double invM_high, double dis, double cosAng) ;
  /** returns indices of the all pairs of tracks that pass a set of constraints from a vector of (non-primary) tracks
   *  default chi2 threshold is 9 and default invariant mass threshold is 10GeV
   */
  //ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> VertexSeed_all( ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
  //							        VertexingUtils::FCCAnalysesVertex PV,
  //							        double chi2_cut=9., double invM_cut=10.) ;

  /** adds indices of tracks (from the remaining tracks) that pass a set of constraints to the (seed) vtx 
   *  default chi2 threshold is 9 and default invariant mass threshold is 10GeV
   *  default threshold for track's chi2 contribution is 5 (?)
   */
  //ROOT::VecOps::RVec<int> addTrack_multi( ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
  //					    ROOT::VecOps::RVec<int> vtx_tr,
  //					    VertexingUtils::FCCAnalysesVertex PV,
  //					    double chi2_cut=9., double invM_cut=10., double chi2Tr_cut=5.) ;


}//end NS VertexFinderLCFIPlus

}//end NS FCCAnalyses
#endif
