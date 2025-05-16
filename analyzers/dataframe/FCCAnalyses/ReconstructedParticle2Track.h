
#ifndef  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H
#define  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/Quantity.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/TrackState.h"
#if __has_include("edm4hep/TrackerHit3DData.h")
#include "edm4hep/TrackerHit3DData.h"
#else
#include "edm4hep/TrackerHitData.h"
namespace edm4hep {
  using TrackerHit3DData = edm4hep::TrackerHitData;
}
#endif
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
					const ROOT::VecOps::RVec<edm4hep::TrackState>& trackstates,
          const ROOT::VecOps::RVec<edm4hep::TrackData>& tracks,
					const TLorentzVector& V, // primary vertex
					const float& Bz);

  ROOT::VecOps::RVec<float> XPtoPar_dz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& trackstates,
          const ROOT::VecOps::RVec<edm4hep::TrackData>& tracks,
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

  /*
  Return the covariance matrix of a track to a reconstructed particle
  @param cov_index: the index of the covariance matrix element:
  - Diagonal elements are: 0: d0d0, 2: phiphi, 5: omegaomega, 9: z0z0, 14: tanLambdatanLambda
  - Off-diagonal elements are: 1: phid0, 3: d0omega, 4: phiomega, 6: d0z0, 7: phiz0, 8: omegaz0, 10: d0tanLambda, 11: phitanLambda, 12: omegatanLambda, 13: tanLambdaz0
  */ 
  ROOT::VecOps::RVec<float> get_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackData> tracks,
                ROOT::VecOps::RVec<edm4hep::TrackState> trackstates,
                int cov_index);


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
