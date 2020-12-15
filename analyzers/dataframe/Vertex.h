#ifndef  VERTEX_ANALYZERS_H
#define  VERTEX_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackState.h"

#include "TVectorD.h"
#include "TVector3.h"
#include "TMatrixDSym.h"
#include "TMath.h"
#include "TDecompChol.h"
#include "TMatrixD.h"


int get_nTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);


// --- Internal methods needed by the code of  Franco B :

TMatrixDSym SymRegInv(TMatrixDSym &Smat) ;
TVectorD get_trackParam( edm4hep::TrackState & atrack) ;
TMatrixDSym get_trackCov( edm4hep::TrackState &  atrack) ;

TVectorD Fillf(TVectorD par, TVectorD xin) ;
TMatrixD FillD(TVectorD par, TVectorD xin) ;
TMatrixD FillB(TVectorD par, TVectorD xin) ;


// Preliminary estimate of the vertex position
// based on transformation of track into points
// and vertices into lines
// No steering of track parameters
// No error calculation
  TVector3 Vertex0( ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;


// Updated vertex 
// Returns:  (  x_vtx, y_vtx, z_vtx,  error on x_vtx, error on y_vtx, error on z_vtx,  chi2 )
std::array<float, 7> Vertex( ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;



#endif

