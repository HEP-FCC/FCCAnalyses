#include "FCCAnalyses/TrackSource.h"

namespace FCCAnalyses ::PodioSource ::Track {
selPDG::selPDG(const int pdg, const bool chargeConjugateAllowed)
    : m_pdg(pdg), m_chargeConjugateAllowed(chargeConjugateAllowed){};

edm4hep::TrackCollection
selPDG::operator()(const edm4hep::TrackMCParticleLinkCollection &inLinkColl) {
  edm4hep::TrackCollection result;
  result.setSubsetCollection();

  for (const auto &assoc : inLinkColl) {
    const auto &particle = assoc.getTo();
    if (m_chargeConjugateAllowed) {
      if (std::abs(particle.getPDG()) == std::abs(m_pdg)) {
        result.push_back(assoc.getFrom());
      }
    } else {
      if (particle.getPDG() == m_pdg) {
        result.push_back(assoc.getFrom());
      }
    }
  }

  return result;
}

ROOT::VecOps::RVec<std::size_t>
getNstates(const edm4hep::TrackCollection &inColl) {
  ROOT::VecOps::RVec<std::size_t> result;
  for (const auto &track : inColl) {
    result.push_back(track.getTrackStates().size());
  }

  return result;
}

ROOT::VecOps::RVec<float> getD0(const edm4hep::TrackCollection &inColl) {
  ROOT::VecOps::RVec<std::size_t> result;
  for (const auto &track : inColl) {
    for (const auto &trackState : track.getTrackStates()) {
      result.push_back(trackState.D0);
      break;
    }
  }

  return result;
}
} // namespace FCCAnalyses::PodioSource::Track
