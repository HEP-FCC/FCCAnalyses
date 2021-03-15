#ifndef  VERTEXFITTERACTS_ANALYZERS_H
#define  VERTEXFITTERACTS_ANALYZERS_H

#include <cmath>
#include <vector>
#include "edm4hep/TrackState.h"
#include "ROOT/RVec.hxx"
#include <TMatrixD.h>
#include <TMatrixDSym.h>
#include "VertexingUtils.h"
#include "edm4hep/ReconstructedParticleData.h"

namespace VertexFitterActs{
  VertexingUtils::FCCAnalysesVertex VertexFitterFullBilloir(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
							    ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
}

#endif
