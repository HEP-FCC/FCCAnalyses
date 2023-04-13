#include "FCCAnalyses/VertexFitterSimple.h"
#include "FCCAnalyses/MCParticle.h"

#include <iostream>

#include "TFile.h"
#include "TString.h"

//#include "TrkUtil.h"    // from delphes

namespace FCCAnalyses {

namespace VertexFitterSimple {

// -----------------------------------------------------------------------------

VertexingUtils::FCCAnalysesVertex VertexFitter(
    int Primary,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks, bool BeamSpotConstraint,
    double bsc_sigmax, double bsc_sigmay, double bsc_sigmaz, double bsc_x,
    double bsc_y, double bsc_z) {

  // input = a collection of recoparticles (in case one want to make
  // associations to RecoParticles ?) and thetracks = the collection of all
  // TrackState in the event

  VertexingUtils::FCCAnalysesVertex thevertex;

  // retrieve the tracks associated to the recoparticles
  ROOT::VecOps::RVec<edm4hep::TrackState> tracks =
      ReconstructedParticle2Track::getRP2TRK(recoparticles, thetracks);

  // and run the vertex fitter

  // FCCAnalysesVertex thevertex = VertexFitter_Tk( Primary, tracks, thetracks)
  // ;
  thevertex =
      VertexFitter_Tk(Primary, tracks, thetracks, BeamSpotConstraint,
                      bsc_sigmax, bsc_sigmay, bsc_sigmaz, bsc_x, bsc_y, bsc_z);

  // fill the indices of the tracks
  ROOT::VecOps::RVec<int> reco_ind;
  int Ntr = tracks.size();
  for (auto &p : recoparticles) {
    // std::cout << " in VertexFitter:  a recoparticle with charge = " <<
    // p.charge << std::endl;
    if (p.tracks_begin >= 0 && p.tracks_begin < thetracks.size()) {
      reco_ind.push_back(p.tracks_begin);
    }
  }
  if (reco_ind.size() != Ntr)
    std::cout << " ... problem in Vertex, size of reco_ind != Ntr "
              << std::endl;

  thevertex.reco_ind = reco_ind;

  return thevertex;
}

// ---------------------------------------------------------------------------------------------------------------------------

VertexingUtils::FCCAnalysesVertex
VertexFitter_Tk(int Primary, ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                bool BeamSpotConstraint, double bsc_sigmax, double bsc_sigmay,
                double bsc_sigmaz, double bsc_x, double bsc_y, double bsc_z) {

  ROOT::VecOps::RVec<edm4hep::TrackState> dummy;
  return VertexFitter_Tk(Primary, tracks, dummy, BeamSpotConstraint, bsc_sigmax,
                         bsc_sigmay, bsc_sigmaz, bsc_x, bsc_y, bsc_z);
}

// ---------------------------------------------------------------------------------------------------------------------------

VertexingUtils::FCCAnalysesVertex
VertexFitter_Tk(int Primary, ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
                bool BeamSpotConstraint, double bsc_sigmax, double bsc_sigmay,
                double bsc_sigmaz, double bsc_x, double bsc_y, double bsc_z) {

  // Units for the beam-spot : mum
  // See
  // https://github.com/HEP-FCC/FCCeePhysicsPerformance/tree/master/General#generating-events-under-realistic-fcc-ee-environment-conditions

  // final results :
  VertexingUtils::FCCAnalysesVertex TheVertex;

  edm4hep::VertexData result;
  ROOT::VecOps::RVec<float> reco_chi2;
  ROOT::VecOps::RVec<TVectorD> updated_track_parameters;
  ROOT::VecOps::RVec<int> reco_ind;
  ROOT::VecOps::RVec<float> final_track_phases;
  ROOT::VecOps::RVec<TVector3> updated_track_momentum_at_vertex;

  // if the collection of all tracks has been passed, keep trace of the indices
  // of the tracks that are used to fit this vertex
  if (alltracks.size() > 0) {
    for (int i = 0; i < tracks.size(); i++) { // the fitted tracks
      edm4hep::TrackState tr1 = tracks[i];
      for (int j = 0; j < alltracks.size();
           j++) { // the collection of all tracks
        edm4hep::TrackState tr2 = alltracks[j];
        if (VertexingUtils::compare_Tracks(tr1, tr2)) {
          reco_ind.push_back(j);
          break;
        }
      }
    }
  }

  TheVertex.vertex = result;
  TheVertex.reco_chi2 = reco_chi2;
  TheVertex.updated_track_parameters = updated_track_parameters;
  TheVertex.reco_ind = reco_ind;
  TheVertex.final_track_phases = final_track_phases;
  TheVertex.updated_track_momentum_at_vertex = updated_track_momentum_at_vertex;

  int Ntr = tracks.size();
  TheVertex.ntracks = Ntr;
  if (Ntr <= 1)
    return TheVertex; // can not reconstruct a vertex with only one track...

  TVectorD **trkPar = new TVectorD *[Ntr];
  TMatrixDSym **trkCov = new TMatrixDSym *[Ntr];

  bool Units_mm = true;

  for (Int_t i = 0; i < Ntr; i++) {
    edm4hep::TrackState t = tracks[i];
    TVectorD par = VertexingUtils::get_trackParam(t, Units_mm);
    trkPar[i] = new TVectorD(par);
    TMatrixDSym Cov = VertexingUtils::get_trackCov(t, Units_mm);
    trkCov[i] = new TMatrixDSym(Cov);
  }

  VertexFit theVertexFit(Ntr, trkPar, trkCov);

  if (BeamSpotConstraint) {
    float conv_BSC = 1e-3; // convert mum to mm
    TVectorD xv_BS(3);
    xv_BS[0] = bsc_x * conv_BSC;
    xv_BS[1] = bsc_y * conv_BSC;
    xv_BS[2] = bsc_z * conv_BSC;
    TMatrixDSym cov_BS(3);
    cov_BS[0][0] = pow(bsc_sigmax * conv_BSC, 2);
    cov_BS[1][1] = pow(bsc_sigmay * conv_BSC, 2);
    cov_BS[2][2] = pow(bsc_sigmaz * conv_BSC, 2);
    theVertexFit.AddVtxConstraint(xv_BS, cov_BS);
  }

  TVectorD x = theVertexFit.GetVtx(); // this actually runs the fit

  result.position =
      edm4hep::Vector3f(x(0), x(1), x(2)); // vertex position in mm

  // store the results in an edm4hep::VertexData object

  float Chi2 = theVertexFit.GetVtxChi2();
  float Ndof = 2.0 * Ntr - 3.0;
  ;
  result.chi2 = Chi2 / Ndof;

  // the chi2 of all the tracks :
  TVectorD tracks_chi2 = theVertexFit.GetVtxChi2List();
  for (int it = 0; it < Ntr; it++) {
    reco_chi2.push_back(tracks_chi2[it]);
  }

  // std::cout << " Fitted vertex: " <<  x(0)*conv << " " << x(1)*conv << " " <<
  // x(2)*conv << std::endl;
  TMatrixDSym covX = theVertexFit.GetVtxCov();
  std::array<float, 6>
      covMatrix; // covMat in edm4hep is a LOWER-triangle matrix.
  covMatrix[0] = covX(0, 0);
  covMatrix[1] = covX(1, 0);
  covMatrix[2] = covX(1, 1);
  covMatrix[3] = covX(2, 0);
  covMatrix[4] = covX(2, 1);
  covMatrix[5] = covX(2, 2);
  result.covMatrix = covMatrix;

  result.algorithmType = 1;

  result.primary = Primary;

  TheVertex.vertex = result;

  // Use VertexMore to retrieve more information :
  VertexMore theVertexMore(&theVertexFit, Units_mm);

  for (Int_t i = 0; i < Ntr; i++) {

    TVectorD updated_par =
        theVertexFit.GetNewPar(i); // updated track parameters
    TVectorD updated_par_edm4hep =
        VertexingUtils::Delphes2Edm4hep_TrackParam(updated_par, Units_mm);
    updated_track_parameters.push_back(updated_par_edm4hep);

    // Momenta of the tracks at the vertex:
    TVector3 ptrack_at_vertex = theVertexMore.GetMomentum(i);
    updated_track_momentum_at_vertex.push_back(ptrack_at_vertex);
  }

  TheVertex.updated_track_parameters = updated_track_parameters;
  TheVertex.updated_track_momentum_at_vertex = updated_track_momentum_at_vertex;
  TheVertex.final_track_phases = final_track_phases;
  TheVertex.reco_chi2 = reco_chi2;

  // memory cleanup
  for (Int_t i = 0; i < Ntr; i++) {
    delete trkPar[i];
    delete trkCov[i];
  }
  delete[] trkPar;
  delete[] trkCov;

  return TheVertex;
}

// ---------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::TrackState>
get_PrimaryTracks(ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                  bool BeamSpotConstraint, double bsc_sigmax, double bsc_sigmay,
                  double bsc_sigmaz, double bsc_x, double bsc_y, double bsc_z) {

  // iterative procedure to determine the primary vertex - and the primary
  // tracks

  // Feb 2023: Avoid the recursive approach used before... else very very slow,
  // with the new VertexFit objects

  // Units for the beam-spot : mum
  // See
  // https://github.com/HEP-FCC/FCCeePhysicsPerformance/tree/master/General#generating-events-under-realistic-fcc-ee-environment-conditions

  // bool debug  = true ;
  bool debug = false;
  float CHI2MAX = 25;
  //  float CHI2MAX = 10;

  if (debug) {
    std::cout << " ... enter in VertexFitterSimple::get_PrimaryTracks   Ntr = "
              << tracks.size() << std::endl;
  }

  ROOT::VecOps::RVec<edm4hep::TrackState> seltracks = tracks;

  if (seltracks.size() <= 1)
    return seltracks;

  int Ntr = tracks.size();

  TVectorD **trkPar = new TVectorD *[Ntr];
  TMatrixDSym **trkCov = new TMatrixDSym *[Ntr];

  for (Int_t i = 0; i < Ntr; i++) {
    edm4hep::TrackState t = tracks[i];
    TVectorD par = VertexingUtils::get_trackParam(t);
    trkPar[i] = new TVectorD(par);
    TMatrixDSym Cov = VertexingUtils::get_trackCov(t);
    trkCov[i] = new TMatrixDSym(Cov);
  }

  VertexFit theVertexFit(Ntr, trkPar, trkCov);

  if (BeamSpotConstraint) {
    TVectorD xv_BS(3);
    xv_BS[0] = bsc_x * 1e-6;
    xv_BS[1] = bsc_y * 1e-6;
    xv_BS[2] = bsc_z * 1e-6;
    TMatrixDSym cov_BS(3);
    cov_BS[0][0] = pow(bsc_sigmax * 1e-6, 2);
    cov_BS[1][1] = pow(bsc_sigmay * 1e-6, 2);
    cov_BS[2][2] = pow(bsc_sigmaz * 1e-6, 2);
    theVertexFit.AddVtxConstraint(xv_BS, cov_BS);
  }

  TVectorD x = theVertexFit.GetVtx(); // this actually runs the fit

  float chi2_max = 1e30;

  while (chi2_max >= CHI2MAX) {

    TVectorD tracks_chi2 = theVertexFit.GetVtxChi2List();
    chi2_max = tracks_chi2.Max();

    int n_removed = 0;
    for (int i = 0; i < theVertexFit.GetNtrk(); i++) {
      float track_chi2 = tracks_chi2[i];
      if (track_chi2 >= chi2_max) {
        theVertexFit.RemoveTrk(i);
        seltracks.erase(seltracks.begin() + i);
        n_removed++;
      }
    }
    if (n_removed > 0) {
      if (theVertexFit.GetNtrk() > 1) {
        // run the fit again:
        x = theVertexFit.GetVtx();
        TVectorD new_tracks_chi2 = theVertexFit.GetVtxChi2List();
        chi2_max = new_tracks_chi2.Max();
      } else {
        chi2_max = 0; // exit from the loop w/o crashing..
      }
    }
  } // end while

  // memory cleanup :
  for (Int_t i = 0; i < Ntr; i++) {
    delete trkPar[i];
    delete trkCov[i];
  }
  delete[] trkPar;
  delete[] trkCov;

  return seltracks;
}

// ---------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::TrackState>
get_NonPrimaryTracks(ROOT::VecOps::RVec<edm4hep::TrackState> allTracks,
                     ROOT::VecOps::RVec<edm4hep::TrackState> primaryTracks) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  for (auto &track : allTracks) {
    bool isInPrimary = false;
    for (auto &primary : primaryTracks) {
      if (VertexingUtils::compare_Tracks(track, primary)) {
        isInPrimary = true;
        break;
      }
    }
    if (!isInPrimary)
      result.push_back(track);
  }

  return result;
}

// ---------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<bool>
IsPrimary_forTracks(ROOT::VecOps::RVec<edm4hep::TrackState> allTracks,
                    ROOT::VecOps::RVec<edm4hep::TrackState> primaryTracks) {

  ROOT::VecOps::RVec<bool> result;
  for (auto &track : allTracks) {
    bool isInPrimary = false;
    for (auto &primary : primaryTracks) {
      if (VertexingUtils::compare_Tracks(track, primary)) {
        isInPrimary = true;
        break;
      }
    }
    result.push_back(isInPrimary);
  }
  return result;
}

} // namespace VertexFitterSimple

} // namespace FCCAnalyses
