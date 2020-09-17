#include "FCCAnalyses.h"

#include "TLorentzVector.h"
#include "datamodel/MCParticleData.h"
#include "datamodel/ParticleData.h"
#include "datamodel/Point.h"
#include "datamodel/LorentzVector.h"

///todo: review
ROOT::VecOps::RVec<float> MTW (ROOT::VecOps::RVec<fcc::ParticleData> in_electrons, ROOT::VecOps::RVec<fcc::ParticleData> in_muons , ROOT::VecOps::RVec<fcc::METData> in_met) {

  ROOT::VecOps::RVec<float> result;

  /// original author in heppy: "this logic is bad"

  TLorentzVector lepton_lv;

  float met_pt;
  float met_phi;
  if (in_met.size() > 0) {
      met_pt = in_met[0].scalarSum;
      met_phi = in_met[0].phi;
  }
  
  if (in_electrons.size() == 1) {

    lepton_lv.SetXYZM(in_electrons[0].core.p4.px, in_electrons[0].core.p4.py, in_electrons[0].core.p4.pz, in_electrons[0].core.p4.mass);


  } else if (in_muons.size() > 0) {

    lepton_lv.SetXYZM(in_muons[0].core.p4.px, in_muons[0].core.p4.py, in_muons[0].core.p4.pz, in_muons[0].core.p4.mass);

  }
  float mtw = sqrt(2. * lepton_lv.Pt() * met_pt * (1. - cos(lepton_lv.Phi() - met_phi)));
  result.push_back(mtw);
 
  
  return result; 
  
};

ROOT::VecOps::RVec<fcc::ParticleData> M3Builder (ROOT::VecOps::RVec<fcc::JetData> in_jet, ROOT::VecOps::RVec<fcc::MET> in_met) {
 ROOT::VecOps::RVec<fcc::ParticleData> result;
  int n = in_jet.size();
  if (n > 2) {
    /// iterate over permutations
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 3, v.end(), true);
    do {
      fcc::ParticleData m3;
      m3.core.pdgId = 6; //pdgid of top quark
      TLorentzVector m3_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
            TLorentzVector jet_lv;
            jet_lv.SetXYZM(in_jet[i].core.p4.px, in_jet[i].core.p4.py, in_jet[i].core.p4.pz, in_jet[i].core.p4.mass);
            m3_lv += jet_lv;
          }
      }
      m3.core.p4.px = m3_lv.Px();
      m3.core.p4.py = m3_lv.Py();
      m3.core.p4.pz = m3_lv.Pz();
      m3.core.p4.mass = m3_lv.M();
      result.emplace_back(m3);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto  ptsort = [&] (fcc::ParticleData i ,fcc::ParticleData j) { return (abs( pow(i.core.p4.px,2)+pow(i.core.p4.py,2))<abs(pow(j.core.p4.px,2) + pow(j.core.p4.py,2))); };
    std::sort(result.begin(), result.end(), ptsort);
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<fcc::ParticleData> highestPtRes(first, last);
    return highestPtRes;
  } else {
    return result;
  }
 return result;
  
  
  };

ROOT::VecOps::RVec<float> pt (ROOT::VecOps::RVec<fcc::MCParticleData> in){
 ROOT::VecOps::RVec<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
		 result.push_back(std::sqrt(in[i].core.p4.px * in[i].core.p4.px + in[i].core.p4.py * in[i].core.p4.py));
	 }
	 return result;
}

ROOT::VecOps::RVec<float> eta(ROOT::VecOps::RVec<fcc::MCParticleData> in){
 ROOT::VecOps::RVec<float> result;
   TLorentzVector lv;
	 for (size_t i = 0; i < in.size(); ++i) {
     lv.SetXYZM(in[i].core.p4.px, in[i].core.p4.py, in[i].core.p4.pz, in[i].core.p4.mass);
		 result.push_back(lv.Eta());
	 }
	 return result;
}

//ROOT::VecOps::RVec<TLorentzVector> tlv(ROOT::VecOps::RVec<fcc::LorentzVector> in){
// ROOT::VecOps::RVec<TLorentzVector> result;
//   TLorentzVector lv;
//	 for (size_t i = 0; i < in.size(); ++i) {
//     lv.SetXYZM(in[i].px, in[i].py, in[i].pz, in[i].mass);
//		 result.push_back(lv);
//	 }
//	 return result;
//}

ROOT::VecOps::RVec<float> r (ROOT::VecOps::RVec<fcc::Point> in) {
 ROOT::VecOps::RVec<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
     result.push_back(std::sqrt(in[i].x*in[i].x + in[i].y*in[i].y));
   }
 return result; 
}


ROOT::VecOps::RVec<float> norm (ROOT::VecOps::RVec<fcc::Point> in) {
 ROOT::VecOps::RVec<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
     result.push_back(std::sqrt(in[i].x*in[i].x + in[i].y*in[i].y + in[i].z*in[i].z));
   }
 return result; 
}

