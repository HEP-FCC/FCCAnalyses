#include "ReconstructedParticle2Track.h"


ROOT::VecOps::RVec<float> getRP2TRK_D0(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).D0);
    else result.push_back(std::nan(""));
  }
  return result;
}
std::vector<float> getRP2TRK_D0_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  std::vector<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).D0);
    else result.push_back(std::nan(""));
  }
  return result;
}

ROOT::VecOps::RVec<float> getRP2TRK_Z0(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).Z0);
  }
  return result;
}
std::vector<float> getRP2TRK_Z0_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  std::vector<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).Z0);
  }
  return result;
}
ROOT::VecOps::RVec<float> getRP2TRK_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).phi);
  }
  return result;
}

ROOT::VecOps::RVec<float> getRP2TRK_omega(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).omega);
  }
  return result;
}

ROOT::VecOps::RVec<float> getRP2TRK_tanLambda(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).tanLambda);
  }
  return result;
}

