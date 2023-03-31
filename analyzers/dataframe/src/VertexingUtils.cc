#include "FCCAnalyses/VertexingUtils.h"
#include "FCCAnalyses/VertexFitterSimple.h"

#include "TrkUtil.h" // from delphes

namespace FCCAnalyses {

namespace VertexingUtils {

TVector3 ParToP(TVectorD Par) {
  double fB = 2; // 2 Tesla
  TrkUtil tu;
  return tu.ParToP(Par, fB);
}

TVectorD XPtoPar(TVector3 x, TVector3 p, Double_t Q) {
  double fB = 2; // 2 Tesla
  TrkUtil tu;
  return tu.XPtoPar(x, p, Q, fB);
}

//
// Selection of particles based on the d0 / z0 significances of the associated
// track
//
selTracks::selTracks(float arg_d0sig_min, float arg_d0sig_max,
                     float arg_z0sig_min, float arg_z0sig_max)
    : m_d0sig_min(arg_d0sig_min), m_d0sig_max(arg_d0sig_max),
      m_z0sig_min(arg_z0sig_min), m_z0sig_max(arg_z0sig_max){};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> selTracks::operator()(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
    ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(recop.size());

  for (size_t i = 0; i < recop.size(); ++i) {
    auto &p = recop[i];
    if (p.tracks_begin < tracks.size()) {
      auto &tr = tracks.at(p.tracks_begin);
      double d0sig = fabs(tr.D0 / sqrt(tr.covMatrix[0]));
      if (fabs(d0sig) > m_d0sig_max || fabs(d0sig) < m_d0sig_min)
        continue;
      // double z0sig = fabs( tr.Z0 / sqrt( tr.covMatrix[12]) );
      double z0sig =
          fabs(tr.Z0 / sqrt(tr.covMatrix[9])); // covMat = lower-triangle
      if (fabs(z0sig) > m_z0sig_max || fabs(z0sig) < m_z0sig_min)
        continue;
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
SelPrimaryTracks(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind,
                 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                 ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                 TVector3 MC_EventPrimaryVertex) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(reco.size());

  // Event primary vertex:
  double xvtx0 = MC_EventPrimaryVertex[0];
  double yvtx0 = MC_EventPrimaryVertex[1];
  double zvtx0 = MC_EventPrimaryVertex[2];

  for (unsigned int i = 0; i < recind.size(); i++) {
    double xvtx = mc.at(mcind.at(i)).vertex.x;
    double yvtx = mc.at(mcind.at(i)).vertex.y;
    double zvtx = mc.at(mcind.at(i)).vertex.z;
    // primary particle ?
    double zero = 1e-12;
    if (fabs(xvtx - xvtx0) < zero && fabs(yvtx - yvtx0) < zero &&
        fabs(zvtx - zvtx0) < zero) {
      int reco_idx = recind.at(i);
      result.push_back(reco.at(reco_idx));
    }
  }
  return result;
}

int get_nTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  int nt = tracks.size();
  return nt;
}

bool compare_Tracks(const edm4hep::TrackState &tr1,
                    const edm4hep::TrackState &tr2) {
  if (tr1.D0 == tr2.D0 && tr1.phi == tr2.phi && tr1.omega == tr2.omega &&
      tr1.Z0 == tr2.Z0 && tr1.tanLambda == tr2.tanLambda &&
      tr1.time == tr2.time && tr1.referencePoint.x == tr2.referencePoint.x &&
      tr1.referencePoint.y == tr2.referencePoint.y &&
      tr1.referencePoint.z == tr2.referencePoint.z)
    return true;
  return false;
}

// ----------------------------------------------------------------------------------------

// --- Conversion methods between the Delphes and edm4hep conventions

TVectorD Edm4hep2Delphes_TrackParam(const TVectorD &param, bool Units_mm) {

  double conv = 1e-3; // convert mm to m
  if (Units_mm)
    conv = 1.;

  double scale0 = conv; // convert mm to m if needed
  double scale1 = 1;
  double scale2 = 0.5 / conv; // C = rho/2, convert from mm-1 to m-1
  double scale3 = conv;       // convert mm to m
  double scale4 = 1.;
  scale2 = -scale2; // sign of omega

  TVectorD result(5);
  result[0] = param[0] * scale0;
  result[1] = param[1] * scale1;
  result[2] = param[2] * scale2;
  result[3] = param[3] * scale3;
  result[4] = param[4] * scale4;

  return result;
}

TVectorD Delphes2Edm4hep_TrackParam(const TVectorD &param, bool Units_mm) {

  double conv = 1e-3; // convert mm to m
  if (Units_mm)
    conv = 1.;

  double scale0 = conv; // convert mm to m if needed
  double scale1 = 1;
  double scale2 = 0.5 / conv; // C = rho/2, convert from mm-1 to m-1
  double scale3 = conv;       // convert mm to m
  double scale4 = 1.;
  scale2 = -scale2; // sign of omega

  TVectorD result(5);
  result[0] = param[0] / scale0;
  result[1] = param[1] / scale1;
  result[2] = param[2] / scale2;
  result[3] = param[3] / scale3;
  result[4] = param[4] / scale4;

  return result;
}

TMatrixDSym
Edm4hep2Delphes_TrackCovMatrix(const std::array<float, 21> &covMatrix,
                               bool Units_mm) {

  // careful: since summer 2022, the covariance matrix in edm4hep is an array of
  // 21 floats because the time has been added as a 6th track parameter. But
  // Delphes (and k4marlinWrapper) samples still fill it as an array of 15
  // floats.

  double conv = 1e-3; // convert mm to m
  if (Units_mm)
    conv = 1.;

  double scale0 = conv; // convert mm to m if needed
  double scale1 = 1;
  double scale2 = 0.5 / conv; // C = rho/2, convert from mm-1 to m-1
  double scale3 = conv;       // convert mm to m
  double scale4 = 1.;
  scale2 = -scale2; // sign of omega

  TMatrixDSym covM(5);

  covM[0][0] = covMatrix[0] * scale0 * scale0;

  covM[1][0] = covMatrix[1] * scale1 * scale0;
  covM[1][1] = covMatrix[2] * scale1 * scale1;

  covM[0][1] = covM[1][0];

  covM[2][0] = covMatrix[3] * scale2 * scale0;
  covM[2][1] = covMatrix[4] * scale2 * scale1;
  covM[2][2] = covMatrix[5] * scale2 * scale2;

  covM[0][2] = covM[2][0];
  covM[1][2] = covM[2][1];

  covM[3][0] = covMatrix[6] * scale3 * scale0;
  covM[3][1] = covMatrix[7] * scale3 * scale1;
  covM[3][2] = covMatrix[8] * scale3 * scale2;
  covM[3][3] = covMatrix[9] * scale3 * scale3;

  covM[0][3] = covM[3][0];
  covM[1][3] = covM[3][1];
  covM[2][3] = covM[3][2];

  covM[4][0] = covMatrix[10] * scale4 * scale0;
  covM[4][1] = covMatrix[11] * scale4 * scale1;
  covM[4][2] = covMatrix[12] * scale4 * scale2;
  covM[4][3] = covMatrix[13] * scale4 * scale3;
  covM[4][4] = covMatrix[14] * scale4 * scale4;

  covM[0][4] = covM[4][0];
  covM[1][4] = covM[4][1];
  covM[2][4] = covM[4][2];
  covM[3][4] = covM[4][3];

  return covM;
}

std::array<float, 21> Delphes2Edm4hep_TrackCovMatrix(const TMatrixDSym &cov,
                                                     bool Units_mm) {

  // careful: since summer 2022, the covariance matrix in edm4hep is an array of
  // 21 floats because the time has been added as a 6th track parameter. But
  // Delphes (and k4marlinWrapper) samples still fill it as an array of 15
  // floats.

  double conv = 1e-3; // convert mm to m
  if (Units_mm)
    conv = 1.;

  double scale0 = conv; // convert mm to m if needed
  double scale1 = 1;
  double scale2 = 0.5 / conv; // C = rho/2, convert from mm-1 to m-1
  double scale3 = conv;       // convert mm to m
  double scale4 = 1.;
  scale2 = -scale2; // sign of omega

  std::array<float, 21> covMatrix;
  covMatrix[0] = cov[0][0] / (scale0 * scale0);
  covMatrix[1] = cov[1][0] / (scale1 * scale0);
  covMatrix[2] = cov[1][1] / (scale1 * scale1);
  covMatrix[3] = cov[2][0] / (scale0 * scale2);
  covMatrix[4] = cov[2][1] / (scale1 * scale2);
  covMatrix[5] = cov[2][2] / (scale2 * scale2);
  covMatrix[6] = cov[3][0] / (scale3 * scale0);
  covMatrix[7] = cov[3][1] / (scale3 * scale1);
  covMatrix[8] = cov[3][2] / (scale3 * scale2);
  covMatrix[9] = cov[3][3] / (scale3 * scale3);
  covMatrix[10] = cov[4][0] / (scale4 * scale0);
  covMatrix[11] = cov[4][1] / (scale4 * scale1);
  covMatrix[12] = cov[4][2] / (scale4 * scale2);
  covMatrix[13] = cov[4][3] / (scale4 * scale3);
  covMatrix[14] = cov[4][4] / (scale4 * scale4);

  for (int i = 15; i < 21; i++) {
    covMatrix[i] = 0.;
  }

  return covMatrix;
}

TVectorD get_trackParam(edm4hep::TrackState &atrack, bool Units_mm) {
  double d0 = atrack.D0;
  double phi0 = atrack.phi;
  double omega = atrack.omega;
  double z0 = atrack.Z0;
  double tanlambda = atrack.tanLambda;
  TVectorD param(5);
  param[0] = d0;
  param[1] = phi0;
  param[2] = omega;
  param[3] = z0;
  param[4] = tanlambda;
  TVectorD res = Edm4hep2Delphes_TrackParam(param, Units_mm);

  return res;
}

TMatrixDSym get_trackCov(edm4hep::TrackState &atrack, bool Units_mm) {
  auto covMatrix = atrack.covMatrix;

  TMatrixDSym covM = Edm4hep2Delphes_TrackCovMatrix(covMatrix, Units_mm);

  return covM;
}

// ----------------------------------------------------------------------------------------

float get_trackMom(edm4hep::TrackState &atrack) {
  double fB = 2; // 2 Tesla

  float C = -0.5 * 1e3 * atrack.omega;
  float phi0 = atrack.phi;
  float ct = atrack.tanLambda;
  //
  float pt = fB * 0.2998 / TMath::Abs(2 * C);
  TVector3 p(pt * TMath::Cos(phi0), pt * TMath::Sin(phi0), pt * ct);
  float result = p.Mag();
  return result;
}

FCCAnalysesVertex
get_FCCAnalysesVertex(ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl,
                      int index) {
  FCCAnalysesVertex result;
  if (index < TheVertexColl.size())
    result = TheVertexColl.at(index);
  return result;
}

int get_Nvertex(ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl) {
  return TheVertexColl.size();
}

edm4hep::VertexData get_VertexData(FCCAnalysesVertex TheVertex) {
  return TheVertex.vertex;
}

ROOT::VecOps::RVec<edm4hep::VertexData>
get_VertexData(ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl) {
  ROOT::VecOps::RVec<edm4hep::VertexData> result;
  for (unsigned int i = 0; i < TheVertexColl.size(); i++) {
    result.push_back(TheVertexColl.at(i).vertex);
  }
  return result;
}

edm4hep::VertexData
get_VertexData(ROOT::VecOps::RVec<FCCAnalysesVertex> TheVertexColl, int index) {
  edm4hep::VertexData result;
  if (index < TheVertexColl.size())
    result = TheVertexColl.at(index).vertex;
  return result;
}

int get_VertexNtrk(FCCAnalysesVertex TheVertex) { return TheVertex.ntracks; }

ROOT::VecOps::RVec<int>
get_VertexNtrk(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<int> result;
  for (auto &TheVertex : vertices) {
    result.push_back(TheVertex.ntracks);
  }
  return result;
}

ROOT::VecOps::RVec<int> get_VertexRecoInd(FCCAnalysesVertex TheVertex) {
  return TheVertex.reco_ind;
}

ROOT::VecOps::RVec<int> get_VertexRecoParticlesInd(
    FCCAnalysesVertex TheVertex,
    const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &reco) {

  ROOT::VecOps::RVec<int> result;
  ROOT::VecOps::RVec<int> indices_tracks = TheVertex.reco_ind;
  for (int i = 0; i < indices_tracks.size(); i++) {
    int tk_index = indices_tracks[i];
    for (int j = 0; j < reco.size(); j++) {
      auto &p = reco[j];
      if (p.tracks_begin == p.tracks_end)
        continue;
      if (p.tracks_begin == tk_index) {
        result.push_back(j);
        break;
      }
    }
  }
  return result;
}

TVectorD ParToACTS(TVectorD Par) {

  TVectorD pACTS(6); // Return vector
  //
  double fB = 2.;
  Double_t b = -0.29988 * fB / 2.;
  pACTS(0) = 1000 * Par(0);             // D from m to mm
  pACTS(1) = 1000 * Par(3);             // z0 from m to mm
  pACTS(2) = Par(1);                    // Phi0 is unchanged
  pACTS(3) = TMath::ATan2(1.0, Par(4)); // Theta in [0, pi] range
  pACTS(4) = Par(2) / (b * TMath::Sqrt(1 + Par(4) * Par(4))); // q/p in GeV
  pACTS(5) = 0.0; // Time: currently undefined
  //
  return pACTS;
}

// Covariance conversion to ACTS format
TMatrixDSym CovToACTS(TMatrixDSym Cov, TVectorD Par) {

  double fB = 2.;
  TMatrixDSym cACTS(6);
  cACTS.Zero();
  Double_t b = -0.29988 * fB / 2.;
  //
  // Fill derivative matrix
  TMatrixD A(5, 5);
  A.Zero();
  Double_t ct = Par(4);                             // cot(theta)
  Double_t C = Par(2);                              // half curvature
  A(0, 0) = 1000.;                                  // D-D	conversion to mm
  A(1, 2) = 1.0;                                    // phi0-phi0
  A(2, 4) = 1.0 / (TMath::Sqrt(1.0 + ct * ct) * b); // q/p-C
  A(3, 1) = 1000.;                                  // z0-z0 conversion to mm
  A(4, 3) = -1.0 / (1.0 + ct * ct);                 // theta - cot(theta)
  A(4, 4) = -C * ct / (b * pow(1.0 + ct * ct, 3.0 / 2.0)); // q/p-cot(theta)
  //
  TMatrixDSym Cv = Cov;
  TMatrixD At(5, 5);
  At.Transpose(A);
  Cv.Similarity(At);
  TMatrixDSub(cACTS, 0, 4, 0, 4) = Cv;
  cACTS(5, 5) =
      0.1; // Currently undefined: set to arbitrary value to avoid crashes
  //
  return cACTS;
}

////////////////////////////////////////////////////

// get all reconstructed vertices in a single vector
ROOT::VecOps::RVec<FCCAnalysesVertex>
get_all_vertices(FCCAnalysesVertex PV,
                 ROOT::VecOps::RVec<FCCAnalysesVertex> SV) {
  // Returns a vector of all vertices (PV and SVs)
  ROOT::VecOps::RVec<FCCAnalysesVertex> result;
  result.push_back(PV);
  for (auto &p : SV) {
    result.push_back(p);
  }
  return result;
}
//
ROOT::VecOps::RVec<FCCAnalysesVertex>
get_all_vertices(FCCAnalysesVertex PV,
                 ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> SV) {
  // Returns a vector of all vertices (PV and SVs)
  ROOT::VecOps::RVec<FCCAnalysesVertex> result;
  result.push_back(PV);
  for (auto i_SV : SV) {
    for (auto &p : i_SV) {
      result.push_back(p);
    }
  }
  return result;
}
//
// get all SVs in a single vector
ROOT::VecOps::RVec<FCCAnalysesVertex> get_all_SVs(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  // Returns a vector of all SVs
  ROOT::VecOps::RVec<FCCAnalysesVertex> result;
  for (auto i_SV : vertices) {
    for (auto &p : i_SV) {
      result.push_back(p);
    }
  }
  return result;
}

// internal fns for SV finder

// invariant mass of a two track vertex
double get_invM_pairs(FCCAnalysesVertex vertex, double m1, double m2) {
  // CAUTION: m1 -> first track; m2 -> second track

  double result;

  ROOT::VecOps::RVec<TVector3> p_tracks =
      vertex.updated_track_momentum_at_vertex;

  TLorentzVector p4_vtx;
  double m[2] = {m1, m2};
  int nTr = p_tracks.size();

  for (unsigned int i = 0; i < nTr; i++) {
    TLorentzVector p4_tr;
    p4_tr.SetXYZM(p_tracks[i].X(), p_tracks[i].Y(), p_tracks[i].Z(), m[i]);
    p4_vtx += p4_tr;
  }

  result = p4_vtx.M();
  return result;
}

ROOT::VecOps::RVec<double>
get_invM_pairs(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices, double m1,
               double m2) {
  // CAUTION: m1 -> first track; m2 -> second track

  ROOT::VecOps::RVec<double> result;
  for (auto &vertex : vertices) {

    double result_i;
    ROOT::VecOps::RVec<TVector3> p_tracks =
        vertex.updated_track_momentum_at_vertex;

    TLorentzVector p4_vtx;
    double m[2] = {m1, m2};
    int nTr = p_tracks.size();

    for (unsigned int i = 0; i < nTr; i++) {
      TLorentzVector p4_tr;
      p4_tr.SetXYZM(p_tracks[i].X(), p_tracks[i].Y(), p_tracks[i].Z(), m[i]);
      p4_vtx += p4_tr;
    }

    result_i = p4_vtx.M();
    result.push_back(result_i);
  }
  return result;
}

// invariant mass of a vertex (assuming all tracks to be pions)
double get_invM(FCCAnalysesVertex vertex) {

  double result;

  ROOT::VecOps::RVec<TVector3> p_tracks =
      vertex.updated_track_momentum_at_vertex;

  TLorentzVector p4_vtx;
  const double m = 0.13957039; // pion mass

  for (TVector3 p_tr : p_tracks) {
    TLorentzVector p4_tr;
    p4_tr.SetXYZM(p_tr.X(), p_tr.Y(), p_tr.Z(), m);
    p4_vtx += p4_tr;
  }

  result = p4_vtx.M();
  return result;
}

ROOT::VecOps::RVec<double>
get_invM(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {

  ROOT::VecOps::RVec<double> result;
  for (auto &vertex : vertices) {

    double result_i;
    ROOT::VecOps::RVec<TVector3> p_tracks =
        vertex.updated_track_momentum_at_vertex;

    TLorentzVector p4_vtx;
    const double m = 0.13957039; // pion mass

    for (TVector3 p_tr : p_tracks) {
      TLorentzVector p4_tr;
      p4_tr.SetXYZM(p_tr.X(), p_tr.Y(), p_tr.Z(), m);
      p4_vtx += p4_tr;
    }

    result_i = p4_vtx.M();
    result.push_back(result_i);
  }
  return result;
}

// cos(angle) b/n V0 candidate's (or any vtx) momentum & PV to V0 displacement
// vector
double get_PV2V0angle(FCCAnalysesVertex V0, FCCAnalysesVertex PV) {
  double result;

  ROOT::VecOps::RVec<TVector3> p_tracks = V0.updated_track_momentum_at_vertex;

  TVector3 p_sum;
  for (TVector3 p_tr : p_tracks)
    p_sum += p_tr;

  edm4hep::Vector3f r_V0 = V0.vertex.position; // in mm
  edm4hep::Vector3f r_PV = PV.vertex.position; // in mm

  TVector3 r_V0_PV(r_V0[0] - r_PV[0], r_V0[1] - r_PV[1], r_V0[2] - r_PV[2]);

  double pDOTr = p_sum.Dot(r_V0_PV);
  double p_mag = p_sum.Mag();
  double r_mag = r_V0_PV.Mag();

  result = pDOTr / (p_mag * r_mag);
  return result;
}

// cos(angle) b/n track momentum sum & PV to vtx displacement vector
double get_PV2vtx_angle(ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                        FCCAnalysesVertex vtx, FCCAnalysesVertex PV) {
  double result;

  TVector3 p_sum;
  for (edm4hep::TrackState tr : tracks) {
    TVectorD ipar = get_trackParam(tr);
    TVector3 ip = ParToP(ipar);
    p_sum += ip;
  }

  edm4hep::Vector3f r_vtx = vtx.vertex.position; // in mm
  edm4hep::Vector3f r_PV = PV.vertex.position;   // in mm

  TVector3 r_vtx_PV(r_vtx[0] - r_PV[0], r_vtx[1] - r_PV[1], r_vtx[2] - r_PV[2]);

  double pDOTr = p_sum.Dot(r_vtx_PV);
  double p_mag = p_sum.Mag();
  double r_mag = r_vtx_PV.Mag();

  result = pDOTr / (p_mag * r_mag);
  return result;
}

// get track's energy assuming it to be a pion
double get_trackE(edm4hep::TrackState track) {

  double result;

  const double m_pi = 0.13957039;

  TVectorD par = get_trackParam(track);
  TVector3 p = ParToP(par);
  TLorentzVector p4;
  p4.SetXYZM(p[0], p[1], p[2], m_pi);

  result = p4.E();
  return result;
}

////////////////////////////////////////////////

// no of reconstructed V0s
int get_n_SV(FCCAnalysesV0 SV) {
  int result = SV.vtx.size();
  return result;
}

// vector of position of all reconstructed V0 (in mm)
ROOT::VecOps::RVec<TVector3> get_position_SV(FCCAnalysesV0 SV) {
  ROOT::VecOps::RVec<TVector3> result;
  for (FCCAnalysesVertex ivtx : SV.vtx) {
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);
    result.push_back(xyz);
  }
  return result;
}

// vector of PDG IDs of all reconstructed V0
ROOT::VecOps::RVec<int> get_pdg_V0(FCCAnalysesV0 V0) {
  ROOT::VecOps::RVec<int> result = V0.pdgAbs;
  return result;
}

// vector of invariant masses of all reconstructed V0
ROOT::VecOps::RVec<double> get_invM_V0(FCCAnalysesV0 V0) {
  ROOT::VecOps::RVec<double> result = V0.invM;
  return result;
}

//
// vector of momenta of all reconstructed V0
ROOT::VecOps::RVec<TVector3> get_p_SV(FCCAnalysesV0 SV) {
  ROOT::VecOps::RVec<TVector3> result;

  for (FCCAnalysesVertex ivtx : SV.vtx) {
    ROOT::VecOps::RVec<TVector3> p_tracks =
        ivtx.updated_track_momentum_at_vertex;

    TVector3 p_sum;
    for (TVector3 p_tr : p_tracks)
      p_sum += p_tr;

    result.push_back(p_sum);
  }
  return result;
}

// vector of chi2 of all reconstructed V0s
ROOT::VecOps::RVec<double> get_chi2_SV(FCCAnalysesV0 SV) {
  ROOT::VecOps::RVec<double> result;

  for (FCCAnalysesVertex ivtx : SV.vtx) {
    int nDOF = 2 * ivtx.ntracks - 3;
    result.push_back(nDOF * ivtx.vertex.chi2);
  }
  return result;
}

// passing a vector of FCCAnalysesVertex instead of new structs

// no of reconstructed SVs
int get_n_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  int result = vertices.size();
  return result;
}

// vector of momenta of all reconstructed vertices (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<TVector3>
get_p_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<TVector3> result;

