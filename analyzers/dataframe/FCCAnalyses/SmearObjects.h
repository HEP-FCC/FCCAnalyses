#ifndef SMEAR_OBJECTS_ANALYZERS_H
#define SMEAR_OBJECTS_ANALYZERS_H

// Standard library
#include <cmath>
#include <vector>
// ROOT
#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"
#include "TMath.h"
#include "TMatrixDSym.h"
#include "TRandom.h"
// EDM4hep
#include "edm4hep/MCParticleData.h"
#include "edm4hep/RecDqdxData.h"
// FCCAnalyses
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/TrackUtils.h"

namespace FCCAnalyses ::SmearObjects {

/// for a given MC particle, returns a "track state", i.e. a vector of 5 helix
/// parameters, in Delphes convention
TVectorD TrackParamFromMC_DelphesConv(edm4hep::MCParticleData aMCParticle);

/// generates new track states, by rescaling the covariance matrix of the tracks
struct SmearedTracks {
  bool m_debug;
  TRandom m_random;
  float m_smear_parameters[5];
  SmearedTracks(float smear_d0, float smear_phi, float smear_omega,
                float smear_z0, float smear_tlambda, bool debug);
  ROOT::VecOps::RVec<edm4hep::TrackState>
  operator()(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
                 &allRecoParticles,
             const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
             const ROOT::VecOps::RVec<int> &RP2MC_indices,
             const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);
};

/// used to validate the method above. Stores the "MC-truth track states", in a
/// collection that runs parallel to the full collection of tracks.
ROOT::VecOps::RVec<edm4hep::TrackState> mcTrackParameters(
    const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
        &allRecoParticles,
    const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
    const ROOT::VecOps::RVec<int> &RP2MC_indices,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);

/// generates random values for a vector, given the covariance matrix of its
/// components, using a Choleski decomposition. Code from Franco Bedeschi
TVectorD CovSmear(TVectorD x, TMatrixDSym C, TRandom *ran, bool debug);

/**
 * @brief Generates new track dNdx, by rescaling the Poisson error of the
 * cluster count.
 */
struct SmearedTracksdNdx {
  bool m_debug; /// Debug flag
  TRandom m_random;
  float m_scale; /// Rescale resolution by this factor

  SmearedTracksdNdx(float m_scale, bool debug);

  /**
   * @brief Returns a vector of dNdx that is parallel to the collection of all
   * tracks of the event (e.g. alltracks), i.e. same number of entries,
   * same order.
   *
   * The method retrieves the MC particle that is associated to a track, and
   * builds a "track state" out of the MC particle and regenerates a new value
   * of the dNdx.
   */
  ROOT::VecOps::RVec<edm4hep::RecDqdxData>
  operator()(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
                 &allRecoParticles,
             const TrackUtils::TrackDqdxHandler &dNdxHandler,
             const ROOT::VecOps::RVec<float> &length,
             const ROOT::VecOps::RVec<int> &RP2MC_indices,
             const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);
};

/// generates new tracker hits, by rescaling the timing measurement
struct SmearedTracksTOF {
  bool m_debug;
  TRandom m_random;
  float m_scale;
  SmearedTracksTOF(float m_scale, bool debug);
  ROOT::VecOps::RVec<edm4hep::TrackerHit3DData>
  operator()(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
                 &allRecoParticles,
             const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata,
             const ROOT::VecOps::RVec<edm4hep::TrackerHit3DData> &trackerhits,
             const ROOT::VecOps::RVec<float> &length,
             const ROOT::VecOps::RVec<int> &RP2MC_indices,
             const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);
};

/// generates new reco particles, smeared by given parameters
struct SmearedReconstructedParticle {
  bool m_debug;
  float m_scale;
  int m_type;
  int m_mode;
  SmearedReconstructedParticle(float scale, int type, int mode, bool debug);

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  operator()(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
                 &allRecoParticles,
             const ROOT::VecOps::RVec<int> &RP2MC_indices,
             const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);
};

} // namespace FCCAnalyses::SmearObjects

#endif /* SMEAR_OBJECTS_ANALYZERS_H */
