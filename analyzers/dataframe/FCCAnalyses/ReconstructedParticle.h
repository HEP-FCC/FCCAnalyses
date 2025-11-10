#ifndef RECONSTRUCTEDPARTICLE_ANALYZERS_H
#define RECONSTRUCTEDPARTICLE_ANALYZERS_H

// Standard library
#include <cmath>
#include <vector>
// ROOT
#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"
// EDM4hep
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/ParticleIDData.h"

namespace FCCAnalyses ::ReconstructedParticle {
/**
 * @brief Build the two particle resonances from an arbitrary list of input
 * ReconstructedPartilces. Keep the closest to the mass given as input.
 */
struct resonanceBuilder {
  resonanceBuilder(float arg_resonance_mass);
  float m_resonance_mass;
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs);
};

/**
 * @brief Build the recoil from an arbitrary list of input
 * ReconstructedPartilces and the center of mass energy.
 */
struct recoilBuilder {
  recoilBuilder(float arg_sqrts);
  float m_sqrts = 240.0;
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> inParticles);
};

  /// return the angular separations (min / max / average) between a collection of particles
  struct angular_separationBuilder {
    angular_separationBuilder( int arg_delta); //  0, 1, 2 = max, min, average
    int m_delta = 0;
    float operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) ;
  };

  /// select ReconstructedParticles by type
  /// Note: type might not correspond to PDG ID
  struct sel_type {
    sel_type(const int type);
    const int m_type;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
    operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select ReconstructedParticles by type absolute value
  /// Note: type might not correspond to PDG ID
  struct sel_absType {
    sel_absType(const int type);
    const int m_type;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
    operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select ReconstructedParticles with transverse momentum greater than a minimum value [GeV]
  struct sel_pt {
    sel_pt(float arg_min_pt);
    float m_min_pt = 1.; //> transverse momentum threshold [GeV]
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select ReconstructedParticles with absolute pseudorapidity less than a maximum absolute value
  struct sel_eta {
    sel_eta(float arg_min_eta);
    float m_min_eta = 2.5; //> pseudorapidity threshold
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select ReconstructedParticles with momentum greater than a minimum value [GeV]
  struct sel_p {
    sel_p(float arg_min_p, float arg_max_p = 1e10);
    float m_min_p = 1.; //> momentum threshold [GeV]
    float m_max_p = 1e10; //< momentum threshold [GeV]
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select ReconstructedParticles with charge equal or in asolute value
  struct sel_charge {
    sel_charge(int arg_charge, bool arg_abs);
    float m_charge; //> charge condition
    bool  m_abs;//> absolute value of the charge
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select a list of reconstructed particles depending on the angle cosTheta axis
  struct sel_axis{
    bool m_pos = 0; //> Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0
    sel_axis(bool arg_pos);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
    operator()(ROOT::VecOps::RVec<float> angle,
               ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// select a list of reconstructed particles depending on the status of a certain boolean flag
  struct sel_tag {
    bool m_pass; // if pass is true, select tagged jets. Otherwise select anti-tagged ones
    sel_tag(bool arg_pass);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
    operator()(ROOT::VecOps::RVec<bool> tags,
               ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /**
   * @brief Retrieve subset collection of reconstructed particles.
   *
   * @param[in] indexes Indexes of the particles belonging to the subset
   *            collection.
   * @param[in] inParticles Collection of original particles.
   *
   * @return subset collection.
   */
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  get(ROOT::VecOps::RVec<int> indexes,
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> inParticles);

  /// return the transverse momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the momenta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the pseudo-rapidity of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the rapidity of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the theta of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the phi of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the energy of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the masses of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the charges of the input ReconstructedParticles
  ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the type of the input ReconstructedParticles
  ROOT::VecOps::RVec<int> get_type(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the TlorentzVector of the input ReconstructedParticles
  ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// return the TlorentzVector of the indexed input ReconstructedParticles
  TLorentzVector get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, int index);

  /// return the TlorentzVector of the one input ReconstructedParticle
  TLorentzVector get_tlv(edm4hep::ReconstructedParticleData in);

  /// return visible 4-momentum vector
  TLorentzVector get_P4vis(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// concatenate both input vectors and return the resulting vector
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  merge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x,
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

  /// remove elements of vector y from vector x
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  remove(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x,
         ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

  /**
   * @brief Return the size of the input collection.
   */
  int get_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> inParticles);

  /**
   * @brief Returns the b-jet mask (vector of bools).
   */
  ROOT::VecOps::RVec<bool>
  getJet_btag(ROOT::VecOps::RVec<int> index,
              ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid,
              ROOT::VecOps::RVec<float> values);

  /**
   * @brief Get number of b-jets.
   */
  int getJet_ntags(ROOT::VecOps::RVec<bool> inBJetMask);
  } // namespace FCCAnalyses::ReconstructedParticle

#endif /* RECONSTRUCTEDPARTICLE_ANALYZERS_H */
