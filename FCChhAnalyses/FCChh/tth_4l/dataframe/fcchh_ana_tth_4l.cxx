
#include <ROOT/RDataFrame.hxx>
#include "TLorentzVector.h"
#include <TSystem.h>

// FCC event datamodel includes
#include "datamodel/ParticleData.h"
#include "datamodel/LorentzVector.h"
#include "datamodel/JetData.h"
#include "datamodel/FloatData.h"
#include "datamodel/TaggedParticleData.h"
#include "datamodel/TaggedJetData.h"


auto _m = fcc::ParticleData();

double deltaR(fcc::LorentzVector v1, fcc::LorentzVector v2) {
  TLorentzVector tv1;
  tv1.SetXYZM(v1.px, v1.py, v1.pz, v1.mass);

  TLorentzVector tv2;
  tv2.SetXYZM(v2.px, v2.py, v2.pz, v2.mass);

  double deltaPhi = M_PI - std::abs(std::abs(tv1.Phi() - tv2.Phi()) - M_PI);
  double deltaEta = std::abs(tv1.Eta() - tv2.Eta());
  double result = std::sqrt(deltaPhi * deltaPhi + deltaEta * deltaEta);
  return result;
}



// Reproduce Heppy analysis
int main(int argc, char* argv[]){


   #ifdef ENABLEIMPLICITMT
   ROOT::EnableImplicitMT();
   #endif

   // fcc edm libraries
   gSystem->Load("libdatamodel.so");

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

   auto  selectLeptons = [](std::vector<fcc::ParticleData> in, std::vector<fcc::TaggedParticleData> iso) {
  std::vector<fcc::ParticleData> result;
  result.reserve(in.size());
  for (int i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.core.p4.px,2) + std::pow(p.core.p4.py,2)) > 20) {
      if (iso[i].tag  < 0.4) {
        result.emplace_back(p);

      }
    }
  }
  return result;
 };


   auto selectJetsBs = [](std::vector<fcc::JetData> in, std::vector<fcc::TaggedJetData> btags) {
    std::vector<fcc::JetData> result;
    result.reserve(in.size());
    for (int i = 0; i < in.size(); ++i) {
      auto & p = in[i];
      if (std::sqrt(std::pow(p.core.p4.px,2) + std::pow(p.core.p4.py,2)) > 30) {
          if (btags[i].tag > 0) {
            result.emplace_back(p);
          }
      }
    }
    return result;
   };

  
   // @todo: refactor to remove code duplication with selectJetsBs
   auto selectJetsLights = [](std::vector<fcc::JetData> in, std::vector<fcc::TaggedJetData> btags) {
    std::vector<fcc::JetData> result;
    result.reserve(in.size());
    for (int i = 0; i < in.size(); ++i) {
      auto & p = in[i];
      if (std::sqrt(std::pow(p.core.p4.px,2) + std::pow(p.core.p4.py,2)) > 30) {
          if (btags[i].tag == 0) {
            result.emplace_back(p);
          }
      }
    }
    return result;
   };

  auto noMatchJets = [](std::vector<fcc::JetData> in, std::vector<fcc::ParticleData> matchParticles) {
    std::vector<fcc::JetData> result;
    result.reserve(in.size());
    for (int i = 0; i < in.size(); ++i) {
      auto & p = in[i];
      bool matched = false;
      for (int j = 0; j < matchParticles.size(); ++j) {
        auto & matchCandidate = matchParticles[j];
        if (deltaR(p.core.p4, matchCandidate.core.p4) < 0.2) {
          matched = true;
        }
      }
      if (matched == false) {
        result.emplace_back(p);
      }
    }
    return result;


    };


   auto get_pt = [](std::vector<fcc::ParticleData> in){
     std::vector<float> result;
       for (int i = 0; i < in.size(); ++i) {
         result.push_back(sqrt(in[i].core.p4.px * in[i].core.p4.px + in[i].core.p4.py * in[i].core.p4.py));
       }
       return result;
   };


   auto mergeElectronsAndMuons = [](std::vector<fcc::ParticleData> x, std::vector<fcc::ParticleData> y) {
     std::vector<fcc::ParticleData> result;
     result.reserve(x.size() + y.size());
     result.insert( result.end(), x.begin(), x.end() );
     result.insert( result.end(), y.begin(), y.end() );
     return result;

   };

  auto LeptonicZBuilder = [](std::vector<fcc::ParticleData> leptons) {

        std::vector<fcc::ParticleData> result;
        int n = leptons.size();
        if (n >2) {
          std::vector<bool> v(n);
          std::fill(v.end() - 2, v.end(), true);
          do {
            fcc::ParticleData zed;
            zed.core.pdgId = 23;
            TLorentzVector zed_lv; 
            for (int i = 0; i < n; ++i) {
                if (v[i]) {
                  zed.core.charge += leptons[i].core.charge;
                  TLorentzVector lepton_lv;
                  lepton_lv.SetXYZM(leptons[i].core.p4.px, leptons[i].core.p4.py, leptons[i].core.p4.pz, leptons[i].core.p4.mass);
                  zed_lv += lepton_lv;
                }
            }
            zed.core.p4.px = zed_lv.Px();
            zed.core.p4.py = zed_lv.Py();
            zed.core.p4.pz = zed_lv.Pz();
            zed.core.p4.mass = zed_lv.M();
            result.emplace_back(zed);
          
          } while (std::next_permutation(v.begin(), v.end()));
        }

    return result;
  };

  /// @todo: refactor to remove code duplication with leptonicZBuilder
  auto LeptonicHiggsBuilder = [](std::vector<fcc::ParticleData> leptons) {

        std::vector<fcc::ParticleData> result;
        int n = leptons.size();
        if (n >2) {
          std::vector<bool> v(n);
          std::fill(v.end() - 2, v.end(), true);
          do {
            fcc::ParticleData zed;
            zed.core.pdgId = 25;
            TLorentzVector zed_lv; 
            for (int i = 0; i < n; ++i) {
                if (v[i]) {
                  zed.core.charge += leptons[i].core.charge;
                  TLorentzVector lepton_lv;
                  lepton_lv.SetXYZM(leptons[i].core.p4.px, leptons[i].core.p4.py, leptons[i].core.p4.pz, leptons[i].core.p4.mass);
                  zed_lv += lepton_lv;
                }
            }
            zed.core.p4.px = zed_lv.Px();
            zed.core.p4.py = zed_lv.Py();
            zed.core.p4.pz = zed_lv.Pz();
            zed.core.p4.mass = zed_lv.M();
            result.emplace_back(zed);

          
          } while (std::next_permutation(v.begin(), v.end()));
        }

    if (result.size() > 1) {
    auto  higgsresonancesort = [] (fcc::ParticleData i ,fcc::ParticleData j) { return (abs( 125. -i.core.p4.mass)<abs(125.-j.core.p4.mass)); };
    std::sort(result.begin(), result.end(), higgsresonancesort);

    std::vector<fcc::ParticleData>::const_iterator first = result.begin();
    std::vector<fcc::ParticleData>::const_iterator last = result.begin() + 1;
    std::vector<fcc::ParticleData> onlyBestHiggs(first, last);
    return onlyBestHiggs;
    } else {
    return result;
    }
  };

  auto id_float = [](std::vector<fcc::FloatData> x) {
    std::vector<float> result;
    for (auto & p: x) {
      result.push_back(p.value);

    }
    return result;
  };

  auto get_mass = [](std::vector<fcc::ParticleData> x) {
    std::vector<float> result;
    for (auto & p: x) {
      result.push_back(p.core.p4.mass);
    }

    return result;
  };

  auto get_nparticles = [](std::vector<fcc::ParticleData> x) {
    int result =  x.size();
    return result;
  };

  auto get_njets = [](std::vector<fcc::JetData> x) {
    int result =  x.size();
    return result;


  };

  auto get_njets2 = [](std::vector<fcc::JetData> x, std::vector<fcc::JetData> y) {
    int result =  x.size() + y.size();
    return result;

  };


   std::cout << "Apply selectors and define new branches ..." << std::endl;
   auto selectors =  df
                      .Define("selected_electrons", selectLeptons, {"electrons", "electronITags"})
                      .Define("selected_muons", selectLeptons, {"muons", "muonITags"})
                      .Define("selected_leptons", mergeElectronsAndMuons, {"selected_electrons", "selected_muons"})
                      .Define("zeds", LeptonicZBuilder, {"selected_leptons"})
                      .Define("selected_leptons_pt", get_pt, {"selected_leptons"})
                      .Define("zeds_pt", get_pt, {"zeds"})
                      .Define("higgs", LeptonicHiggsBuilder, {"zeds"})
                      .Define("higgs_m", get_mass, {{"higgs"}})
                      .Define("higgs_pt", get_pt, {"higgs"})
                      .Define("jets_30_bs", selectJetsBs, {"pfjets04", "pfbTags04"})
                      .Define("jets_30_lights", selectJetsLights, {"pfjets04", "pfbTags04"})
                      .Define("selected_bs", noMatchJets, {"jets_30_bs", "selected_leptons"})
                      .Define("selected_lights", noMatchJets, {"jets_30_lights", "selected_leptons"})
                      .Define("nbjets", get_njets, {"selected_bs"})
                      .Define("njets", get_njets2, {"selected_bs", "selected_lights"})
                      .Define("weight", id_float, {"mcEventWeights"})
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
