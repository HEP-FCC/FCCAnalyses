#include "ReconstructedParticle.h"


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

