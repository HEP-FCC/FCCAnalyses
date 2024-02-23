#ifndef RECONSTRUCTEDTRACK_ANALYZERS_H
#define RECONSTRUCTEDTRACK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "edm4hep/Quantity.h"
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

namespace FCCAnalyses {

namespace ReconstructedTrack {

/// for FullSim:
ROOT::VecOps::RVec<edm4hep::TrackState>
TrackStates_at_IP(const ROOT::VecOps::RVec<edm4hep::TrackData> &in,
                  const ROOT::VecOps::RVec<edm4hep::TrackState> &trackstates);

/// returns the subset of tracks that are common to two collections
ROOT::VecOps::RVec<edm4hep::TrackState>
Intersection(const ROOT::VecOps::RVec<edm4hep::TrackState> &Col1,
             const ROOT::VecOps::RVec<edm4hep::TrackState> &Col2);

/// removes a subset of tracks from a large collection
ROOT::VecOps::RVec<edm4hep::TrackState>
Remove(const ROOT::VecOps::RVec<edm4hep::TrackState> &Subset,
       const ROOT::VecOps::RVec<edm4hep::TrackState> &LargerCollection);

/// Merge two collections of tracks
ROOT::VecOps::RVec<edm4hep::TrackState>
Merge(const ROOT::VecOps::RVec<edm4hep::TrackState> &Col1,
      const ROOT::VecOps::RVec<edm4hep::TrackState> &Col2);

/// indices of a subset of tracks, in the full tracks collection
ROOT::VecOps::RVec<int>
get_indices(const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
            const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks);

/// the lengths of a subset of tracks - passed as a vector of indices of these
/// tracks in the full tracks collection
ROOT::VecOps::RVec<float>
tracks_length(const ROOT::VecOps::RVec<int> &track_indices,
              const ROOT::VecOps::RVec<float> &length);

ROOT::VecOps::RVec<float>
tracks_length(const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
              const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks,
              const ROOT::VecOps::RVec<float> &length);

/// the TOF times in ps (times of the hit at the calo entrance )
ROOT::VecOps::RVec<float> tracks_TOF(
    const ROOT::VecOps::RVec<int> &track_indices,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::TrackerHit3DData> &trackerhits);

ROOT::VecOps::RVec<float> tracks_TOF(
    const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
    const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::TrackerHit3DData> &trackerhits);

/// the dndx values
ROOT::VecOps::RVec<float> tracks_dNdx(
    const ROOT::VecOps::RVec<int> &track_indices,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::Quantity> &dNdx);      // ETrackFlow_2

ROOT::VecOps::RVec<float> tracks_dNdx(
    const ROOT::VecOps::RVec<edm4hep::TrackState> &some_tracks,
    const ROOT::VecOps::RVec<edm4hep::TrackState> &FullTracks,
    const ROOT::VecOps::RVec<edm4hep::TrackData> &trackdata, // Eflowtrack
    const ROOT::VecOps::RVec<edm4hep::Quantity> &dNdx);      // ETrackFlow_2

} // namespace ReconstructedTrack
} // namespace FCCAnalyses
#endif
