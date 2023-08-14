#ifndef  FCCANALYSES_TRACK_ANALYZERS_H
#define  FCCANALYSES_TRACK_ANALYZERS_H

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
      selPDG(const int pdgID, const bool chargeConjugateAllowed = false);
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

#endif /* FCCANALYSES_TRACK_ANALYZERS_H */
