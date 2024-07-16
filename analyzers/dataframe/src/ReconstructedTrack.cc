#include "FCCAnalyses/ReconstructedParticle.h"
#include <iostream>

#include "edm4hep/EDM4hepVersion.h"

#include "FCCAnalyses/ReconstructedTrack.h"
#include "FCCAnalyses/VertexingUtils.h"

#include "VertexFit.h" // from Delphes - updates Franco, Jul 2022
#include "VertexMore.h"

namespace FCCAnalyses {

namespace ReconstructedTrack {

ROOT::VecOps::RVec<edm4hep::TrackState>
Intersection(const ROOT::VecOps::RVec<edm4hep::TrackState> &Col1,
             const ROOT::VecOps::RVec<edm4hep::TrackState> &Col2) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  for (auto &track1 : Col1) {
    bool isInBoth = false;
    for (auto &track2 : Col2) {
      if (VertexingUtils::compare_Tracks(track1, track2)) {
        isInBoth = true;
        break;
      }
    }
    if (isInBoth)
      result.push_back(track1);
  }

  return result;
}

// --------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::TrackState>
Remove(const ROOT::VecOps::RVec<edm4hep::TrackState> &Subset,
       const ROOT::VecOps::RVec<edm4hep::TrackState> &LargerCollection) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  for (auto &track1 : LargerCollection) {
    bool isInBoth = false;
    for (auto &track2 : Subset) {
      if (VertexingUtils::compare_Tracks(track1, track2)) {
        isInBoth = true;
        break;
      }
    }
    if (!isInBoth)
      result.push_back(track1);
  }

  return result;
}

// --------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::TrackState>
Merge(const ROOT::VecOps::RVec<edm4hep::TrackState> &Col1,
      const ROOT::VecOps::RVec<edm4hep::TrackState> &Col2) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  result.reserve(Col1.size() + Col2.size());
  result.insert(result.end(), Col1.begin(), Col1.end());

  for (auto &track2 : Col2) {
    bool isInBoth = false;
    for (auto &track1 : Col1) {
      if (VertexingUtils::compare_Tracks(track1, track2)) {
        isInBoth = true;
        break;
      }
    }
    if (!isInBoth)
      result.push_back(track2);
  }

  return result;
}

// --------------------------------------------------------------------------------------------------------------------

// for FullSim :

// ---- make a collection of TrackStates from only the Trackstates at (0,0,0)

ROOT::VecOps::RVec<edm4hep::TrackState>
TrackStates_at_IP(const ROOT::VecOps::RVec<edm4hep::TrackData> &in,
                  const ROOT::VecOps::RVec<edm4hep::TrackState> &trackstates) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  int n_trackstates = trackstates.size();
  int nm4 = n_trackstates % 4;
  if (nm4 != 0)
    std::cout << " ================= modulo 4 != 0 " << nm4 << std::endl;

  for (size_t i = 0; i < in.size(); ++i) {
    auto &p = in[i];
    int idx = p.trackStates_begin;
    int idx_out = p.trackStates_end;

    edm4hep::TrackState trackstate_in = trackstates[idx];
    edm4hep::Vector3f RefPoint = trackstate_in.referencePoint;
    result.push_back(trackstate_in);
  }

  return result;
}

// --------------------------------------------------------------------------------------------------------------------

/// indices of a subset of tracks, in the full tracks collection

ROOT::VecOps::RVec<int>
get_indices(const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
            const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks) {

  ROOT::VecOps::RVec<int> result;
  for (auto &track1 : some_tracks) {
    int idx = -1;
    for (int itrack = 0; itrack < FullTracks.size(); itrack++) {
      edm4hep::TrackState track2 = FullTracks[itrack];
      if (VertexingUtils::compare_Tracks(track1, track2)) {
        idx = itrack;
        break;
      }
    }
    result.push_back(idx);
  }
  return result;
}

// --------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<float> tracks_length(
    const ROOT::VecOps::RVec<int> &track_indices,
    const ROOT::VecOps::RVec<float> &length) { // collection EFlowTrack_L

  ROOT::VecOps::RVec<float> results;
  for (int i = 0; i < track_indices.size(); i++) {
    int tk_idx = track_indices[i];
    float l = length[tk_idx];
    results.push_back(l);
  }
  return results;
}

ROOT::VecOps::RVec<float> tracks_length(
    const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
    const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks,
    const ROOT::VecOps::RVec<float> &length) { // collection EFlowTrack_L

  ROOT::VecOps::RVec<int> indices = get_indices(some_tracks, FullTracks);
  return tracks_length(indices, length);
}

// --------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<float> tracks_TOF(
    const ROOT::VecOps::RVec<int> &track_indices,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::TrackerHit3DData> &trackerhits) {

  ROOT::VecOps::RVec<float> results;
  for (int i = 0; i < track_indices.size(); i++) {
    int tk_idx = track_indices[i]; // index of the track in EFlowTrack_1

    int tk_jdx = -1;
    // find the index of the track in Eflowtrack (in principle, it is the same
    // as tk_idx)
    for (int k = 0; k < trackdata.size(); k++) {
      int id_trackStates = trackdata[k].trackStates_begin;
      if (id_trackStates == tk_idx) {
        tk_jdx = k;
        break;
      }
    }

    float tof = -1;
    if (tk_jdx >= 0) {
      int idx_tout = trackdata[tk_jdx].trackerHits_end - 1; // at calo
      edm4hep::TrackerHit3DData thits_2 = trackerhits.at(idx_tout);
      float hit_time = thits_2.time; // in s
      tof = hit_time * 1e12;         // in ps
    }

    results.push_back(tof);
  }
  return results;
}

ROOT::VecOps::RVec<float> tracks_TOF(
    const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
    const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::TrackerHit3DData> &trackerhits) {
  ROOT::VecOps::RVec<int> indices = get_indices(some_tracks, FullTracks);
  return tracks_TOF(indices, trackdata, trackerhits);
}

// --------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<float> tracks_dNdx(
    const ROOT::VecOps::RVec<int> &track_indices,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::Quantity> &dNdx)       // ETrackFlow_2
{
  ROOT::VecOps::RVec<float> results;
  for (int i = 0; i < track_indices.size(); i++) {
    int tk_idx = track_indices[i]; // index of the track in EFlowTrack_1
    int tk_jdx = -1;
    // find the index of the track in Eflowtrack (in principle, it is the same
    // as tk_idx)
    for (int k = 0; k < trackdata.size(); k++) {
      int id_trackStates = trackdata[k].trackStates_begin;
      if (id_trackStates == tk_idx) {
        tk_jdx = k;
        break;
      }
    }
    float dndx = -1;
#if EDM4HEP_BUILD_VERSION <= EDM4HEP_VERSION(0, 10, 5)
    if (tk_jdx >= 0) {
      int j = trackdata[tk_jdx].dxQuantities_begin;
      dndx = dNdx[j].value / 1000;
    }
#endif
    results.push_back(dndx);
  }
  return results;
}

ROOT::VecOps::RVec<float> tracks_dNdx(
    const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
    const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::Quantity> &dNdx)       // ETrackFlow_2
{
  ROOT::VecOps::RVec<int> indices = get_indices(some_tracks, FullTracks);
  return tracks_dNdx(indices, trackdata, dNdx);
}

// --------------------------------------------------------------------------------------------------------------------

} // namespace ReconstructedTrack
} // namespace FCCAnalyses
