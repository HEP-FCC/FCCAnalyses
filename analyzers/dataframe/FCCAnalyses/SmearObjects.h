#ifndef SMEARING_ANALYZERS_H
#define SMEARING_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "TMatrixDSym.h"
#include "TRandom.h"
#include <TMath.h>
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"

#include "FCCAnalyses/ReconstructedParticle2Track.h"

namespace FCCAnalyses
{

  namespace SmearObjects
  {

    /// for a given MC particle, returns a "track state", i.e. a vector of 5 helix parameters, in Delphes convention
    TVectorD TrackParamFromMC_DelphesConv(edm4hep::MCParticleData aMCParticle);

    /// generates new track states, by rescaling the covariance matrix of the tracks
    struct SmearedTracks
    {
      bool m_debug;
      TRandom m_random;
      float m_smear_parameters[5];
      SmearedTracks(float smear_d0, float smear_phi, float smear_omega, float smear_z0, float smear_tlambda, bool debug);
      ROOT::VecOps::RVec<edm4hep::TrackState> operator()(
          const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &allRecoParticles,
          const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
          const ROOT::VecOps::RVec<int> &RP2MC_indices,
          const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);
    };

    /// used to validate the method above. Stores the "MC-truth track states", in a collection that runs parallel to the full collection of tracks.
    ROOT::VecOps::RVec<edm4hep::TrackState> mcTrackParameters(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &allRecoParticles,
                                                              const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
                                                              const ROOT::VecOps::RVec<int> &RP2MC_indices,
                                                              const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);

    /// generates random values for a vector, given the covariance matrix of its components, using a Choleski decomposition. Code from Franco Bedeschi
    TVectorD CovSmear(TVectorD x, TMatrixDSym C, TRandom *ran, bool debug);

    /// generates new reco particles, smeared by given parameters
    struct SmearedReconstructedParticle
    {
      bool m_debug;
      float m_scale;
      int m_type;
      int m_mode;
      SmearedReconstructedParticle(float scale, int type, int mode, bool debug);

      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(
          const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &allRecoParticles,
          const ROOT::VecOps::RVec<int> &RP2MC_indices,
          const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles);
    };

  }
}

#endif
