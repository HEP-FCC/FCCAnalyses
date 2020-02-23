
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
#include "datamodel/FloatData.h"


/// good luck charm against segfaults
//fcc::MCParticleData __magicParticle();
//


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


ROOT::VecOps::RVec<float> pt (ROOT::VecOps::RVec<fcc::MCParticleData> in);

ROOT::VecOps::RVec<float> eta(ROOT::VecOps::RVec<fcc::MCParticleData> in);

ROOT::VecOps::RVec<TLorentzVector> tlv(ROOT::VecOps::RVec<fcc::LorentzVector> in);

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

struct selectJets {
  float m_min_pt;
  bool m_btag_must_be_zero;
  selectJets(float arg_min_pt, bool arg_btag_must_be_zero);
ROOT::VecOps::RVec<fcc::JetData> operator()(ROOT::VecOps::RVec<fcc::JetData> in, ROOT::VecOps::RVec<fcc::TaggedJetData> btags);
};


struct selectParticlesPtIso {
  selectParticlesPtIso(float arg_min_pt, float arg_max_iso);
  float m_min_pt = 20;
  float m_max_iso = 0.4;
  ROOT::VecOps::RVec<fcc::ParticleData>  operator() (ROOT::VecOps::RVec<fcc::ParticleData> in, ROOT::VecOps::RVec<fcc::TaggedParticleData> iso) ;
};

struct selectParticlesPt {
  selectParticlesPt(float arg_min_pt);
  float m_min_pt = 20;
  ROOT::VecOps::RVec<fcc::ParticleData>  operator() (ROOT::VecOps::RVec<fcc::ParticleData> in);
};

ROOT::VecOps::RVec<float> get_pt_lv(ROOT::VecOps::RVec<fcc::LorentzVector> in);


ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<fcc::ParticleData> in);


ROOT::VecOps::RVec<fcc::ParticleData> mergeParticles(ROOT::VecOps::RVec<fcc::ParticleData> x, ROOT::VecOps::RVec<fcc::ParticleData> y);

struct ResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
ROOT::VecOps::RVec<fcc::ParticleData> operator()(ROOT::VecOps::RVec<fcc::ParticleData> leptons);
};

ROOT::VecOps::RVec<float> id_float(ROOT::VecOps::RVec<fcc::FloatValueData> x);

ROOT::VecOps::RVec<float> id_float_legacy(ROOT::VecOps::RVec<fcc::FloatData> x);

ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<fcc::ParticleData> x); 

int get_nparticles(ROOT::VecOps::RVec<fcc::ParticleData> x);


int get_njets(ROOT::VecOps::RVec<fcc::JetData> x);

int get_njets2(ROOT::VecOps::RVec<fcc::JetData> x, ROOT::VecOps::RVec<fcc::JetData> y);


ROOT::VecOps::RVec<fcc::ParticleData> LeptonicZBuilder (ROOT::VecOps::RVec<fcc::ParticleData> leptons);

  /// @todo: refactor to remove code duplication with leptonicZBuilder
inline ROOT::VecOps::RVec<fcc::ParticleData> LeptonicHiggsBuilder(ROOT::VecOps::RVec<fcc::ParticleData> leptons) {

        ROOT::VecOps::RVec<fcc::ParticleData> result;
        int n = leptons.size();
        if (n >2) {
          ROOT::VecOps::RVec<bool> v(n);
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

    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<fcc::ParticleData> onlyBestHiggs(first, last);
    return onlyBestHiggs;
    } else {
    return result;
    }
  };


inline ROOT::VecOps::RVec<fcc::ParticleData> mergeElectronsAndMuons(ROOT::VecOps::RVec<fcc::ParticleData> x, ROOT::VecOps::RVec<fcc::ParticleData> y) {
     std::vector<fcc::ParticleData> result;
     result.reserve(x.size() + y.size());
     result.insert( result.end(), x.begin(), x.end() );
     result.insert( result.end(), y.begin(), y.end() );

     return ROOT::VecOps::RVec(result);

   };

#endif
