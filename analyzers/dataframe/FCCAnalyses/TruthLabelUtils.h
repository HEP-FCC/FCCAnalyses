#ifndef TRUTHLABELUTILS_ANALYZERS_H
#define TRUTHLABELUTILS_ANALYZERS_H

#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"

namespace FCCAnalyses {
/**
 * @brief Shared primitives for ATLAS-style truth labelling.
 *
 * Navigation of the EDM4hep MC record (ancestry walks, heavy-flavour
 * classification) used by the jet-level ghost labels.
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

} // namespace TruthLabelUtils
} // namespace FCCAnalyses

#endif
