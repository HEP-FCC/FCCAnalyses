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

#include "ReconstructedParticle2Track.h"
#include "ReconstructedParticle2MC.h"

#include "edm4hep/VertexData.h"
#include "edm4hep/Vertex.h"



int get_nTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);


// -- Selection of particles based on the d0 / z0 significances of the associated track

struct selTracks {
  selTracks( float arg_d0sig_min, float arg_d0sig_max, float arg_z0sig_min, float arg_z0sig_max)  ;
  float m_d0sig_min = 0;
  float m_d0sig_max = 3;
  float m_z0sig_min = 0;
  float m_z0sig_max = 3;
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, 
									ROOT::VecOps::RVec<edm4hep::TrackState> tracks  ) ;

};


// Selection of primary particles :
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> SelPrimaryTracks( ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, 
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);



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
TVector3 Vertex0FB( ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;


// Updated vertex 
edm4hep::VertexData  VertexFB( int Primary, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
					ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;



#endif

