
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

// legacy
#include "datamodel/FloatData.h"


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

std::vector<float> id_float_legacy(std::vector<fcc::FloatData> x);

std::vector<float> get_mass(std::vector<fcc::ParticleData> x); 

int get_nparticles(std::vector<fcc::ParticleData> x);

int get_njets(std::vector<fcc::JetData> x);

int get_njets2(std::vector<fcc::JetData> x, std::vector<fcc::JetData> y);


std::vector<fcc::ParticleData> LeptonicZBuilder (std::vector<fcc::ParticleData> leptons);

  /// @todo: refactor to remove code duplication with leptonicZBuilder
inline std::vector<fcc::ParticleData> LeptonicHiggsBuilder(std::vector<fcc::ParticleData> leptons) {

        std::vector<fcc::ParticleData> result;
        int n = leptons.size();
        if (n >2) {
          std::vector<bool> v(n);
          std::fill(v.end() - 2, v.end(), true);
          do {
            fcc::ParticleData zed;
            zed.core.pdgId = 25;
            TLorentzVector zed_lv; 
            for (int i = 0; i < n; ++i) {
                if (v[i]) {
                  zed.core.charge += leptons[i].core.charge;
                  TLorentzVector lepton_lv;
                  lepton_lv.SetXYZM(leptons[i].core.p4.px, leptons[i].core.p4.py, leptons[i].core.p4.pz, leptons[i].core.p4.mass);
                  zed_lv += lepton_lv;
                }
            }
            zed.core.p4.px = zed_lv.Px();
            zed.core.p4.py = zed_lv.Py();
            zed.core.p4.pz = zed_lv.Pz();
            zed.core.p4.mass = zed_lv.M();
            result.emplace_back(zed);

          
          } while (std::next_permutation(v.begin(), v.end()));
        }

    if (result.size() > 1) {
    auto  higgsresonancesort = [] (fcc::ParticleData i ,fcc::ParticleData j) { return (abs( 125. -i.core.p4.mass)<abs(125.-j.core.p4.mass)); };
    std::sort(result.begin(), result.end(), higgsresonancesort);

    std::vector<fcc::ParticleData>::const_iterator first = result.begin();
    std::vector<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    std::vector<fcc::ParticleData> onlyBestHiggs(first, last);
    return onlyBestHiggs;
    } else {
    return result;
    }
  };


inline std::vector<fcc::ParticleData> mergeElectronsAndMuons(std::vector<fcc::ParticleData> x, std::vector<fcc::ParticleData> y) {
     std::vector<fcc::ParticleData> result;
     result.reserve(x.size() + y.size());
     result.insert( result.end(), x.begin(), x.end() );
     result.insert( result.end(), y.begin(), y.end() );
     return result;

   };

#endif
