#ifndef CONSTITUENTTRUTHLABELS_ANALYZERS_H
#define CONSTITUENTTRUTHLABELS_ANALYZERS_H

#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"

#include <vector>

namespace FCCAnalyses {
/**
 * @brief ATLAS-style truth labels for jet constituents.
 *
 * Each constituent is matched to an MC particle through the reco<->MC link
 * and labelled with the ATLAS track-truth quantities. All outputs are jagged
 * (jet -> constituent) and float valued, matching the other pfcand_*
 * variables of the tagger input set.
 *
 * FCC-ee Delphes samples have no pile-up and no fake tracks (every particle
 * has simulatorStatus 0), so the origin classes Pileup (0) and Fake (1) and
 * the source class HadronicInteraction (2) are never produced.
 */
namespace ConstituentTruthLabels {

using ConstituentsData = ROOT::VecOps::RVec<float>;

/// ftagTruthOriginLabel:
///   2 Primary, 3 FromB, 4 FromBC, 5 FromC, 6 FromTau, 7 OtherSecondary.
/// Constituents without a reco<->MC link get -1, which is the label Salt
/// treats as invalid and masks out of the loss, rather than being folded
/// into OtherSecondary.
ROOT::VecOps::RVec<ConstituentsData>
get_truthOriginLabel(const ROOT::VecOps::RVec<int> &recin,
                     const ROOT::VecOps::RVec<int> &mcin,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     const ROOT::VecOps::RVec<int> &parents,
                     const std::vector<std::vector<int>> &indices);

/// ftagTruthTypeLabel:
///   0 NoTruth, 1 Other, 2 Pion, 3 Kaon, 4 Lambda, 5 Electron, 6 Muon,
///   7 Photon. For |label| > 1 the sign follows the electric charge of the
///   truth particle, not the sign of its PDG id, so an electron is -5 and a
///   positron +5.
ROOT::VecOps::RVec<ConstituentsData>
get_truthTypeLabel(const ROOT::VecOps::RVec<int> &recin,
                   const ROOT::VecOps::RVec<int> &mcin,
                   const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                   const ROOT::VecOps::RVec<int> &parents,
                   const std::vector<std::vector<int>> &indices);

/// ftagTruthSourceLabel:
///   0 NoTruth, 1 NotSecondary, 2 HadronicInteraction, 3 StrangeMesonDecay,
///   4 StrangeBaryonDecay, 5 GammaConversion, 6 Other.
/// This describes the secondary interaction a particle came from, so
/// heavy-flavour decay products are NotSecondary; their displacement is
/// carried by the origin label instead. Classes 2 and 6 need detector
/// simulation and are never produced by a Delphes sample.
ROOT::VecOps::RVec<ConstituentsData>
get_truthSourceLabel(const ROOT::VecOps::RVec<int> &recin,
                     const ROOT::VecOps::RVec<int> &mcin,
                     const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
                     const ROOT::VecOps::RVec<int> &parents,
                     const std::vector<std::vector<int>> &indices);

/// ftagTruthVertexIndex: 0 for the truth primary vertex, 1, 2, ... for
/// secondary vertices in decreasing occupancy, -2 when there is no MC link.
/// Vertices are clustered event-wide so the index identifies the same vertex
/// across all jets of an event.
ROOT::VecOps::RVec<ConstituentsData> get_truthVertexIndex(
    const ROOT::VecOps::RVec<int> &recin, const ROOT::VecOps::RVec<int> &mcin,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    const std::vector<std::vector<int>> &indices, float merge_radius_mm = 0.1f);

/// PDG id of the matched MC particle, 0 when there is no MC link.
ROOT::VecOps::RVec<ConstituentsData>
get_truthPdgId(const ROOT::VecOps::RVec<int> &recin,
               const ROOT::VecOps::RVec<int> &mcin,
               const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
               const std::vector<std::vector<int>> &indices);

} // namespace ConstituentTruthLabels
} // namespace FCCAnalyses

#endif
