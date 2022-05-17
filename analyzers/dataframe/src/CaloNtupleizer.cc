#include "FCCAnalyses/CaloNtupleizer.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include "edm4hep/MCParticleData.h"

#include <math.h>

#include "DD4hep/Detector.h"

namespace FCCAnalyses{

namespace CaloNtupleizer{

dd4hep::DDSegmentation::BitFieldCoder* m_decoder;

void loadGeometry(std::string xmlGeometryPath, std::string readoutName){
  dd4hep::Detector* dd4hepgeo = &(dd4hep::Detector::getInstance());
  dd4hepgeo->fromCompact(xmlGeometryPath);
  dd4hepgeo->volumeManager();
  dd4hepgeo->apply("DD4hepVolumeManager", 0, 0);
  m_decoder = dd4hepgeo->readout(readoutName).idSpec().decoder();
}


// calo hit
ROOT::VecOps::RVec<float> getCaloHit_x (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_y (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_z (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloHit_phiBin (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    dd4hep::DDSegmentation::CellID cellId = p.cellID;
    result.push_back(m_decoder->get(cellId, "phi"));
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_eta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloHit_etaBin (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    dd4hep::DDSegmentation::CellID cellId = p.cellID;
    result.push_back(m_decoder->get(cellId, "eta"));
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_energy (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloHit_layer (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    dd4hep::DDSegmentation::CellID cellId = p.cellID;
    result.push_back(m_decoder->get(cellId, "layer"));
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

// calo cluster
ROOT::VecOps::RVec<float> getCaloCluster_x (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_y (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_z (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_phi (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_theta (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_eta (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_energy (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_firstCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_begin);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_lastCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_end);
  }
  return result;
}

ROOT::VecOps::RVec<float> getSimParticleSecondaries_x (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.vertex.x);
  }
  return result;
}


ROOT::VecOps::RVec<float> getSimParticleSecondaries_y (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
for (auto & p: in) {
  result.push_back(p.vertex.y);
}
return result;
}


ROOT::VecOps::RVec<float> getSimParticleSecondaries_z (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
for (auto & p: in) {
  result.push_back(p.vertex.z);
}
return result;
}


  ROOT::VecOps::RVec<float> getSimParticleSecondaries_PDG (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in) {
      result.push_back(p.PDG);
    }
    return result;
  }

ROOT::VecOps::RVec<float> getSimParticleSecondaries_phi (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}


ROOT::VecOps::RVec<float> getSimParticleSecondaries_theta (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getSimParticleSecondaries_eta (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getSimParticleSecondaries_energy (ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.E());
  }
  return result;
}

}//end NS CaloNtupleizer

}//end NS FCCAnalyses
