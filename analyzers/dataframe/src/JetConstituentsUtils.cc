#include "FCCAnalyses/JetConstituentsUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"

namespace FCCAnalyses {
  namespace JetConstituentsUtils {
    ROOT::VecOps::RVec<FCCAnalysesJetConstituents> build_constituents(
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> rps) {
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs;
      for (const auto& jet : jets) {
        auto& jc = jcs.emplace_back();
        for (auto it = jet.particles_begin; it < jet.particles_end; ++it)
          jc.emplace_back(rps.at(it));
      }
      return jcs;
    }

    FCCAnalysesJetConstituents get_jet_constituents(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> csts, int jet) {
      if (jet < 0)
        return FCCAnalysesJetConstituents();
      return csts.at(jet);
    }

    ROOT::VecOps::RVec<FCCAnalysesJetConstituents> get_constituents(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> csts,
                                                                    ROOT::VecOps::RVec<int> jets) {
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs;
      for (size_t i = 0; i < jets.size(); ++i)
        if (jets.at(i) >= 0)
          jcs.emplace_back(csts.at(i));
      return jcs;
    }

    /// recasting helper for jet constituents methods
    /// \param[in] jcs collection of jets constituents
    /// \param[in] meth variables retrieval method for constituents
    auto cast_constituent = [](const auto& jcs, auto&& meth) {
      //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> out;
      std::vector<FCCAnalysesJetConstituentsData> out;
      for (const auto& jc : jcs) {
        //out.emplace_back(meth(jc));
        auto& cnsts = out.emplace_back();
        for (const auto& cnst : meth(jc))
          cnsts.emplace_back(cnst);
      }
      return out;
    };

    //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_pt(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
    std::vector<FCCAnalysesJetConstituentsData> get_pt(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_pt);
    }

    //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_e(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
    std::vector<FCCAnalysesJetConstituentsData> get_e(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_e);
    }

    //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_theta(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
    std::vector<FCCAnalysesJetConstituentsData> get_theta(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_theta);
    }

    //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_phi(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
    std::vector<FCCAnalysesJetConstituentsData> get_phi(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_phi);
    }

    //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_type(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
    std::vector<FCCAnalysesJetConstituentsData> get_type(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_type);
    }

    //ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_charge(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
    std::vector<FCCAnalysesJetConstituentsData> get_charge(ROOT::VecOps::RVec<FCCAnalysesJetConstituents> jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_charge);
    }
  }  // namespace JetConstituentsUtils
}  // namespace FCCAnalyses
