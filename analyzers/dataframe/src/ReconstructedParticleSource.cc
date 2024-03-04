#include "FCCAnalyses/ReconstructedParticleSource.h"

// std
#include <vector>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <stdexcept>

// ROOT
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>


#define rdfFatal R__LOG_FATAL(ROOT::Detail::RDF::RDFLogChannel())
#define rdfError R__LOG_ERROR(ROOT::Detail::RDF::RDFLogChannel())
#define rdfWarning R__LOG_WARNING(ROOT::Detail::RDF::RDFLogChannel())
#define rdfInfo R__LOG_INFO(ROOT::Detail::RDF::RDFLogChannel())


namespace FCCAnalyses :: ReconstructedParticle {
  selPDG::selPDG(const int pdg): m_pdg(pdg) {};

  edm4hep::ReconstructedParticleCollection selPDG::operator() (
      const edm4hep::MCRecoParticleAssociationCollection& inAssocColl) {
    edm4hep::ReconstructedParticleCollection result;
    result.setSubsetCollection();

    rdfInfo << "ReconstructedParticle::selPDG: Assoc. coll size: "
            << inAssocColl.size();

    for (const auto& assoc: inAssocColl) {
      const auto& particle = assoc.getSim();
      if (particle.getPDG() == m_pdg) {
        result.push_back(assoc.getRec());
      }
    }

    return result;
  }


  // --------------------------------------------------------------------------
  selAbsPDG::selAbsPDG(const int pdg): m_absPdg(pdg) {
    if (m_absPdg < 0) {
      throw std::invalid_argument("ReconstructedParticle::selAbsPDG: Provided "
                                  "PDG ID is negative!");
    }
  };

  edm4hep::ReconstructedParticleCollection selAbsPDG::operator() (
      const edm4hep::MCRecoParticleAssociationCollection& inAssocColl) {
    edm4hep::ReconstructedParticleCollection result;
    result.setSubsetCollection();

    rdfInfo << "ReconstructedParticle::selAbsPDG: Assoc. coll size: "
            << inAssocColl.size();

    for (const auto& assoc: inAssocColl) {
      const auto& particle = assoc.getSim();
      if (std::abs(particle.getPDG()) == m_absPdg) {
        result.push_back(assoc.getRec());
      }
    }

    return result;
  }


  // --------------------------------------------------------------------------
  selUpTo::selUpTo(const size_t size) : m_size(size) {};

  edm4hep::ReconstructedParticleCollection selUpTo::operator() (
      const edm4hep::ReconstructedParticleCollection& inColl) {
    edm4hep::ReconstructedParticleCollection result;
    result.setSubsetCollection();

    for (const auto& particle: inColl) {
      if (result.size() >= m_size) {
        break;
      }
      result.push_back(particle);
    }

    return result;
  }


  // --------------------------------------------------------------------------
  selGenStatus::selGenStatus(int status) : m_status(status) {};

  edm4hep::ReconstructedParticleCollection selGenStatus::operator() (
      const edm4hep::MCRecoParticleAssociationCollection& inAssocColl) {
    edm4hep::ReconstructedParticleCollection result;
    result.setSubsetCollection();


    for (const auto& assoc: inAssocColl) {
      const auto& mcParticle = assoc.getSim();
      const auto& recoParticle = assoc.getRec();
      if (mcParticle.getGeneratorStatus() == m_status) {
        result.push_back(assoc.getRec());
      }
    }

    return result;
  }


  // --------------------------------------------------------------------------
  ROOT::VecOps::RVec<double>
  getPt(const edm4hep::ReconstructedParticleCollection& inParticles) {
   ROOT::VecOps::RVec<double> result;

   for (const auto& particle: inParticles) {
     result.push_back(std::sqrt(std::pow(particle.getMomentum().x, 2) +
                                std::pow(particle.getMomentum().y, 2)));
   }

   return result;
  }


  // --------------------------------------------------------------------------
  edm4hep::ReconstructedParticleCollection
  sortByPt(const edm4hep::ReconstructedParticleCollection& inColl) {
    edm4hep::ReconstructedParticleCollection outColl;
    outColl.setSubsetCollection();

    std::vector<edm4hep::ReconstructedParticle> rpVec;
    for (const auto& particle: inColl) {
      rpVec.emplace_back(particle);
    }

    auto pt = [] (const auto& particle) {
      return std::sqrt(std::pow(particle.getMomentum().x, 2) +
                       std::pow(particle.getMomentum().y, 2));
    };

    std::sort(rpVec.begin(), rpVec.end(),
              [&pt](const auto& lhs, const auto& rhs) {
                return pt(lhs) > pt(rhs);
              });

    for (const auto& particle: rpVec) {
      outColl.push_back(particle);
    }

    return outColl;
  }

} /* FCCAnalyses :: ReconstructedParticle */
