#ifndef RECONSTRUCTEDTRACK_ANALYZERS_H
#define RECONSTRUCTEDTRACK_ANALYZERS_H

// Standard library
#include <cmath>
#include <vector>

// EDM4hep
#include "edm4hep/RecDqdxData.h"
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

// FCCAnalyses
#include "FCCAnalyses/TrackUtils.h"

namespace FCCAnalyses ::ReconstructedTrack {
/**
 * @brief Make a collection of TrackStates from only the Trackstates at (0,0,0).
 *
 * Indented for FullSim samples.
 */
ROOT::VecOps::RVec<edm4hep::TrackState>
TrackStates_at_IP(const ROOT::VecOps::RVec<edm4hep::TrackData> &inTracks,
                  const ROOT::VecOps::RVec<edm4hep::TrackState> &trackStates);

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

/**
 * @brief Indices of subset tracks, in the full tracks collection.
 */
ROOT::VecOps::RVec<int>
get_indices(const ROOT::VecOps::RVec<edm4hep::TrackState> &someTrackStates,
            const ROOT::VecOps::RVec<edm4hep::TrackState> &allTrackStates);

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

/**
 * @brief Obtain dNdx values for specified track state indices.
 *
 * @param[in] trackStateIndices  full track states collection of the event.
 * @param[in] trackColl          full track collection of the event (e.g.
 * EFlowtrack)
 * @param[in] dNdxHandler        instance of a
 * FCCAnalyses::TrackUtils::TrackDqdxHandler.
 */
ROOT::VecOps::RVec<float>
tracks_dNdx(const ROOT::VecOps::RVec<int> &trackStateIndices,
            const ROOT::VecOps::RVec<edm4hep::TrackData> &trackColl,
            const FCCAnalyses::TrackUtils::TrackDqdxHandler &dNdxHandler);

/**
 * @brief Obtain dNdx values for selected subset of track states.
 *
 * @param[in] someTrackStates   selected track states.
 * @param[in] allTrackStates    full track states collection of the event.
 * @param[in] trackColl         full track collection of the event (e.g.
 * EFlowtrack)
 * @param[in] dNdxHandler       instance of a TrackUtils::TrackDqdxHandler.
 */
ROOT::VecOps::RVec<float>
tracks_dNdx(const ROOT::VecOps::RVec<edm4hep::TrackState> &someTrackStates,
            const ROOT::VecOps::RVec<edm4hep::TrackState> &allTrackStates,
            const ROOT::VecOps::RVec<edm4hep::TrackData> &tracksColl,
            const FCCAnalyses::TrackUtils::TrackDqdxHandler &dNdxHandler);
} // namespace FCCAnalyses::ReconstructedTrack

#endif /* RECONSTRUCTEDTRACK_ANALYZERS_H */
