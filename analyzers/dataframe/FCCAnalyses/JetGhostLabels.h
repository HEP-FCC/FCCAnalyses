#ifndef JETGHOSTLABELS_ANALYZERS_H
#define JETGHOSTLABELS_ANALYZERS_H

#include "FastJet/JetClustering.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
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
 *
 * Label conventions follow ATLAS:
 *   - HadronGhostTruthLabelID: 0 light, 4 c, 5 b, 15 tau
 *   - extended: adds 44 (cc), 54 (bc), 55 (bb), 1515 (tautau)
 *   - PartonTruthLabelID: -1 none, 1 d, 2 u, 3 s, 4 c, 5 b, 21 gluon
 */
namespace JetGhostLabels {

/// A set of truth particles to be ghost-associated. @c p carries the true
/// momentum; the scaling to ghost size happens inside associate_ghosts.
struct GhostParticles {
  std::vector<fastjet::PseudoJet> p;
  std::vector<int> pdg;
  std::vector<int> mc_index;
};

/// Heavy hadrons (and optionally taus) to ghost-associate.
///
/// @param pt_min_gev   minimum transverse momentum of the truth particle
/// @param weakly_decaying  if true keep the last hadron of a chain (the ATLAS
///        Hadron* convention); if false keep the first, i.e. the
///        production-flavour hadron, which also keeps the pre-oscillation
///        state of a neutral B (the ATLAS HadronGhostInitial* convention)
/// @param include_taus add final taus, labelled 15
///
/// c hadrons descending from a b hadron are always dropped: they are the
/// c-leg of the b decay, not an independent c.
GhostParticles
get_ghost_hadrons(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                  const ROOT::VecOps::RVec<int> &parents,
                  const ROOT::VecOps::RVec<int> &daughters,
                  float pt_min_gev = 1.0f, bool weakly_decaying = true,
                  bool include_taus = true);

/// Partons to ghost-associate: the last parton of each branch before
/// hadronisation, identified from the decay tree rather than from generator
/// status codes so that the selection is generator independent.
GhostParticles
get_ghost_partons(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                  const ROOT::VecOps::RVec<int> &daughters,
                  float pt_min_gev = 0.0f);

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

/// HadronGhostTruthLabelID: 0 light, 4 c, 5 b, 15 tau.
ROOT::VecOps::RVec<int>
get_hadron_label(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                 const ROOT::VecOps::RVec<int> &assignment,
                 const GhostParticles &ghosts);

/// HadronGhostExtendedTruthLabelID: adds 44 (cc), 54 (bc), 55 (bb),
/// 1515 (tautau).
ROOT::VecOps::RVec<int>
get_hadron_extended_label(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                          const ROOT::VecOps::RVec<int> &assignment,
                          const GhostParticles &ghosts);

/// PDG id of the highest-pT ghost of the labelling flavour, 0 for light jets.
ROOT::VecOps::RVec<int>
get_hadron_label_pdg(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                     const ROOT::VecOps::RVec<int> &assignment,
                     const GhostParticles &ghosts);

/// pT of the labelling ghost, NaN for light jets.
ROOT::VecOps::RVec<float>
get_hadron_label_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                    const ROOT::VecOps::RVec<int> &assignment,
                    const GhostParticles &ghosts);

/// Number of ghosts of a given heavy-flavour class per jet.
ROOT::VecOps::RVec<int>
count_ghosts(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
             const ROOT::VecOps::RVec<int> &assignment,
             const GhostParticles &ghosts, int flavour);

/// PartonTruthLabelID from the highest-energy ghost-associated parton:
/// -1 none, 1 d, 2 u, 3 s, 4 c, 5 b, 21 gluon.
ROOT::VecOps::RVec<int>
get_parton_label(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                 const ROOT::VecOps::RVec<int> &assignment,
                 const GhostParticles &ghosts);

/// pT of the parton that defines PartonTruthLabelID, NaN if there is none.
ROOT::VecOps::RVec<float>
get_parton_label_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                    const ROOT::VecOps::RVec<int> &assignment,
                    const GhostParticles &ghosts);

/// Angular distance between the jet and the parton that defines
/// PartonTruthLabelID, NaN if there is none.
ROOT::VecOps::RVec<float>
get_parton_label_dr(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                    const ROOT::VecOps::RVec<int> &assignment,
                    const GhostParticles &ghosts);

} // namespace JetGhostLabels
} // namespace FCCAnalyses

#endif
