
#ifndef  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H
#define  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/Quantity.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/TrackState.h"
#include "edm4hep/TrackerHitData.h"
#include <TVectorD.h>
#include <TVector3.h>
#include <TLorentzVector.h>

#include <TMath.h>
#include <iostream>

namespace FCCAnalyses{

namespace ReconstructedParticle2Track{

  /// Return the momentum of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_mom (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, 
					   ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the charge of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  
					     ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  //compute the magnetic field Bz
  ROOT::VecOps::RVec<float> getRP2TRK_Bz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& rps,
					 const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks); //here computed for all particles passed

  float Bz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& rps,
	   const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks); //here only computed for the first charged particle encountered

  ROOT::VecOps::RVec<float> XPtoPar_dxy(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
					const TLorentzVector& V, // primary vertex
					const float& Bz);

  ROOT::VecOps::RVec<float> XPtoPar_dz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
                                        const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
                                        const TLorentzVector& V, // primary vertex
                                        const float& Bz);

  ROOT::VecOps::RVec<float> XPtoPar_phi(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
                                        const TLorentzVector& V, // primary vertex
                                        const float& Bz);

  ROOT::VecOps::RVec<float> XPtoPar_C(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
                                        const float& Bz);

  ROOT::VecOps::RVec<float> XPtoPar_ct(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
                                        const float& Bz);

  /// Return the D0 of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_D0 (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					  ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the Z0 of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_Z0 (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					  ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the Phi of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_phi (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					   ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the omega of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_omega (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					     ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the tanLambda of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_tanLambda (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						 ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the D0 significance of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_D0_sig (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the Z0 significance of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_Z0_sig (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tracks);


  /// Return the variance (not the sigma)  of the the D0 of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_D0_cov (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the variance (not the sigma)  of the the Z0 of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_Z0_cov (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the variance (not the sigma)  of the the Phi of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_phi_cov (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					       ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the variance (not the sigma)  of the omega of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_omega_cov (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						 ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the variance (not the sigma)  of the tanLambda of a track to a reconstructed particle
  ROOT::VecOps::RVec<float> getRP2TRK_tanLambda_cov (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						     ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (d0, phi0) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_d0_phi0_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						  ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (d0, omega) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_d0_omega_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						   ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (d0,z0) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_d0_z0_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (d0,tanlambda) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_d0_tanlambda_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						       ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (phi0,omega) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_phi0_omega_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						     ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (phi0,z0) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_phi0_z0_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						  ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// Return the off-diag term (phi0,tanlambda) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_phi0_tanlambda_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
							 ROOT::VecOps::RVec<edm4hep::TrackState> tracks) ;

  /// Return the off-diag term (omega,z0) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_omega_z0_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						   ROOT::VecOps::RVec<edm4hep::TrackState> tracks) ;

  /// Return the off-diag term (omega,tanlambda) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_omega_tanlambda_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
							  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) ;

  /// Return the off-diag term (z0,tanlambda) of the covariance matrix
  ROOT::VecOps::RVec<float> getRP2TRK_z0_tanlambda_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						       ROOT::VecOps::RVec<edm4hep::TrackState> tracks);


  /// Return the tracks associated to reco'ed particles
  ROOT::VecOps::RVec<edm4hep::TrackState> getRP2TRK( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						     ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;

  /// Return the reco indices of particles that have tracks
  ROOT::VecOps::RVec<int> get_recoindTRK( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, 
					  ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;
  
  /// Return the size of a collection of TrackStates
  int getTK_n(ROOT::VecOps::RVec<edm4hep::TrackState> x) ;

  /// Return if a Reco particle have an associated track
  ROOT::VecOps::RVec<bool> hasTRK( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in ) ;

}//end NS ReconstructedParticle2Track

}//end NS FCCAnalyses
#endif
