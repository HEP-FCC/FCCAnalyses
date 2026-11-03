#ifndef JETGHOSTLABELS_ANALYZERS_H
#define JETGHOSTLABELS_ANALYZERS_H

#include "FastJet/JetClustering.h"
#include "ROOT/RVec.hxx"
#include "fastjet/PseudoJet.hh"

#include <algorithm>
#include <cmath>
#include <unordered_map>
#include <vector>

namespace FCCAnalyses {
/**
 * @brief ATLAS-style ghost labelling of jets.
 *
 * Truth particles are added to the jet clustering with their momentum scaled
 * down to a negligible value, so they follow the jet they belong to without
 * changing any jet axis. The labelling is therefore a property of the
 * clustering, not of an ad-hoc cone, and works for every jet algorithm.
 */
namespace JetGhostLabels {

/// A set of truth particles to be ghost-associated. @c p carries the true
/// momentum; the scaling to ghost size happens inside associate_ghosts.
struct GhostParticles {
  std::vector<fastjet::PseudoJet> p;
  std::vector<int> pdg;
  std::vector<int> mc_index;
};

/// Re-run @p clustering with @p ghosts added and report, for every ghost, the
/// index of the jet it landed in (-1 if it ended up outside every jet, which
/// can happen for algorithms with a radius or a pT cut).
///
/// @p jet_constituents are the constituent index lists of the jets the
/// analysis already built (@c _jetc), so the ghosts are matched back onto
/// exactly those jets. Matching uses the shared real constituents rather than
/// the jet ordering, which stays correct if the ghost-augmented clustering
/// returns the jets in a different order.
///
/// @p clustering must be the same functor used to build those jets.
template <typename Clustering>
ROOT::VecOps::RVec<int>
associate_ghosts(Clustering clustering,
                 const std::vector<fastjet::PseudoJet> &constituents,
                 const std::vector<std::vector<int>> &jet_constituents,
                 const GhostParticles &ghosts, double ghost_scale = 1e-18) {
  ROOT::VecOps::RVec<int> assignment(ghosts.p.size(), -1);
  if (ghosts.p.empty() || jet_constituents.empty())
    return assignment;

  const int n_real = static_cast<int>(constituents.size());
  std::vector<fastjet::PseudoJet> input = constituents;
  input.reserve(constituents.size() + ghosts.p.size());

  std::vector<int> ghost_slot(ghosts.p.size(), -1);
  for (size_t i = 0; i < ghosts.p.size(); ++i) {
    const auto &g = ghosts.p[i];
    double mag = std::sqrt(g.px() * g.px() + g.py() * g.py() + g.pz() * g.pz());
    if (!(mag > 0.))
      continue;
    double s = ghost_scale / mag;
    ghost_slot[i] = static_cast<int>(input.size());
    input.emplace_back(g.px() * s, g.py() * s, g.pz() * s, mag * s);
    // constituent indices are read back from the user index, which the real
    // constituents already carry from JetClusteringUtils::set_pseudoJets
    input.back().set_user_index(ghost_slot[i]);
  }

  JetClustering::FCCAnalysesJet aug = clustering(input);
  if (aug.constituents.empty())
    return assignment;

  std::unordered_map<int, int> real_to_orig;
  for (size_t o = 0; o < jet_constituents.size(); ++o)
    for (int ci : jet_constituents[o])
      real_to_orig[ci] = static_cast<int>(o);

  std::vector<int> aug_to_orig(aug.constituents.size(), -1);
  for (size_t j = 0; j < aug.constituents.size(); ++j) {
    std::vector<int> overlap(jet_constituents.size(), 0);
    for (int ci : aug.constituents[j]) {
      if (ci >= n_real)
        continue;
      auto it = real_to_orig.find(ci);
      if (it != real_to_orig.end())
        overlap[it->second]++;
    }
    auto best = std::max_element(overlap.begin(), overlap.end());
    if (best != overlap.end() && *best > 0)
      aug_to_orig[j] = static_cast<int>(std::distance(overlap.begin(), best));
  }

  std::unordered_map<int, int> slot_to_augjet;
  for (size_t j = 0; j < aug.constituents.size(); ++j)
    for (int ci : aug.constituents[j])
      if (ci >= n_real)
        slot_to_augjet[ci] = static_cast<int>(j);

  for (size_t i = 0; i < ghosts.p.size(); ++i) {
    if (ghost_slot[i] < 0)
      continue;
    auto it = slot_to_augjet.find(ghost_slot[i]);
    if (it != slot_to_augjet.end())
      assignment[i] = aug_to_orig[it->second];
  }
  return assignment;
}

} // namespace JetGhostLabels
} // namespace FCCAnalyses

#endif