double deltaR(fcc::LorentzVector v1, fcc::LorentzVector v2) {
  TLorentzVector tv1;
  tv1.SetXYZM(v1.px, v1.py, v1.pz, v1.mass);

  TLorentzVector tv2;
  tv2.SetXYZM(v2.px, v2.py, v2.pz, v2.mass);

  double deltaPhi = M_PI - std::abs(std::abs(tv1.Phi() - tv2.Phi()) - M_PI);
  double deltaEta = std::abs(tv1.Eta() - tv2.Eta());
  double result = std::sqrt(deltaPhi * deltaPhi + deltaEta * deltaEta);
  return result;
}

recoil::recoil(float arg_sqrts) : m_sqrts(arg_sqrts) {};
ROOT::VecOps::RVec<fcc::ParticleData>  recoil::operator() (ROOT::VecOps::RVec<fcc::ParticleData> in) {
  ROOT::VecOps::RVec<fcc::ParticleData> result;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
  for (auto & v1: in) {
    TLorentzVector tv1;
    tv1.SetXYZM(v1.core.p4.px, v1.core.p4.py, v1.core.p4.pz, v1.core.p4.mass);
    recoil_p4 -= tv1;
  }
  auto recoil_fcc = fcc::ParticleData();
  recoil_fcc.core.p4.px = recoil_p4.Px();
  recoil_fcc.core.p4.py = recoil_p4.Py();
  recoil_fcc.core.p4.pz = recoil_p4.Pz();
  recoil_fcc.core.p4.mass = recoil_p4.M();
  result.push_back(recoil_fcc);
  return result;
};

ROOT::VecOps::RVec<float> get_pt_lv(ROOT::VecOps::RVec<fcc::LorentzVector> x){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < x.size(); ++i) {
   result.push_back(sqrt(x[i].px * x[i].px + x[i].py * x[i].py));
 }
 return result;
}

ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<fcc::ParticleData> x){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < x.size(); ++i) {
   result.push_back(sqrt(x[i].core.p4.px * x[i].core.p4.px + x[i].core.p4.py * x[i].core.p4.py));
 }
 return result;
}

ROOT::VecOps::RVec<fcc::ParticleData> mergeParticles(ROOT::VecOps::RVec<fcc::ParticleData> x, ROOT::VecOps::RVec<fcc::ParticleData> y) {
  std::vector<fcc::ParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}

ROOT::VecOps::RVec<float> id_float(ROOT::VecOps::RVec<fcc::FloatValueData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    result.push_back(p.value);
  }
  return result;
}

ROOT::VecOps::RVec<float> id_float_legacy(ROOT::VecOps::RVec<fcc::FloatData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    result.push_back(p.value);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    result.push_back(p.core.p4.mass);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.core.p4.px, p.core.p4.py, p.core.p4.pz, p.core.p4.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.core.p4.px, p.core.p4.py, p.core.p4.pz, p.core.p4.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.core.p4.px, p.core.p4.py, p.core.p4.pz, p.core.p4.mass);
    result.push_back(tlv.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.core.p4.px, p.core.p4.py, p.core.p4.pz, p.core.p4.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: x) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.core.p4.px, p.core.p4.py, p.core.p4.pz, p.core.p4.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

int get_nparticles(ROOT::VecOps::RVec<fcc::ParticleData> x) {
  int result =  x.size();
  return result;
}


int get_njets(ROOT::VecOps::RVec<fcc::JetData> x) {
  int result =  x.size();
  return result;
}

int get_njets2(ROOT::VecOps::RVec<fcc::JetData> x, ROOT::VecOps::RVec<fcc::JetData> y) {
  int result =  x.size() + y.size();
  return result;
}

noMatchJets::noMatchJets(float arg_max_rel_iso) {m_max_rel_iso = arg_max_rel_iso;}

ROOT::VecOps::RVec<fcc::JetData> noMatchJets::operator() (ROOT::VecOps::RVec<fcc::JetData> in, ROOT::VecOps::RVec<fcc::ParticleData> matchParticles) {
  ROOT::VecOps::RVec<fcc::JetData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    bool matched = false;
    for (size_t j = 0; j < matchParticles.size(); ++j) {
      auto & matchCandidate = matchParticles[j];
      if (deltaR(p.core.p4, matchCandidate.core.p4) < m_max_rel_iso) {
        matched = true;
      }
    }
    if (matched == false) {
      result.emplace_back(p);
    }
  }
  return result;
}

selectJets::selectJets(float arg_min_pt, bool arg_btag_must_be_zero) {m_min_pt = arg_min_pt; m_btag_must_be_zero = arg_btag_must_be_zero;}

