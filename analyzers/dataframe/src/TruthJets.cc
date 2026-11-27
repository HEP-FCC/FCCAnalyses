#include "FCCAnalyses/TruthJets.h"
#include "FCCAnalyses/TruthLabelUtils.h"

#include <algorithm>
#include <limits>
#include <tuple>
#include <unordered_map>

namespace FCCAnalyses {
namespace TruthJets {

namespace {

constexpr float kNaN = std::numeric_limits<float>::quiet_NaN();

double mc_energy(const edm4hep::MCParticleData &p) {
  const auto &m = p.momentum;
  return std::sqrt(m.x * m.x + m.y * m.y + m.z * m.z + p.mass * p.mass);
}

/// MC index -> truth jet index, for every clustered truth-jet input.
std::unordered_map<int, int> mc_to_truth_jet(const TruthJetCollection &truth) {
  std::unordered_map<int, int> out;
  const auto &consts = truth.jets.constituents;
  for (size_t j = 0; j < consts.size(); ++j)
    for (int ci : consts[j])
      if (ci >= 0 && ci < static_cast<int>(truth.mc_index.size()))
        out[truth.mc_index[ci]] = static_cast<int>(j);
  return out;
}

/// Per reco jet: MC-linked energy shared with each truth jet, and the total
/// MC-linked energy of the reco jet.
struct SharedEnergy {
  std::vector<double> per_truth_jet;
  double total = 0.;
};

std::vector<SharedEnergy>
shared_energies(const std::vector<std::vector<int>> &jet_constituents,
                const ROOT::VecOps::RVec<int> &recin,
                const ROOT::VecOps::RVec<int> &mcin,
                const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                const TruthJetCollection &truth) {
  std::unordered_map<int, int> mc_of_reco =
      TruthLabelUtils::reco_to_mc_map(recin, mcin);
  std::unordered_map<int, int> truth_jet_of_mc = mc_to_truth_jet(truth);
  size_t n_truth = truth.jets.jets.size();

  std::vector<SharedEnergy> out(jet_constituents.size());
  for (size_t j = 0; j < jet_constituents.size(); ++j) {
    out[j].per_truth_jet.assign(n_truth, 0.);
    for (int ci : jet_constituents[j]) {
      auto link = mc_of_reco.find(ci);
      if (link == mc_of_reco.end() || link->second < 0 ||
          link->second >= static_cast<int>(mc.size()))
        continue;
      double e = mc_energy(mc[link->second]);
      out[j].total += e;
      auto tj = truth_jet_of_mc.find(link->second);
      if (tj != truth_jet_of_mc.end() && tj->second < static_cast<int>(n_truth))
        out[j].per_truth_jet[tj->second] += e;
    }
  }
  return out;
}

bool valid_match(int m, const TruthJetCollection &truth) {
  return m >= 0 && m < static_cast<int>(truth.jets.jets.size());
}

} // namespace

std::vector<int>
select_truth_jet_inputs(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc) {
  std::vector<int> out;
  for (size_t i = 0; i < mc.size(); ++i) {
    if (mc[i].generatorStatus != 1)
      continue;
    int apdg = std::abs(mc[i].PDG);
    if (apdg == 12 || apdg == 14 || apdg == 16)
      continue;
    out.push_back(static_cast<int>(i));
  }
  return out;
}

ROOT::VecOps::RVec<int>
match_truth_jets(const std::vector<std::vector<int>> &jet_constituents,
                 const ROOT::VecOps::RVec<int> &recin,
                 const ROOT::VecOps::RVec<int> &mcin,
                 const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                 const TruthJetCollection &truth) {
  std::vector<SharedEnergy> shared =
      shared_energies(jet_constituents, recin, mcin, mc, truth);

  std::vector<std::tuple<double, int, int>> pairs;
  for (size_t j = 0; j < shared.size(); ++j)
    for (size_t t = 0; t < shared[j].per_truth_jet.size(); ++t)
      if (shared[j].per_truth_jet[t] > 0.)
        pairs.emplace_back(shared[j].per_truth_jet[t], static_cast<int>(j),
                           static_cast<int>(t));
  std::sort(pairs.begin(), pairs.end(), [](const auto &a, const auto &b) {
    return std::get<0>(a) > std::get<0>(b);
  });

  // one-to-one: the pair sharing the most energy wins, so two reco jets can
  // never be matched to the same truth jet
  ROOT::VecOps::RVec<int> out(jet_constituents.size(), -1);
  std::vector<bool> truth_used(truth.jets.jets.size(), false);
  for (const auto &[e, j, t] : pairs) {
    if (out[j] >= 0 || truth_used[t])
      continue;
    out[j] = t;
    truth_used[t] = true;
  }
  return out;
}

ROOT::VecOps::RVec<float> get_truth_jet_pt(const ROOT::VecOps::RVec<int> &match,
                                           const TruthJetCollection &truth) {
  ROOT::VecOps::RVec<float> out(match.size(), kNaN);
  for (size_t j = 0; j < match.size(); ++j)
    if (valid_match(match[j], truth))
      out[j] = static_cast<float>(truth.jets.jets[match[j]].pt());
  return out;
}

ROOT::VecOps::RVec<float>
get_truth_jet_energy(const ROOT::VecOps::RVec<int> &match,
                     const TruthJetCollection &truth) {
  ROOT::VecOps::RVec<float> out(match.size(), kNaN);
  for (size_t j = 0; j < match.size(); ++j)
    if (valid_match(match[j], truth))
      out[j] = static_cast<float>(truth.jets.jets[match[j]].e());
  return out;
}

ROOT::VecOps::RVec<float>
get_truth_jet_dr(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                 const ROOT::VecOps::RVec<int> &match,
                 const TruthJetCollection &truth) {
  size_t n = std::min(jets.size(), match.size());
  ROOT::VecOps::RVec<float> out(jets.size(), kNaN);
  for (size_t j = 0; j < n; ++j)
    if (valid_match(match[j], truth))
      out[j] = static_cast<float>(jets[j].delta_R(truth.jets.jets[match[j]]));
  return out;
}

ROOT::VecOps::RVec<float> get_truth_jet_purity(
    const std::vector<std::vector<int>> &jet_constituents,
    const ROOT::VecOps::RVec<int> &recin, const ROOT::VecOps::RVec<int> &mcin,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const ROOT::VecOps::RVec<int> &match, const TruthJetCollection &truth) {
  std::vector<SharedEnergy> shared =
      shared_energies(jet_constituents, recin, mcin, mc, truth);
  size_t n = std::min(shared.size(), match.size());
  ROOT::VecOps::RVec<float> out(shared.size(), kNaN);
  for (size_t j = 0; j < n; ++j)
    if (valid_match(match[j], truth) && shared[j].total > 0.)
      out[j] = static_cast<float>(shared[j].per_truth_jet[match[j]] /
                                  shared[j].total);
  return out;
}

ROOT::VecOps::RVec<float> get_truth_jet_completeness(
    const std::vector<std::vector<int>> &jet_constituents,
    const ROOT::VecOps::RVec<int> &recin, const ROOT::VecOps::RVec<int> &mcin,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const ROOT::VecOps::RVec<int> &match, const TruthJetCollection &truth) {
  std::vector<SharedEnergy> shared =
      shared_energies(jet_constituents, recin, mcin, mc, truth);
  size_t n = std::min(shared.size(), match.size());
  ROOT::VecOps::RVec<float> out(shared.size(), kNaN);
  for (size_t j = 0; j < n; ++j) {
    if (!valid_match(match[j], truth))
      continue;
    double truth_e = truth.jets.jets[match[j]].e();
    if (truth_e > 0.)
      out[j] = static_cast<float>(shared[j].per_truth_jet[match[j]] / truth_e);
  }
  return out;
}

} // namespace TruthJets
} // namespace FCCAnalyses
