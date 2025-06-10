// std
#include <cstdlib>
#include <iostream>
#include <ostream>

// ROOT
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>
#include <ROOT/RVec.hxx>
#include <TCanvas.h>
#include <TMatrixDSym.h>
#include <TRandom.h>
#include <TVector3.h>
#include <TVectorD.h>

// PODIO
#include <podio/DataSource.h>

// EDM4hep
#include "edm4hep/RecoMCParticleLinkCollection.h"
#include "edm4hep/TrackState.h"
#include <edm4hep/MCParticle.h>
#include <edm4hep/MCParticleCollection.h>
#include <edm4hep/SimCalorimeterHitCollection.h>

// FCCAnalyses
#include "FCCAnalyses/SmearObjects.h"
#include "FCCAnalyses/VertexingUtils.h"

const std::string getKey4hepOsAndStackType() {
  std::string result;

  const char *k4hEnvVar_cstr = std::getenv("KEY4HEP_STACK");
  std::string k4hEnvVar;
  if (k4hEnvVar_cstr) {
    k4hEnvVar = k4hEnvVar_cstr;
  }

  if (k4hEnvVar.find("almalinux9") != std::string::npos) {
    result += "alma9";
  } else if (k4hEnvVar.find("ubuntu22") != std::string::npos) {
    result += "ubuntu22";
  } else if (k4hEnvVar.find("ubuntu24") != std::string::npos) {
    result += "ubuntu24";
  }

  result += "/";

  if (k4hEnvVar.find("sw-nightlies.hsf.org") != std::string::npos) {
    result += "nightlies";
  } else if (k4hEnvVar.find("sw.hsf.org") != std::string::npos) {
    result += "release";
  }

  return result;
}

/// for a given MC particle, returns a "track state", i.e. a vector of 5 helix
/// parameters, in Delphes convention
TVectorD TrackParamFromMC_DelphesConv(edm4hep::MCParticle aMCParticle) {

  TVector3 p(aMCParticle.getMomentum().x, aMCParticle.getMomentum().y,
             aMCParticle.getMomentum().z);
  TVector3 x(1e-3 * aMCParticle.getVertex().x, 1e-3 * aMCParticle.getVertex().y,
             1e-3 * aMCParticle.getVertex().z); // mm to m
  float Q = aMCParticle.getCharge();
  TVectorD param =
      FCCAnalyses::VertexingUtils::XPtoPar(x, p, Q); // convention Franco

  return param;
}

TMatrixDSym get_trackCov(const edm4hep::TrackState &atrack, bool Units_mm) {
  auto covMatrix = atrack.covMatrix;

  TMatrixDSym covM =
      FCCAnalyses::VertexingUtils::Edm4hep2Delphes_TrackCovMatrix(covMatrix,
                                                                  Units_mm);

  return covM;
}

/**
 * \brief Generates new track states, by rescaling the covariance matrix of the
 *        tracks.
 */
struct SmearedTracks {
  bool m_debug;
  TRandom m_random;
  float m_smear_parameters[5];
  SmearedTracks(float smear_d0, float smear_phi, float smear_omega,
                float smear_z0, float smear_tlambda, bool debug);
  ROOT::VecOps::RVec<edm4hep::TrackState>
  operator()(const edm4hep::RecoMCParticleLinkCollection &mcRecoLink);
};

SmearedTracks::SmearedTracks(float smear_d0, float smear_phi, float smear_omega,
                             float smear_z0, float smear_tlambda,
                             bool debug = false) {

  m_smear_parameters[0] = smear_d0;
  m_smear_parameters[1] = smear_phi;
  m_smear_parameters[2] = smear_omega;
  m_smear_parameters[3] = smear_z0;
  m_smear_parameters[4] = smear_tlambda;

  m_debug = debug;
}

