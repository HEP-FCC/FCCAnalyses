#ifndef  VERTEXING_ANALYZERS_H
#define  VERTEXING_ANALYZERS_H

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


/** Vertex interface using Franco Bedeshi's code. 
This represents a set functions and utilities to perfom vertexing from a list of tracks.  
*/

namespace Vertexing{


  /// Selection of particles based on the d0 / z0 significances of the associated track
  struct selTracks {
    selTracks( float arg_d0sig_min, float arg_d0sig_max, float arg_z0sig_min, float arg_z0sig_max)  ;
    float m_d0sig_min = 0;
    float m_d0sig_max = 3;
    float m_z0sig_min = 0;
    float m_z0sig_max = 3;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, 
									 ROOT::VecOps::RVec<edm4hep::TrackState> tracks  ) ;
  };

  /// Selection of primary particles :
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> SelPrimaryTracks( ROOT::VecOps::RVec<int> recind,
									   ROOT::VecOps::RVec<int> mcind, 
									   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
									   ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
									   TVector3 MC_EventPrimaryVertex) ;

  /// Updated vertex (code from Franco Bedeschi), in millimeters
  edm4hep::VertexData  VertexFitter( int Primary,
				     ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
				     ROOT::VecOps::RVec<edm4hep::TrackState> tracks ) ;
  
  /// Return the number of tracks in a given track collection
  int get_nTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
  
  // --- Internal methods needed by the code of  Franco B :  
  TVectorD get_trackParam( edm4hep::TrackState & atrack) ;
  TMatrixDSym get_trackCov( edm4hep::TrackState &  atrack) ;
  
  Double_t FastRv(TVectorD p1, TVectorD p2) ;
  TMatrixDSym RegInv3(TMatrixDSym &Smat0) ;
  TMatrixD Fill_A(TVectorD par, Double_t phi) ;
  TVectorD Fill_a(TVectorD par, Double_t phi) ;
  TVectorD Fill_x0(TVectorD par) ;
  TVectorD Fill_x(TVectorD par, Double_t phi) ;
}
#endif

