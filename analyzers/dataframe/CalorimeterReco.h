#ifndef  CALORIMETERRECO_ANALYZERS_H
#define  CALORIMETERRECO_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "datamodel/PositionedCaloHitData.h"

// legacy
#include "datamodel/FloatData.h"


ROOT::VecOps::RVec<float> getCalo_phi (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);
ROOT::VecOps::RVec<float> getCalo_theta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in);


#endif
