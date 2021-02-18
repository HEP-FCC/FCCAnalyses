#ifndef  VERTEXINGACTS_ANALYZERS_H
#define  VERTEXINGACTS_ANALYZERS_H

#include <cmath>
#include <vector>
#include "edm4hep/TrackState.h"
#include "ROOT/RVec.hxx"
#include <TMatrixD.h>
#include <TMatrixDSym.h>

namespace VertexingACTS{
  TVectorD ParToACTS(TVectorD Par);
  TMatrixDSym CovToACTS(TMatrixDSym Cov,TVectorD Par);
  bool VertexFinder(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
}

#endif
