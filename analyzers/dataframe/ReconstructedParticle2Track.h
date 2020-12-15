
#ifndef  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H
#define  RECONSTRUCTEDPARTICLE2TRACK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackState.h"



/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float> getRP2TRK_D0 (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the Z0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float> getRP2TRK_Z0 (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the Phi of a track to a reconstructed particle
ROOT::VecOps::RVec<float> getRP2TRK_phi (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the omega of a track to a reconstructed particle
ROOT::VecOps::RVec<float> getRP2TRK_omega (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the tanLambda of a track to a reconstructed particle
ROOT::VecOps::RVec<float> getRP2TRK_tanLambda (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);


// Variances (not the sigmas) of these parameters

ROOT::VecOps::RVec<float> getRP2TRK_D0_var (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
ROOT::VecOps::RVec<float> getRP2TRK_Z0_var (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
ROOT::VecOps::RVec<float> getRP2TRK_phi_var (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
ROOT::VecOps::RVec<float> getRP2TRK_omega_var (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
ROOT::VecOps::RVec<float> getRP2TRK_tanLambda_var (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);



#endif
