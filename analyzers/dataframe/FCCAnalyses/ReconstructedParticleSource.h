#ifndef ANALYZERS_SOURCE_RECONSTRUCTED_PARTICLE_H
#define ANALYZERS_SOURCE_RECONSTRUCTED_PARTICLE_H

// ROOT
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/RecoMCParticleLinkCollection.h"
#include "edm4hep/ReconstructedParticleCollection.h"

namespace FCCAnalyses ::PodioSource ::ReconstructedParticle {
// --------------------  Selectors  -----------------------------------------

/**
 * \brief Analyzer to select reconstructed particles associated with MC
 *        particle of the specified PDG ID.
 */
struct selPDG {
  const int m_pdg;
  /**
   * \brief Constructor.
   *
   * \param[in] pdgID  Desired value of the PDG ID.
   */
  explicit selPDG(const int pdgID);
  /**
   * \brief Operator over the input link collection.
   *
   * \param[in] inLinkColl  Input collection of the reco-MC links.
   * \param[out] result  Collection of the reconstructed particles associated
   *                     with the MC particle of the desired PDG ID.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::RecoMCParticleLinkCollection &inLinkColl);
};

/**
 * \brief Analyzer to select reconstructed particles associated with MC
 *        particle with the specified absolute value of the PDG ID.
 */
struct selAbsPDG {
  const int m_absPdg;
  /**
   * \brief Constructor.
   *
   * \param[in] pdgID  Desired absolute value of the PDG ID.
   */
  explicit selAbsPDG(const int pdgID);
  /**
   * \brief Operator over the input link collection.
   *
   * \param[in] inLinkColl  Input collection of the MC-reco links.
   * \param[out] result  Collection of the reconstructed particles associated
   *                     with the MC particle with the desired absolute value
   *                     of the PDG ID.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::RecoMCParticleLinkCollection &inLinkColl);
};

/**
 * \brief Select reconstructed particles with transverse momentum greater
 *        than a minimum value [GeV].
 */
struct selPt {
  const float m_minPt;
  /**
   * \brief Constructor.
   *
   * \param[in] minPt  Transverse momentum threshold [GeV].
   */
  explicit selPt(float minPt);
  /**
   * \brief Operator over input link collection.
   *
   * \param[in] inColl  Input collection of the reconstructed particles.
   * \param[out] result  Collection of the selected reconstructed particles.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::ReconstructedParticleCollection &inColl);
};

/**
 * \brief Analyzer to select specified number of reconstructed particles.
 */
struct selUpTo {
  const size_t m_size;
  /**
   * \brief Constructor.
   *
   * \param[in] size  Desired number of reconstructed particles.
   */
  explicit selUpTo(const size_t size);
  /**
   * \brief Operator over input link collection.
   *
   * \param[out] inColl  Input collection of reconstructed particles.
   * \param[out] result  Output collection of reconstructed particles.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::ReconstructedParticleCollection &inColl);
};

/**
 * \brief Analyzer to select reconstructed particles associated with the MC
 *        particle of the desired generator status.
 */
struct selGenStatus {
  const int m_status;
  /**
   * \brief Constructor.
   *
   * \param[in] status  Desired generator status of the MC particle.
   */
  explicit selGenStatus(const int status);
  /**
   * \brief Operator over input link collection.
   *
   * \param[in] inColl  Input collection of the reco-MC particle links.
   * \param[out] result  Output collection of the reconstructed particles.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::RecoMCParticleLinkCollection &inLinkColl);
};

// --------------------  Getters  -------------------------------------------

/**
 * \brief Get momenta of the input reconstructed particles.
 *
 * \param[in] inColl  Input particle collection.
 * \param[out] result  Vector of particle momenta.
 */
ROOT::VecOps::RVec<float>
getP(const edm4hep::ReconstructedParticleCollection &inColl);

/**
 * \brief Get transverse momenta (pT) of the input particles.
 *
 * \param[in] inColl  Input particle collection.
 * \param[out] result  Vector of particle pTs.
 */
ROOT::VecOps::RVec<float>
getPt(const edm4hep::ReconstructedParticleCollection &inColl);

/**
 * \brief Get rapidity (y) of the input reconstructed particles.
 *
 * \param[in] inColl  Input particle collection.
 * \param[out] result  Vector of particle rapidities.
 */
ROOT::VecOps::RVec<float>
getY(const edm4hep::ReconstructedParticleCollection &inColl);

/**
 * \brief Get energy (E) of the input reconstructed particles.
 *
 * \param[in] inColl  Input particle collection.
 * \param[out] result  Vector of particle energies.
 */
ROOT::VecOps::RVec<float>
getE(const edm4hep::ReconstructedParticleCollection &inColl);

/**
 * \brief Get mass of the input reconstructed particles.
 *
 * \param[in] inColl  Input particle collection.
 * \param[out] result  Vector of particle masses.
 */
ROOT::VecOps::RVec<float>
getMass(const edm4hep::ReconstructedParticleCollection &inColl);

/**
 * \brief Get charge of the input reconstructed particles.
 *
 * \param[in] inColl  Input particle collection.
 * \param[out] result  Vector of particle charges.
 */
ROOT::VecOps::RVec<float>
getCharge(const edm4hep::ReconstructedParticleCollection &inColl);

// --------------------  Transformers  --------------------------------------

/**
 * \brief Sort input particles by pT.
 *
 * \param[in] inColl  Input particles.
 * \param[out] result  Sorted collection of particles.
 */
edm4hep::ReconstructedParticleCollection
sortByPt(const edm4hep::ReconstructedParticleCollection &inColl);

/**
 * \brief Build two particle resonances from an arbitrary list of input
 *        reconstructed particles.
 *        Select the one closest to the pre-defined mass.
 */
struct resonanceBuilder {
  const float m_resonanceMass;
  /**
   * \brief Constructor.
   *
   * \param[in] resonanceMass  Desired value of the resonance mass.
   */
  explicit resonanceBuilder(float resonanceMass);
  /**
   * \brief Operator over input particle collection.
   *
   * \param[in] inColl  Input collection of the reconstructed particles.
   * \param[out] result  Selected reconstructed particle resonance.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::ReconstructedParticleCollection &inColl);
};

/**
 * \brief Build the recoil from an arbitrary list of input resonances at the
 *        specified center of mass energy.
 */
struct recoilBuilder {
  const float m_sqrts;
  /**
   * \brief Constructor.
   *
   * \param[in] sqrts  Center of mass energy.
   */
  explicit recoilBuilder(float sqrts);
  /**
   * \brief Operator over input collection of resonances.
   *
   * \param[in] inColl  Input collection of resonances.
   * \param[out] result  Resulting recoil.
   */
  edm4hep::ReconstructedParticleCollection
  operator()(const edm4hep::ReconstructedParticleCollection &inColl);
};

} // namespace FCCAnalyses::PodioSource::ReconstructedParticle

// namespace recoParticle = FCCAnalyses::PodioSource::ReconstructedParticle;

#endif /* ANALYZERS_SOURCE_RECONSTRUCTED_PARTICLE_H */
