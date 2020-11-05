
#include <ROOT/RDataFrame.hxx>
#include "TLorentzVector.h"
#include <TSystem.h>

// FCC event datamodel includes
//#include "datamodel/ParticleData.h"
//#include "datamodel/LorentzVector.h"
//#include "datamodel/JetData.h"
//#include "datamodel/TaggedParticleData.h"
//#include "datamodel/TaggedJetData.h"
// Legacy class

#include "ReconstructedParticle.h"
#include "ReconstructedParticle2MC.h"
#include "ReconstructedParticle2Track.h"
#include "MCParticle.h"


auto _m = edm4hep::ReconstructedParticleData();
auto _pod  = podio::ObjectID();


// Reproduce Heppy analysis
int main(int argc, char* argv[]){


   #ifdef ENABLEIMPLICITMT
   ROOT::EnableImplicitMT();
   #endif

   // fcc edm libraries
   //gSystem->Load("libdatamodel.so");
   gSystem->Load("libedm4hep");
   gSystem->Load("libpodio");
   gSystem->Load("libFCCAnalyses");
   // very basic command line argument parsing
   if (argc < 3) {
     std::cout << "error: need to specify fcc data files to analyze as command line arguments" << std::endl;
     std::cout << "usage:  analysis outfilename.root datafile1.root datafile2.root ... datafileN.root " << std::endl;
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
     .Define("MC_px",         getMC_px,{"Particle"})
     .Define("MC_py",         getMC_py,{"Particle"})
     .Define("MC_pz",         getMC_pz,{"Particle"})
     .Define("MC_p",         getMC_p,{"Particle"})
     .Define("RP_p",         getRP_p,{"ReconstructedParticles"})
     //.Define("RPMC_p",        getRP2MC_p,{"MCRecoAssociations#0", "MCRecoAssociations#1","ReconstructedParticles", "Particle"})
     .Define("RPMC_p",        getRP2MC_p,{"MCRecoAssociations#0.index", "MCRecoAssociations#1.index","ReconstructedParticles", "Particle"})
     //.Define("RPMC_p2",        getRP2MC_p_test2,{"MCRecoAssociations#0.index", "MCRecoAssociations#1.index","ReconstructedParticles", "Particle"})
     //.Define("RPMC_p3",        getRP2MC_p_test3,{"MCRecoAssociations#0.index", "MCRecoAssociations#1.index"})
     ;
   auto nentries = selectors.Count();
   std::cout << "Count events: " <<  *nentries << std::endl;
   std::cout << "Writing snapshot to disk ... \t" << outfilename << std::endl;
   selectors.Snapshot("events", outfilename,
		      { 
			"MC_px",
			  "MC_py",
			  "MC_pz",
			  "MC_p",			  
			  "RP_p",			  
			  //"RPMC_p",
			  "RPMC_p2",
			  "RPMC_p3"
			  }
		      );

   return 0;
}
