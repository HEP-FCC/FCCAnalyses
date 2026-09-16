#include "FCCAnalyses/ConstituentTruthLabels.h"
#include "FCCAnalyses/TruthLabelUtils.h"

#include <cmath>
#include <unordered_map>

namespace FCCAnalyses {
namespace ConstituentTruthLabels {

namespace {

using TruthLabelUtils::AncestryFlags;

/// MC index a constituent is linked to, or -1.
int matched_mc(const std::unordered_map<int, int> &mc_of_reco, int reco_index,
               size_t n_mc) {
  auto it = mc_of_reco.find(reco_index);
  if (it == mc_of_reco.end())
    return -1;
  if (it->second < 0 || it->second >= static_cast<int>(n_mc))
    return -1;
  return it->second;
}

int origin_label(int mc_index,
                 const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                 const ROOT::VecOps::RVec<int> &parents) {
  AncestryFlags f = TruthLabelUtils::walk_ancestry(mc_index, mc, parents);
  if (f.from_b && f.from_c)
    return 4;
  if (f.from_b)
    return 3;
  if (f.from_c)
    return 5;
  if (f.from_tau)
    return 6;
  if (f.from_sllp)
    return 7;
  return 2;
}

int type_label(int mc_index,
               const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
               const ROOT::VecOps::RVec<int> &parents) {
  int pdg = mc[mc_index].PDG;
  int apdg = std::abs(pdg);

  if (apdg == 211)
    return pdg > 0 ? 2 : -2;
  if (apdg == 321)
    return pdg > 0 ? 3 : -3;
  if (apdg == 3122)
    return 4;
  if (apdg == 11)
    return pdg > 0 ? -5 : 5;
  if (apdg == 13)
    return pdg > 0 ? -6 : 6;
  if (apdg == 22)
    return 7;

  // a Lambda decays before it is tracked, so its charged daughters carry the
  // Lambda type, as in ATLAS
  if (apdg == 2212 || apdg == 211) {
    const auto &p = mc[mc_index];
    for (unsigned int r = p.parents_begin; r < p.parents_end; ++r) {
      if (r >= parents.size())
        continue;
      int par = parents[r];
      if (par >= 0 && par < static_cast<int>(mc.size()) &&
          std::abs(mc[par].PDG) == 3122)
        return 4;
    }
  }
  return 1;
}

/// Classified from the immediate parent only. As in ATLAS this describes the
/// secondary *interaction* a particle came from, so heavy-flavour decay
/// products are NotSecondary: that information lives in the origin label.
/// HadronicInteraction (2) needs detector simulation and is never produced by
/// a Delphes sample, and so is Other (6).
int source_label(int mc_index,
                 const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                 const ROOT::VecOps::RVec<int> &parents) {
  const auto &p = mc[mc_index];
  if (p.parents_begin == p.parents_end)
    return 1;

  for (unsigned int r = p.parents_begin; r < p.parents_end; ++r) {
    if (r >= parents.size())
      continue;
    int par = parents[r];
    if (par < 0 || par >= static_cast<int>(mc.size()))
      continue;
    int ppdg = mc[par].PDG;
    if (TruthLabelUtils::is_strange_meson(ppdg))
      return 3;
    if (TruthLabelUtils::is_strange_baryon(ppdg))
      return 4;
    if (std::abs(ppdg) == 22)
      return 5;
  }
  return 1;
}

} // namespace

ROOT::VecOps::RVec<ConstituentsData>
get_truthOriginLabel(const ROOT::VecOps::RVec<int> &recin,
                     const ROOT::VecOps::RVec<int> &mcin,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     const ROOT::VecOps::RVec<int> &parents,
                     const std::vector<std::vector<int>> &indices) {
  ROOT::VecOps::RVec<ConstituentsData> out;
  std::unordered_map<int, int> mc_of_reco =
      TruthLabelUtils::reco_to_mc_map(recin, mcin);
  std::unordered_map<int, int> cache;

  for (const auto &jet : indices) {
    ConstituentsData tmp;
    tmp.reserve(jet.size());
    for (int ci : jet) {
      int m = matched_mc(mc_of_reco, ci, mc.size());
      if (m < 0) {
        tmp.push_back(-1.f);
        continue;
      }
      auto it = cache.find(m);
      if (it == cache.end())
        it = cache.emplace(m, origin_label(m, mc, parents)).first;
      tmp.push_back(static_cast<float>(it->second));
    }
    out.push_back(tmp);
  }
  return out;
}

ROOT::VecOps::RVec<ConstituentsData>
get_truthTypeLabel(const ROOT::VecOps::RVec<int> &recin,
                   const ROOT::VecOps::RVec<int> &mcin,
                   const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                   const ROOT::VecOps::RVec<int> &parents,
                   const std::vector<std::vector<int>> &indices) {
  ROOT::VecOps::RVec<ConstituentsData> out;
  std::unordered_map<int, int> mc_of_reco =
      TruthLabelUtils::reco_to_mc_map(recin, mcin);

  for (const auto &jet : indices) {
    ConstituentsData tmp;
    tmp.reserve(jet.size());
    for (int ci : jet) {
      int m = matched_mc(mc_of_reco, ci, mc.size());
      tmp.push_back(m < 0 ? 0.f
                          : static_cast<float>(type_label(m, mc, parents)));
    }
    out.push_back(tmp);
  }
  return out;
}

ROOT::VecOps::RVec<ConstituentsData>
get_truthSourceLabel(const ROOT::VecOps::RVec<int> &recin,
                     const ROOT::VecOps::RVec<int> &mcin,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     const ROOT::VecOps::RVec<int> &parents,
                     const std::vector<std::vector<int>> &indices) {
  ROOT::VecOps::RVec<ConstituentsData> out;
  std::unordered_map<int, int> mc_of_reco =
      TruthLabelUtils::reco_to_mc_map(recin, mcin);
  std::unordered_map<int, int> cache;

  for (const auto &jet : indices) {
    ConstituentsData tmp;
    tmp.reserve(jet.size());
    for (int ci : jet) {
      int m = matched_mc(mc_of_reco, ci, mc.size());
      if (m < 0) {
        tmp.push_back(0.f);
        continue;
      }
      auto it = cache.find(m);
      if (it == cache.end())
        it = cache.emplace(m, source_label(m, mc, parents)).first;
      tmp.push_back(static_cast<float>(it->second));
    }
    out.push_back(tmp);
  }
  return out;
}

ROOT::VecOps::RVec<ConstituentsData> get_truthVertexIndex(
    const ROOT::VecOps::RVec<int> &recin, const ROOT::VecOps::RVec<int> &mcin,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const std::vector<std::vector<int>> &indices, float merge_radius_mm) {
  std::unordered_map<int, int> mc_of_reco =
      TruthLabelUtils::reco_to_mc_map(recin, mcin);

  std::vector<int> matched;
  for (const auto &jet : indices)
    for (int ci : jet) {
      int m = matched_mc(mc_of_reco, ci, mc.size());
      if (m >= 0)
        matched.push_back(m);
    }

  std::unordered_map<int, int> vtx =
      TruthLabelUtils::truth_vertex_indices(matched, mc, merge_radius_mm);

  ROOT::VecOps::RVec<ConstituentsData> out;
  for (const auto &jet : indices) {
    ConstituentsData tmp;
    tmp.reserve(jet.size());
    for (int ci : jet) {
      int m = matched_mc(mc_of_reco, ci, mc.size());
      auto it = (m >= 0) ? vtx.find(m) : vtx.end();
      tmp.push_back(it == vtx.end() ? -2.f : static_cast<float>(it->second));
    }
    out.push_back(tmp);
  }
  return out;
}

ROOT::VecOps::RVec<ConstituentsData>
get_truthPdgId(const ROOT::VecOps::RVec<int> &recin,
               const ROOT::VecOps::RVec<int> &mcin,
               const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
               const std::vector<std::vector<int>> &indices) {
  ROOT::VecOps::RVec<ConstituentsData> out;
  std::unordered_map<int, int> mc_of_reco =
      TruthLabelUtils::reco_to_mc_map(recin, mcin);

  for (const auto &jet : indices) {
    ConstituentsData tmp;
    tmp.reserve(jet.size());
    for (int ci : jet) {
      int m = matched_mc(mc_of_reco, ci, mc.size());
      tmp.push_back(m < 0 ? 0.f : static_cast<float>(mc[m].PDG));
    }
    out.push_back(tmp);
  }
  return out;
}

} // namespace ConstituentTruthLabels
} // namespace FCCAnalyses
