#ifndef FCCANALYSES_TRACKUTILS_H
#define FCCANALYSES_TRACKUTILS_H

// std
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
     * @brief Adjusted utility class to invert the relations between RecDqdx to
     * Track relation
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
      /// Add the information from the passed collection to the handler
      void addColl(const ROOT::VecOps::RVec<edm4hep::RecDqdxData>& dqdxColl,
                   const ROOT::VecOps::RVec<size_t> trackIndexes);

      /// Get all RecDqdx objects for the given track
      std::vector<edm4hep::RecDqdxData> getDqdxValues(const size_t trackIndex) const;
    };

    /**
     * Creates an instance of TrackDqdxHandler.
     */
    TrackDqdxHandler
    get_dqdxHandler(const ROOT::VecOps::RVec<edm4hep::RecDqdxData>& dqdxColl,
                    const ROOT::VecOps::RVec<size_t> trackIndexes);

  }  // namespace TrackUtils
}  // namespace FCCAnalyses

#endif /* FCCANALYSES_TRACKUTILS_H */
