#include "FCCAnalyses.h"

#include "TLorentzVector.h"
#include "datamodel/MCParticleData.h"
#include "datamodel/ParticleData.h"
#include "datamodel/Point.h"
#include "datamodel/LorentzVector.h"

std::vector<float> pt (std::vector<fcc::MCParticleData> in){
 std::vector<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
		 result.push_back(std::sqrt(in[i].core.p4.px * in[i].core.p4.px + in[i].core.p4.py * in[i].core.p4.py));
	 }
	 return result;
}

std::vector<float> eta(std::vector<fcc::MCParticleData> in){
 std::vector<float> result;
   TLorentzVector lv;
	 for (size_t i = 0; i < in.size(); ++i) {
     lv.SetXYZM(in[i].core.p4.px, in[i].core.p4.py, in[i].core.p4.pz, in[i].core.p4.mass);
		 result.push_back(lv.Eta());
	 }
	 return result;
}

std::vector<TLorentzVector> tlv(std::vector<fcc::LorentzVector> in){
 std::vector<TLorentzVector> result;
   TLorentzVector lv;
	 for (size_t i = 0; i < in.size(); ++i) {
     lv.SetXYZM(in[i].px, in[i].py, in[i].pz, in[i].mass);
		 result.push_back(lv);
	 }
	 return result;
}

std::vector<float> r (std::vector<fcc::Point> in) {
 std::vector<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
     result.push_back(std::sqrt(in[i].x*in[i].x + in[i].y*in[i].y));
   }
 return result; 
}


std::vector<float> norm (std::vector<fcc::Point> in) {
 std::vector<float> result;
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
  std::vector<fcc::ParticleData>  recoil::operator() (std::vector<fcc::ParticleData> in) {
      std::vector<fcc::ParticleData> result;
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

std::vector<float> get_pt_lv(std::vector<fcc::LorentzVector> in){
 std::vector<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].px * in[i].px + in[i].py * in[i].py));
 }
 return result;
}

std::vector<float> get_pt(std::vector<fcc::ParticleData> in){
 std::vector<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].core.p4.px * in[i].core.p4.px + in[i].core.p4.py * in[i].core.p4.py));
 }
 return result;
}

std::vector<fcc::ParticleData> mergeParticles(std::vector<fcc::ParticleData> x, std::vector<fcc::ParticleData> y) {
  std::vector<fcc::ParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return result;
}

std::vector<float> id_float(std::vector<fcc::FloatValueData> x) {
  std::vector<float> result;
  for (auto & p: x) {
    result.push_back(p.value);
  }
  return result;
}

std::vector<float> get_mass(std::vector<fcc::ParticleData> x) {
  std::vector<float> result;
  for (auto & p: x) {
    result.push_back(p.core.p4.mass);
  }
  return result;
}

int get_nparticles(std::vector<fcc::ParticleData> x) {
  int result =  x.size();
  return result;
}

int get_njets(std::vector<fcc::JetData> x) {
  int result =  x.size();
  return result;
}

int get_njets2(std::vector<fcc::JetData> x, std::vector<fcc::JetData> y) {
  int result =  x.size() + y.size();
  return result;
}

noMatchJets::noMatchJets(float arg_max_rel_iso) {m_max_rel_iso = arg_max_rel_iso;}

std::vector<fcc::JetData> noMatchJets::operator() (std::vector<fcc::JetData> in, std::vector<fcc::ParticleData> matchParticles) {
  std::vector<fcc::JetData> result;
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

std::vector<fcc::JetData> selectJets::operator()(std::vector<fcc::JetData> in, std::vector<fcc::TaggedJetData> btags) {
  std::vector<fcc::JetData> result;
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

std::vector<fcc::ParticleData>  selectParticlesPtIso::operator() (std::vector<fcc::ParticleData> in, std::vector<fcc::TaggedParticleData> iso) {
  std::vector<fcc::ParticleData> result;
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

std::vector<fcc::ParticleData>  selectParticlesPt::operator() (std::vector<fcc::ParticleData> in) {
  std::vector<fcc::ParticleData> result;
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

std::vector<fcc::ParticleData> ResonanceBuilder::operator()(std::vector<fcc::ParticleData> leptons) {
  std::vector<fcc::ParticleData> result;
  int n = leptons.size();
  if (n >2) {
    std::vector<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      fcc::ParticleData zed;
      zed.core.pdgId = m_resonance_pdgid;
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
    auto  higgsresonancesort = [&] (fcc::ParticleData i ,fcc::ParticleData j) { return (abs( m_resonance_mass -i.core.p4.mass)<abs(m_resonance_mass-j.core.p4.mass)); };
    std::sort(result.begin(), result.end(), higgsresonancesort);
    std::vector<fcc::ParticleData>::const_iterator first = result.begin();
    std::vector<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    std::vector<fcc::ParticleData> onlyBestHiggs(first, last);
    return onlyBestHiggs;
  } else {
    return result;
  }
}
