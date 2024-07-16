
#include <ROOT/RDataFrame.hxx>
#include "TLorentzVector.h"
#include <TSystem.h>

// FCC event datamodel includes
#include "datamodel/ParticleData.h"
#include "datamodel/LorentzVector.h"
#include "datamodel/JetData.h"
#include "datamodel/TaggedParticleData.h"
#include "datamodel/TaggedJetData.h"
// Legacy class
#include "datamodel/FloatData.h"

#include "FCCAnalyses.h"


auto _m = fcc::ParticleData();




// Reproduce Heppy analysis
int main(int argc, char* argv[]){


   #ifdef ENABLEIMPLICITMT
   ROOT::EnableImplicitMT();
   #endif

   // fcc edm libraries
   gSystem->Load("libdatamodel");

   // very basic command line argument parsing
   if (argc < 3) {
     std::cout << "error: need to specify fcc data files to analyze as command line arguments" << std::endl;
     std::cout << "usage:  fccanalysis_tth_4l outfilename.root datafile1.root datafile2.root ... datafileN.root " << std::endl;
     return 1;
   }
   std::cout << "Read files... ";
   std::vector<std::string> filenames;

   std::string outfilename = argv[1];
   for (int i = 2; i < argc; ++i) {
     std::cout << " " << argv[i];
     filenames.push_back(argv[i]);
   }
   std::cout << std::endl;
   
   std::cout << "Creating TDataFrame ..." << std::endl;
   ROOT::RDataFrame df("events", filenames);


   std::cout << "Apply selectors and define new branches ..." << std::endl;
   auto selectors =  df
                      .Define("selected_electrons", selectParticlesPtIso(20, 0.4), {"electrons", "electronITags"})
                      .Define("selected_muons", selectParticlesPtIso(20, 0.4), {"muons", "muonITags"})
                      .Define("selected_leptons", mergeElectronsAndMuons, {"selected_electrons", "selected_muons"})
                      .Define("zeds", LeptonicZBuilder, {"selected_leptons"})
                      .Define("selected_leptons_pt", get_pt, {"selected_leptons"})
                      .Define("zeds_pt", get_pt, {"zeds"})
                      .Define("higgs", LeptonicHiggsBuilder, {"zeds"})
                      .Define("higgs_m", get_mass, {{"higgs"}})
                      .Define("higgs_pt", get_pt, {"higgs"})
                      .Define("jets_30_bs", selectJets(30, true), {"pfjets04", "pfbTags04"})
                      .Define("jets_30_lights", selectJets(30, false), {"pfjets04", "pfbTags04"})
                      .Define("selected_bs", noMatchJets(0.2), {"jets_30_bs", "selected_leptons"})
                      .Define("selected_lights", noMatchJets(0.2), {"jets_30_lights", "selected_leptons"})
                      .Define("nbjets", get_njets, {"selected_bs"})
                      .Define("njets", get_njets2, {"selected_bs", "selected_lights"})
                      .Define("weight", id_float_legacy, {"mcEventWeights"})
                      .Define("n_selected_leptons", get_nparticles, {"selected_leptons"})
                    ;
  auto nentries = selectors.Count();
  std::cout << "Count events: " <<  *nentries << std::endl;
  std::cout << "Writing snapshot to disk ... \t" << outfilename << std::endl;
  selectors.Snapshot("events", outfilename,
    { 
      // fcc particles with additional infos
       /* 
      "zeds",
      "zeds_pt",
      "selected_muons",
      "selected_leptons",
      "selected_electrons",
      "selected_bs",
      "selected_lights",
      "higgs",
      */
      "selected_leptons_pt",
      "higgs_pt",
      "higgs_m",
      "nbjets",
      "njets",
      "weight"

      }
    );

   return 0;
}
