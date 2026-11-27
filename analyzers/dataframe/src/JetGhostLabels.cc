#include "FCCAnalyses/JetGhostLabels.h"
#include "FCCAnalyses/TruthLabelUtils.h"

#include <limits>

namespace FCCAnalyses {
namespace JetGhostLabels {

namespace {

constexpr float kNaN = std::numeric_limits<float>::quiet_NaN();

/// Per-jet tally of the ghosts assigned to it.
struct JetTally {
  int n_b = 0;
  int n_c = 0;
  int n_tau = 0;
};

std::vector<JetTally> tally(size_t njets,
                            const ROOT::VecOps::RVec<int> &assignment,
                            const GhostParticles &ghosts) {
  std::vector<JetTally> t(njets);
  size_t n = std::min(assignment.size(), ghosts.pdg.size());
  for (size_t i = 0; i < n; ++i) {
    int j = assignment[i];
    if (j < 0 || j >= static_cast<int>(njets))
      continue;
    int apdg = std::abs(ghosts.pdg[i]);
    if (apdg == 15) {
      t[j].n_tau++;
      continue;
    }
    int fla = TruthLabelUtils::heavy_flavour_from_pdg(ghosts.pdg[i]);
    if (fla == 5)
      t[j].n_b++;
    else if (fla == 4)
      t[j].n_c++;
  }
  return t;
}

int standard_label(const JetTally &t) {
  if (t.n_b > 0)
    return 5;
  if (t.n_c > 0)
    return 4;
  if (t.n_tau > 0)
    return 15;
  return 0;
}

/// Flavour class of a ghost: 5, 4, 15 or 0.
int ghost_class(int pdg) {
  if (std::abs(pdg) == 15)
    return 15;
  return TruthLabelUtils::heavy_flavour_from_pdg(pdg);
}

/// Index of the highest-pT ghost of class @p want assigned to jet @p jet,
/// or -1.
int leading_ghost(int jet, int want, const ROOT::VecOps::RVec<int> &assignment,
                  const GhostParticles &ghosts) {
  int best = -1;
  double best_pt = -1.;
  size_t n = std::min(assignment.size(), ghosts.pdg.size());
  for (size_t i = 0; i < n; ++i) {
    if (assignment[i] != jet)
      continue;
    if (ghost_class(ghosts.pdg[i]) != want)
      continue;
    double pt = ghosts.p[i].pt();
    if (pt > best_pt) {
      best_pt = pt;
      best = static_cast<int>(i);
    }
  }
  return best;
}

/// Index of the highest-energy ghost assigned to jet @p jet, or -1.
int leading_energy_ghost(int jet, const ROOT::VecOps::RVec<int> &assignment,
                         const GhostParticles &ghosts) {
  int best = -1;
  double best_e = -1.;
  size_t n = std::min(assignment.size(), ghosts.p.size());
  for (size_t i = 0; i < n; ++i) {
    if (assignment[i] != jet)
      continue;
    double e = ghosts.p[i].e();
    if (e > best_e) {
      best_e = e;
      best = static_cast<int>(i);
    }
  }
  return best;
}

} // namespace

GhostParticles
get_ghost_hadrons(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                  const ROOT::VecOps::RVec<int> &parents,
                  const ROOT::VecOps::RVec<int> &daughters, float pt_min_gev,
                  bool weakly_decaying, bool include_taus) {
  GhostParticles out;
  for (size_t i = 0; i < mc.size(); ++i) {
    const auto &p = mc[i];
    int pdg = p.PDG;
    int apdg = std::abs(pdg);

    bool keep = false;
    if (include_taus && apdg == 15) {
      // only the last tau of a radiative chain
      keep = true;
      for (unsigned int r = p.daughters_begin; r < p.daughters_end; ++r) {
        if (r >= daughters.size())
          continue;
        int dau = daughters[r];
        if (dau >= 0 && dau < static_cast<int>(mc.size()) &&
            std::abs(mc[dau].PDG) == 15) {
          keep = false;
          break;
        }
      }
    } else {
      int fla = TruthLabelUtils::heavy_flavour_from_pdg(pdg);
      if (fla == 4 || fla == 5) {
        // a c hadron below a b hadron is the c-leg of the b decay
        TruthLabelUtils::AncestryFlags anc =
            TruthLabelUtils::walk_ancestry(static_cast<int>(i), mc, parents);
        if (!(fla == 4 && anc.from_b)) {
          keep = weakly_decaying ? TruthLabelUtils::is_weakly_decaying(
                                       static_cast<int>(i), fla, mc, daughters)
                                 : !TruthLabelUtils::has_same_flavour_ancestor(
                                       static_cast<int>(i), fla, mc, parents);
        }
      }
    }
    if (!keep)
      continue;

    const auto &mom = p.momentum;
    double pt = std::sqrt(mom.x * mom.x + mom.y * mom.y);
    if (pt < pt_min_gev)
      continue;

    double e = std::sqrt(mom.x * mom.x + mom.y * mom.y + mom.z * mom.z +
                         p.mass * p.mass);
    out.p.emplace_back(mom.x, mom.y, mom.z, e);
    out.pdg.push_back(pdg);
    out.mc_index.push_back(static_cast<int>(i));
  }
  return out;
}

GhostParticles
get_ghost_partons(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                  const ROOT::VecOps::RVec<int> &daughters, float pt_min_gev) {
  GhostParticles out;
  for (size_t i = 0; i < mc.size(); ++i) {
    if (!TruthLabelUtils::is_final_parton(static_cast<int>(i), mc, daughters))
      continue;
    const auto &mom = mc[i].momentum;
    double pt = std::sqrt(mom.x * mom.x + mom.y * mom.y);
    if (pt < pt_min_gev)
      continue;
    double e = std::sqrt(mom.x * mom.x + mom.y * mom.y + mom.z * mom.z +
                         mc[i].mass * mc[i].mass);
    out.p.emplace_back(mom.x, mom.y, mom.z, e);
    out.pdg.push_back(mc[i].PDG);
    out.mc_index.push_back(static_cast<int>(i));
  }
  return out;
}

ROOT::VecOps::RVec<int>
get_hadron_label(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                 const ROOT::VecOps::RVec<int> &assignment,
                 const GhostParticles &ghosts) {
  std::vector<JetTally> t = tally(jets.size(), assignment, ghosts);
  ROOT::VecOps::RVec<int> out(jets.size(), 0);
  for (size_t j = 0; j < jets.size(); ++j)
    out[j] = standard_label(t[j]);
  return out;
}

ROOT::VecOps::RVec<int>
get_hadron_extended_label(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                          const ROOT::VecOps::RVec<int> &assignment,
                          const GhostParticles &ghosts) {
  std::vector<JetTally> t = tally(jets.size(), assignment, ghosts);
  ROOT::VecOps::RVec<int> out(jets.size(), 0);
  for (size_t j = 0; j < jets.size(); ++j) {
    const JetTally &c = t[j];
    if (c.n_b >= 2)
      out[j] = 55;
    else if (c.n_b == 1 && c.n_c >= 1)
      out[j] = 54;
    else if (c.n_b == 1)
      out[j] = 5;
    else if (c.n_c >= 2)
      out[j] = 44;
    else if (c.n_c == 1)
      out[j] = 4;
    else if (c.n_tau >= 2)
      out[j] = 1515;
    else if (c.n_tau == 1)
      out[j] = 15;
  }
  return out;
}

ROOT::VecOps::RVec<int>
get_hadron_label_pdg(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                     const ROOT::VecOps::RVec<int> &assignment,
                     const GhostParticles &ghosts) {
  std::vector<JetTally> t = tally(jets.size(), assignment, ghosts);
  ROOT::VecOps::RVec<int> out(jets.size(), 0);
  for (size_t j = 0; j < jets.size(); ++j) {
    int label = standard_label(t[j]);
    if (label == 0)
      continue;
    int i = leading_ghost(static_cast<int>(j), label, assignment, ghosts);
    if (i >= 0)
      out[j] = ghosts.pdg[i];
  }
  return out;
}

ROOT::VecOps::RVec<float>
get_hadron_label_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                    const ROOT::VecOps::RVec<int> &assignment,
                    const GhostParticles &ghosts) {
  std::vector<JetTally> t = tally(jets.size(), assignment, ghosts);
  ROOT::VecOps::RVec<float> out(jets.size(), kNaN);
  for (size_t j = 0; j < jets.size(); ++j) {
    int label = standard_label(t[j]);
    if (label == 0)
      continue;
    int i = leading_ghost(static_cast<int>(j), label, assignment, ghosts);
    if (i >= 0)
      out[j] = static_cast<float>(ghosts.p[i].pt());
  }
  return out;
}

ROOT::VecOps::RVec<int>
count_ghosts(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
             const ROOT::VecOps::RVec<int> &assignment,
             const GhostParticles &ghosts, int flavour) {
  std::vector<JetTally> t = tally(jets.size(), assignment, ghosts);
  ROOT::VecOps::RVec<int> out(jets.size(), 0);
  for (size_t j = 0; j < jets.size(); ++j) {
    if (flavour == 5)
      out[j] = t[j].n_b;
    else if (flavour == 4)
      out[j] = t[j].n_c;
    else if (flavour == 15)
      out[j] = t[j].n_tau;
  }
  return out;
}

ROOT::VecOps::RVec<int>
get_parton_label(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                 const ROOT::VecOps::RVec<int> &assignment,
                 const GhostParticles &ghosts) {
  ROOT::VecOps::RVec<int> out(jets.size(), -1);
  for (size_t j = 0; j < jets.size(); ++j) {
    int i = leading_energy_ghost(static_cast<int>(j), assignment, ghosts);
    if (i >= 0)
      out[j] = std::abs(ghosts.pdg[i]);
  }
  return out;
}

ROOT::VecOps::RVec<float>
get_parton_label_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                    const ROOT::VecOps::RVec<int> &assignment,
                    const GhostParticles &ghosts) {
  ROOT::VecOps::RVec<float> out(jets.size(), kNaN);
  for (size_t j = 0; j < jets.size(); ++j) {
    int i = leading_energy_ghost(static_cast<int>(j), assignment, ghosts);
    if (i >= 0)
      out[j] = static_cast<float>(ghosts.p[i].pt());
  }
  return out;
}

ROOT::VecOps::RVec<float>
get_parton_label_dr(const ROOT::VecOps::RVec<fastjet::PseudoJet> &jets,
                    const ROOT::VecOps::RVec<int> &assignment,
                    const GhostParticles &ghosts) {
  ROOT::VecOps::RVec<float> out(jets.size(), kNaN);
  for (size_t j = 0; j < jets.size(); ++j) {
    int i = leading_energy_ghost(static_cast<int>(j), assignment, ghosts);
    if (i >= 0)
      out[j] = static_cast<float>(jets[j].delta_R(ghosts.p[i]));
  }
  return out;
}

} // namespace JetGhostLabels
} // namespace FCCAnalyses
