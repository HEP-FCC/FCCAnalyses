#include "FCCAnalyses/TruthLabelUtils.h"

#include <cmath>
#include <set>

namespace FCCAnalyses {
namespace TruthLabelUtils {

int heavy_flavour_from_pdg(int pdg) {
  int apid = std::abs(pdg);
  if (apid < 100)
    return 0;
  int d3 = (apid / 1000) % 10;
  int d2 = (apid / 100) % 10;
  int d1 = (apid / 10) % 10;
  if (d3 == 5 || d2 == 5 || d1 == 5)
    return 5;
  if (d3 == 4 || d2 == 4 || d1 == 4)
    return 4;
  return 0;
}

bool is_heavy_hadron(int pdg) { return heavy_flavour_from_pdg(pdg) != 0; }

bool is_strange_llp(int pdg) {
  int apid = std::abs(pdg);
  return apid == 310 || apid == 3122 || apid == 3112 || apid == 3222 ||
         apid == 3312 || apid == 3322 || apid == 3334;
}

bool is_parton(int pdg) {
  int apid = std::abs(pdg);
  return (apid >= 1 && apid <= 6) || apid == 21;
}

AncestryFlags
walk_ancestry(int idx, const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
              const ROOT::VecOps::RVec<int> &parents) {
  AncestryFlags flags;
  if (idx < 0 || idx >= static_cast<int>(mc.size()))
    return flags;

  std::set<int> visited;
  std::vector<int> stack;
  auto push_parents = [&](int i) {
    const auto &p = mc[i];
    for (unsigned int r = p.parents_begin; r < p.parents_end; ++r) {
      if (r >= parents.size())
        continue;
      int par = parents[r];
      if (par >= 0 && par < static_cast<int>(mc.size()))
        stack.push_back(par);
    }
  };

  push_parents(idx);
  while (!stack.empty()) {
    int i = stack.back();
    stack.pop_back();
    if (!visited.insert(i).second)
      continue;
    int pdg = std::abs(mc[i].PDG);
    if (pdg == 15)
      flags.from_tau = true;
    if (pdg >= 100) {
      if (is_strange_llp(pdg))
        flags.from_sllp = true;
      int fla = heavy_flavour_from_pdg(pdg);
      if (fla == 5)
        flags.from_b = true;
      else if (fla == 4)
        flags.from_c = true;
    }
    push_parents(i);
  }
  return flags;
}

bool has_same_flavour_ancestor(
    int idx, int flavour, const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const ROOT::VecOps::RVec<int> &parents) {
  AncestryFlags flags = walk_ancestry(idx, mc, parents);
  if (flavour == 5)
    return flags.from_b;
  if (flavour == 4)
    return flags.from_c;
  return false;
}

bool is_weakly_decaying(int idx, int flavour,
                        const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                        const ROOT::VecOps::RVec<int> &daughters) {
  if (idx < 0 || idx >= static_cast<int>(mc.size()))
    return false;
  const auto &p = mc[idx];
  for (unsigned int r = p.daughters_begin; r < p.daughters_end; ++r) {
    if (r >= daughters.size())
      continue;
    int dau = daughters[r];
    if (dau < 0 || dau >= static_cast<int>(mc.size()))
      continue;
    if (heavy_flavour_from_pdg(mc[dau].PDG) == flavour)
      return false;
  }
  return true;
}

bool is_final_parton(int idx,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     const ROOT::VecOps::RVec<int> &daughters) {
  if (idx < 0 || idx >= static_cast<int>(mc.size()))
    return false;
  if (!is_parton(mc[idx].PDG))
    return false;
  const auto &p = mc[idx];
  for (unsigned int r = p.daughters_begin; r < p.daughters_end; ++r) {
    if (r >= daughters.size())
      continue;
    int dau = daughters[r];
    if (dau < 0 || dau >= static_cast<int>(mc.size()))
      continue;
    if (is_parton(mc[dau].PDG))
      return false;
  }
  return true;
}

} // namespace TruthLabelUtils
} // namespace FCCAnalyses
