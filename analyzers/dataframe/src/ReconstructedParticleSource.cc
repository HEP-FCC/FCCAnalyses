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
#include <TLorentzVector.h>


#define rdfFatal R__LOG_FATAL(ROOT::Detail::RDF::RDFLogChannel())
#define rdfError R__LOG_ERROR(ROOT::Detail::RDF::RDFLogChannel())
#define rdfWarning R__LOG_WARNING(ROOT::Detail::RDF::RDFLogChannel())
#define rdfInfo R__LOG_INFO(ROOT::Detail::RDF::RDFLogChannel())


namespace FCCAnalyses :: ReconstructedParticle :: Source {
  selPDG::selPDG(const int pdg): m_pdg(pdg) {};

  edm4hep::ReconstructedParticleCollection selPDG::operator() (
      const edm4hep::MCRecoParticleAssociationCollection& inAssocColl) {
    edm4hep::ReconstructedParticleCollection result;
    result.setSubsetCollection();

    rdfInfo << "Assoc. coll size: " << inAssocColl.size();

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

    for (const auto& assoc: inAssocColl) {
      const auto& particle = assoc.getSim();
      if (std::abs(particle.getPDG()) == m_absPdg) {
        result.push_back(assoc.getRec());
      }
    }

    return result;
  }


  // --------------------------------------------------------------------------
  selPt::selPt(float minPt): m_minPt(minPt) {
    if (m_minPt < 0) {
      throw std::invalid_argument("ReconstructedParticle::selPt: Provided "
                                  "pT threshold is negative!");
    }
  };

  edm4hep::ReconstructedParticleCollection selPt::operator() (
      const edm4hep::ReconstructedParticleCollection& inColl) {
    edm4hep::ReconstructedParticleCollection result;
    result.setSubsetCollection();

    for (const auto& particle: inColl) {
      if (std::sqrt(std::pow(particle.getMomentum().x, 2) +
                    std::pow(particle.getMomentum().y, 2)) > m_minPt) {
        result.push_back(particle);
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
  ROOT::VecOps::RVec<float>
  getP(const edm4hep::ReconstructedParticleCollection& inColl) {
    ROOT::VecOps::RVec<float> result;

    for (const auto& particle: inColl) {
      TLorentzVector lVec;
      lVec.SetXYZM(particle.getMomentum().x,
                   particle.getMomentum().y,
                   particle.getMomentum().z,
                   particle.getMass());
      result.push_back(static_cast<float>(lVec.P()));
    }
    return result;
  }


  // --------------------------------------------------------------------------
  ROOT::VecOps::RVec<float>
  getPt(const edm4hep::ReconstructedParticleCollection& inColl) {
    ROOT::VecOps::RVec<float> result;

    std::transform(
      inColl.begin(), inColl.end(),
      std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p){
        return std::sqrt(std::pow(p.getMomentum().x, 2) +
                         std::pow(p.getMomentum().y, 2));
      }
    );

    return result;
  }


  // --------------------------------------------------------------------------
  ROOT::VecOps::RVec<float>
  getY(const edm4hep::ReconstructedParticleCollection& inColl) {
    ROOT::VecOps::RVec<float> result;

    for (const auto& particle: inColl) {
      TLorentzVector lVec;
      lVec.SetXYZM(particle.getMomentum().x,
                   particle.getMomentum().y,
                   particle.getMomentum().z,
                   particle.getMass());
      result.push_back(static_cast<float>(lVec.Rapidity()));
    }

    return result;
  }


  // --------------------------------------------------------------------------
  ROOT::VecOps::RVec<float>
  getE(const edm4hep::ReconstructedParticleCollection& inColl) {
    ROOT::VecOps::RVec<float> result;

    std::transform(
      inColl.begin(), inColl.end(),
      std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p){ return p.getEnergy(); }
    );

    return result;
  }


  // --------------------------------------------------------------------------
  ROOT::VecOps::RVec<float>
  getMass(const edm4hep::ReconstructedParticleCollection& inColl) {
    ROOT::VecOps::RVec<float> result;

    std::transform(
      inColl.begin(), inColl.end(),
      std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p){ return p.getMass(); }
    );

    return result;
  }