  for (auto &ivtx : vertices) {
    ROOT::VecOps::RVec<TVector3> p_tracks =
        ivtx.updated_track_momentum_at_vertex;

    TVector3 p_sum;
    for (TVector3 p_tr : p_tracks)
      p_sum += p_tr;

    result.push_back(p_sum);
  }
  return result;
}

// vector of position of all reconstructed SV (in mm)
ROOT::VecOps::RVec<TVector3>
get_position_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<TVector3> result;
  for (FCCAnalysesVertex ivtx : vertices) {
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);
    result.push_back(xyz);
  }
  return result;
}

// vector of momentum magnitude of all reconstructed vertices (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<double>
get_pMag_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    ROOT::VecOps::RVec<TVector3> p_tracks =
        ivtx.updated_track_momentum_at_vertex;

    TVector3 p_sum;
    for (TVector3 p_tr : p_tracks)
      p_sum += p_tr;

    result.push_back(p_sum.Mag());
  }
  return result;
}

// vector of chi2 of all reconstructed vertices (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<double>
get_chi2_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    int nDOF = 2 * ivtx.ntracks - 3;
    result.push_back(nDOF * ivtx.vertex.chi2);
  }
  return result;
}

// vector of chi2 (normalised) of all reconstructed vertices (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<double>
get_norm_chi2_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices)
    result.push_back(ivtx.vertex.chi2);
  return result;
}

