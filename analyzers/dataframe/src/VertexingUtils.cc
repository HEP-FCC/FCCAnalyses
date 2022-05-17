#include "FCCAnalyses/VertexingUtils.h"

namespace FCCAnalyses{

namespace VertexingUtils{

//
// Selection of particles based on the d0 / z0 significances of the associated track
//
selTracks::selTracks( float arg_d0sig_min, float arg_d0sig_max, float arg_z0sig_min, float arg_z0sig_max) : m_d0sig_min(arg_d0sig_min),
													    m_d0sig_max( arg_d0sig_max ),
													    m_z0sig_min( arg_z0sig_min ),
													    m_z0sig_max (arg_z0sig_max) { };
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
selTracks::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
				       ROOT::VecOps::RVec<edm4hep::TrackState> tracks  ) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  result;
  result.reserve(recop.size());

  for (size_t i = 0; i < recop.size(); ++i) {
    auto & p = recop[i];
    if (p.tracks_begin<tracks.size()) {
      auto & tr = tracks.at( p.tracks_begin );
      double d0sig = fabs( tr.D0 / sqrt( tr.covMatrix[0]) ) ;
      if ( fabs( d0sig ) > m_d0sig_max || fabs( d0sig ) < m_d0sig_min  ) continue;
      //double z0sig = fabs( tr.Z0 / sqrt( tr.covMatrix[12]) );
      double z0sig = fabs( tr.Z0 / sqrt( tr.covMatrix[9])  );	// covMat = lower-triangle
      if ( fabs( z0sig ) > m_z0sig_max || fabs( z0sig ) < m_z0sig_min  ) continue;
      result.emplace_back(p);
    }
  }
  return result;
}


//
// Selection of primary particles based on the matching of RecoParticles
// to MC particles
//
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
SelPrimaryTracks (ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind,
				  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
				  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
				  TVector3 MC_EventPrimaryVertex) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(reco.size());

  // Event primary vertex:
  double xvtx0 = MC_EventPrimaryVertex[0];
  double yvtx0 = MC_EventPrimaryVertex[1];
  double zvtx0 = MC_EventPrimaryVertex[2];

  for (unsigned int i=0; i<recind.size();i++) {
    double xvtx = mc.at(mcind.at(i)).vertex.x ;
    double yvtx = mc.at(mcind.at(i)).vertex.y ;
    double zvtx = mc.at(mcind.at(i)).vertex.z ;
    // primary particle ?
     double zero = 1e-12;
    if ( fabs( xvtx - xvtx0) < zero && fabs( yvtx - yvtx0) < zero && fabs( zvtx -zvtx0) < zero ) {
        int reco_idx = recind.at(i);
        result.push_back( reco.at( reco_idx )  );
    }

  }
  return result;
}


int
get_nTracks( ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  int nt = tracks.size();
  return nt;
}


TVectorD
get_trackParam( edm4hep::TrackState & atrack) {
    double d0 =atrack.D0 ;
    double phi0 = atrack.phi ;
    double omega = atrack.omega ;
    double z0 = atrack.Z0 ;
    double tanlambda = atrack.tanLambda ;
    TVectorD res(5);

    double scale0 = 1e-3;   //convert mm to m
    double scale1 = 1;
    double scale2 = 0.5*1e3;  // C = rho/2, convert from mm-1 to m-1
    double scale3 = 1e-3 ;  //convert mm to m
    double scale4 = 1.;

  scale2 = -scale2 ;   // sign of omega

    res[0] = d0 * scale0;
    res[1] = phi0 * scale1 ;
    res[2] = omega * scale2 ;
    res[3] = z0 * scale3 ;
    res[4] = tanlambda * scale4 ;
    return res;
}

