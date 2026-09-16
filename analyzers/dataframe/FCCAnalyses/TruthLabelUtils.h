#ifndef TRUTHLABELUTILS_ANALYZERS_H
#define TRUTHLABELUTILS_ANALYZERS_H

#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"

#include <unordered_map>
#include <vector>

namespace FCCAnalyses {
/**
 * @brief Shared primitives for ATLAS-style truth labelling.
 *
 * Navigation of the EDM4hep MC record (ancestry walks, heavy-flavour
 * classification, truth vertices) used by both the jet-level ghost labels
 * and the per-constituent track labels.
 *
 * Throughout, @c parents and @c daughters are the flat relation-index
 * collections @c _Particle_parents.index and @c _Particle_daughters.index.
 */
namespace TruthLabelUtils {

/// Heavy-flavour class of a PDG id: 5 (b hadron), 4 (c hadron), 0 otherwise.
/// Bare quarks are not hadrons and return 0.
int heavy_flavour_from_pdg(int pdg);

/// True for a hadron carrying a b or c quark.
bool is_heavy_hadron(int pdg);

/// Long-lived strange hadron whose decay products are secondary tracks
/// (K_S0, Lambda, Sigma, Xi, Omega), as in the ATLAS truth-origin scheme.
bool is_strange_llp(int pdg);

/// Strange meson whose decay feeds ATLAS TruthSource::StrangeMesonDecay.
bool is_strange_meson(int pdg);

/// Strange baryon whose decay feeds ATLAS TruthSource::StrangeBaryonDecay.
bool is_strange_baryon(int pdg);

/// True for a parton: quark (|PDG| <= 6) or gluon.
bool is_parton(int pdg);

/// What was found while walking a particle's ancestry.
struct AncestryFlags {
  bool from_b = false;    ///< a b hadron sits above
  bool from_c = false;    ///< a c hadron sits above
  bool from_tau = false;  ///< a tau sits above
  bool from_sllp = false; ///< a long-lived strange hadron sits above
};

/// Walk the full parent ancestry of @p idx, collecting heavy-flavour, tau and
/// strange-LLP flags. Only hadrons (and taus) are considered, so bare partons
/// never set the heavy-flavour flags.
AncestryFlags
walk_ancestry(int idx, const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
              const ROOT::VecOps::RVec<int> &parents);

/// True if @p idx has an ancestor hadron of the same heavy-flavour class.
/// Used to keep only production-flavour ("initial") heavy hadrons, which also
/// keeps the pre-oscillation state of a neutral B.
bool has_same_flavour_ancestor(
    int idx, int flavour, const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const ROOT::VecOps::RVec<int> &parents);

/// True if no daughter of @p idx carries the same heavy-flavour class, i.e.
/// @p idx is the last (weakly decaying) hadron of its chain, as used by the
/// ATLAS Hadron* labels.
bool is_weakly_decaying(int idx, int flavour,
                        const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                        const ROOT::VecOps::RVec<int> &daughters);

/// True if @p idx has no parton daughter, i.e. it is the last parton of its
/// branch before hadronisation. Generator independent: it does not rely on
/// generator status codes, which differ between productions (Pythia8 exposes
/// 71-79, Whizard+Pythia6 only 1 and 2).
bool is_final_parton(int idx,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     const ROOT::VecOps::RVec<int> &daughters);

/// Position of the MC primary vertex, with the same three-tier fallback as
/// MCParticle::get_EventPrimaryVertexP4: Pythia8 hard-process particle
/// (generatorStatus 21), then HepMC beam particle (4), then the first
/// parentless particle.
edm4hep::Vector3d
mc_primary_vertex(const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc);

/// Squared distance between two points, in mm^2.
double distance2(const edm4hep::Vector3d &a, const edm4hep::Vector3d &b);

/// Reco index -> MC index, from the from/to index collections of a
/// reco<->MC link. Duplicated links keep the last entry; the link weight
/// carries no information in the FCC samples (it is always 1).
std::unordered_map<int, int>
reco_to_mc_map(const ROOT::VecOps::RVec<int> &recin,
               const ROOT::VecOps::RVec<int> &mcin);

/// Cluster the production vertices of @p mc_indices and return, per MC index,
/// an ATLAS-style truth vertex index: 0 for the cluster holding the MC primary
/// vertex, then 1, 2, ... for the remaining vertices in decreasing occupancy.
/// Vertices closer than @p merge_radius_mm are merged.
std::unordered_map<int, int>
truth_vertex_indices(const std::vector<int> &mc_indices,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     float merge_radius_mm = 0.1f);

} // namespace TruthLabelUtils
} // namespace FCCAnalyses

#endif
