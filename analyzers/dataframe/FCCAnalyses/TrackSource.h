#ifndef ANALYZERS_SOURCE_TRACK_H
#define ANALYZERS_SOURCE_TRACK_H

// std
#include <cstddef>

// ROOT
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/TrackCollection.h"
#include "edm4hep/TrackMCParticleLinkCollection.h"

namespace FCCAnalyses ::PodioSource ::Track {
/**
 * \brief Analyzer to select tracks associated with a MC particle of a
 *        specified PDG ID.
 *
 * \param pdgID  Desired PDG ID of the MC particle.
 * \param chargeConjugateAllowed  Whether to allow also charge conjugate
 *        PDG ID. Default value false --- charge conjugate not allowed.
 */
struct selPDG {
  explicit selPDG(const int pdgID, const bool chargeConjugateAllowed = false);
  const int m_pdg;
  const bool m_chargeConjugateAllowed;
  edm4hep::TrackCollection
  operator()(const edm4hep::TrackMCParticleLinkCollection &inLinkColl);
};

/**
 * \brief Analyzer to get number of track states
 *
 */
ROOT::VecOps::RVec<std::size_t>
getNstates(const edm4hep::TrackCollection &inColl);

/**
 * \brief Analyzer to get track D0.
 *
 */
ROOT::VecOps::RVec<float> getD0(const edm4hep::TrackCollection &inColl);
} // namespace FCCAnalyses::PodioSource::Track

#endif /* ANALYZERS_SOURCE_TRACK_H */
