
#ifndef RECONSTRUCTEDPARTICLE2MC_ANALYZERS_H
#define RECONSTRUCTEDPARTICLE2MC_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "podio/ObjectID.h"

namespace FCCAnalyses {

namespace ReconstructedParticle2MC {

/// select ReconstructedParticles matched with a MC particle of a given PDG_id
struct selRP_PDG {
  selRP_PDG(int arg_PDG, bool arg_chargedOnly);
  int m_PDG = 13;
  bool m_chargedOnly = true;
  std::vector<edm4hep::ReconstructedParticleData>
  operator()(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
             ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);
};

/// select ReconstructedParticles matched with a MC particle of a given PDG_id
struct selRP_PDG_index {
  selRP_PDG_index(int arg_PDG, bool arg_chargedOnly);
  int m_PDG = 13;
  bool m_chargedOnly = true;
  ROOT::VecOps::RVec<int>
  operator()(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
             ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);
};

/// select ReconstructedParticles with transverse momentum greater than a
/// minimum value [GeV]
struct getRP2MC_p_func {
  ROOT::VecOps::RVec<float>
  operator()(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
             ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);
};

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_p(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
           ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
           ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_px(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
            ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_py(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
            ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_pz(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
            ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_mass(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
              ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
              ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_charge(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float>
getRP2MC_pdg(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
             ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<TLorentzVector>
getRP2MC_tlv(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
             ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<int>
getRP2MC_index(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
               ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>>
getRP2MC_indexVec(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
                  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<int>
getRP2MC_index_test(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
                    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                    ROOT::VecOps::RVec<int> parents);

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<int>
getRP2MC_parentid(ROOT::VecOps::RVec<int> recin, ROOT::VecOps::RVec<int> mcin,
                  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                  ROOT::VecOps::RVec<int> parents);

/// select ReconstructedParticles matched with a MC  charged hadrons
std::vector<edm4hep::ReconstructedParticleData> selRP_ChargedHadrons(
    ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

/// select ReconstructedParticles matched to the MC particles whose indices are
/// passed in a list
/// @param mcParticles_indices indices of the MC particles to look up
/// @param recind: reco index component of the MCRecoAssociations
/// @param mcind: mc index component of the MCRecoAssociations
/// @param reco: full reco particle list (ReconstructedParticles)
/// @param mc: full mc particle list (Particles)
/// @param require_stable: if set to true, will only match stable particles.
/// @return List of ReconstructedParticle candidates with length corresponding
/// to the number of *stable* MC particles in the mcParticles_indices vector. In
/// presence of unstable particles, no 1:1 correspondence. For non-reconstructed
/// stable MC particles, a dummy particle will be inserted. If 1:1 length
/// correspondence is required, set require_stable to false.
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> selRP_matched_to_list(
    const ROOT::VecOps::RVec<int> &mcParticles_indices,
    const ROOT::VecOps::RVec<int> &recind, const ROOT::VecOps::RVec<int> &mcind,
    const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &reco,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    bool require_stable = true);
/// select indices of ReconstructedParticles matched to the MC particles whose
/// indices are passed in a list
/// @param mcParticles_indices indices of the MC particles to look up
/// @param recind: reco index component of the MCRecoAssociations
/// @param mcind: mc index component of the MCRecoAssociations
/// @param mc: full mc particle list (Particles)
/// @param require_stable: if set to true, will only match stable particles.
/// @return List of ReconstructedParticle candidates with length corresponding
/// to the number of *stable* MC particles in the mcParticles_indices vector. In
/// presence of unstable particles, no 1:1 correspondence. For non-reconstructed
/// stable MC particles, a "-1" entry will be inserted. If 1:1 length
/// correspondence is required, set require_stable to false.
ROOT::VecOps::RVec<int> selRP_indices_matched_to_list(
    const ROOT::VecOps::RVec<int> &mcParticles_indices,
    const ROOT::VecOps::RVec<int> &recind, const ROOT::VecOps::RVec<int> &mcind,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mc,
    bool require_stable = true);

/// return the index of the MC particle that is associated to a given track (via
/// the track-reco association)
int getTrack2MC_index(
    int track_index, ROOT::VecOps::RVec<int> recind,
    ROOT::VecOps::RVec<int> mcind,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco);

} // namespace ReconstructedParticle2MC

} // namespace FCCAnalyses
#endif
