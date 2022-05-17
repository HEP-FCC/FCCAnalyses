
#ifndef  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H
#define  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackState.h"

namespace FCCAnalyses{

namespace ReconstructedParticle2Track{

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

  /// Return the size of a collection of TrackStates
  int getTK_n(ROOT::VecOps::RVec<edm4hep::TrackState> x) ;

}//end NS ReconstructedParticle2Track

}//end NS FCCAnalyses
#endif
