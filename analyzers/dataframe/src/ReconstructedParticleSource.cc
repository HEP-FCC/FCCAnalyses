#include "FCCAnalyses/ReconstructedParticleSource.h"
#include "FCCAnalyses/Logger.h"

// std
#include <cmath>
#include <cstdlib>
#include <stdexcept>
#include <vector>

// ROOT
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>
#include <TLorentzVector.h>

// EDM4hep
#include <edm4hep/utils/kinematics.h>

namespace FCCAnalyses ::PodioSource ::ReconstructedParticle {
selPDG::selPDG(const int pdg) : m_pdg(pdg){};

edm4hep::ReconstructedParticleCollection
selPDG::operator()(const edm4hep::RecoMCParticleLinkCollection &inLinkColl) {
  edm4hep::ReconstructedParticleCollection result;
  result.setSubsetCollection();

  rdfDebug << "Link collection size: " << inLinkColl.size();

  for (const auto &link : inLinkColl) {
    const auto &particle = link.getTo();
    if (particle.getPDG() == m_pdg) {
      result.push_back(link.getFrom());
    }
  }

  return result;
}

// --------------------------------------------------------------------------
selAbsPDG::selAbsPDG(const int pdg) : m_absPdg(pdg) {
  if (m_absPdg < 0) {
    throw std::invalid_argument("ReconstructedParticle::selAbsPDG: Provided "
                                "PDG ID is negative!");
  }
};

edm4hep::ReconstructedParticleCollection
selAbsPDG::operator()(const edm4hep::RecoMCParticleLinkCollection &inLinkColl) {
  edm4hep::ReconstructedParticleCollection result;
  result.setSubsetCollection();

  for (const auto &link : inLinkColl) {
    const auto &particle = link.getTo();
    if (std::abs(particle.getPDG()) == m_absPdg) {
      result.push_back(link.getFrom());
    }
  }

  return result;
}

// --------------------------------------------------------------------------
selPt::selPt(float minPt) : m_minPt(minPt) {
  if (m_minPt < 0) {
    throw std::invalid_argument("ReconstructedParticle::selPt: Provided "
                                "pT threshold is negative!");
  }
};

edm4hep::ReconstructedParticleCollection
selPt::operator()(const edm4hep::ReconstructedParticleCollection &inColl) {
  edm4hep::ReconstructedParticleCollection result;
  result.setSubsetCollection();

  for (const auto &particle : inColl) {
    if (edm4hep::utils::pt(particle) > m_minPt) {
      result.push_back(particle);
    }
  }

  return result;
}

// --------------------------------------------------------------------------
selUpTo::selUpTo(const size_t size) : m_size(size){};

edm4hep::ReconstructedParticleCollection
selUpTo::operator()(const edm4hep::ReconstructedParticleCollection &inColl) {
  edm4hep::ReconstructedParticleCollection result;
  result.setSubsetCollection();

  for (const auto &particle : inColl) {
    if (result.size() >= m_size) {
      break;
    }
    result.push_back(particle);
  }

  return result;
}

// --------------------------------------------------------------------------
selGenStatus::selGenStatus(int status) : m_status(status){};

edm4hep::ReconstructedParticleCollection selGenStatus::operator()(
    const edm4hep::RecoMCParticleLinkCollection &inLinkColl) {
  edm4hep::ReconstructedParticleCollection result;
  result.setSubsetCollection();

  for (const auto &link : inLinkColl) {
    const auto &mcParticle = link.getTo();
    const auto &recoParticle = link.getFrom();
    if (mcParticle.getGeneratorStatus() == m_status) {
      result.push_back(link.getFrom());
    }
  }

  return result;
}

// --------------------------------------------------------------------------
ROOT::VecOps::RVec<float>
getP(const edm4hep::ReconstructedParticleCollection &inColl) {
  ROOT::VecOps::RVec<float> result;

  for (const auto &particle : inColl) {
    auto lVec = edm4hep::utils::p4(particle, edm4hep::utils::UseMass);
    result.push_back(static_cast<float>(lVec.P()));
  }
  return result;
}

// --------------------------------------------------------------------------
ROOT::VecOps::RVec<float>
getPt(const edm4hep::ReconstructedParticleCollection &inColl) {
  ROOT::VecOps::RVec<float> result;
  result.reserve(inColl.size());

  std::transform(
      inColl.begin(), inColl.end(), std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p) { return edm4hep::utils::pt(p); });

