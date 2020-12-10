
#ifndef  MCPARTICLE_ANALYZERS_H
#define  MCPARTICLE_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"


/// Filter events based on a MCParticles PDGID
struct filterMC_pdgID {
  filterMC_pdgID(int arg_pdgid, bool arg_abs);
  float m_pdgid; //> Generator pdgid
  bool m_abs;//> Use absolute value for pdgig
  bool  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
};



/// select MCParticles with transverse momentum greater than a minimum value [GeV]
struct selMC_pT {
  selMC_pT(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  ROOT::VecOps::RVec<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
};

/// select MCParticles with their status
struct selMC_genStatus {
  selMC_genStatus(int arg_status);
  float m_status = 1; //> Generator status
  ROOT::VecOps::RVec<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
};

/// get MC history tree for a given MCParticle index
struct getMC_tree{
  getMC_tree(int arg_index);
  float m_index; //> MC Particle index to build the tree from
  ROOT::VecOps::RVec<int> operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind);
};

/// get the decay of a given particle
struct getMC_decay {
  getMC_decay(int arg_mother, int arg_daughters, bool arg_inf);
  int m_mother = 0; //> mother pdg id
  int m_daughters = 0;//> daughters pdg id
  bool m_inf = false;//> boolean to check if the pdgid is below a value rather than equal
  bool  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind);
};


/// return the parent index of a given list of MC particles
ROOT::VecOps::RVec<int> getMC_parentid(ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents);

/// return the time of the input MCParticles
ROOT::VecOps::RVec<float> getMC_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the PDG of the input MCParticles
ROOT::VecOps::RVec<float> getMC_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the generator status of the input MCParticles
ROOT::VecOps::RVec<float> getMC_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the simulation status of the input MCParticles
ROOT::VecOps::RVec<float> getMC_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex of the input MCParticles
ROOT::VecOps::RVec<edm4hep::Vector3d> getMC_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex x of the input MCParticles
ROOT::VecOps::RVec<float> getMC_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex y of the input MCParticles
ROOT::VecOps::RVec<float> getMC_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex z of the input MCParticles
ROOT::VecOps::RVec<float> getMC_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the end point of the input MCParticles
ROOT::VecOps::RVec<edm4hep::Vector3d> getMC_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the end point x of the input MCParticles
ROOT::VecOps::RVec<float> getMC_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the end point y of the input MCParticles
ROOT::VecOps::RVec<float> getMC_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the z of the input MCParticles
ROOT::VecOps::RVec<float> getMC_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the transverse momenta of the input MCParticles
ROOT::VecOps::RVec<float> getMC_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
ROOT::VecOps::RVec<float> getMC_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
ROOT::VecOps::RVec<float> getMC_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
ROOT::VecOps::RVec<float> getMC_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
ROOT::VecOps::RVec<float> getMC_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the pseudo-rapidity of the input MCParticles
ROOT::VecOps::RVec<float> getMC_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the rapidity of the input MCParticles
ROOT::VecOps::RVec<float> getMC_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the theta of the input MCParticles
ROOT::VecOps::RVec<float> getMC_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the phi of the input MCParticles
ROOT::VecOps::RVec<float> getMC_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the energy of the input MCParticles
ROOT::VecOps::RVec<float> getMC_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the masses of the input MCParticles
ROOT::VecOps::RVec<float> getMC_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in); 

/// return the charges of the input MCParticles
ROOT::VecOps::RVec<float> getMC_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in); 

/// return the TlorentzVector of the input MCParticles
ROOT::VecOps::RVec<TLorentzVector> getMC_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<edm4hep::MCParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y);

/// return the size of the input collection
int getMC_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);


#endif