TMatrixDSym
get_trackCov( edm4hep::TrackState &  atrack) {
  std::array<float, 15> covMatrix = atrack.covMatrix;
  TMatrixDSym covM(5);

  double scale0 = 1e-3;
  double scale1 = 1.;
  double scale2 = 0.5*1e3;
  double scale3 = 1e-3 ;
  double scale4 = 1.;

  scale2 = -scale2 ;   // sign of omega

  // covMatrix = lower-triang;e

  covM[0][0] = covMatrix[0] *scale0 * scale0;

  covM[1][0] = covMatrix[1] *scale1 * scale0;
  covM[1][1] = covMatrix[2] *scale1 * scale1;

  covM[0][1] = covM[1][0];

  covM[2][0] = covMatrix[3] *scale2 * scale0;
  covM[2][1] = covMatrix[4] *scale2 * scale1;
  covM[2][2] = covMatrix[5] *scale2 * scale2;

  covM[0][2] = covM[2][0];
  covM[1][2] = covM[2][1];

  covM[3][0] = covMatrix[6] *scale3 * scale0;
  covM[3][1] = covMatrix[7] *scale3 * scale1;
  covM[3][2] = covMatrix[8] *scale3 * scale2;
  covM[3][3] = covMatrix[9] *scale3 * scale3;

  covM[0][3] = covM[3][0];
  covM[1][3] = covM[3][1];
  covM[2][3] = covM[3][2];

  covM[4][0] = covMatrix[10] *scale4 * scale0;
  covM[4][1] = covMatrix[11] *scale4 * scale1;
  covM[4][2] = covMatrix[12] *scale4 * scale2;
  covM[4][3] = covMatrix[13] *scale4 * scale3;
  covM[4][4] = covMatrix[14] *scale4 * scale4;

  covM[0][4] = covM[4][0];
  covM[1][4] = covM[4][1];
  covM[2][4] = covM[4][2];
  covM[3][4] = covM[4][3];

  return covM;
}


FCCAnalysesVertex
get_FCCAnalysesVertex(ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl, int index ){
  FCCAnalysesVertex result;
  if (index<TheVertexColl.size())result=TheVertexColl.at(index);
  return result;
}


int
get_Nvertex( ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl ){
  return TheVertexColl.size();
}


edm4hep::VertexData get_VertexData( FCCAnalysesVertex TheVertex ) {
  return TheVertex.vertex ;
}

ROOT::VecOps::RVec<edm4hep::VertexData> get_VertexData( ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl ) {
  ROOT::VecOps::RVec<edm4hep::VertexData> result;
  for (unsigned int i=0; i<TheVertexColl.size();i++) {
    result.push_back(TheVertexColl.at(i).vertex);
  }
  return result;
}

edm4hep::VertexData get_VertexData( ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl, int index) {
  edm4hep::VertexData result;
  if (index<TheVertexColl.size())result=TheVertexColl.at(index).vertex;
  return result;
}


int get_VertexNtrk( FCCAnalysesVertex TheVertex ) {
  return TheVertex.ntracks;
}

ROOT::VecOps::RVec<int> get_VertexRecoInd( FCCAnalysesVertex TheVertex ) {
  return TheVertex.reco_ind;
}

TVectorD ParToACTS(TVectorD Par){

  TVectorD pACTS(6);	// Return vector
  //
  double fB=2.;
  Double_t b = -0.29988*fB / 2.;
  pACTS(0) = 1000*Par(0);		// D from m to mm
  pACTS(1) = 1000 * Par(3);	// z0 from m to mm
  pACTS(2) = Par(1);			// Phi0 is unchanged
  pACTS(3) = TMath::ATan2(1.0,Par(4));		// Theta in [0, pi] range
  pACTS(4) = Par(2) / (b*TMath::Sqrt(1 + Par(4)*Par(4)));		// q/p in GeV
  pACTS(5) = 0.0;				// Time: currently undefined
  //
  return pACTS;
}


// Covariance conversion to ACTS format
TMatrixDSym CovToACTS(TMatrixDSym Cov, TVectorD Par){

  double fB=2.;
  TMatrixDSym cACTS(6); cACTS.Zero();
  Double_t b = -0.29988*fB / 2.;
  //
  // Fill derivative matrix
  TMatrixD A(5, 5);	A.Zero();
  Double_t ct = Par(4);	// cot(theta)
  Double_t C = Par(2);		// half curvature
  A(0, 0) = 1000.;		// D-D	conversion to mm
  A(1, 2) = 1.0;		// phi0-phi0
  A(2, 4) = 1.0/(TMath::Sqrt(1.0 + ct*ct) * b);	// q/p-C
  A(3, 1) = 1000.;		// z0-z0 conversion to mm
  A(4, 3) = -1.0 / (1.0 + ct*ct); // theta - cot(theta)
  A(4, 4) = -C*ct / (b*pow(1.0 + ct*ct,3.0/2.0)); // q/p-cot(theta)
  //
  TMatrixDSym Cv = Cov;
  TMatrixD At(5, 5);
  At.Transpose(A);
  Cv.Similarity(At);
  TMatrixDSub(cACTS, 0, 4, 0, 4) = Cv;
  cACTS(5, 5) = 0.1;	// Currently undefined: set to arbitrary value to avoid crashes
  //
  return cACTS;
}

}//end NS VertexingUtils

}//end NS FCCAnalyses
