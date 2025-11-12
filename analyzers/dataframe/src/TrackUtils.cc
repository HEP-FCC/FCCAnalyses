#include "FCCAnalyses/TrackUtils.h"

namespace FCCAnalyses ::TrackUtils {
void TrackDqdxHandler::addColl(
    const ROOT::VecOps::RVec<edm4hep::RecDqdxData> &dQdxColl,
    const ROOT::VecOps::RVec<size_t> &dQdxTrackIndexes) {
  for (size_t i = 0; i < dQdxColl.size(); ++i) {
    m_trackDqMap.emplace(dQdxTrackIndexes[i], dQdxColl[i]);
  }
}

ROOT::VecOps::RVec<edm4hep::RecDqdxData>
TrackDqdxHandler::getDqdxObjects(const size_t trackIndex) const {
  const auto &[begin, end] = m_trackDqMap.equal_range(trackIndex);
  std::vector<edm4hep::RecDqdxData> dqdxs{};
  dqdxs.reserve(std::distance(begin, end));

  for (auto it = begin; it != end; ++it) {
    dqdxs.emplace_back(it->second);
  }

  return dqdxs;
}

ROOT::VecOps::RVec<float>
TrackDqdxHandler::getDqdxValues(const size_t trackIndex) const {
  auto dQdxObjects = getDqdxObjects(trackIndex);
  ROOT::VecOps::RVec<float> dQdxVec;
  dQdxVec.reserve(dQdxObjects.size());

  for (const auto &dQdxObject : dQdxObjects) {
    dQdxVec.emplace_back(dQdxObject.dQdx.value);
  }

  return dQdxVec;
}

TrackDqdxHandler
createTrackDqdxHandler(const ROOT::VecOps::RVec<edm4hep::RecDqdxData> &dQdxColl,
                       const ROOT::VecOps::RVec<size_t> &dQdxTrackIndexes) {
  auto trackDqdxHandler = TrackDqdxHandler{};
  trackDqdxHandler.addColl(dQdxColl, dQdxTrackIndexes);

  return trackDqdxHandler;
}
} // namespace FCCAnalyses::TrackUtils
