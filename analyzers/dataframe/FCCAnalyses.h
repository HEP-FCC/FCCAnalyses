
#ifndef  FCCANALYSES_ANALYZERS_H
#define  FCCANALYSES_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/ClusterData.h"
#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"
#include "edm4hep/MCRecoParticleAssociationData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/TrackState.h"




/// transverse mass 
ROOT::VecOps::RVec<float> MTW (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in_electrons, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in_muons , ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in_met);


/*** @M3Builder
 * Computes the event variable M3
 *   
 *   All combinations of 3 jets are tested to retain
 *   the one with highest pT (transverse momentum of the 3-jet system).
 *   This combination of three jets is used to build an "M3" particle,
 *   with the pdgid of the top quark. 
 *   
 **/
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> M3Builder (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in_jets, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in_met);


/// compute transverse momentum of a particle
ROOT::VecOps::RVec<float> pt (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// compute pseudorapidity of a particle
ROOT::VecOps::RVec<float> eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// cast a fcc lorentzvector to a root
//ROOT::VecOps::RVec<TLorentzVector> tlv(ROOT::VecOps::RVec<edm4hep::LorentzVector> in);

/// calc
ROOT::VecOps::RVec<float> r (ROOT::VecOps::RVec<edm4hep::vector3d> in); 

double deltaR(edm4hep::LorentzVector v1, edm4hep::LorentzVector v2);

struct recoil {
  recoil(float arg_sqrts);
  float m_sqrts = 240.0;
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) ;
};

struct noMatchJets {
  float m_max_rel_iso;
  // constructor
  noMatchJets(float arg_max_rel_iso);
  ROOT::VecOps::RVec<edm4hep::JetData> operator() (ROOT::VecOps::RVec<edm4hep::JetData> in, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> matchParticles);
};

/// select jets according to transverse momentum and btag
struct selectJets {
  float m_min_pt;
  bool m_btag_must_be_zero;
  selectJets(float arg_min_pt, bool arg_btag_must_be_zero);
ROOT::VecOps::RVec<edm4hep::JetData> operator()(ROOT::VecOps::RVec<edm4hep::JetData> in, ROOT::VecOps::RVec<edm4hep::TaggedJetData> btags);
};


/// select particles with a minimum transverse momentum and isolation
struct selectParticlesPtIso {
  selectParticlesPtIso(float arg_min_pt, float arg_max_iso); //> ctor, set thresholds
  float m_min_pt = 20;  //> transverse momentum threshold [GeV]
  float m_max_iso = 0.4; //> isolation threshold
  ROOT::VecOps::RVec<edm4hep::RecoParticleRefData>  operator() (ROOT::VecOps::RVec<edm4hep::RecoParticleRefData> in, ROOT::VecOps::RVec<edm4hep::TaggedParticleData> iso) ;
};

/// select particles with transverse momentum greater than a minimum value [GeV]
struct selectParticlesPt {
  selectParticlesPt(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};


/// return the transverse momenta of the input lorentz vectors
ROOT::VecOps::RVec<float> get_pt_lv(ROOT::VecOps::RVec<edm4hep::LorentzVector> in);

/// return the transverse momenta of the input particles
ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input particles
ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the pseudo-rapidity of the input particles
ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the rapidity of the input particles
ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the phi of the input particles
ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the energy of the input particles
ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

struct ResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs);
};

struct JetResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  JetResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::JetData> legs);
};

/// cast FloatValueData to a primitive float
ROOT::VecOps::RVec<float> id_float(ROOT::VecOps::RVec<edm4hep::FloatValueData> x);

/// cast FloatData (used in earlier versions of fcc-edm) to a primitive float
ROOT::VecOps::RVec<float> id_float_legacy(ROOT::VecOps::RVec<edm4hep::FloatData> x);

/// return the masses of the input particles
ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x); 

/// return the size of the input collection 
int get_nparticles(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x);

/// return the size of the input collection 
int get_njets(ROOT::VecOps::RVec<edm4hep::JetData> x);

/// return the sum of the  sizes of the input collections collection 
int get_njets2(ROOT::VecOps::RVec<edm4hep::JetData> x, ROOT::VecOps::RVec<edm4hep::JetData> y);

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> LeptonicZBuilder (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons);

  /// @todo: refactor to remove code duplication with leptonicZBuilder
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> LeptonicHiggsBuilder(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> mergeElectronsAndMuons(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

#endif
