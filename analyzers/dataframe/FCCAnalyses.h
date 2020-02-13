
#ifndef  FCCANALYSES_ANALYZERS_H
#define  FCCANALYSES_ANALYZERS_H

#include <cmath>
#include <vector>

//class TLorentzVector;
//
//namespace fcc {
//  class Point;
//  class LorentzVector;
//
//  class MCParticleData;
//  class ParticleData;
//}

#include "TLorentzVector.h"
#include "datamodel/MCParticleData.h"
#include "datamodel/ParticleData.h"
#include "datamodel/JetData.h"
#include "datamodel/TaggedJetData.h"
#include "datamodel/TaggedParticleData.h"

#include "datamodel/Point.h"
#include "datamodel/LorentzVector.h"
#include "datamodel/FloatValueData.h"


/// good luck charm against segfaults
fcc::MCParticleData __magicParticle();

std::vector<float> pt (std::vector<fcc::MCParticleData> in);

std::vector<float> eta(std::vector<fcc::MCParticleData> in);

std::vector<TLorentzVector> tlv(std::vector<fcc::LorentzVector> in);

std::vector<float> r (std::vector<fcc::Point> in); 

double deltaR(fcc::LorentzVector v1, fcc::LorentzVector v2);

struct recoil {
  recoil(float arg_sqrts);
  float m_sqrts = 240.0;
  std::vector<fcc::ParticleData> operator() (std::vector<fcc::ParticleData> in) ;
};

struct noMatchJets {
  float m_max_rel_iso;
  // constructor
  noMatchJets(float arg_max_rel_iso);
  std::vector<fcc::JetData> operator() (std::vector<fcc::JetData> in, std::vector<fcc::ParticleData> matchParticles);
};

struct selectJets {
  float m_min_pt;
  bool m_btag_must_be_zero;
  selectJets(float arg_min_pt, bool arg_btag_must_be_zero);
std::vector<fcc::JetData> operator()(std::vector<fcc::JetData> in, std::vector<fcc::TaggedJetData> btags);
};


struct selectParticlesPtIso {
  selectParticlesPtIso(float arg_min_pt, float arg_max_iso);
  float m_min_pt = 20;
  float m_max_iso = 0.4;
  std::vector<fcc::ParticleData>  operator() (std::vector<fcc::ParticleData> in, std::vector<fcc::TaggedParticleData> iso) ;
};

struct selectParticlesPt {
  selectParticlesPt(float arg_min_pt);
  float m_min_pt = 20;
  std::vector<fcc::ParticleData>  operator() (std::vector<fcc::ParticleData> in);
};

std::vector<float> get_pt_lv(std::vector<fcc::LorentzVector> in);


std::vector<float> get_pt(std::vector<fcc::ParticleData> in);


std::vector<fcc::ParticleData> mergeParticles(std::vector<fcc::ParticleData> x, std::vector<fcc::ParticleData> y);

struct ResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
std::vector<fcc::ParticleData> operator()(std::vector<fcc::ParticleData> leptons);
};

std::vector<float> id_float(std::vector<fcc::FloatValueData> x);

std::vector<float> get_mass(std::vector<fcc::ParticleData> x); 

int get_nparticles(std::vector<fcc::ParticleData> x);

int get_njets(std::vector<fcc::JetData> x);

int get_njets2(std::vector<fcc::JetData> x, std::vector<fcc::JetData> y);

#endif