  return result;
}

// --------------------------------------------------------------------------
ROOT::VecOps::RVec<float>
getY(const edm4hep::ReconstructedParticleCollection &inColl) {
  ROOT::VecOps::RVec<float> result;

  for (const auto &particle : inColl) {
    auto lVec = edm4hep::utils::p4(particle, edm4hep::utils::UseMass);
    result.push_back(static_cast<float>(lVec.Rapidity()));
  }

  return result;
}

// --------------------------------------------------------------------------
ROOT::VecOps::RVec<float>
getE(const edm4hep::ReconstructedParticleCollection &inColl) {
  ROOT::VecOps::RVec<float> result;

  std::transform(
      inColl.begin(), inColl.end(), std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p) { return p.getEnergy(); });

  return result;
}

// --------------------------------------------------------------------------
ROOT::VecOps::RVec<float>
getMass(const edm4hep::ReconstructedParticleCollection &inColl) {
  ROOT::VecOps::RVec<float> result;

  std::transform(inColl.begin(), inColl.end(), std::back_inserter(result),
                 [](edm4hep::ReconstructedParticle p) { return p.getMass(); });

  return result;
}

// --------------------------------------------------------------------------
ROOT::VecOps::RVec<float>
getCharge(const edm4hep::ReconstructedParticleCollection &inColl) {
  ROOT::VecOps::RVec<float> result;

  std::transform(
      inColl.begin(), inColl.end(), std::back_inserter(result),
      [](edm4hep::ReconstructedParticle p) { return p.getCharge(); });

  return result;
}

// --------------------------------------------------------------------------
edm4hep::ReconstructedParticleCollection
sortByPt(const edm4hep::ReconstructedParticleCollection &inColl) {
  edm4hep::ReconstructedParticleCollection outColl;
  outColl.setSubsetCollection();

  std::vector<edm4hep::ReconstructedParticle> rpVec;
  rpVec.reserve(inColl.size());
  for (const auto &particle : inColl) {
    rpVec.emplace_back(particle);
  }

  std::sort(rpVec.begin(), rpVec.end(), [](const auto &lhs, const auto &rhs) {
    return edm4hep::utils::pt(lhs) > edm4hep::utils::pt(rhs);
  });

  for (const auto &particle : rpVec) {
    outColl.push_back(particle);
  }

  return outColl;
}

// ----------------------------------------------------------------------------
edm4hep::ReconstructedParticleCollection
remove(const edm4hep::ReconstructedParticleCollection &inColl,
       const edm4hep::ReconstructedParticle &inPartToBeRemoved,
       const bool matching) {
  edm4hep::ReconstructedParticleCollection inPartsToBeRemoved;
  inPartsToBeRemoved.setSubsetCollection();
  inPartsToBeRemoved.push_back(inPartToBeRemoved);

  return remove(inColl, inPartsToBeRemoved, matching);
}

