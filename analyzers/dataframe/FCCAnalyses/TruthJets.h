#ifndef TRUTHJETS_ANALYZERS_H
#define TRUTHJETS_ANALYZERS_H

#include "FastJet/JetClustering.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "fastjet/PseudoJet.hh"

#include <cmath>
#include <vector>

namespace FCCAnalyses {
/**
 * @brief Truth jets matched to reconstructed jets.
 *
 * Truth jets are clustered from MC particles with the same clustering as the
 * reconstructed jets, so the matching works for every jet algorithm. A reco
 * jet is matched to the truth jet it shares the most energy with, following
 * the reco<->MC link of its constituents, rather than to the nearest truth
 * jet in angle.
 */
namespace TruthJets {

/// Truth jets, plus the MC index behind every clustering input.
struct TruthJetCollection {
  JetClustering::FCCAnalysesJet jets;
  std::vector<int> mc_index;
};

/// Indices of the MC particles used as truth-jet input: stable
/// (generatorStatus 1) and visible (neutrinos removed). No lepton or photon
/// dressing is applied.
std::vector<int>
select_truth_jet_inputs(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc);

/// Cluster truth jets with @p clustering, which should be the functor used
/// for the reconstructed jets.
template <typename Clustering>
TruthJetCollection
cluster_truth_jets(Clustering clustering,
                   const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc) {
  TruthJetCollection out;
  out.mc_index = select_truth_jet_inputs(mc);

  std::vector<fastjet::PseudoJet> input;
  input.reserve(out.mc_index.size());
  for (size_t i = 0; i < out.mc_index.size(); ++i) {
    const auto &p = mc[out.mc_index[i]];
    const auto &mom = p.momentum;
    double e = std::sqrt(mom.x * mom.x + mom.y * mom.y + mom.z * mom.z +
                         p.mass * p.mass);
    input.emplace_back(mom.x, mom.y, mom.z, e);
    input.back().set_user_index(static_cast<int>(i));
  }
  out.jets = clustering(input);
  return out;
}

/// Per reco jet, the index of its matched truth jet, or -1. Matching is
/// one-to-one and greedy in shared energy: reco-truth pairs are taken in
/// decreasing order of the MC-linked energy they share, skipping jets that are
/// already matched.
ROOT::VecOps::RVec<int>
match_truth_jets(const std::vector<std::vector<int>> &jet_constituents,
                 const ROOT::VecOps::RVec<int> &recin,
                 const ROOT::VecOps::RVec<int> &mcin,
                 const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                 const TruthJetCollection &truth);

/// pT of the matched truth jet, NaN if unmatched.
ROOT::VecOps::RVec<float> get_truth_jet_pt(const ROOT::VecOps::RVec<int> &match,
                                           const TruthJetCollection &truth);

/// Energy of the matched truth jet, NaN if unmatched.
ROOT::VecOps::RVec<float>
get_truth_jet_energy(const ROOT::VecOps::RVec<int> &match,
                     const TruthJetCollection &truth);

/// Angular distance between the reco jet and its truth jet, NaN if unmatched.
ROOT::VecOps::RVec<float>
get_truth_jet_dr(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                 const ROOT::VecOps::RVec<int> &match,
                 const TruthJetCollection &truth);

/// Fraction of the MC-linked energy of the reco jet that lies in its matched
/// truth jet, NaN if unmatched. Low values flag an ambiguous match.
ROOT::VecOps::RVec<float> get_truth_jet_purity(
    const std::vector<std::vector<int>> &jet_constituents,
    const ROOT::VecOps::RVec<int> &recin, const ROOT::VecOps::RVec<int> &mcin,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const ROOT::VecOps::RVec<int> &match, const TruthJetCollection &truth);

/// Fraction of the matched truth jet's energy that is linked to constituents
/// of the reco jet, NaN if unmatched. Low values flag a reco jet that covers
/// only part of its truth jet, i.e. the two clusterings split the event
/// differently.
ROOT::VecOps::RVec<float> get_truth_jet_completeness(
    const std::vector<std::vector<int>> &jet_constituents,
    const ROOT::VecOps::RVec<int> &recin, const ROOT::VecOps::RVec<int> &mcin,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const ROOT::VecOps::RVec<int> &match, const TruthJetCollection &truth);

} // namespace TruthJets
} // namespace FCCAnalyses

#endif