ROOT::VecOps::RVec<fcc::JetData> selectJets::operator()(ROOT::VecOps::RVec<fcc::JetData> in, ROOT::VecOps::RVec<fcc::TaggedJetData> btags) {
  ROOT::VecOps::RVec<fcc::JetData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.core.p4.px,2) + std::pow(p.core.p4.py,2)) > m_min_pt) {
      if (m_btag_must_be_zero) {
        if (btags[i].tag > 0) {
          result.emplace_back(p);
        }
      } else {
        if (btags[i].tag == 0) {
          result.emplace_back(p);
        }
      }
    }
  }
  return result;
}
selectParticlesPtIso::selectParticlesPtIso(float arg_min_pt, float arg_max_iso) : m_min_pt(arg_min_pt), m_max_iso(arg_max_iso) {};

ROOT::VecOps::RVec<edm4hep::RecoParticleRefData>  selectParticlesPtIso::operator() (ROOT::VecOps::RVec<edm4hep::RecoParticleRefData> in, ROOT::VecOps::RVec<fcc::TaggedParticleData> iso) {
  ROOT::VecOps::RVec<fcc::ParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.core.p4.px,2) + std::pow(p.core.p4.py,2)) > m_min_pt) {
      if (iso[i].tag  < m_max_iso) {
        result.emplace_back(p);
      }
    }
  }
  return result;
}

selectParticlesPt::selectParticlesPt(float arg_min_pt) : m_min_pt(arg_min_pt) {};

ROOT::VecOps::RVec<fcc::ParticleData>  selectParticlesPt::operator() (ROOT::VecOps::RVec<fcc::ParticleData> in) {
  ROOT::VecOps::RVec<fcc::ParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.core.p4.px,2) + std::pow(p.core.p4.py,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}

ResonanceBuilder::ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass) {m_resonance_pdgid = arg_resonance_pdgid; m_resonance_mass = arg_resonance_mass;}

ROOT::VecOps::RVec<fcc::ParticleData> ResonanceBuilder::operator()(ROOT::VecOps::RVec<fcc::ParticleData> legs) {
  ROOT::VecOps::RVec<fcc::ParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      fcc::ParticleData reso;
      reso.core.pdgId = m_resonance_pdgid;
      TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
            reso.core.charge += legs[i].core.charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs[i].core.p4.px, legs[i].core.p4.py, legs[i].core.p4.pz, legs[i].core.p4.mass);
            reso_lv += leg_lv;
          }
      }
      reso.core.p4.px = reso_lv.Px();
      reso.core.p4.py = reso_lv.Py();
      reso.core.p4.pz = reso_lv.Pz();
      reso.core.p4.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (fcc::ParticleData i ,fcc::ParticleData j) { return (abs( m_resonance_mass -i.core.p4.mass)<abs(m_resonance_mass-j.core.p4.mass)); };
    std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<fcc::ParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}


JetResonanceBuilder::JetResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass) {m_resonance_pdgid = arg_resonance_pdgid; m_resonance_mass = arg_resonance_mass;}

ROOT::VecOps::RVec<fcc::ParticleData> JetResonanceBuilder::operator()(ROOT::VecOps::RVec<fcc::JetData> legs) {
  ROOT::VecOps::RVec<fcc::ParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      fcc::ParticleData reso;
      reso.core.pdgId = m_resonance_pdgid;
      TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
            ///reso.core.charge += legs[i].core.charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs[i].core.p4.px, legs[i].core.p4.py, legs[i].core.p4.pz, legs[i].core.p4.mass);
            reso_lv += leg_lv;
          }
      }
      reso.core.p4.px = reso_lv.Px();
      reso.core.p4.py = reso_lv.Py();
      reso.core.p4.pz = reso_lv.Pz();
      reso.core.p4.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (fcc::ParticleData i ,fcc::ParticleData j) { return (abs( m_resonance_mass -i.core.p4.mass)<abs(m_resonance_mass-j.core.p4.mass)); };
    std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<fcc::ParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}


ROOT::VecOps::RVec<fcc::ParticleData> LeptonicZBuilder (ROOT::VecOps::RVec<fcc::ParticleData> leptons) {

        ROOT::VecOps::RVec<fcc::ParticleData> result;
        int n = leptons.size();
        if (n >1) {
          ROOT::VecOps::RVec<bool> v(n);
          std::fill(v.end() - 2, v.end(), true);
          do {
            fcc::ParticleData zed;
            zed.core.pdgId = 23;
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

    return result;
  };

  /// @todo: refactor to remove code duplication with leptonicZBuilder
ROOT::VecOps::RVec<fcc::ParticleData> LeptonicHiggsBuilder(ROOT::VecOps::RVec<fcc::ParticleData> leptons) {
        ROOT::VecOps::RVec<fcc::ParticleData> result;
        int n = leptons.size();
        if (n > 1) {
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

ROOT::VecOps::RVec<fcc::ParticleData> mergeElectronsAndMuons(ROOT::VecOps::RVec<fcc::ParticleData> x, ROOT::VecOps::RVec<fcc::ParticleData> y) {
  std::vector<fcc::ParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
};
