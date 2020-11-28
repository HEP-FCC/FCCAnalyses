#ifndef  CALORIMETERRECO_ANALYZERS_H
#define  CALORIMETERRECO_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "datamodel/PositionedCaloHitData.h"
#include "datamodel/CaloClusterData.h"

#include "TVector3.h"

// legacy
#include "datamodel/FloatData.h"

// calo hits (single cells)
ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCaloHit_energy (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<TVector3> getCaloHit_vector (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);

// calo clusters
ROOT::VecOps::RVec<float> getCaloCluster_energy (ROOT::VecOps::RVec<fcc::CaloClusterData> in);


#endif
