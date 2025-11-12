#ifndef FCCANALYSES_TRACKUTILS_H
#define FCCANALYSES_TRACKUTILS_H

// Standard library
#include "vector"
// ROOT
#include "ROOT/RVec.hxx"
// EDM4hep
#include "edm4hep/RecDqdxData.h"

namespace FCCAnalyses {
/**
 * Utilities for the EDM4hep::Track objects and collections.
 */
namespace TrackUtils {
/**
 * @brief Adjusted utility class to invert the relations between RecDqdx and
 * Track.
 *
 * This is adjusted version of `edm4hep::TrackPIDHandler` able to work with
 * ROOT::VecOps::RVec<*Data> versions of the EDM4hep collections.
 *
 * Original can be found here:
 * https://github.com/key4hep/EDM4hep/blob/main/utils/include/edm4hep/utils/TrackUtils.h#L12
 */
class TrackDqdxHandler {
  using TrackMapT = std::multimap<size_t, edm4hep::RecDqdxData>;

  TrackMapT m_trackDqMap{}; ///< The internal map from tracks to RecDqdx
public:
  /**
   *  @brief Add the information from the collections to the handler
   *
   *  @param[in dQdxColl           Collection of all dQdx objects in the event
   * (e.g. EFlowTrack_dNdx).
   *  @param[in] dQdxTrackIndexes  Track indexes corresponding to the dQdx
   * record (e.g. _EFlowTrack_dNdx_track.index).
   */
  void addColl(const ROOT::VecOps::RVec<edm4hep::RecDqdxData> &dQdxColl,
               const ROOT::VecOps::RVec<size_t> &dQdxTrackIndexes);

  /// Get all RecDqdxData objects for a given track
  ROOT::VecOps::RVec<edm4hep::RecDqdxData>
  getDqdxObjects(const size_t trackIndex) const;

  /// Get all dQdx values for a given track
  ROOT::VecOps::RVec<float> getDqdxValues(const size_t trackIndex) const;
};

/**
 * Creates an instance of TrackDqdxHandler.
 *
 *  @param[in dQdxColl           Collection of all dQdx objects in the event
 * (e.g. EFlowTrack_dNdx).
 *  @param[in] dQdxTrackIndexes  Track indexes corresponding to the dQdx record
 * (e.g. _EFlowTrack_dNdx_track.index).
 */
TrackDqdxHandler
createTrackDqdxHandler(const ROOT::VecOps::RVec<edm4hep::RecDqdxData> &dQdxColl,
                       const ROOT::VecOps::RVec<size_t> &dQdxTrackIndexes);

} // namespace TrackUtils
} // namespace FCCAnalyses

#endif /* FCCANALYSES_TRACKUTILS_H */
