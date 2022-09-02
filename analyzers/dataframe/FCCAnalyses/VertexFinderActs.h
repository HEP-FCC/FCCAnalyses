#ifndef  VERTEXFINDERACTS_ANALYZERS_H
#define  VERTEXFINDERACTS_ANALYZERS_H

#include <cmath>
#include <vector>
#include "edm4hep/TrackState.h"
#include "ROOT/RVec.hxx"
#include <TMatrixD.h>
#include <TMatrixDSym.h>
#include "VertexingUtils.h"

namespace FCCAnalyses{

namespace VertexFinderActs{

  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> VertexFinderAMVF(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

}//end NS VertexFinderActs

}//end NS FCCAnalyses
#endif
