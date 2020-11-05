#include "ReconstructedParticle2MC.h"

std::vector<float> getRP2MC_p(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv.P();
  }
  return result;
}

std::vector<TLorentzVector> getRP2MC_tlv(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<TLorentzVector> result;
  result.resize(reco.size(),TLorentzVector());

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv;
  }
  return result;
}

std::vector<float> getRP2MC_px(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).momentum.x;
  }
  return result;
}

std::vector<float> getRP2MC_py(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).momentum.y;
  }
  return result;
}

std::vector<float> getRP2MC_pz(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).momentum.z;
  }
  return result;
}

std::vector<float> getRP2MC_pdg(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).PDG;
  }
  return result;
}

std::vector<float> getRP2MC_charge(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).charge;
  }
  return result;
}

std::vector<float> getRP2MC_mass(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).mass;
  }
  return result;
}

std::vector<int> getRP2MC_index(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<int> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mcind.at(i);
  }
  return result;
}

std::vector<int> getRP2MC_parentid (ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents){
  std::vector<int> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    if (mc.at(mcind.at(i)).parents_begin!=mc.at(mcind.at(i)).parents_end){
      result[recind.at(i)]=parents.at(mc.at(mcind.at(i)).parents_begin);
    }
  }

  /*if (recind.size()>reco.size()){ 
    std::cout << recind.size() <<"========="<<reco.size()<<std::endl;
     for (unsigned int i=0; i<recind.size();i++) {
       TLorentzVector tlv;
       tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
       TLorentzVector tlv2;
       tlv2.SetXYZM(reco.at(recind.at(i)).momentum.x,reco.at(recind.at(i)).momentum.y,reco.at(recind.at(i)).momentum.z,reco.at(recind.at(i)).mass);
       std::cout << "n mc " << mc.size() << " rec ind " << recind.at(i) << " reco P "<< tlv2.P()<< "  mc ind " << mcind.at(i) << " truth P " << tlv.P() << " pdg_id " << mc.at(mcind.at(i)).PDG << " parent_begin " <<  mc.at(mcind.at(i)).parents_begin << " parent_end " <<  mc.at(mcind.at(i)).parents_end << " daut_begin " <<  mc.at(mcind.at(i)).daughters_begin << " daut_end " <<  mc.at(mcind.at(i)).daughters_end << "  parent id " << parents.at(mc.at(mcind.at(i)).parents_begin) << " parent pdg id " << mc.at(parents.at(mc.at(mcind.at(i)).parents_begin)).PDG  <<std::endl;
     }
     }*/
 return result;
}


std::vector<float>  getRP2MC_p_func::operator() (ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  std::vector<float> result;
  result.resize(reco.size(),-1.);

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv.P();
  }

  if (recind.size()>reco.size()){ 
    std::cout << recind.size() <<"========="<<reco.size()<<std::endl;
     for (unsigned int i=0; i<recind.size();i++) {
       TLorentzVector tlv;
       tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
       TLorentzVector tlv2;
       tlv2.SetXYZM(reco.at(recind.at(i)).momentum.x,reco.at(recind.at(i)).momentum.y,reco.at(recind.at(i)).momentum.z,reco.at(recind.at(i)).mass);
       std::cout << "n mc " << mc.size() << " rec ind " << recind.at(i) << " reco P "<< tlv2.P()<< "  mc ind " << mcind.at(i) << " truth P " << tlv.P() << " pdg_id " << mc.at(mcind.at(i)).PDG << " parent_begin " <<  mc.at(mcind.at(i)).parents_begin << " parent_end " <<  mc.at(mcind.at(i)).parents_end << " daut_begin " <<  mc.at(mcind.at(i)).daughters_begin << " daut_end " <<  mc.at(mcind.at(i)).daughters_end <<std::endl;
     }
  }
  return result;
}
