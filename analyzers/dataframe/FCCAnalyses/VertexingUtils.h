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

#include "TLorentzVector.h"
#include "TVectorD.h"
#include "TVector3.h"
#include "TMatrixDSym.h"

#include "fastjet/JetDefinition.hh"


/** Vertexing utilities
*/
namespace FCCAnalyses{

namespace VertexingUtils{

  /// from delphes: returns track state parameters (delphes convention) for a given vertex (x), momentum (p) and charge
  TVectorD XPtoPar(TVector3 x, TVector3 p, Double_t Q);

  /// from delphes: returns the momentum corresponding to a given track state
  TVector3 ParToP(TVectorD Par);


  /// Structure to keep useful track information that is related to the vertex
  struct FCCAnalysesVertex{
    edm4hep::VertexData vertex;
    int ntracks;
    int mc_ind; ///index in the MC vertex collection if any
    ROOT::VecOps::RVec<int> reco_ind;      // indices of the tracks fitted to that vertex, in the collection of all tracks
    ROOT::VecOps::RVec<float> reco_chi2;
    ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex;
    ROOT::VecOps::RVec< TVectorD >  updated_track_parameters;
    ROOT::VecOps::RVec<float> final_track_phases;
  };

  /// Structure to keep useful information that is related to the V0
  struct FCCAnalysesV0{
    ROOT::VecOps::RVec<FCCAnalysesVertex> vtx; // vertex object
    ROOT::VecOps::RVec<int> pdgAbs;            // pdg ID from reconstructions
    ROOT::VecOps::RVec<double> invM;           // invariant mass
    ROOT::VecOps::RVec<int> nSV_jet;           // no of V0s per jet
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

  ROOT::VecOps::RVec<int> get_VertexNtrk( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices ) ;
  
   /// Retrieve the tracks indices from FCCAnalysesVertex
  ROOT::VecOps::RVec<int> get_VertexRecoInd( FCCAnalysesVertex TheVertex ) ;

  /// Retrieve the indices of the tracks fitted to that vertex, but now in the collection of RecoParticles
  ROOT::VecOps::RVec<int> get_VertexRecoParticlesInd( FCCAnalysesVertex TheVertex, 
						      const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& reco );
 
  /// Return the number of tracks in a given track collection
  int get_nTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

  /// compare two track states
  bool compare_Tracks( const edm4hep::TrackState& tr1, const edm4hep::TrackState& tr2 ) ;

  ///////////////////////////////////////////////////
  /// functions used for SV reconstruction

  /** returns a vector of all vertices (PV and SVs), e.g to use in myUtils::get_Vertex_d2PV
   *  first entry: PV, all subsequent entries: SVs
   */
  ROOT::VecOps::RVec<FCCAnalysesVertex> get_all_vertices( FCCAnalysesVertex PV,
							  ROOT::VecOps::RVec<FCCAnalysesVertex> SV ); 

  ROOT::VecOps::RVec<FCCAnalysesVertex> get_all_vertices( FCCAnalysesVertex PV,
							  ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> SV ); 

  /** returns the invariant mass of a two-track vertex
   *  CAUTION: m1 -> mass of first track, m2 -> mass of second track
   *  by default both pions
   */
  double get_invM_pairs( FCCAnalysesVertex vertex,
			 double m1 = 0.13957039,
			 double m2 = 0.13957039) ;

  ROOT::VecOps::RVec<double> get_invM_pairs( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					     double m1 = 0.13957039,
					     double m2 = 0.13957039 ) ;  

  /** returns the invariant mass of a vertex
   *  assuming all tracks to be pions
   */
  double get_invM( FCCAnalysesVertex vertex ) ;

  /** returns the invariant mass of a vector of vertices
   *  assuming all tracks to be pions
   */
  ROOT::VecOps::RVec<double> get_invM( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices ) ;

  /** returns the cos of the angle b/n V0 candidate's (or any vtx's) momentum & PV to V0 (vtx) displacement vector */
  double get_PV2V0angle( FCCAnalysesVertex V0,
			 FCCAnalysesVertex PV) ;

  /** returns cos of the angle b/n track (that form the vtx) momentum sum & PV to vtx displacement vector */
  double get_PV2vtx_angle( ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
			   FCCAnalysesVertex vtx,
			   FCCAnalysesVertex PV ) ;

  /** returns a track's energy
   *  assuming the track to be a pion
   */
  double get_trackE( edm4hep::TrackState track ) ;

  ///////////////////////////////////////////////////
  /// V0 Reconstruction
  /// Return the number of reconstructed V0s
  int get_n_SV( FCCAnalysesV0 SV );

  /// Return the vertex position of all reconstructed V0s (in mm)
  ROOT::VecOps::RVec<TVector3> get_position_SV( FCCAnalysesV0 SV );

  /// Return the PDG IDs of all reconstructed V0s
  ROOT::VecOps::RVec<int> get_pdg_V0( FCCAnalysesV0 V0 );

  /// Return the invariant masses of all reconstructed V0s
  ROOT::VecOps::RVec<double> get_invM_V0( FCCAnalysesV0 V0 );

  /// Return the momentum of all reconstructed V0s
  ROOT::VecOps::RVec<TVector3> get_p_SV( FCCAnalysesV0 SV );

  /// Return chi2 of all reconstructed V0s
  ROOT::VecOps::RVec<double> get_chi2_SV( FCCAnalysesV0 SV );

  ///////////////////////////////////////////////////