// ----------------------------------------------------------------------------
edm4hep::ReconstructedParticleCollection
remove(const edm4hep::ReconstructedParticleCollection &inColl,
       const edm4hep::ReconstructedParticleCollection &inPartsToBeRemoved,
       const bool matching) {
  edm4hep::ReconstructedParticleCollection outColl;
  outColl.setSubsetCollection();

  if (!matching) {
    for (const auto &particle : inColl) {
      // TODO: Use std::find for this
      // if (std::find(inPartsToBeRemoved.begin(), inPartsToBeRemoved.end(),
      //               particle) != inPartsToBeRemoved.end()) {
      bool removePart = false;
      for (const auto &partToBeRemoved : inPartsToBeRemoved) {
        if (particle == partToBeRemoved) {
          removePart = true;
        }
      }
      if (removePart) {
        continue;
      }
      outColl.push_back(particle);
    }
  } else {
    float epsilon = 1e-6;
    for (const auto &particle1 : inColl) {
      bool removePart = false;
      for (const auto &particle2 : inPartsToBeRemoved) {
        float massDiff = 0.;
        if (particle1.getMass() > 0.) {
          massDiff = std::fabs(particle1.getMass() - particle2.getMass()) /
                     particle1.getMass();
        }
        float pXDiff = 0.;
        if (particle1.getMomentum().x != 0.) {
          pXDiff = std::fabs(
              (particle1.getMomentum().x - particle2.getMomentum().x) /
              particle1.getMomentum().x);
        }
        float pYDiff = 0.;
        if (particle1.getMomentum().y != 0.) {
          pYDiff = std::fabs(
              (particle1.getMomentum().y - particle2.getMomentum().y) /
              particle1.getMomentum().y);
        }
        float pZDiff = 0.;
        if (particle1.getMomentum().z != 0.) {
          pZDiff = std::fabs(
              (particle1.getMomentum().z - particle2.getMomentum().z) /
              particle1.getMomentum().z);
        }
        float chargeDiff =
            std::fabs(particle1.getCharge() - particle2.getCharge());
        int32_t pdgDiff = std::abs(particle1.getPDG() - particle1.getPDG());

        if (massDiff < epsilon && pXDiff < epsilon && pYDiff < epsilon &&
            pZDiff < epsilon && chargeDiff < epsilon && pdgDiff < 1) {
          removePart = true;
        }
      }
      if (removePart) {
        continue;
      }
      outColl.push_back(particle1);
    }
  }

  return outColl;
}

// ----------------------------------------------------------------------------
edm4hep::ReconstructedParticleCollection
merge(const edm4hep::ReconstructedParticleCollection &inColl1,
      const edm4hep::ReconstructedParticleCollection &inColl2) {
  edm4hep::ReconstructedParticleCollection outColl;
  outColl.setSubsetCollection();

  for (const auto &particle : inColl1) {
    outColl.push_back(particle);
  }

  for (const auto &particle : inColl2) {
    outColl.push_back(particle);
  }

  return outColl;
}

// --------------------------------------------------------------------------
resonanceBuilder::resonanceBuilder(float resonanceMass)
    : m_resonanceMass(resonanceMass) {
  if (m_resonanceMass < 0) {
    throw std::invalid_argument("ReconstructedParticle::resonanceBuilder: "
                                "Provided resonance mass is negative!");
  }
}

edm4hep::ReconstructedParticleCollection resonanceBuilder::operator()(
    const edm4hep::ReconstructedParticleCollection &inColl) {
  edm4hep::ReconstructedParticleCollection result;

  if (inColl.size() < 2) {
    return result;
  }

  // Convert collection into std::vector
  std::vector<edm4hep::ReconstructedParticle> rpVec;
  rpVec.reserve(inColl.size());
  for (const auto &particle : inColl) {
    rpVec.emplace_back(particle);
  }

  // Loop over all possible combinations
  std::vector<edm4hep::ReconstructedParticle> resonanceVec;
  for (auto p1 = rpVec.begin(); p1 != rpVec.end(); ++p1) {
    for (auto p2 = p1 + 1; p2 != rpVec.end(); ++p2) {
      edm4hep::MutableReconstructedParticle resonance;
      resonance.setCharge(p1->getCharge() + p2->getCharge());

      auto lVec1 = edm4hep::utils::p4(*p1, edm4hep::utils::UseMass);
      auto lVec2 = edm4hep::utils::p4(*p2, edm4hep::utils::UseMass);

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
recoilBuilder::recoilBuilder(float sqrts) : m_sqrts(sqrts) {
  if (m_sqrts < 0) {
    throw std::invalid_argument("ReconstructedParticle::recoilBuilder: "
                                "Provided center-of-mass is negative!");
  }
}

edm4hep::ReconstructedParticleCollection recoilBuilder::operator()(
    const edm4hep::ReconstructedParticleCollection &inColl) {
  edm4hep::ReconstructedParticleCollection result;

  auto recoilVec = TLorentzVector(0, 0, 0, m_sqrts);
  for (const auto &r : inColl) {
    auto lVec = TLorentzVector(r.getMomentum().x, r.getMomentum().y,
                               r.getMomentum().z, r.getMass());
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

} // namespace FCCAnalyses::PodioSource::ReconstructedParticle
