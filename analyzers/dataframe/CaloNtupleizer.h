
#ifndef  CALONTUPLEIZER_ANALYZERS_H
#define  CALONTUPLEIZER_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/CalorimeterHitData.h"
#include "edm4hep/ClusterData.h"
//#include "edm4hep/MCParticleData.h"

#include "TVector3.h"
#include "TLorentzVector.h"

namespace CaloNtupleizer{

// calo hits (single cells)
ROOT::VecOps::RVec<float> getCaloHit_x (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_y (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_z (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_eta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_energy (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);

// calo clusters
ROOT::VecOps::RVec<float> getCaloCluster_x (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<float> getCaloCluster_y (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<float> getCaloCluster_z (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<float> getCaloCluster_phi (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<float> getCaloCluster_theta (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<float> getCaloCluster_eta (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<float> getCaloCluster_energy (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<int> getCaloCluster_firstCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in);
ROOT::VecOps::RVec<int> getCaloCluster_lastCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in);

//// mc particle
//ROOT::VecOps::RVec<float> getMC_phi (ROOT::VecOps::RVec<fcc::MCParticleData> in);
//ROOT::VecOps::RVec<float> getMC_theta (ROOT::VecOps::RVec<fcc::MCParticleData> in);
//ROOT::VecOps::RVec<float> getMC_eta (ROOT::VecOps::RVec<fcc::MCParticleData> in);
//ROOT::VecOps::RVec<float> getMC_energy (ROOT::VecOps::RVec<fcc::MCParticleData> in);
//ROOT::VecOps::RVec<TLorentzVector> getMC_lorentzVector (ROOT::VecOps::RVec<fcc::MCParticleData> in);
//ROOT::VecOps::RVec<int> getMC_pid (ROOT::VecOps::RVec<fcc::MCParticleData> in);
//ROOT::VecOps::RVec<int> getMC_status (ROOT::VecOps::RVec<fcc::MCParticleData> in);

}
#endif
