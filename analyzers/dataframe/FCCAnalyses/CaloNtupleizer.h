
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

/// select layers
struct sel_layers {
public:
  sel_layers(int arg_min=0, int arg_max=10);
  ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> operator()(const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);

private:
  int _min;//> min layer
  int _max;//> max layer
};


// calo hits (single cells)
ROOT::VecOps::RVec<float> getCaloHit_x (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<float> getCaloHit_y (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<float> getCaloHit_z (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<float> getCaloHit_phi (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<int> getCaloHit_phiBin (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<float> getCaloHit_theta (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<float> getCaloHit_eta (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<int> getCaloHit_etaBin (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<int> getCaloHit_layer (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<float> getCaloHit_energy (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);
ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in);

// calo clusters
ROOT::VecOps::RVec<float> getCaloCluster_x (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<float> getCaloCluster_y (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<float> getCaloCluster_z (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<float> getCaloCluster_phi (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<float> getCaloCluster_theta (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<float> getCaloCluster_eta (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<float> getCaloCluster_energy (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<int> getCaloCluster_firstCell (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<int> getCaloCluster_lastCell (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in);
ROOT::VecOps::RVec<std::vector<float>> getCaloCluster_energyInLayers (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in, const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells, const int nLayers=12);

// SimParticleSecondary
ROOT::VecOps::RVec<float> getSimParticleSecondaries_x (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_y (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_z (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_z (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_phi (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_theta (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_eta (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_energy (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);
ROOT::VecOps::RVec<float> getSimParticleSecondaries_PDG (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in);

struct getFloatAt {
  size_t m_pos;
  getFloatAt(size_t pos);
  ROOT::RVecF operator()(const ROOT::VecOps::RVec<std::vector<float>>& in);
};


}//end NS CaloNtupleizer

}//end NS FCCAnalyses
#endif