  // --------------------------------------------------------------------------
  ROOT::VecOps::RVec<float>
  getCharge(const edm4hep::ReconstructedParticleCollection& inColl) {
    ROOT::VecOps::RVec<float> result;

    std::transform(
      inColl.begin(), inColl.end(),
      std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p){ return p.getCharge(); }
    );

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


  // --------------------------------------------------------------------------
  resonanceBuilder::resonanceBuilder(float resonanceMass):
      m_resonanceMass(resonanceMass) {
    if (m_resonanceMass < 0) {
      throw std::invalid_argument("ReconstructedParticle::resonanceBuilder: "
                                  "Provided resonance mass is negative!");
    }
  }

  edm4hep::ReconstructedParticleCollection resonanceBuilder::operator() (
      const edm4hep::ReconstructedParticleCollection& inColl) {
    edm4hep::ReconstructedParticleCollection result;

    if (inColl.size() < 2) {
      return result;
    }

    // Convert collection into std::vector
    std::vector<edm4hep::ReconstructedParticle> rpVec;
    for (const auto& particle: inColl) {
      rpVec.emplace_back(particle);
    }

    // Loop over all possible combinations
    std::vector<edm4hep::ReconstructedParticle> resonanceVec;
    for (auto first = rpVec.begin(); first != rpVec.end(); ++first) {
      for (auto second = first + 1; second != rpVec.end(); ++second) {
        edm4hep::MutableReconstructedParticle resonance;
        resonance.setCharge(first->getCharge() + second->getCharge());

        TLorentzVector lVec1;
        lVec1.SetXYZM(first->getMomentum().x,
                      first->getMomentum().y,
                      first->getMomentum().z,
                      first->getMass());

        TLorentzVector lVec2;
        lVec2.SetXYZM(second->getMomentum().x,
                      second->getMomentum().y,
                      second->getMomentum().z,
                      second->getMass());

        auto lVec = lVec1 + lVec2;
        resonance.setMomentum({static_cast<float>(lVec.Px()),
                               static_cast<float>(lVec.Py()),
                               static_cast<float>(lVec.Pz())});
        resonance.setMass(static_cast<float>(lVec.M()));
        resonanceVec.emplace_back(resonance);
      }
    }

    // Sort by the distance from desired mass value
    auto resonanceSort = [&](edm4hep::ReconstructedParticle i,
                             edm4hep::ReconstructedParticle j) {
      return std::fabs(m_resonanceMass - i.getMass()) <
             std::fabs(m_resonanceMass - j.getMass());
    };
    std::sort(resonanceVec.begin(), resonanceVec.end(), resonanceSort);
    result.push_back(resonanceVec.front().clone());

    return result;
  }


  // --------------------------------------------------------------------------
  recoilBuilder::recoilBuilder(float sqrts): m_sqrts(sqrts) {
    if (m_sqrts < 0) {
      throw std::invalid_argument("ReconstructedParticle::recoilBuilder: "
                                  "Provided center-of-mass is negative!");
    }
  }

  edm4hep::ReconstructedParticleCollection recoilBuilder::operator() (
      const edm4hep::ReconstructedParticleCollection& inColl) {
    edm4hep::ReconstructedParticleCollection result;

    auto recoilVec = TLorentzVector(0, 0, 0, m_sqrts);
    for (const auto& r: inColl) {
      auto lVec = TLorentzVector(r.getMomentum().x,
                                 r.getMomentum().y,
                                 r.getMomentum().z,
                                 r.getMass());
      recoilVec -= lVec;
    }

    edm4hep::MutableReconstructedParticle recoil;
    recoil.setMomentum({static_cast<float>(recoilVec.Px()),
                        static_cast<float>(recoilVec.Py()),
                        static_cast<float>(recoilVec.Pz())});
    recoil.setMass(static_cast<float>(recoilVec.M()));
    result.push_back(recoil);

    return result;
  };

} /* FCCAnalyses :: ReconstructedParticle :: Source */
