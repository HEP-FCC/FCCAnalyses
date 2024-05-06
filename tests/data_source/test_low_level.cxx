// ROOT
#include <ROOT/RVec.hxx>
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>
#include <TCanvas.h>
// EDM4hep
#include <edm4hep/MCParticleData.h>
#include <edm4hep/SimCalorimeterHitData.h>

ROOT::VecOps::RVec<edm4hep::MCParticleData> selElectrons(ROOT::VecOps::RVec<edm4hep::MCParticleData>& inParticles) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> electrons;
  for (size_t i = 0; i < inParticles.size(); ++i) {
    if (inParticles[i].PDG == 11) {
      electrons.emplace_back(inParticles[i]);
    }
  }

  return electrons;
}

struct selPDG {
  selPDG(int pdg = 11, bool chargeConjugateAllowed = true);
  const int m_pdg;
  const bool m_chargeConjugateAllowed;
  ROOT::VecOps::RVec<edm4hep::MCParticleData> operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData>& inParticles);
};

selPDG::selPDG(int pdg,
               bool chargeConjugateAllowed) : m_pdg(pdg),
                                              m_chargeConjugateAllowed(chargeConjugateAllowed) {};

ROOT::VecOps::RVec<edm4hep::MCParticleData> selPDG::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData>& inParticles) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  for (size_t i = 0; i < inParticles.size(); ++i) {
    auto &particle = inParticles[i];
    if (m_chargeConjugateAllowed) {
      if (std::abs(particle.PDG ) == std::abs(m_pdg)) {
        result.emplace_back(particle);
      }
    }
    else {
      if(particle.PDG == m_pdg) {
        result.emplace_back(particle);
      }
    }
  }

  return result;
}

ROOT::VecOps::RVec<float> getPx(ROOT::VecOps::RVec<edm4hep::MCParticleData> inParticles) {
  ROOT::VecOps::RVec<float> result;
  for (auto& p: inParticles) {
    result.push_back(p.momentum.x);
  }

  return result;
}


int main(int argc, char *argv[]) {
  // auto verbosity = ROOT::Experimental::RLogScopedVerbosity(ROOT::Detail::RDF::RDFLogChannel(), ROOT::Experimental::ELogLevel::kInfo);

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
  std::cout << std::endl;

  std::cout << "Info: Num. of slots: " <<  rdf.GetNSlots() << std::endl;

  auto rdf2 = rdf.Define("particles_px", getPx, {"Particle"});
  // auto rdf3 = rdf2.Define("electrons", selElectrons, {"MCParticles"});
  auto rdf3 = rdf2.Define("electrons", selPDG(11, false), {"Particle"});
  auto rdf4 = rdf3.Define("electrons_px", getPx, {"electrons"});
  auto h_particles_px = rdf4.Histo1D("particles_px");
  auto h_electrons_px = rdf4.Histo1D("electrons_px");

  h_particles_px->Print();
  h_electrons_px->Print();

  auto canvas = std::make_unique<TCanvas>("canvas", "Canvas", 450, 450);
  h_particles_px->Draw();
  canvas->Print("low_level_particles_px.pdf");
  h_electrons_px->Draw();
  canvas->Print("low_level_electrons_px.pdf");

  return EXIT_SUCCESS;
}
