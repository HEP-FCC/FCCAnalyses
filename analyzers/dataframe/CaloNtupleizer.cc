#include "CaloNtupleizer.h"
#include "TVector3.h"
#include "TLorentzVector.h"

#include <math.h>

using namespace CaloNtupleizer;

// calo hit
ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_x (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_y (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_z (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_phi (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_theta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_eta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_energy (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> CaloNtupleizer::getCaloHit_positionVector3 (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

// calo cluster
ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_x (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_y (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_z (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_phi (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_theta (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_eta (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_energy (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> CaloNtupleizer::getCaloCluster_positionVector3 (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

ROOT::VecOps::RVec<int> CaloNtupleizer::getCaloCluster_firstCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_begin);
  }
  return result;
}

ROOT::VecOps::RVec<int> CaloNtupleizer::getCaloCluster_lastCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_end);
  }
  return result;
}