ROOT::VecOps::RVec<edm4hep::TrackState> SmearedTracks::operator()(
    const edm4hep::RecoMCParticleLinkCollection &mcRecoLink) {

  // returns a vector of TrackStates that is parallel to the collection of full
  // tracks (alltracks), i.e. same number of entries, same order. The method
  // retrieve the MC particle that is associated to a track, and builds a "track
  // state" out of the MC particle (i.e. it determines the corresponding (d0,
  // phi, omega, z0, tanlambda). From this vector, and from the covariance
  // matrix of the track, which is scaled by the user, new track states are
  // generated.

  ROOT::VecOps::RVec<edm4hep::TrackState> result;

  TVectorD zero(5);
  for (int k = 0; k < 5; k++) {
    zero(k) = 0.;
  }

  for (const auto &assoc : mcRecoLink) {
    const auto &recoParticle = assoc.getFrom();
    const auto &mcParticle = assoc.getTo();

    if (recoParticle.getTracks().size() < 1) {
      continue;
    }

    if (recoParticle.getTracks().size() > 1) {
      std::cout << "More than one track for one reco particle encountered!"
                << std::endl;
    }

    const edm4hep::Track &track = recoParticle.getTracks().at(0);

    // the MC-truth track parameters, in Delphes's comvention
    TVectorD mcTrackParam = TrackParamFromMC_DelphesConv(mcParticle);
    // and in edm4hep convention
    TVectorD mcTrackParam_edm4hep =
        FCCAnalyses::VertexingUtils::Delphes2Edm4hep_TrackParam(mcTrackParam,
                                                                false);

    if (track.getTrackStates().size() < 1) {
      continue;
    }

    if (track.getTrackStates().size() > 1) {
      std::cout << "More than one track state for one track encountered!"
                << std::endl;
    }

    const edm4hep::TrackState &trackState = track.getTrackStates().at(0);

    // the covariance matrix of the track, in Delphes's convention
    TMatrixDSym Cov = get_trackCov(trackState, false);

    // if the covMat of the track is pathological (numerical precision issue,
    // fraction of tracks = 5e-6): return original track
    if (Cov.Determinant() <= 0) {
      result.emplace_back(trackState);
      continue;
    }

    // scale the covariance matrix
    for (int j = 0; j < 5; j++) {
      for (int k = 0; k < 5; k++) {
        Cov[j][k] = Cov[j][k] * (m_smear_parameters[j] * m_smear_parameters[k]);
      }
    }
    // if (m_debug) {
    // Cov.Print();
    //}

    // generate a new track state (in Delphes's convention)
    TVectorD smeared_param_delphes = FCCAnalyses::SmearObjects::CovSmear(
        mcTrackParam, Cov, &m_random, m_debug);

    if (smeared_param_delphes == zero) { // Cholesky decomposition failed
      result.emplace_back(trackState);
      continue;
    }

    // back to the edm4hep conventions..
    TVectorD smeared_param =
        FCCAnalyses::VertexingUtils::Delphes2Edm4hep_TrackParam(
            smeared_param_delphes, false);

    auto smearedTrackState = trackState;
    if (smeared_param.GetNoElements() > 4) {
      smearedTrackState.D0 = smeared_param[0];
      smearedTrackState.phi = smeared_param[1];
      smearedTrackState.omega = smeared_param[2];
      smearedTrackState.Z0 = smeared_param[3];
      smearedTrackState.tanLambda = smeared_param[4];
    } else {
      result.emplace_back(trackState);
      continue;
    }

    // transform rescaled cov matrix from Delphes convention to EDM4hep
    // convention
    std::array<float, 21> covMatrix_edm4hep =
        FCCAnalyses::VertexingUtils::Delphes2Edm4hep_TrackCovMatrix(Cov, false);

    smearedTrackState.covMatrix = covMatrix_edm4hep;

    if (m_debug) {
      std::cout << std::endl
                << "Original track " << trackState.D0 << " " << trackState.phi
                << " " << trackState.omega << " " << trackState.Z0 << " "
                << trackState.tanLambda << std::endl;
      std::cout << "Smeared track " << smearedTrackState.D0 << " "
                << smearedTrackState.phi << " " << smearedTrackState.omega
                << " " << smearedTrackState.Z0 << " "
                << smearedTrackState.tanLambda << std::endl;
      std::cout << "MC particle " << mcTrackParam_edm4hep[0] << " "
                << mcTrackParam_edm4hep[1] << " " << mcTrackParam_edm4hep[2]
                << " " << mcTrackParam_edm4hep[3] << " "
                << mcTrackParam_edm4hep[4] << std::endl;
      for (int j = 0; j < 15; j++)
        std::cout << "smeared cov matrix(" << j
                  << "): " << smearedTrackState.covMatrix[j]
                  << ", scale factor: "
                  << smearedTrackState.covMatrix[j] / trackState.covMatrix[j]
                  << std::endl;
    }
    /*
    unsigned int recoIndex = assoc.getRec().getObjectID().index;
    unsigned int mcIndex = assoc.getSim().getObjectID().index;
    std::cout << "Reco: " << recoIndex << " ---> MC: " << mcIndex << std::endl;
    */

    result.emplace_back(smearedTrackState);
  }

  return result;
}

int main(int argc, char *argv[]) {
#if ROOT_VERSION_CODE >= ROOT_VERSION(6, 36, 0)
  auto verbosity = ROOT::RLogScopedVerbosity(ROOT::Detail::RDF::RDFLogChannel(),
                                             ROOT::ELogLevel::kInfo);
#else
  auto verbosity = ROOT::Experimental::RLogScopedVerbosity(
      ROOT::Detail::RDF::RDFLogChannel(), ROOT::Experimental::ELogLevel::kInfo);
#endif

  bool success = gInterpreter->Declare("#include \"edm4hep/TrackState.h\"");
  if (!success) {
    std::cerr << "ERROR: Unable to find edm4hep::TrackState header file!"
              << std::endl;
    return EXIT_FAILURE;
  }

  int nThreads = 1;
  if (argc > 1) {
    nThreads = atoi(argv[1]);
  }

  if (nThreads > 1) {
    ROOT::EnableImplicitMT(nThreads);
  }

  std::string filePath = "https://fccsw.web.cern.ch/fccsw/analysis/"
                         "test-samples/edm4hep099/" +
                         getKey4hepOsAndStackType() +
                         "/p8_ee_WW_ecm240_edm4hep.root";
  if (argc > 2) {
    filePath = argv[2];
  }

  ROOT::RDataFrame rdf(std::make_unique<podio::DataSource>(filePath));

  // rdf.Describe().Print();
  // std::cout << std::endl;

  std::cout << "Info: Num. of slots: " << rdf.GetNSlots() << std::endl;

  auto rdf2 =
      rdf.Define("SmearedTracks", SmearedTracks(2.0, 2.0, 2.0, 2.0, 2.0, false),
                 {"RecoMCLink"});

  auto rdf3 = rdf2.Define(
      "smearTrack_omega",
      "return SmearedTracks.empty() ? -1 : SmearedTracks.at(0).omega;");
  auto h_smeared_tracks_omega = rdf3.Histo1D("smearTrack_omega");

  h_smeared_tracks_omega->Print();

  auto canvas = std::make_unique<TCanvas>("canvas", "Canvas", 450, 450);
  h_smeared_tracks_omega->Draw();
  canvas->Print("/tmp/source_smeared_tracks_omega.pdf");

  return EXIT_SUCCESS;
}