// vector of nDOF of all reconstructed vertices (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<int>
get_nDOF_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<int> result;

  for (auto &ivtx : vertices)
    result.push_back(2 * ivtx.ntracks - 3);
  return result;
}

// vector of polar angle (theta) of all reconstructed vertices (SV.vtx or
// V0.vtx)
ROOT::VecOps::RVec<double>
get_theta_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);
    result.push_back(xyz.Theta());
  }
  return result;
}

// vector of azimuth angle (phi) of all reconstructed vertices (SV.vtx or
// V0.vtx)
ROOT::VecOps::RVec<double>
get_phi_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);
    result.push_back(xyz.Phi());
  }
  return result;
}

// vector of (cos of) angles b/n vtx momenta & PV to vtx displacement vectors
ROOT::VecOps::RVec<double>
get_pointingangle_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
                     FCCAnalysesVertex PV) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    double iresult = 0.;

    ROOT::VecOps::RVec<TVector3> p_tracks =
        ivtx.updated_track_momentum_at_vertex;
    TVector3 p_sum;
    for (TVector3 p_tr : p_tracks)
      p_sum += p_tr;

    edm4hep::Vector3f r_vtx = ivtx.vertex.position; // in mm
    edm4hep::Vector3f r_PV = PV.vertex.position;    // in mm

    TVector3 r_vtx_PV(r_vtx[0] - r_vtx[0], r_vtx[1] - r_PV[1],
                      r_vtx[2] - r_PV[2]);

    double pDOTr = p_sum.Dot(r_vtx_PV);
    double p_mag = p_sum.Mag();
    double r_mag = r_vtx_PV.Mag();

    iresult = pDOTr / (p_mag * r_mag);
    result.push_back(iresult);
  }
  return result;
}

