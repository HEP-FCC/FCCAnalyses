// std
#include <cstdlib>

// ROOT
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RLogger.hxx>
#include <ROOT/RVec.hxx>
#include <TCanvas.h>

// PODIO
#include <podio/DataSource.h>

// EDM4hep
#include <edm4hep/MCParticle.h>
#include <edm4hep/MCParticleCollection.h>
#include <edm4hep/RecoMCParticleLinkCollection.h>
#include <edm4hep/ReconstructedParticle.h>
#include <edm4hep/SimCalorimeterHitCollection.h>

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

edm4hep::MCParticleCollection
selElectrons(const edm4hep::MCParticleCollection &inParticles) {
  edm4hep::MCParticleCollection electrons;
  electrons.setSubsetCollection();
  for (auto particle : inParticles) {
    if (particle.getPDG() == 11) {
      auto electron = edm4hep::MCParticle(particle);
      electrons.push_back(electron);
    }
  }

  return electrons;
}

struct selPDG {
  selPDG(int pdg, bool chargeConjugateAllowed);
  const int m_pdg;
  const bool m_chargeConjugateAllowed;
  edm4hep::MCParticleCollection
  operator()(const edm4hep::MCParticleCollection &inParticles);
};

selPDG::selPDG(int pdg, bool chargeConjugateAllowed)
    : m_pdg(pdg), m_chargeConjugateAllowed(chargeConjugateAllowed){};

edm4hep::MCParticleCollection
selPDG::operator()(const edm4hep::MCParticleCollection &inParticles) {
  edm4hep::MCParticleCollection result;
  result.setSubsetCollection();
  for (auto particle : inParticles) {
    if (m_chargeConjugateAllowed) {
      if (std::abs(particle.getPDG()) == std::abs(m_pdg)) {
        result.push_back(particle);
      }
    } else {
      if (particle.getPDG() == m_pdg) {
        result.push_back(particle);
      }
    }
  }

  return result;
}

ROOT::VecOps::RVec<float>
getPx(const edm4hep::MCParticleCollection &inParticles) {
  ROOT::VecOps::RVec<float> result;
  for (auto particle : inParticles) {
    result.push_back(particle.getMomentum().x);
  }

  return result;
}

edm4hep::MCParticleCollection
get_stable_particles_from_decay(edm4hep::MCParticle in) {
  edm4hep::MCParticleCollection result;
  result.setSubsetCollection();

  auto daughters = in.getDaughters();
  if (daughters.size() != 0) { // particle is unstable
    for (const auto &daughter : daughters) {
      auto stable_daughters = get_stable_particles_from_decay(daughter);
      for (const auto &stable_daughter : stable_daughters) {
        result.push_back(stable_daughter);
      }
    }
  } else {
    result.push_back(in);
  }

  return result;
}

edm4hep::MCParticle
get_mcParticle(const edm4hep::ReconstructedParticle &recoParticle,
               const edm4hep::RecoMCParticleLinkCollection &assocColl) {
  edm4hep::MCParticle no_result;

  for (const auto &assoc : assocColl) {
    if (assoc.getFrom() == recoParticle) {
      return assoc.getTo();
    }
  }

  return no_result;
}

int main(int argc, const char *argv[]) {
#if ROOT_VERSION_CODE >= ROOT_VERSION(6, 36, 0)
  auto verbosity = ROOT::RLogScopedVerbosity(ROOT::Detail::RDF::RDFLogChannel(),
                                             ROOT::ELogLevel::kInfo);
#else
  auto verbosity = ROOT::Experimental::RLogScopedVerbosity(
      ROOT::Detail::RDF::RDFLogChannel(), ROOT::Experimental::ELogLevel::kInfo);
#endif

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
  canvas->Print("/tmp/source_particles_px.pdf");
  h_electrons_px->Draw();
  canvas->Print("/tmp/source_electrons_px.pdf");

  return EXIT_SUCCESS;
}
