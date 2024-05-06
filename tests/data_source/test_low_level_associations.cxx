// ROOT
#include "ROOT/RVec.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RLogger.hxx"
#include "TCanvas.h"
// EDM4hep
#include "edm4hep/MCParticleData.h"
#include "edm4hep/SimCalorimeterHitData.h"
// FCCAnalyses
#include "FCCAnalyses/SmearObjects.h"
#include "FCCAnalyses/ReconstructedParticle2MC.h"


int main(int argc, char *argv[]) {
  // auto verbosity = ROOT::Experimental::RLogScopedVerbosity(ROOT::Detail::RDF::RDFLogChannel(), ROOT::Experimental::ELogLevel::kInfo);

  bool success = gInterpreter->Declare("#include \"edm4hep/TrackState.h\"");
  if (!success) {
    std::cerr << "ERROR: Unable to find edm4hep::TrackState header file!"
              << std::endl;
    return EXIT_FAILURE;
  }

  int nCPU = 4;
  if (argc > 1) {
    nCPU = atoi(argv[1]);
  }

  std::vector<std::string> filePathList;
  std::string filePathBase = "/home/jsmiesko/source/FCCAnalyses/inputs/";
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_10.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_11.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_12.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_1.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_2.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_3.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_4.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_5.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_6.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_7.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_8.edm4hep.root");
  filePathList.emplace_back(filePathBase + "p8_ee_WW_ecm240/p8_ee_WW_ecm240_9.edm4hep.root");

  ROOT::EnableImplicitMT(nCPU);

  ROOT::RDataFrame rdf("events", filePathList);

  // rdf.Describe().Print();
  // std::cout << std::endl;

  std::cout << "Info: Num. of slots: " <<  rdf.GetNSlots() << std::endl;

  auto rdf2 = rdf.Alias("MCRecoAssociations0", "_MCRecoAssociations_rec.index");
  auto rdf3 = rdf2.Alias("MCRecoAssociations1", "_MCRecoAssociations_sim.index");
  auto rdf4 = rdf3.Define(
      "RP_MC_index",
      FCCAnalyses::ReconstructedParticle2MC::getRP2MC_index,
      {"MCRecoAssociations0", "MCRecoAssociations1", "ReconstructedParticles"}
  );
  auto rdf5 = rdf4.Define(
      "SmearedTracks",
      FCCAnalyses::SmearObjects::SmearedTracks(2.0, 2.0, 2.0, 2.0, 2.0, true),
      {"ReconstructedParticles", "_EFlowTrack_trackStates", "RP_MC_index", "Particle"}
  );
  auto rdf6 = rdf5.Define("smearTrack_omega", "return SmearedTracks.empty() ? -1 : SmearedTracks.at(0).omega;");
  // auto rdf6 = rdf5.Define("smearTrack_omega", "return RP_MC_index[0];");
  auto h_smeared_tracks_omega = rdf6.Histo1D("smearTrack_omega");


  h_smeared_tracks_omega->Print();

  auto canvas = std::make_unique<TCanvas>("canvas", "Canvas", 450, 450);
  h_smeared_tracks_omega->Draw();
  canvas->Print("low_level_smeared_tracks_omega.pdf");

  return EXIT_SUCCESS;
}