  /// Passing a vector of FCCAnalysesVertex instead of FCCAnalysesV0
  /// Return the number of reconstructed SVs
  int get_n_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return the momentum of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<TVector3> get_p_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return the vertex position of all reconstructed SVs (in mm)
  ROOT::VecOps::RVec<TVector3> get_position_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return the momentum magnitude of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<double> get_pMag_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return chi2 of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<double> get_chi2_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return normalised chi2 of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<double> get_norm_chi2_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return no of DOF of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<int> get_nDOF_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return polar angle (theta) of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<double> get_theta_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return azimuthal angle (phi) of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<double> get_phi_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices );

  /// Return polar angle (theta) of all reconstructed vertices wrt jets (or V0.vtx)
  ROOT::VecOps::RVec<double> get_relTheta_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					      ROOT::VecOps::RVec<int> nSV_jet,
					      ROOT::VecOps::RVec<fastjet::PseudoJet> jets );

  /// Return azimuthal angle (phi) of all reconstructed vertices wrt jets (or V0.vtx)
  ROOT::VecOps::RVec<double> get_relPhi_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					    ROOT::VecOps::RVec<int> nSV_jet,
					    ROOT::VecOps::RVec<fastjet::PseudoJet> jets );
  
  /// Return the pointing angle of all reconstructed vertices (or V0.vtx)
  ROOT::VecOps::RVec<double> get_pointingangle_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
						   FCCAnalysesVertex PV );

  /// Return the distances of all reconstructed vertices from PV in xy plane [mm] (or V0.vtx)
  ROOT::VecOps::RVec<double> get_dxy_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					 FCCAnalysesVertex PV );

  /// Return the distances of all reconstructed vertices from PV in 3D [mm] (or V0.vtx)
  ROOT::VecOps::RVec<double> get_d3d_SV( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					 FCCAnalysesVertex PV );

  /// Return the distances of all reconstructed verteces from given TVector3d object in 3D [mm] (or V0.vtx)
  ROOT::VecOps::RVec<double> get_d3d_SV_obj( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					     TVector3 location );

  /// Return the distances of all reconstructed verteces from given edm4hep::Vector3d object in 3D [mm] (or V0.vtx)
  ROOT::VecOps::RVec<double> get_d3d_SV_obj( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					     edm4hep::Vector3d location );

  /// Return the distance in R of all reconstructed verteces from given TVector3d object in 3D [mm] (or V0.vtx)
  ROOT::VecOps::RVec<double> get_dR_SV_obj( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					    TVector3 location );

  /// Return the distances in R of all reconstructed verteces from given edm4hep::Vector3d object in 3D [mm] (or V0.vtx)
  ROOT::VecOps::RVec<double> get_dR_SV_obj( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
					    edm4hep::Vector3d location );

  ///////////////////////////////////////////////////

  /// For get_SV_jets ///
  
  /// Return the number of reconstructed SVs
  ROOT::VecOps::RVec<FCCAnalysesVertex> get_all_SVs( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );

  /// Return the total number of reconstructed SVs
  int get_n_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );

  /// Return the number of reconstructed SVs per jet
  ROOT::VecOps::RVec<int> get_n_SV_jets( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );

  /// Return the tracks separated by jets
  std::vector<std::vector<edm4hep::TrackState>> get_tracksInJets( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
								  ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
								  ROOT::VecOps::RVec<fastjet::PseudoJet> jets,
								  std::vector<std::vector<int>> jet_consti );

  /// Return V0s separated by jets
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> get_svInJets( ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
									  ROOT::VecOps::RVec<int> nSV_jet );

  // --- for get_SV_jets --- //
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_invM( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>> get_p_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_pMag_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> get_VertexNtrk( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_chi2_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_norm_chi2_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> get_nDOF_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_theta_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_phi_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_relTheta_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices, ROOT::VecOps::RVec<fastjet::PseudoJet> jets );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_relPhi_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices, ROOT::VecOps::RVec<fastjet::PseudoJet> jets );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_pointingangle_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices, FCCAnalysesVertex PV );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_dxy_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices, FCCAnalysesVertex PV );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_d3d_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices, FCCAnalysesVertex PV );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> get_pdg_V0( ROOT::VecOps::RVec<int> pdg, ROOT::VecOps::RVec<int> nSV_jet );
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_invM_V0( ROOT::VecOps::RVec<double> invM, ROOT::VecOps::RVec<int> nSV_jet );
  /// Return the vertex position of all reconstructed SVs (in mm)
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>> get_position_SV( ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices ); 
  // --- for get_SV_jets --- //

  float get_trackMom( edm4hep::TrackState & atrack );


// --- Conversion methods between the Delphes and edm4hep conventions

/// convert track parameters, from edm4hep to delphes conventions 
  TVectorD Edm4hep2Delphes_TrackParam( const TVectorD& param, bool Units_mm );
/// convert track parameters, from delphes to edm4hep conventions
  TVectorD Delphes2Edm4hep_TrackParam( const TVectorD& param, bool Units_mm );
/// convert track covariance matrix, from edm4hep to delphes conventions
  TMatrixDSym  Edm4hep2Delphes_TrackCovMatrix( const std::array<float, 21>&  covMatrix, bool Units_mm );
/// convert track covariance matrix, from delphes to edm4hep conventions
  std::array<float, 21> Delphes2Edm4hep_TrackCovMatrix( const TMatrixDSym& cov, bool Units_mm ) ;


 /// --- Internal methods needed by the code of  Franco B:
  TVectorD get_trackParam( edm4hep::TrackState & atrack, bool Units_mm = false) ;
  TMatrixDSym get_trackCov( edm4hep::TrackState &  atrack, bool Units_mm = false) ;

  TVectorD ParToACTS(TVectorD Par);
  TMatrixDSym CovToACTS(TMatrixDSym Cov,TVectorD Par);



}//end NS VertexingUtils

}//end NS FCCAnalyses
#endif
