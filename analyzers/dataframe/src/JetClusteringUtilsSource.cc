#include "FCCAnalyses/JetClusteringUtilsSource.h"

namespace FCCAnalyses ::PodioSource ::JetClustering {
// ----------------------------------------------------------------------------
std::vector<fastjet::PseudoJet>
createPseudoJets(const edm4hep::ReconstructedParticleCollection &inColl) {
  std::vector<fastjet::PseudoJet> result;
  unsigned index = 0;
  for (const auto &particle : inColl) {
    result.emplace_back(particle.getMomentum().x, particle.getMomentum().y,
                        particle.getMomentum().z, particle.getEnergy());
    result.back().set_user_index(index);
    ++index;
  }
  return result;
}

} // namespace FCCAnalyses::PodioSource::JetClustering
