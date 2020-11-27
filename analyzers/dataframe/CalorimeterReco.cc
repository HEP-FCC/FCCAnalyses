#include "CalorimeterReco.h"
#include "TVector3.h"

ROOT::VecOps::RVec<float> getCalo_phi (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TVector3 t3;
    t3.SetXYZ(p.position.x,p.position.y,p.position.z);
    result.push_back(t3.Phi());
  }
  return result;

}

ROOT::VecOps::RVec<float> getCalo_theta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TVector3 t3;
    t3.SetXYZ(p.position.x,p.position.y,p.position.z);
    result.push_back(t3.Theta());
  }
  return result;

}
