// ROOT
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RLogger.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
// EDM4hep
#include "edm4hep/MCParticleData.h"
#include "edm4hep/SimCalorimeterHitData.h"
// FCCAnalyses
#include "FCCAnalyses/ReconstructedParticle2MC.h"
#include "FCCAnalyses/SmearObjects.h"

int main(int argc, const char *argv[]) {
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

  std::string filePath = "https://fccsw.web.cern.ch/fccsw/testsamples/"
                         "edm4hep1/p8_ee_WW_ecm240_edm4hep.root";
  if (argc > 2) {
    filePath = argv[2];
  }

  ROOT::RDataFrame rdf("events", filePath);

  // rdf.Describe().Print();
  // std::cout << std::endl;

  std::cout << "Info: Num. of slots: " << rdf.GetNSlots() << std::endl;

  auto rdf2 =
      rdf.Alias("MCRecoAssociations0", "_MCRecoAssociations_from.index");
  auto rdf3 = rdf2.Alias("MCRecoAssociations1", "_MCRecoAssociations_to.index");
  auto rdf4 = rdf3.Define(
      "RP_MC_index", FCCAnalyses::ReconstructedParticle2MC::getRP2MC_index,
      {"MCRecoAssociations0", "MCRecoAssociations1", "ReconstructedParticles"});
  auto rdf5 = rdf4.Define(
      "SmearedTracks",
      FCCAnalyses::SmearObjects::SmearedTracks(2.0, 2.0, 2.0, 2.0, 2.0, true),
      {"ReconstructedParticles", "_EFlowTrack_trackStates", "RP_MC_index",
       "Particle"});
  auto rdf6 = rdf5.Define(
      "smearTrack_omega",
      "return SmearedTracks.empty() ? -1 : SmearedTracks.at(0).omega;");
  // auto rdf6 = rdf5.Define("smearTrack_omega", "return RP_MC_index[0];");
  auto h_smeared_tracks_omega = rdf6.Histo1D("smearTrack_omega");

  h_smeared_tracks_omega->Print();

  auto canvas = std::make_unique<TCanvas>("canvas", "Canvas", 450, 450);
  h_smeared_tracks_omega->Draw();
  canvas->Print("/tmp/low_level_smeared_tracks_omega.pdf");

  return EXIT_SUCCESS;
}
