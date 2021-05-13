#ifndef  VERTEXFITTERSIMPLE_ANALYZERS_H
#define  VERTEXFITTERSIMPLE_ANALYZERS_H

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

#include "ReconstructedParticle2Track.h"
#include "ReconstructedParticle2MC.h"
#include "VertexingUtils.h"

#include "edm4hep/VertexData.h"
#include "edm4hep/Vertex.h"


/** Vertex interface using Franco Bedeshi's code. 
This represents a set functions and utilities to perfom vertexing from a list of tracks.  
*/

namespace VertexFitterSimple{

  /// Vertex (code from Franco Bedeschi): passing the recoparticles. Units for the beamspot constraint: mum
  VertexingUtils::FCCAnalysesVertex  VertexFitter( int Primary, 
						   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
						   ROOT::VecOps::RVec<edm4hep::TrackState> alltracks,
						   bool BeamSpotConstraint = false,
						   double sigmax=0., double sigmay=0., double sigmaz=0.,
                                                   double bsc_x=0., double bsc_y=0., double bsc_z=0. )  ;


  /// Vertex (code from Franco Bedeschi): passing the tracks. Units for the beamspot constraint: mum
  VertexingUtils::FCCAnalysesVertex  VertexFitter_Tk( int Primary, ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
						      bool BeamSpotConstraint = false,		
						      double sigmax=0., double sigmay=0., double sigmaz=0., 
                                                      double bsc_x=0., double bsc_y=0., double bsc_z=0. )  ;

  
  Double_t FastRv(TVectorD p1, TVectorD p2) ;
  TMatrixDSym RegInv3(TMatrixDSym &Smat0) ;
  TMatrixD Fill_A(TVectorD par, Double_t phi) ;
  TVectorD Fill_a(TVectorD par, Double_t phi) ;
  TVectorD Fill_x0(TVectorD par) ;
  TVectorD Fill_x(TVectorD par, Double_t phi) ;

  TVectorD XPtoPar(TVector3 x, TVector3 p, Double_t Q);
  TVector3 ParToP(TVectorD Par);
}
#endif

