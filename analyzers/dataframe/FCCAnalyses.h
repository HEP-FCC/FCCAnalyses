
#ifndef  FCCANALYSES_ANALYZERS_H
#define  FCCANALYSES_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "datamodel/MCParticleData.h"
#include "datamodel/ParticleData.h"
#include "datamodel/JetData.h"
#include "datamodel/TaggedJetData.h"
#include "datamodel/TaggedParticleData.h"
#include "datamodel/MET.h"
#include "datamodel/Point.h"
#include "datamodel/LorentzVector.h"
#include "datamodel/FloatValueData.h"
// legacy
#include "utilities/FloatData.h"



/// transverse mass 
ROOT::VecOps::RVec<float> MTW (ROOT::VecOps::RVec<fcc::ParticleData> in_electrons, ROOT::VecOps::RVec<fcc::ParticleData> in_muons , ROOT::VecOps::RVec<fcc::METData> in_met);


/*** @M3Builder
 * Computes the event variable M3
 *   
 *   All combinations of 3 jets are tested to retain
 *   the one with highest pT (transverse momentum of the 3-jet system).
 *   This combination of three jets is used to build an "M3" particle,
 *   with the pdgid of the top quark. 
 *   
 **/
ROOT::VecOps::RVec<fcc::ParticleData> M3Builder (ROOT::VecOps::RVec<fcc::JetData> in_jets, ROOT::VecOps::RVec<fcc::MET> in_met);


/// compute transverse momentum of a particle
ROOT::VecOps::RVec<float> pt (ROOT::VecOps::RVec<fcc::MCParticleData> in);

/// compute pseudorapidity of a particle
ROOT::VecOps::RVec<float> eta(ROOT::VecOps::RVec<fcc::MCParticleData> in);

/// cast a fcc lorentzvector to a root
ROOT::VecOps::RVec<TLorentzVector> tlv(ROOT::VecOps::RVec<fcc::LorentzVector> in);

/// calc
ROOT::VecOps::RVec<float> r (ROOT::VecOps::RVec<fcc::Point> in); 

double deltaR(fcc::LorentzVector v1, fcc::LorentzVector v2);

struct recoil {
  recoil(float arg_sqrts);
  float m_sqrts = 240.0;
  ROOT::VecOps::RVec<fcc::ParticleData> operator() (ROOT::VecOps::RVec<fcc::ParticleData> in) ;
};

struct noMatchJets {
  float m_max_rel_iso;
  // constructor
  noMatchJets(float arg_max_rel_iso);
  ROOT::VecOps::RVec<fcc::JetData> operator() (ROOT::VecOps::RVec<fcc::JetData> in, ROOT::VecOps::RVec<fcc::ParticleData> matchParticles);
};

/// select jets according to transverse momentum and btag
struct selectJets {
  float m_min_pt;
  bool m_btag_must_be_zero;
  selectJets(float arg_min_pt, bool arg_btag_must_be_zero);
ROOT::VecOps::RVec<fcc::JetData> operator()(ROOT::VecOps::RVec<fcc::JetData> in, ROOT::VecOps::RVec<fcc::TaggedJetData> btags);
};


/// select particles with a minimum transverse momentum and isolation
struct selectParticlesPtIso {
  selectParticlesPtIso(float arg_min_pt, float arg_max_iso); //> ctor, set thresholds
  float m_min_pt = 20;  //> transverse momentum threshold [GeV]
  float m_max_iso = 0.4; //> isolation threshold
  ROOT::VecOps::RVec<fcc::ParticleData>  operator() (ROOT::VecOps::RVec<fcc::ParticleData> in, ROOT::VecOps::RVec<fcc::TaggedParticleData> iso) ;
};

/// select particles with transverse momentum greater than a minimum value [GeV]
struct selectParticlesPt {
  selectParticlesPt(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  ROOT::VecOps::RVec<fcc::ParticleData>  operator() (ROOT::VecOps::RVec<fcc::ParticleData> in);
};


/// return the transverse momenta of the input lorentz vectors
ROOT::VecOps::RVec<float> get_pt_lv(ROOT::VecOps::RVec<fcc::LorentzVector> in);

/// return the transverse momenta of the input particles
ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<fcc::ParticleData> in);

/// return the momenta of the input particles
ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<fcc::ParticleData> in);

/// return the pseudo-rapidity of the input particles
ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<fcc::ParticleData> in);

/// return the rapidity of the input particles
ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<fcc::ParticleData> in);

/// return the phi of the input particles
ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<fcc::ParticleData> in);

/// return the energy of the input particles
ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<fcc::ParticleData> in);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<fcc::ParticleData> mergeParticles(ROOT::VecOps::RVec<fcc::ParticleData> x, ROOT::VecOps::RVec<fcc::ParticleData> y);

struct ResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
ROOT::VecOps::RVec<fcc::ParticleData> operator()(ROOT::VecOps::RVec<fcc::ParticleData> legs);
};

struct JetResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  JetResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
ROOT::VecOps::RVec<fcc::ParticleData> operator()(ROOT::VecOps::RVec<fcc::JetData> legs);
};

/// cast FloatValueData to a primitive float
ROOT::VecOps::RVec<float> id_float(ROOT::VecOps::RVec<fcc::FloatValueData> x);

/// cast FloatData (used in earlier versions of fcc-edm) to a primitive float
ROOT::VecOps::RVec<float> id_float_legacy(ROOT::VecOps::RVec<fcc::FloatData> x);

/// return the masses of the input particles
ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<fcc::ParticleData> x); 

/// return the size of the input collection 
int get_nparticles(ROOT::VecOps::RVec<fcc::ParticleData> x);

/// return the size of the input collection 
int get_njets(ROOT::VecOps::RVec<fcc::JetData> x);

/// return the sum of the  sizes of the input collections collection 
int get_njets2(ROOT::VecOps::RVec<fcc::JetData> x, ROOT::VecOps::RVec<fcc::JetData> y);

ROOT::VecOps::RVec<fcc::ParticleData> LeptonicZBuilder (ROOT::VecOps::RVec<fcc::ParticleData> leptons);

  /// @todo: refactor to remove code duplication with leptonicZBuilder
ROOT::VecOps::RVec<fcc::ParticleData> LeptonicHiggsBuilder(ROOT::VecOps::RVec<fcc::ParticleData> leptons);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<fcc::ParticleData> mergeElectronsAndMuons(ROOT::VecOps::RVec<fcc::ParticleData> x, ROOT::VecOps::RVec<fcc::ParticleData> y);

#endif
