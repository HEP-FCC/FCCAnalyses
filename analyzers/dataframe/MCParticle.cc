#include "MCParticle.h"


std::vector<float> getMC_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
 std::vector<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::MCParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y) {
  //to be keept as std::vector
  std::vector<edm4hep::MCParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}


std::vector<float> getMC_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.time);
  }
  return result;
}

std::vector<float> getMC_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.PDG);
  }
  return result;
}

std::vector<float> getMC_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.generatorStatus);
  }
  return result;
}

std::vector<float> getMC_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.simulatorStatus);
  }
  return result;
}

std::vector<edm4hep::Vector3d> getMC_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.vertex);
  }
  return result;
}

std::vector<float> getMC_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.x);
  }
  return result;
}

std::vector<float> getMC_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.y);
  }
  return result;
}

std::vector<float> getMC_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.z);
  }
  return result;
}

std::vector<edm4hep::Vector3d> getMC_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.endpoint);
  }
  return result;
}

std::vector<float> getMC_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.x);
  }
  return result;
}

std::vector<float> getMC_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.y);
  }
  return result;
}

std::vector<float> getMC_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.z);
  }
  return result;
}

std::vector<float> getMC_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

std::vector<float> getMC_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

std::vector<float> getMC_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

std::vector<float> getMC_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.E());
  }
  return result;
}

std::vector<float> getMC_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

std::vector<float> getMC_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}

std::vector<float> getMC_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

std::vector<float> getMC_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

std::vector<float> getMC_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

std::vector<float> getMC_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

std::vector<float> getMC_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

std::vector<TLorentzVector> getMC_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}

int getMC_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> x) {
  int result =  x.size();
  return result;
}

selMC_pT::selMC_pT(float arg_min_pt) : m_min_pt(arg_min_pt) {};

std::vector<edm4hep::MCParticleData>  selMC_pT::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  std::vector<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}

