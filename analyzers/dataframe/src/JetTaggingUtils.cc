#include "FCCAnalyses/JetTaggingUtils.h"

namespace FCCAnalyses {

namespace JetTaggingUtils {

ROOT::VecOps::RVec<int>
get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in,
            ROOT::VecOps::RVec<edm4hep::MCParticleData> MCin) {
  ROOT::VecOps::RVec<int> result(in.size(), 0);

  int loopcount = 0;
  for (size_t i = 0; i < MCin.size(); ++i) {
    auto &parton = MCin[i];
    // Select partons only (for pythia8 71-79, for pythia6 2):
    if ((parton.generatorStatus > 80 || parton.generatorStatus < 70) &&
        parton.generatorStatus != 2)
      continue;
    if (std::abs(parton.PDG) > 5 && parton.PDG != 21)
      continue;
    ROOT::Math::PxPyPzMVector lv(parton.momentum.x, parton.momentum.y,
                                 parton.momentum.z, parton.mass);

    for (size_t j = 0; j < in.size(); ++j) {
      auto &p = in[j];
      // float dEta = lv.Eta() - p.eta();
      // float dPhi = lv.Phi() - p.phi();
      // float deltaR = sqrt(dEta*dEta+dPhi*dPhi);
      // if (deltaR <= 0.5 && gRandom->Uniform() <= efficiency) result[j] =
      // true;

      Float_t dot = p.px() * parton.momentum.x + p.py() * parton.momentum.y +
                    p.pz() * parton.momentum.z;
      Float_t lenSq1 = p.px() * p.px() + p.py() * p.py() + p.pz() * p.pz();
      Float_t lenSq2 = parton.momentum.x * parton.momentum.x +
                       parton.momentum.y * parton.momentum.y +
                       parton.momentum.z * parton.momentum.z;
      Float_t norm = sqrt(lenSq1 * lenSq2);
      Float_t angle = acos(dot / norm);

      if (angle <= 0.3) {
        if (result[j] == 21 or result[j] == 0) {
          // if no match before, or matched to gluon, match to
          // this particle (favour quarks over gluons)
          result[j] = std::abs(parton.PDG);
        } else if (parton.PDG != 21) {
          // if matched to quark, and this is a quark, favour
          // heavier flavours
          result[j] = std::max(result[j], std::abs(parton.PDG));
        } else {
          // if matched to quark, and this is a gluon, keep
          // previous result (favour quark)
          ;
        }
      }
    }
  }

  return result;
}

ROOT::VecOps::RVec<int> get_btag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_c, float mistag_l,
                                 float mistag_g) {

  ROOT::VecOps::RVec<int> result(in.size(), 0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) == 5 && gRandom->Uniform() <= efficiency)
      result[j] = 1;
    if (in.at(j) == 4 && gRandom->Uniform() <= mistag_c)
      result[j] = 1;
    if (in.at(j) < 4 && gRandom->Uniform() <= mistag_l)
      result[j] = 1;
    if (in.at(j) == 21 && gRandom->Uniform() <= mistag_g)
      result[j] = 1;
  }
  return result;
}

ROOT::VecOps::RVec<int> get_ctag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_b, float mistag_l,
                                 float mistag_g) {

  ROOT::VecOps::RVec<int> result(in.size(), 0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) == 4 && gRandom->Uniform() <= efficiency)
      result[j] = 1;
    if (in.at(j) == 5 && gRandom->Uniform() <= mistag_b)
      result[j] = 1;
    if (in.at(j) < 4 && gRandom->Uniform() <= mistag_l)
      result[j] = 1;
    if (in.at(j) == 21 && gRandom->Uniform() <= mistag_g)
      result[j] = 1;
  }
  return result;
}

ROOT::VecOps::RVec<int> get_ltag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_b, float mistag_c,
                                 float mistag_g) {

  ROOT::VecOps::RVec<int> result(in.size(), 0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) < 4 && gRandom->Uniform() <= efficiency)
      result[j] = 1;
    if (in.at(j) == 5 && gRandom->Uniform() <= mistag_b)
      result[j] = 1;
    if (in.at(j) == 4 && gRandom->Uniform() <= mistag_c)
      result[j] = 1;
    if (in.at(j) == 21 && gRandom->Uniform() <= mistag_g)
      result[j] = 1;
  }
  return result;
}

ROOT::VecOps::RVec<int> get_gtag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_b, float mistag_c,
                                 float mistag_l) {

  ROOT::VecOps::RVec<int> result(in.size(), 0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) == 21 && gRandom->Uniform() <= efficiency)
      result[j] = 1;
    if (in.at(j) == 5 && gRandom->Uniform() <= mistag_b)
      result[j] = 1;
    if (in.at(j) == 4 && gRandom->Uniform() <= mistag_c)
      result[j] = 1;
    if (in.at(j) < 4 && gRandom->Uniform() <= mistag_l)
      result[j] = 1;
  }
  return result;
}

sel_tag::sel_tag(bool arg_pass) : m_pass(arg_pass){};
ROOT::VecOps::RVec<fastjet::PseudoJet>
sel_tag::operator()(ROOT::VecOps::RVec<bool> tags,
                    ROOT::VecOps::RVec<fastjet::PseudoJet> in) {
  ROOT::VecOps::RVec<fastjet::PseudoJet> result;
  for (size_t i = 0; i < in.size(); ++i) {
    if (m_pass) {
      if (tags.at(i))
        result.push_back(in.at(i));
    } else {
      if (!tags.at(i))
        result.push_back(in.at(i));
    }
  }
  return result;
}

} // namespace JetTaggingUtils

} // namespace FCCAnalyses
