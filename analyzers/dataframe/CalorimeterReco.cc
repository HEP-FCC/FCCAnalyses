#include "CalorimeterReco.h"
#include "TVector3.h"

// calo hit
ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_energy (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

// calo cluster
ROOT::VecOps::RVec<float> getCaloCluster_energy (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.core.position.x, p.core.position.y, p.core.position.z);
    result.push_back(t3);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_firstCell (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_begin);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_lastCell (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_end);
  }
  return result;
}
