#include "edm4hep/MCParticleData.h"

ROOT::VecOps::RVec<edm4hep::MCParticleData> gen_particles() {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  edm4hep::MCParticleData mcPart;
  mcPart.momentum.x = 11;
  result.push_back(mcPart);

  return result;
}