// vector of distances of all reconstructed SV from PV (in mm in xy plane)
ROOT::VecOps::RVec<double>
get_dxy_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
           FCCAnalysesVertex PV) {
  ROOT::VecOps::RVec<double> result;
  TVector3 x_PV(PV.vertex.position[0], PV.vertex.position[1],
                PV.vertex.position[2]);
  for (auto &ivtx : vertices) {
    TVector3 x_vtx(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
    TVector3 x_vtx_PV = x_vtx - x_PV;

    result.push_back(x_vtx_PV.Perp());
  }
  return result;
}

// vector of distances of all reconstructed SV from PV (in mm in 3D)
ROOT::VecOps::RVec<double>
get_d3d_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
           FCCAnalysesVertex PV) {
  ROOT::VecOps::RVec<double> result;
  TVector3 x_PV(PV.vertex.position[0], PV.vertex.position[1],
                PV.vertex.position[2]);
  for (auto &ivtx : vertices) {
    TVector3 x_vtx(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
    TVector3 x_vtx_PV = x_vtx - x_PV;

    result.push_back(x_vtx_PV.Mag());
  }
  return result;
}

// vector of distances of all reconstructed SV from given TVector3d (in mm in
// 3D)
ROOT::VecOps::RVec<double>
get_d3d_SV_obj(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
               TVector3 object) {
  ROOT::VecOps::RVec<double> result;
  for (auto &ivtx : vertices) {
    TVector3 x_vtx(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
    x_vtx = x_vtx - object;

    result.push_back(x_vtx.Mag());
  }
  return result;
}

// vector of distances of all reconstructed SV from given edm4hep::Vector3d (in
// mm in 3D)
ROOT::VecOps::RVec<double>
get_d3d_SV_obj(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
               edm4hep::Vector3d object) {
  ROOT::VecOps::RVec<double> result;
  for (auto &ivtx : vertices) {
    double dx = ivtx.vertex.position[0] - object.x;
    double dy = ivtx.vertex.position[1] - object.y;
    double dz = ivtx.vertex.position[2] - object.z;

    TVector3 d3d(dx, dy, dz);

    result.push_back(d3d.Mag());
  }
  return result;
}

// vector of decay position distances of all reconstructed SV from given
// TVector3d (in mm in 3D)
ROOT::VecOps::RVec<double>
get_dR_SV_obj(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices, TVector3 object) {
  ROOT::VecOps::RVec<double> result;
  for (auto &ivtx : vertices) {
    TVector3 x_vtx(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
    result.push_back(1e3 * TMath::Sqrt(pow(ivtx.vertex.position[0], 2) +
                                       pow(ivtx.vertex.position[1], 2) +
                                       pow(ivtx.vertex.position[2], 2)) -
                     1e3 * TMath::Sqrt(pow(object.x(), 2) + pow(object.y(), 2) +
                                       pow(object.z(), 2)));
  }
  return result;
}

// vector of decay position distances of all reconstructed SV from given
// edm4hep::Vector3d (in mm in 3D)
ROOT::VecOps::RVec<double>
get_dR_SV_obj(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
              edm4hep::Vector3d object) {
  ROOT::VecOps::RVec<double> result;
  for (auto &ivtx : vertices) {
    result.push_back(1e3 * TMath::Sqrt(pow(ivtx.vertex.position[0], 2) +
                                       pow(ivtx.vertex.position[1], 2) +
                                       pow(ivtx.vertex.position[2], 2)) -
                     1e3 * TMath::Sqrt(pow(object.x, 2) + pow(object.y, 2) +
                                       pow(object.z, 2)));
  }
  return result;
}

// vector of polar angle (theta) of all reconstructed vertices wrt jet axis
// (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<double>
get_relTheta_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
                ROOT::VecOps::RVec<int> nSV_jet,
                ROOT::VecOps::RVec<fastjet::PseudoJet> jets) {
  ROOT::VecOps::RVec<double> result;

  unsigned int j = 0;
  int nSV = nSV_jet[0];
  for (unsigned int i = 0; i < vertices.size(); i++) {
    auto &ivtx = vertices[i];
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);

    if (i >= nSV) {
      j++;
      nSV += nSV_jet[j];
    }
    auto &ijet = jets[j];
    double jetTheta = ijet.theta();

    result.push_back(xyz.Theta() - jetTheta);
  }
  return result;
}

// vector of azimuthal angle (phi) of all reconstructed vertices wrt jet axis
// (SV.vtx or V0.vtx)
ROOT::VecOps::RVec<double>
get_relPhi_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
              ROOT::VecOps::RVec<int> nSV_jet,
              ROOT::VecOps::RVec<fastjet::PseudoJet> jets) {
  ROOT::VecOps::RVec<double> result;

  unsigned int j = 0;
  int nSV = nSV_jet[0];
  for (unsigned int i = 0; i < vertices.size(); i++) {
    auto &ivtx = vertices[i];
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);

    if (i >= nSV) {
      j++;
      nSV += nSV_jet[j];
    }
    auto &ijet = jets[j];
    TVector3 jetP(ijet.px(), ijet.py(), ijet.pz());

    result.push_back(xyz.DeltaPhi(jetP));
  }
  return result;
}

