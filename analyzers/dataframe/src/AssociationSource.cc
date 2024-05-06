#include "FCCAnalyses/AssociationSource.h"

// std
#include <cstdlib>
#include <cmath>


namespace FCCAnalyses :: Association {
  sel_PDG::sel_PDG(const int pdg) : m_pdg(pdg) {};

  template <typename T>
  T sel_PDG::operator() (const T& inAssocColl) {
    T result;
    result.setSubsetCollection();

    for (const auto& assoc: inAssocColl) {
      const auto& particle = assoc.getSim();
      if (particle.getPDG() == m_pdg) {
        result.push_back(assoc);
      }
    }

    return result;
  }


  /*
  sel_absPDG::sel_absPDG(const int pdg) : m_pdg(pdg) {
    if (m_pdg < 0) {
      throw std::invalid_argument(
          "Association::sel_absPDG: Received negative value!");
    }
  }

  template <typename T>
  auto sel_absPDG::operator() (const T& inAssocColl) {
    T result;
    result.setSubsetCollection();

    for (const auto& assoc: inAssocColl) {
      const auto& particle = assoc.getSim();
      if (std::abs(particle.getPDG()) == m_pdg) {
        result.push_back(assoc);
      }
    }

    return result;
  }
  */


  sel_genStatus::sel_genStatus(const int status) : m_status(status) {};

  template <typename T>
  T sel_genStatus::operator() (const T& inAssocColl) {
    T result;
    result.setSubsetCollection();

    for (const auto& assoc: inAssocColl) {
      const auto& particle = assoc.getSim();
      if (particle.getGeneratorStatus() == m_status) {
        result.push_back(assoc);
      }
    }

    return result;
  }
} /* FCCAnalyses::Association */
