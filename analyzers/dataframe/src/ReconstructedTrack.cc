#include "FCCAnalyses/ReconstructedParticle.h"

// Standard library
#include <iostream>

// FCCAnalyses
#include "FCCAnalyses/TrackUtils.h"
#include "FCCAnalyses/VertexingUtils.h"

// Delphes
#include "TrackCovariance/VertexFit.h" // from Delphes - updates Franco, Jul 2022
#include "TrackCovariance/VertexMore.h"

namespace FCCAnalyses ::ReconstructedTrack {

ROOT::VecOps::RVec<edm4hep::TrackState>
Intersection(const ROOT::VecOps::RVec<edm4hep::TrackState> &Col1,
             const ROOT::VecOps::RVec<edm4hep::TrackState> &Col2) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  for (const auto &track1 : Col1) {
    bool isInBoth = false;
    for (const auto &track2 : Col2) {
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
  for (const auto &track1 : LargerCollection) {
    bool isInBoth = false;
    for (const auto &track2 : Subset) {
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

  for (const auto &track2 : Col2) {
    bool isInBoth = false;
    for (const auto &track1 : Col1) {
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

ROOT::VecOps::RVec<edm4hep::TrackState>
TrackStates_at_IP(const ROOT::VecOps::RVec<edm4hep::TrackData> &inTracks,
                  const ROOT::VecOps::RVec<edm4hep::TrackState> &trackStates) {
  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  result.reserve(inTracks.size());

  if ((trackStates.size() % 4) != 0) {
    std::cout << " ================= modulo 4 != 0 but "
              << (trackStates.size() % 4) << std::endl;
  }

  for (const auto &t : inTracks) {
    int idx = t.trackStates_begin;

    edm4hep::TrackState trackstate_in = trackStates[idx];
    result.push_back(trackstate_in);
  }

  return result;
}

ROOT::VecOps::RVec<int>
get_indices(const ROOT::VecOps::RVec<edm4hep::TrackState> &someTrackStates,
            const ROOT::VecOps::RVec<edm4hep::TrackState> &allTrackStates) {
  ROOT::VecOps::RVec<int> result;
  result.reserve(someTrackStates.size());

  for (const auto &track1 : someTrackStates) {
    int idx = -1;
    for (size_t itrack = 0; itrack < allTrackStates.size(); itrack++) {
      edm4hep::TrackState track2 = allTrackStates[itrack];

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
  for (size_t i = 0; i < track_indices.size(); i++) {
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
  for (size_t i = 0; i < track_indices.size(); i++) {
    int tk_idx = track_indices[i]; // index of the track in EFlowTrack_1

    int tk_jdx = -1;
    // find the index of the track in Eflowtrack (in principle, it is the same
    // as tk_idx)
    for (size_t k = 0; k < trackdata.size(); k++) {
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

ROOT::VecOps::RVec<float>
tracks_dNdx(const ROOT::VecOps::RVec<int> &trackStateIndices,
            const ROOT::VecOps::RVec<edm4hep::TrackData> &trackColl,
            const TrackUtils::TrackDqdxHandler &dNdxHandler) {
  ROOT::VecOps::RVec<float> results;
  results.reserve(trackStateIndices.size());

  // Loop over track states
  for (const auto &trackStateIndex : trackStateIndices) {
    float dNdx = -1;

    // Find the index of the corresponding track in the track collection
    // (e.g. EFlowtrack)
    int trackIndex = -1;
    for (size_t k = 0; k < trackColl.size(); k++) {
      // TODO: Currently only the first track state is considered
      int id_trackStates = trackColl[k].trackStates_begin;
      if (id_trackStates == trackStateIndex) {
        trackIndex = k;
        break;
      }
    }

    if (trackIndex < 0) {
      results.push_back(dNdx);
      continue;
    }

    auto dNdxValues = dNdxHandler.getDqdxValues(trackIndex);

    // Taking only first value
    if (dNdxValues.size() > 0) {
      dNdx = dNdxValues[0] / 1000.;
    }

    results.push_back(dNdx);
  }

  return results;
}

ROOT::VecOps::RVec<float>
tracks_dNdx(const ROOT::VecOps::RVec<edm4hep::TrackState> &someTrackStates,
            const ROOT::VecOps::RVec<edm4hep::TrackState> &allTrackStates,
            const ROOT::VecOps::RVec<edm4hep::TrackData> &trackColl,
            const TrackUtils::TrackDqdxHandler &dNdxHandler) {
  ROOT::VecOps::RVec<int> indices =
      get_indices(someTrackStates, allTrackStates);

  return tracks_dNdx(indices, trackColl, dNdxHandler);
}

} // namespace FCCAnalyses::ReconstructedTrack