// For get_SV_jets outputs

// no of reconstructed SVs
int get_n_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  int result = 0;
  if (vertices.size() != 0) {
    for (auto SV_jets : vertices)
      result += SV_jets.size();
  }
  return result;
}

// Return the number of reconstructed SVs
ROOT::VecOps::RVec<int> get_n_SV_jets(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<int> result;
  if (vertices.size() != 0) {
    for (auto SV_jets : vertices)
      result.push_back(SV_jets.size());
  }
  return result;
}

//
// separate V0s by jets
ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>>
get_svInJets(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
             ROOT::VecOps::RVec<int> nSV_jet) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> result;
  ROOT::VecOps::RVec<FCCAnalysesVertex> i_result;

  int index = 0;
  for (unsigned int i : nSV_jet) {
    for (unsigned int j = 0; j < i; j++) {
      i_result.push_back(vertices[j + index]);
    }

    result.push_back(i_result);
    i_result.clear();
    index += i;
  }
  return result;
}

// separate tracks by jet
std::vector<std::vector<edm4hep::TrackState>> get_tracksInJets(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
    ROOT::VecOps::RVec<fastjet::PseudoJet> jets,
    std::vector<std::vector<int>> jet_consti) {
  std::vector<std::vector<edm4hep::TrackState>> result;
  std::vector<edm4hep::TrackState> iJet_tracks;

  int nJet = jets.size();
  //
  for (unsigned int j = 0; j < nJet; j++) {

    std::vector<int> i_jetconsti = jet_consti[j];

    for (unsigned int ip : i_jetconsti) {
      auto &p = recoparticles[ip];
      if (p.tracks_begin >= 0 && p.tracks_begin < thetracks.size())
        iJet_tracks.push_back(thetracks.at(p.tracks_begin));
    }

    result.push_back(iJet_tracks);
    iJet_tracks.clear();
  }
  return result;
}

