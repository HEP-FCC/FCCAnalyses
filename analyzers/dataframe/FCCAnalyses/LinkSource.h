#ifndef SOURCE_LINK_ANALYZERS_H
#define SOURCE_LINK_ANALYZERS_H

// EDM4hep
#include "edm4hep/RecoMCParticleLinkCollection.h"


namespace FCCAnalyses :: Source :: Link {
  /**
   * \brief Analyzer to select links where the MC particle has a specified PDG
   *        ID.
   *
   * \param[in] pdg  Desired PDG ID of the MC particle.
   */
  struct sel_PDG {
    const int m_pdg;

    explicit sel_PDG(const int pdg) : m_pdg(pdg) {};

    template <typename T>
    T operator() (const T& inLinkColl) {
      T result;
      result.setSubsetCollection();

      for (const auto& link: inLinkColl) {
        const auto& particle = link.getTo();
        if (particle.getPDG() == m_pdg) {
          result.push_back(link);
        }
      }

      return result;
    }
  };



  /**
   * \brief Analyzer to select links where MC particle has a specified absolute
   *        value of PDG ID.
   *
   * \param pdg[in]  Desired absolute value of PDG ID of the MC particle.
   */
  struct sel_absPDG {
    const int m_pdg;

    explicit sel_absPDG(const int pdg) : m_pdg(pdg) {
      if (m_pdg < 0) {
        throw std::invalid_argument(
            "FCCAnalyses::Source::Link::sel_absPDG: Received negative value!");
      }
    };

    template <typename T>
    auto operator() (const T& inLinkColl) {
      T result;
      result.setSubsetCollection();

      for (const auto& link: inLinkColl) {
        const auto& particle = link.getTo();
        if (std::abs(particle.getPDG()) == m_pdg) {
          result.push_back(link);
        }
      }

      return result;
    };
  };


  /**
   * \brief Analyzer to select links where the MC particle has a specified
   *        generator status.
   *
   * \param status[in]  Desired generator status of the particle.
   */
  struct sel_genStatus {
    const int m_status;

    explicit sel_genStatus(const int status) : m_status(status) {};

    template <typename T>
    T operator() (const T& inLinkColl) {
      T result;
      result.setSubsetCollection();

      for (const auto& link: inLinkColl) {
        const auto& particle = link.getTo();
        if (particle.getGeneratorStatus() == m_status) {
          result.push_back(link);
        }
      }

      return result;
    }
  };
} /* FCCAnalyses::Source::Link */

#endif /* SOURCE_LINK_ANALYZERS_H */
