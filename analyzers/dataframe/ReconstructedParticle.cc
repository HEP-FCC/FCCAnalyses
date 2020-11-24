#include "ReconstructedParticle.h"


//TOBEMOVED LATER
ResonanceBuilder::ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass) {m_resonance_pdgid = arg_resonance_pdgid; m_resonance_mass = arg_resonance_mass;}

std::vector<edm4hep::ReconstructedParticleData> ResonanceBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {
  std::vector<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      //reso.pdg = m_resonance_pdgid;
      TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
    std::sort(result.begin(), result.end(), resonancesort);
    std::vector<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    std::vector<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    std::vector<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}



recoil::recoil(float arg_sqrts) : m_sqrts(arg_sqrts) {};
std::vector<edm4hep::ReconstructedParticleData>  recoil::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<edm4hep::ReconstructedParticleData> result;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
  for (auto & v1: in) {
    TLorentzVector tv1;
    tv1.SetXYZM(v1.momentum.x, v1.momentum.y, v1.momentum.z, v1.mass);
    recoil_p4 -= tv1;
  }
  auto recoil_fcc = edm4hep::ReconstructedParticleData();
  recoil_fcc.momentum.x = recoil_p4.Px();
  recoil_fcc.momentum.y = recoil_p4.Py();
  recoil_fcc.momentum.z = recoil_p4.Pz();
  recoil_fcc.mass = recoil_p4.M();
  result.push_back(recoil_fcc);
  return result;
};

std::vector<float> getRP_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
 std::vector<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y) {
  //to be keept as std::vector
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}

std::vector<edm4hep::ReconstructedParticleData> getRP(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  std::vector<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < index.size(); ++i) {
    result.push_back(in.at(index[i]));
  }  
  return result;
}


std::vector<float> getRP_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

std::vector<float> getRP_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

std::vector<float> getRP_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

std::vector<float> getRP_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.energy);
  }
  return result;
}

std::vector<float> getRP_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

std::vector<float> getRP_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}


std::vector<float> getRP_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

std::vector<float> getRP_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

std::vector<float> getRP_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

std::vector<float> getRP_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

std::vector<float> getRP_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

std::vector<TLorentzVector> getRP_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}


int getRP_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x) {
  int result =  x.size();
  return result;
}

selRP_pT::selRP_pT(float arg_min_pt) : m_min_pt(arg_min_pt) {};

std::vector<edm4hep::ReconstructedParticleData>  selRP_pT::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}