// vector of polar angle (theta) of reconstructed vertices of a jet wrt that jet
// axis [only for vertices from 1 jet]
ROOT::VecOps::RVec<double>
get_relTheta_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
                fastjet::PseudoJet jet) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);
    //
    result.push_back(xyz.Theta() - jet.theta());
  }
  //
  return result;
}

// vector of azimuthal angle (phi) of all reconstructed vertices wrt jet axis
// [only for vertices from 1 jet]
ROOT::VecOps::RVec<double>
get_relPhi_SV(ROOT::VecOps::RVec<FCCAnalysesVertex> vertices,
              fastjet::PseudoJet jet) {
  ROOT::VecOps::RVec<double> result;

  for (auto &ivtx : vertices) {
    TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                 ivtx.vertex.position[2]);
    TVector3 jetP(jet.px(), jet.py(), jet.pz());
    //
    result.push_back(xyz.DeltaPhi(jetP));
  }
  //
  return result;
}

/////// vec of vec functions (for get_SV_jets) /////////

// SV invariant mass
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>>
get_invM(ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);

    for (auto &vertex : i_vertices) {
      ROOT::VecOps::RVec<TVector3> p_tracks =
          vertex.updated_track_momentum_at_vertex;
      //
      TLorentzVector p4_vtx;
      const double m = 0.13957039; // pion mass
      //
      for (TVector3 p_tr : p_tracks) {
        TLorentzVector p4_tr;
        p4_tr.SetXYZM(p_tr.X(), p_tr.Y(), p_tr.Z(), m);
        p4_vtx += p4_tr;
      }
      i_result.push_back(p4_vtx.M());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV momentum
ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>>
get_p_SV(ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>> result;
  ROOT::VecOps::RVec<TVector3> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices) {
      ROOT::VecOps::RVec<TVector3> p_tracks =
          ivtx.updated_track_momentum_at_vertex;

      TVector3 p_sum;
      for (TVector3 p_tr : p_tracks)
        p_sum += p_tr;

      i_result.push_back(p_sum);
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV momentum magnitude
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_pMag_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices) {
      ROOT::VecOps::RVec<TVector3> p_tracks =
          ivtx.updated_track_momentum_at_vertex;

      TVector3 p_sum;
      for (TVector3 p_tr : p_tracks)
        p_sum += p_tr;

      i_result.push_back(p_sum.Mag());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV daughters multiplicity
ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> get_VertexNtrk(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result;
  ROOT::VecOps::RVec<int> i_result;
  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &TheVertex : i_vertices) {
      i_result.push_back(TheVertex.ntracks);
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV chi2
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_chi2_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices) {
      int nDOF = 2 * ivtx.ntracks - 3;
      i_result.push_back(nDOF * ivtx.vertex.chi2);
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV normalised chi2
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_norm_chi2_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices)
      i_result.push_back(ivtx.vertex.chi2);
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV no of DOF
ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> get_nDOF_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result;
  ROOT::VecOps::RVec<int> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices)
      i_result.push_back(2 * ivtx.ntracks - 3);
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV theta
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_theta_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);

    for (auto &ivtx : i_vertices) {
      TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
      i_result.push_back(xyz.Theta());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV phi
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>>
get_phi_SV(ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);

    for (auto &ivtx : i_vertices) {
      TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
      i_result.push_back(xyz.Phi());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV relative theta
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_relTheta_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices,
    ROOT::VecOps::RVec<fastjet::PseudoJet> jets) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < jets.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    fastjet::PseudoJet i_jet = jets.at(i);
    for (auto &ivtx : i_vertices) {
      TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
      //
      i_result.push_back(xyz.Theta() - i_jet.theta());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  //
  return result;
}

// SV relative phi
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_relPhi_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices,
    ROOT::VecOps::RVec<fastjet::PseudoJet> jets) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  for (unsigned int i = 0; i < jets.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    fastjet::PseudoJet i_jet = jets.at(i);
    for (auto &ivtx : i_vertices) {
      TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
      TVector3 jetP(i_jet.px(), i_jet.py(), i_jet.pz());
      //
      i_result.push_back(xyz.DeltaPhi(jetP));
    }
    result.push_back(i_result);
    i_result.clear();
  }
  //
  return result;
}

