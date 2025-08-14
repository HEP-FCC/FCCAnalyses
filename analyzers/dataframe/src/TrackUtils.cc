#include "FCCAnalyses/TrackUtils.h"

namespace FCCAnalyses ::TrackUtils {
  void TrackDqdxHandler::addColl(const ROOT::VecOps::RVec<edm4hep::RecDqdxData>& dqdxColl,
                                 const ROOT::VecOps::RVec<size_t> trackIndexes) {
    for (size_t i = 0; i < dqdxColl.size(); ++i) {
      m_trackDqMap.emplace(trackIndexes[i], dqdxColl[i]);
    }
  }

  std::vector<edm4hep::RecDqdxData> TrackDqdxHandler::getDqdxValues(const size_t trackIndex) const {
    const auto& [begin, end] = m_trackDqMap.equal_range(trackIndex);
    std::vector<edm4hep::RecDqdxData> dqdxs{};
    dqdxs.reserve(std::distance(begin, end));

    for (auto it = begin; it != end; ++it) {
      dqdxs.emplace_back(it->second);
    }

    return dqdxs;
  }

  TrackDqdxHandler
  get_dqdxHandler(const ROOT::VecOps::RVec<edm4hep::RecDqdxData>& dqdxColl,
                  const ROOT::VecOps::RVec<size_t> trackIndexes) {
    auto trackDqdxHandler = TrackDqdxHandler();
    trackDqdxHandler.addColl(dqdxColl, trackIndexes);

    return trackDqdxHandler;
  }
}
