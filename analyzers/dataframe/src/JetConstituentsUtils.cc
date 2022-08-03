#include "FCCAnalyses/JetConstituentsUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"

namespace FCCAnalyses {
  namespace JetConstituentsUtils {
    rv::RVec<FCCAnalysesJetConstituents> build_constituents(const rv::RVec<edm4hep::ReconstructedParticleData>& jets,
                                                            const rv::RVec<edm4hep::ReconstructedParticleData>& rps) {
      rv::RVec<FCCAnalysesJetConstituents> jcs;
      for (const auto& jet : jets) {
        auto& jc = jcs.emplace_back();
        for (auto it = jet.particles_begin; it < jet.particles_end; ++it)
          jc.emplace_back(rps.at(it));
      }
      return jcs;
    }

    FCCAnalysesJetConstituents get_jet_constituents(const rv::RVec<FCCAnalysesJetConstituents>& csts, int jet) {
      if (jet < 0)
        return FCCAnalysesJetConstituents();
      return csts.at(jet);
    }

    rv::RVec<FCCAnalysesJetConstituents> get_constituents(const rv::RVec<FCCAnalysesJetConstituents>& csts,
                                                          const rv::RVec<int>& jets) {
      rv::RVec<FCCAnalysesJetConstituents> jcs;
      for (size_t i = 0; i < jets.size(); ++i)
        if (jets.at(i) >= 0)
          jcs.emplace_back(csts.at(i));
      return jcs;
    }

    /// recasting helper for jet constituents methods
    /// \param[in] jcs collection of jets constituents
    /// \param[in] meth variables retrieval method for constituents
    auto cast_constituent = [](const auto& jcs, auto&& meth) {
      rv::RVec<FCCAnalysesJetConstituentsData> out;
      for (const auto& jc : jcs)
        out.emplace_back(meth(jc));
      return out;
    };

    rv::RVec<FCCAnalysesJetConstituentsData> get_pt(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_pt);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_e(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_e);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_theta(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_theta);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_phi(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_phi);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_type(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_type);
    }

    rv::RVec<FCCAnalysesJetConstituentsData> get_charge(const rv::RVec<FCCAnalysesJetConstituents>& jcs) {
      return cast_constituent(jcs, ReconstructedParticle::get_charge);
    }
  }  // namespace JetConstituentsUtils
}  // namespace FCCAnalyses