// SV pointing angle wrt PV
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> get_pointingangle_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices,
    FCCAnalysesVertex PV) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  edm4hep::Vector3f r_PV = PV.vertex.position; // in mm

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    for (auto &ivtx : i_vertices) {
      double pointangle = 0.;

      ROOT::VecOps::RVec<TVector3> p_tracks =
          ivtx.updated_track_momentum_at_vertex;
      TVector3 p_sum;
      for (TVector3 p_tr : p_tracks)
        p_sum += p_tr;

      edm4hep::Vector3f r_vtx = ivtx.vertex.position; // in mm

      TVector3 r_vtx_PV(r_vtx[0] - r_vtx[0], r_vtx[1] - r_PV[1],
                        r_vtx[2] - r_PV[2]);

      double pDOTr = p_sum.Dot(r_vtx_PV);
      double p_mag = p_sum.Mag();
      double r_mag = r_vtx_PV.Mag();

      pointangle = pDOTr / (p_mag * r_mag);
      i_result.push_back(pointangle);
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV distance from PV in xy
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>>
get_dxy_SV(ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices,
           FCCAnalysesVertex PV) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;
  TVector3 x_PV(PV.vertex.position[0], PV.vertex.position[1],
                PV.vertex.position[2]);

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices) {
      TVector3 x_vtx(ivtx.vertex.position[0], ivtx.vertex.position[1],
                     ivtx.vertex.position[2]);
      TVector3 x_vtx_PV = x_vtx - x_PV;

      i_result.push_back(x_vtx_PV.Perp());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV distance from PV in 3D
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>>
get_d3d_SV(ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices,
           FCCAnalysesVertex PV) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;
  TVector3 x_PV(PV.vertex.position[0], PV.vertex.position[1],
                PV.vertex.position[2]);

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices) {
      TVector3 x_vtx(ivtx.vertex.position[0], ivtx.vertex.position[1],
                     ivtx.vertex.position[2]);
      TVector3 x_vtx_PV = x_vtx - x_PV;

      i_result.push_back(x_vtx_PV.Mag());
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// SV position in 3D
ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>> get_position_SV(
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalysesVertex>> vertices) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>> result;
  ROOT::VecOps::RVec<TVector3> i_result;

  for (unsigned int i = 0; i < vertices.size(); i++) {
    ROOT::VecOps::RVec<TVector3> i_result;
    ROOT::VecOps::RVec<FCCAnalysesVertex> i_vertices = vertices.at(i);
    //
    for (auto &ivtx : i_vertices) {
      TVector3 xyz(ivtx.vertex.position[0], ivtx.vertex.position[1],
                   ivtx.vertex.position[2]);
      i_result.push_back(xyz);
    }
    result.push_back(i_result);
    i_result.clear();
  }
  return result;
}

// V0 pdg
ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>>
get_pdg_V0(ROOT::VecOps::RVec<int> pdg, ROOT::VecOps::RVec<int> nSV_jet) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result;
  ROOT::VecOps::RVec<int> i_result;

  int index = 0;
  for (unsigned int i : nSV_jet) {
    for (unsigned int j = 0; j < i; j++) {
      i_result.push_back(pdg[j + index]);
    }

    result.push_back(i_result);
    i_result.clear();
    index += i;
  }
  return result;
}

// V0 invariant mass
ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>>
get_invM_V0(ROOT::VecOps::RVec<double> invM, ROOT::VecOps::RVec<int> nSV_jet) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>> result;
  ROOT::VecOps::RVec<double> i_result;

  int index = 0;
  for (unsigned int i : nSV_jet) {
    for (unsigned int j = 0; j < i; j++) {
      i_result.push_back(invM[j + index]);
    }

    result.push_back(i_result);
    i_result.clear();
    index += i;
  }
  return result;
}

} // namespace VertexingUtils

} // namespace FCCAnalyses
