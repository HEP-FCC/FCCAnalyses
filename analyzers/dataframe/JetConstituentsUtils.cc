#include "JetConstituentsUtils.h"
#include "ReconstructedParticle.h"

namespace JetConstituentsUtils {
  ROOT::VecOps::RVec<FCCAnalysesJetConstituents> build_constituents(
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> rps) {
    ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents;
    for (const auto& jet : jets) {
      auto& jc = jets_constituents.emplace_back();
      for (auto it = jet.particles_begin; it < jet.particles_end; ++it)
        jc.emplace_back(rps.at(it));
    }
    return jets_constituents;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > get_constituents(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> constituents, ROOT::VecOps::RVec<int> jets) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > jets_constituents;
    for (size_t i = 0; i < jets.size(); ++i)
      if (jets.at(i) >= 0)
        jets_constituents.emplace_back(constituents.at(i));
    return jets_constituents;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_pt(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > pts;
    for (const auto& constituent : jets_constituents)
      pts.emplace_back(ReconstructedParticle::get_pt(constituent));
    return pts;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_e(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > es;
    for (const auto& constituent : jets_constituents)
      es.emplace_back(ReconstructedParticle::get_e(constituent));
    return es;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_theta(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > thetas;
    for (const auto& constituent : jets_constituents)
      thetas.emplace_back(ReconstructedParticle::get_theta(constituent));
    return thetas;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_phi(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > phis;
    for (const auto& constituent : jets_constituents)
      phis.emplace_back(ReconstructedParticle::get_phi(constituent));
    return phis;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_pid(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > pids;
    for (const auto& constituent : jets_constituents)
      pids.emplace_back(ReconstructedParticle::get_type(constituent));
    return pids;
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_charge(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jets_constituents) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > charges;
    for (const auto& constituent : jets_constituents)
      charges.emplace_back(ReconstructedParticle::get_charge(constituent));
    return charges;
  }
}  // namespace JetConstituentsUtils
