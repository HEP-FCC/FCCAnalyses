#ifndef ANALYZERS_SOURCE_JET_CLUSTERING_UTILS_H
#define ANALYZERS_SOURCE_JET_CLUSTERING_UTILS_H

// EDM4hep
#include "edm4hep/ReconstructedParticleCollection.h"

// FastJet
#include "FastJet/JetClustering.h"
#include "fastjet/JetDefinition.hh"

/**
 * @brief  Jet clustering tools and utilities.
 *
 * This namespace contains a set of functions and utilities to perform jet
 * clustering using FastJet clustering algorithms with pseudoJets created from
 * EDM4hep collections of particles.
 *
 * Most of the analyzers work with FastJet pseudoJets.
 */
namespace FCCAnalyses ::PodioSource ::JetClustering {
/**
 * @brief  Create FastJet pseudoJets for later usage by the jet clustering
 *         algorithm(s).
 *
 * @param[in] inColl  Input collection of the reconstructed particles.
 * @return  Vector of pseudoJets.
 */
std::vector<fastjet::PseudoJet>
createPseudoJets(const edm4hep::ReconstructedParticleCollection &inColl);
} // namespace FCCAnalyses::PodioSource::JetClustering

#endif /* ANALYZERS_SOURCE_JET_CLUSTERING_UTILS_H */
