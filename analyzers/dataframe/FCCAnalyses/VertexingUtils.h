#ifndef  VERTEXINGUTILS_ANALYZERS_H
#define  VERTEXINGUTILS_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/TrackState.h"

#include "edm4hep/VertexData.h"
#include "edm4hep/Vertex.h"

#include "TVectorD.h"
#include "TVector3.h"
#include "TMatrixDSym.h"


/** Vertexing utilities
*/
namespace FCCAnalyses{

namespace VertexingUtils{

  /// Structure to keep useful track information that is related to the vertex
  struct FCCAnalysesVertex{
    edm4hep::VertexData vertex;
    int ntracks;
    int mc_ind; ///index in the MC vertex collection if any
    ROOT::VecOps::RVec<int> reco_ind;
    ROOT::VecOps::RVec<float> reco_chi2;
    ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex;
    ROOT::VecOps::RVec< TVectorD >  updated_track_parameters;
    ROOT::VecOps::RVec<float> final_track_phases;
  };

  /// Structure to keep useful track information that is related to the vertex
  struct FCCAnalysesVertexMC{
    TVector3 vertex;
    ROOT::VecOps::RVec<int> mc_ind;
    ROOT::VecOps::RVec<int> mc_indneutral;
    ROOT::VecOps::RVec<int> mother_ind;
    ROOT::VecOps::RVec<int> gmother_ind;
  };

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

  /// Retrieve the number of reconstructed vertices from the collection of vertex object
  int get_Nvertex( ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl );

  /// Retrieve a single FCCAnalyses vertex from the collection of vertex object
  FCCAnalysesVertex get_FCCAnalysesVertex(ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl, int index );

  /// Retrieve the edm4hep::VertexData from the vertex object
  edm4hep::VertexData get_VertexData( FCCAnalysesVertex TheVertex ) ;

  /// Retrieve a vector of edm4hep::VertexData from the collection of vertex object
  ROOT::VecOps::RVec<edm4hep::VertexData> get_VertexData( ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl ) ;

  /// Retrieve a edm4hep::VertexData from the collection of vertex object at a given index
  edm4hep::VertexData get_VertexData( ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl, int index);

  /// Retrieve the number of tracks from FCCAnalysesVertex
  int get_VertexNtrk( FCCAnalysesVertex TheVertex ) ;

   /// Retrieve the tracks indices from FCCAnalysesVertex
  ROOT::VecOps::RVec<int> get_VertexRecoInd( FCCAnalysesVertex TheVertex ) ;

  /// Return the number of tracks in a given track collection
  int get_nTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);


 // --- Internal methods needed by the code of  Franco B :
  TVectorD get_trackParam( edm4hep::TrackState & atrack) ;
  TMatrixDSym get_trackCov( edm4hep::TrackState &  atrack) ;

  TVectorD ParToACTS(TVectorD Par);
  TMatrixDSym CovToACTS(TMatrixDSym Cov,TVectorD Par);

}//end NS VertexingUtils

}//end NS FCCAnalyses
#endif
