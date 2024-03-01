#ifndef  ASSOCIATION_ANALYZERS_H
#define  ASSOCIATION_ANALYZERS_H

// EDM4hep
#include "edm4hep/MCRecoParticleAssociationCollection.h"


namespace FCCAnalyses :: Association {
  /**
   * \brief Analyzer to select associations with a mcparticle with a
   *        specified PDG ID.
   *
   * \param pdg  Desired PDG ID of the partile.
   */
  struct sel_PDG {
    explicit sel_PDG(const int pdg);
    const int m_pdg;
    template <typename T>
    T operator() (
        const T& inAssocColl);
  };


  /**
   * \brief Analyzer to select associations with a mcparticle with a
   *        specified absolute value of PDG ID.
   *
   * \param pdg  Desired absolute value of PDG ID of the partile.
   */
  struct sel_absPDG {
    const int m_pdg;

    explicit sel_absPDG(const int pdg) : m_pdg(pdg) {
      if (m_pdg < 0) {
        throw std::invalid_argument(
            "Association::sel_absPDG: Received negative value!");
      }
    };

    template <typename T>
    auto operator() (const T& inAssocColl) {
      T result;
      result.setSubsetCollection();

      for (const auto& assoc: inAssocColl) {
        const auto& particle = assoc.getSim();
        if (std::abs(particle.getPDG()) == m_pdg) {
          result.push_back(assoc);
        }
      }

      return result;
    };
  };


  /**
   * \brief Analyzer to select associations with a mcparticle with a
   *        specified generator status.
   *
   * \param pdg  Desired generator status of the partile.
   */
  struct sel_genStatus {
    explicit sel_genStatus(const int status);
    const int m_status;
    template <typename T>
    T operator() (
        const T& inAssocColl);
  };
} /* FCCAnalyses::Association */

#endif /* ASSOCIATION_ANALYZERS_H */
