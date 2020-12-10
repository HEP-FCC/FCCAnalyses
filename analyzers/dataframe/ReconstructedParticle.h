
#ifndef  RECONSTRUCTEDPARTICLE_ANALYZERS_H
#define  RECONSTRUCTEDPARTICLE_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/ParticleIDData.h"


/// TO BE MOVED LATER
struct ResonanceBuilder {
  int m_resonance_pdgid;
  float m_resonance_mass;
  ResonanceBuilder(int arg_resonance_pdgid, float arg_resonance_mass);
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs);
};

struct recoil {
  recoil(float arg_sqrts);
  float m_sqrts = 240.0;
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) ;
};

/// select ReconstructedParticles with transverse momentum greater than a minimum value [GeV]
struct selRP_pT {
  selRP_pT(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

/// select ReconstructedParticles with momentum greater than a minimum value [GeV]
struct selRP_p {
  selRP_p(float arg_min_p);
  float m_min_p = 1.; //> momentum threshold [GeV]
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

/// select ReconstructedParticles with charge equal or in asolute value
struct selRP_charge {
  selRP_charge(int arg_charge, bool arg_abs);
  float m_charge; //> charge condition
  bool  m_abs;//> absolute value of the charge
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

/// return reconstructed particles
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> getRP(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the transverse momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the pseudo-rapidity of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the rapidity of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the theta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the phi of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the energy of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the masses of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in); 

/// return the charges of the input ReconstructedParticles
ROOT::VecOps::RVec<float> getRP_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in); 

/// return the TlorentzVector of the input ReconstructedParticles
ROOT::VecOps::RVec<TLorentzVector> getRP_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

/// return the size of the input collection
int getRP_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);


/// returns the bjet flavour
ROOT::VecOps::RVec<bool> getJet_btag(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid, ROOT::VecOps::RVec<float> values); 

int getJet_ntags(ROOT::VecOps::RVec<bool> in);
#endif
