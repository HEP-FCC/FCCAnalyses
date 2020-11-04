#include "ReconstructedParticle2MC.h"

std::vector<float> getRP2MC_p(std::vector<podio::ObjectID> recind, ROOT::VecOps::RVec<podio::ObjectID> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  std::vector<float> result;
  result.reserve(reco.size());

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i).index).momentum.x,mc.at(mcind.at(i).index).momentum.y,mc.at(mcind.at(i).index).momentum.z,mc.at(mcind.at(i).index).mass);
    result[recind.at(i).index]=tlv.P();
  }
  
  return result;
}

std::vector<float> getRP2MC_p_test(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  std::vector<float> result;
  result.reserve(reco.size());

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv.P();
  }
  
  return result;
}


