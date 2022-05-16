
#ifndef  CALONTUPLEIZER_ANALYZERS_H
#define  CALONTUPLEIZER_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/CalorimeterHitData.h"
#include "edm4hep/ClusterData.h"
#include "edm4hep/MCParticleData.h"

#include "TVector3.h"
#include "TLorentzVector.h"

namespace FCCAnalyses{

namespace CaloNtupleizer{

void loadGeometry(std::string xmlGeometryPath, std::string readoutName);

// calo hits (single cells)
ROOT::VecOps::RVec<float> getCaloHit_x (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_y (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_z (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<int> getCaloHit_phiBin (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_eta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<int> getCaloHit_etaBin (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
ROOT::VecOps::RVec<int> getCaloHit_layer (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in);
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

// SimParticleSecondary
ROOT::VecOps::RVec<float> getSimParticleSecondaries_x (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_y (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_z (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_z (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_phi (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_theta (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_eta (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_energy (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_PDG (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);


}//end NS CaloNtupleizer

}//end NS FCCAnalyses
#endif
