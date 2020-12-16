#ifndef  CALORIMETERRECO_ANALYZERS_H
#define  CALORIMETERRECO_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "datamodel/PositionedCaloHitData.h"
#include "datamodel/CaloClusterData.h"
#include "datamodel/MCParticleData.h"

#include "TVector3.h"
#include "TLorentzVector.h"

// legacy
#include "datamodel/FloatData.h"

// calo hits (single cells)
ROOT::VecOps::RVec<float> getCaloHit_x (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_y (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_z (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_eta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_energy (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);

// calo clusters
ROOT::VecOps::RVec<float> getCaloCluster_energy (ROOT::VecOps::RVec<fcc::CaloClusterData> in);
ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (ROOT::VecOps::RVec<fcc::CaloClusterData> in);
ROOT::VecOps::RVec<int> getCaloCluster_firstCell (ROOT::VecOps::RVec<fcc::CaloClusterData> in);
ROOT::VecOps::RVec<int> getCaloCluster_lastCell (ROOT::VecOps::RVec<fcc::CaloClusterData> in);

// mc particle FIXME should be moved to a dedicated MCParticle.cc file but since we will move to edm4hep where this is already done I dont bother...
ROOT::VecOps::RVec<int> getMC_pid (ROOT::VecOps::RVec<fcc::MCParticleData> in);
ROOT::VecOps::RVec<int> getMC_status (ROOT::VecOps::RVec<fcc::MCParticleData> in);
ROOT::VecOps::RVec<TLorentzVector> getMC_lorentzVector (ROOT::VecOps::RVec<fcc::MCParticleData> in);
ROOT::VecOps::RVec<float> getMC_phi (ROOT::VecOps::RVec<fcc::MCParticleData> in);

#endif
