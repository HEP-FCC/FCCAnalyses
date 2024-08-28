// ROOT
#include <ROOT/RVec.hxx>
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>
#include <TCanvas.h>

// PODIO
#include <podio/DataSource.h>

// EDM4hep
#include <edm4hep/ReconstructedParticle.h>
#include <edm4hep/MCRecoParticleAssociationCollection.h>
#include <edm4hep/MCParticle.h>
#include <edm4hep/MCParticleCollection.h>
#include <edm4hep/SimCalorimeterHitCollection.h>

edm4hep::MCParticleCollection selElectrons(edm4hep::MCParticleCollection& inParticles) {
  edm4hep::MCParticleCollection electrons;
  electrons.setSubsetCollection();
  for (auto particle: inParticles) {
    if (particle.getPDG() == 11) {
      auto electron = edm4hep::MCParticle(particle);
      electrons.push_back(electron);
    }
  }

  return electrons;
}

struct selPDG {
  selPDG(int pdg = 11, bool chargeConjugateAllowed = true);
  const int m_pdg;
  const bool m_chargeConjugateAllowed;
  edm4hep::MCParticleCollection operator() (edm4hep::MCParticleCollection& inParticles);
};

selPDG::selPDG(int pdg,
               bool chargeConjugateAllowed) : m_pdg(pdg),
                                              m_chargeConjugateAllowed(chargeConjugateAllowed) {};

edm4hep::MCParticleCollection selPDG::operator() (edm4hep::MCParticleCollection& inParticles) {
  edm4hep::MCParticleCollection result;
  result.setSubsetCollection();
  for (auto particle: inParticles) {
    if (m_chargeConjugateAllowed) {
      if (std::abs(particle.getPDG() ) == std::abs(m_pdg)) {
        result.push_back(particle);
      }
    }
    else {
      if(particle.getPDG() == m_pdg) {
        result.push_back(particle);
      }
    }
  }

  return result;
}

ROOT::VecOps::RVec<float> getPx(edm4hep::MCParticleCollection& inParticles) {
  ROOT::VecOps::RVec<float> result;
  for (auto particle: inParticles) {
    result.push_back(particle.getMomentum().x);
  }

  return result;
}

edm4hep::MCParticleCollection get_stable_particles_from_decay(edm4hep::MCParticle in) {
  edm4hep::MCParticleCollection result;
  result.setSubsetCollection();

  auto daughters = in.getDaughters();
  if (daughters.size() != 0) {  // particle is unstable
    for (const auto& daughter : daughters) {
      auto stable_daughters = get_stable_particles_from_decay(daughter);
      for (const auto& stable_daughter : stable_daughters) {
        result.push_back(stable_daughter);
      }
    }
  } else {
    result.push_back(in);
  }

  return result;
}

edm4hep::MCParticle get_mcParticle(
    const edm4hep::ReconstructedParticle& recoParticle,
    const edm4hep::MCRecoParticleAssociationCollection& assocColl) {
  edm4hep::MCParticle no_result;

  for (const auto& assoc: assocColl) {
    if (assoc.getRec() == recoParticle) {
      return assoc.getSim();
    }
  }

  return no_result;
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

  ROOT::RDataFrame rdf(std::make_unique<podio::DataSource>(filePathList));

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
  canvas->Print("source_particles_px.pdf");
  h_electrons_px->Draw();
  canvas->Print("source_electrons_px.pdf");

  return EXIT_SUCCESS;
}
