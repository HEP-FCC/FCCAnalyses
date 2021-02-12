
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


/** MCParticle interface. 
This represents a set functions and utilities to access and perform operations on the MCParticle collection.  
*/

bool dummyloader();

namespace MCParticle{

  /// Filter events based on a MCParticles PDGID
  struct filter_pdgID {
    filter_pdgID(int arg_pdgid, bool arg_abs);
    float m_pdgid; //> Generator pdgid
    bool m_abs;//> Use absolute value for pdgig
    bool  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };
  
  /// select MCParticles with transverse momentum greater than a minimum value [GeV]
  struct sel_pT {
    sel_pT(float arg_min_pt);
    float m_min_pt = 20; //> transverse momentum threshold [GeV]
    ROOT::VecOps::RVec<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };
  
  /// select MCParticles with their status
  struct sel_genStatus {
    sel_genStatus(int arg_status);
    float m_status = 1; //> Generator status
    ROOT::VecOps::RVec<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };
  
  /// get MC history tree for a given MCParticle index
  struct get_tree{
    get_tree(int arg_index);
    float m_index; //> MC Particle index to build the tree from
    ROOT::VecOps::RVec<int> operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind);
  };
  
  /// get the decay of a given particle
  struct get_decay {
    get_decay(int arg_mother, int arg_daughters, bool arg_inf);
    int m_mother = 0; //> mother pdg id
    int m_daughters = 0;//> daughters pdg id
    bool m_inf = false;//> boolean to check if the pdgid is below a value rather than equal
    bool  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind);
  };
  
 /// return the event primary vertex  (mm)
  struct get_EventPrimaryVertex {
    get_EventPrimaryVertex( int arg_genstatus  );
    int m_genstatus = 21;   // Pythia8  code of the incoming particles of the hardest subprocess
    TVector3  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };
  
  /// return the parent index of a given list of MC particles
  ROOT::VecOps::RVec<int> get_parentid(ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents);

  /// return the time of the input MCParticles
  ROOT::VecOps::RVec<float> get_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the PDG of the input MCParticles
  ROOT::VecOps::RVec<float> get_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  
  /// return the generator status of the input MCParticles
  ROOT::VecOps::RVec<float> get_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  
  /// return the simulation status of the input MCParticles
  ROOT::VecOps::RVec<float> get_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the production vertex of the input MCParticles
  ROOT::VecOps::RVec<edm4hep::Vector3d> get_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  
  /// return the production vertex x of the input MCParticles
  ROOT::VecOps::RVec<float> get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the production vertex y of the input MCParticles
  ROOT::VecOps::RVec<float> get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  
  /// return the production vertex z of the input MCParticles
  ROOT::VecOps::RVec<float> get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the end point of the input MCParticles
  ROOT::VecOps::RVec<edm4hep::Vector3d> get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the end point x of the input MCParticles
  ROOT::VecOps::RVec<float> get_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the end point y of the input MCParticles
  ROOT::VecOps::RVec<float> get_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the z of the input MCParticles
  ROOT::VecOps::RVec<float> get_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the transverse momenta of the input MCParticles
  ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the momenta of the input MCParticles
  ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the momenta of the input MCParticles
  ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the momenta of the input MCParticles
  ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the momenta of the input MCParticles
  ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the pseudo-rapidity of the input MCParticles
  ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the rapidity of the input MCParticles
  ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the theta of the input MCParticles
  ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the phi of the input MCParticles
  ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  
  /// return the energy of the input MCParticles
  ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

  /// return the masses of the input MCParticles
  ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in); 
  
  /// return the charges of the input MCParticles
  ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in); 
  
  /// return the TlorentzVector of the input MCParticles
  ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  
  /// concatenate both input vectors and return the resulting vector
  ROOT::VecOps::RVec<edm4hep::MCParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y);

  /// return the size of the input collection
  int get_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

}
#endif
