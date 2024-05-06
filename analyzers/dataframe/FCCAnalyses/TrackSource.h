#ifndef  TRACK_SOURCE_ANALYZERS_H
#define  TRACK_SOURCE_ANALYZERS_H

// std
#include <cstddef>


// ROOT
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/TrackCollection.h"
#include "edm4hep/MCRecoTrackParticleAssociationCollection.h"


namespace FCCAnalyses {
  namespace Track {
    /**
     * \brief Analyzer to select tracks associated with a specified PDG ID.
     *
     * \param pdgID  Desired PDG ID.
     * \param chargeConjugateAllowed  Whether to allow also charge conjugate
     *        PDG ID. Default value false --- charge conjugate not allowed.
     */
    struct selPDG {
      explicit selPDG(const int pdgID, const bool chargeConjugateAllowed = false);
      const int m_pdg;
      const bool m_chargeConjugateAllowed;
      edm4hep::TrackCollection operator() (
          const edm4hep::MCRecoTrackParticleAssociationCollection& inAssocColl);
    };

    /**
     * \brief Analyzer to get number of track states
     *
     */
    ROOT::VecOps::RVec<std::size_t>
    getNstates (const edm4hep::TrackCollection& inColl);

    /**
     * \brief Analyzer to get track D0.
     *
     */
    ROOT::VecOps::RVec<float>
    getD0 (const edm4hep::TrackCollection& inColl);
  }
}

#endif /* TRACK_SOURCE_ANALYZERS_H */
