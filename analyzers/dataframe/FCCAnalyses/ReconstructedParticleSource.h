#ifndef  RECONSTRUCTED_PARTICLE_SOURCE_ANALYZERS_H
#define  RECONSTRUCTED_PARTICLE_SOURCE_ANALYZERS_H

// ROOT
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/ReconstructedParticleCollection.h"
#include "edm4hep/MCRecoParticleAssociationCollection.h"

namespace FCCAnalyses :: ReconstructedParticle {
  /**
   * \brief Analyzer to select reconstructed particles associated with MC
   *        particle of the specified PDG ID.
   */
  struct selPDG {
    /**
     * \brief Constructor.
     *
     * \param[in] pdgID  Desired value of the PDG ID.
     */
    explicit selPDG(const int pdgID);
    const int m_pdg;
    /**
     * \brief Operator over the input particle collection.
     *
     * \param[in] inAssocColl  Input collection of the MC-reco associations.
     * \param[out] result  Collection of the reconstructed particles associated
     *                     with the MC particle with the desired PDG ID.
     */
    edm4hep::ReconstructedParticleCollection operator() (
        const edm4hep::MCRecoParticleAssociationCollection& inAssocColl);
  };


  /**
   * \brief Analyzer to select reconstructed particles associated with MC
   *        particle with the specified absolute value of the PDG ID.
   */
  struct selAbsPDG {
    /**
     * \brief Constructor.
     *
     * \param[in] pdgID  Desired absolute value of the PDG ID.
     */
    explicit selAbsPDG(const int pdgID);
    const int m_absPdg;
    /**
     * \brief Operator over input particle associations collection.
     *
     * \param[in] inAssocColl  Input collection of the MC-reco associations.
     * \param[out] result  Collection of the reconstructed particles associated
     *                     with the MC particle with the absolute value of the
     *                     desired PDG ID.
     */
    edm4hep::ReconstructedParticleCollection operator() (
        const edm4hep::MCRecoParticleAssociationCollection& inAssocColl);
  };


  /**
   * \brief Analyzer to select specified number of reconstructed particles.
   */
  struct selUpTo {
    /**
     * \brief Constructor.
     *
     * \param[in] size  Desired number of reconstructed particles.
     */
    explicit selUpTo(const size_t size);
    const size_t m_size;
    /**
     * \brief Operator over input particle associations collection.
     *
     * \param[out] inColl  Input collection of reconstructed particles.
     * \param[out] result  Output collection of reconstructed particles.
     */
    edm4hep::ReconstructedParticleCollection operator() (
        const edm4hep::ReconstructedParticleCollection& inColl);
  };


  /**
   * \brief Analyzer to select reconstructed particles associated with the MC
   *        particle of the desired generator status.
   */
  struct selGenStatus {
    /**
     * \brief Constructor.
     *
     * \param[in] status  Desired generator status of the MC particle.
     */
    explicit selGenStatus(const int status);
    const int m_status;
    /**
     * \brief Operator over input particle associations collection.
     *
     * \param[in] inColl  Input collection of the MC-reco particle associations.
     * \param[out] result  Output collection of reconstructed particles.
     */
    edm4hep::ReconstructedParticleCollection operator() (
        const edm4hep::MCRecoParticleAssociationCollection& inAssocColl);
  };


  /**
   * \brief Get transverse momenta (pT) of the input particles.
   *
   * \param[in] inParticles  Input particles.
   * \param[out] result  Vector of particle pTs.
   */
  ROOT::VecOps::RVec<double>
  getPt(const edm4hep::ReconstructedParticleCollection& inParticles);


  /**
   * \brief Sort input particles by pT.
   *
   * \param[in] inParticles  Input particles.
   * \param[out] result  Sorted collection of particles.
   */
  edm4hep::ReconstructedParticleCollection
  sortByPt(const edm4hep::ReconstructedParticleCollection& inParticles);
} /* FCCAnalyses :: ReconstructedParticle */

#endif /* RECONSTRUCTED_PARTICLE_SOURCE_ANALYZERS_H */
