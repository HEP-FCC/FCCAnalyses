#include "FCCAnalyses/TruthLabelUtils.h"

#include <algorithm>
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

bool is_strange_meson(int pdg) {
  int apid = std::abs(pdg);
  return apid == 310 || apid == 130 || apid == 321;
}

bool is_strange_baryon(int pdg) {
  int apid = std::abs(pdg);
  return apid == 3122 || apid == 3112 || apid == 3212 || apid == 3222 ||
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

edm4hep::Vector3d
mc_primary_vertex(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc) {
  for (const auto &p : mc)
    if (p.generatorStatus == 21)
      return p.vertex;
  for (const auto &p : mc)
    if (p.generatorStatus == 4)
      return p.vertex;
  for (const auto &p : mc)
    if (p.parents_begin == p.parents_end)
      return p.vertex;
  return edm4hep::Vector3d(0., 0., 0.);
}

double distance2(const edm4hep::Vector3d &a, const edm4hep::Vector3d &b) {
  double dx = a.x - b.x;
  double dy = a.y - b.y;
  double dz = a.z - b.z;
  return dx * dx + dy * dy + dz * dz;
}

std::unordered_map<int, int>
reco_to_mc_map(const ROOT::VecOps::RVec<int> &recin,
               const ROOT::VecOps::RVec<int> &mcin) {
  std::unordered_map<int, int> m;
  size_t n = std::min(recin.size(), mcin.size());
  m.reserve(n);
  for (size_t i = 0; i < n; ++i)
    m[recin[i]] = mcin[i];
  return m;
}

std::unordered_map<int, int>
truth_vertex_indices(const std::vector<int> &mc_indices,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     float merge_radius_mm) {
  const double radius2 = static_cast<double>(merge_radius_mm) *
                         static_cast<double>(merge_radius_mm);

  std::set<int> unique_mc;
  for (int m : mc_indices)
    if (m >= 0 && m < static_cast<int>(mc.size()))
      unique_mc.insert(m);

  std::vector<edm4hep::Vector3d> cluster_pos;
  std::vector<int> cluster_size;
  std::unordered_map<int, int> mc_to_cluster;
  for (int m : unique_mc) {
    const auto &vtx = mc[m].vertex;
    int assigned = -1;
    for (size_t ci = 0; ci < cluster_pos.size(); ++ci) {
      if (distance2(vtx, cluster_pos[ci]) < radius2) {
        assigned = static_cast<int>(ci);
        break;
      }
    }
    if (assigned < 0) {
      assigned = static_cast<int>(cluster_pos.size());
      cluster_pos.push_back(vtx);
      cluster_size.push_back(0);
    }
    cluster_size[assigned]++;
    mc_to_cluster[m] = assigned;
  }

  // index 0 is the cluster holding the MC primary vertex; the rest follow in
  // decreasing occupancy so the numbering is stable across jets of an event
  std::unordered_map<int, int> relabel;
  if (!cluster_pos.empty()) {
    const edm4hep::Vector3d pv = mc_primary_vertex(mc);
    int pv_cluster = -1;
    for (size_t ci = 0; ci < cluster_pos.size(); ++ci) {
      if (distance2(pv, cluster_pos[ci]) < radius2) {
        pv_cluster = static_cast<int>(ci);
        break;
      }
    }

    std::vector<int> order(cluster_pos.size());
    for (size_t ci = 0; ci < order.size(); ++ci)
      order[ci] = static_cast<int>(ci);
    std::stable_sort(order.begin(), order.end(), [&](int a, int b) {
      return cluster_size[a] > cluster_size[b];
    });
    if (pv_cluster < 0)
      pv_cluster = order.front();

    relabel[pv_cluster] = 0;
    int next_idx = 1;
    for (int ci : order)
      if (ci != pv_cluster)
        relabel[ci] = next_idx++;
  }

  std::unordered_map<int, int> result;
  result.reserve(mc_to_cluster.size());
  for (const auto &kv : mc_to_cluster)
    result[kv.first] = relabel[kv.second];
  return result;
}

} // namespace TruthLabelUtils
} // namespace FCCAnalyses
