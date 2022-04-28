
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
namespace FCCAnalyses{
  
namespace MCParticle{

  /// Filter events based on a MCParticles PDGID
  struct filter_pdgID {
    filter_pdgID(int arg_pdgid, bool arg_abs);
    float m_pdgid; //> Generator pdgid
    bool m_abs;//> Use absolute value for pdgig
    bool  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };

  /// select MCParticles with transverse momentum greater than a minimum value [GeV]
  struct sel_pt {
    sel_pt(float arg_min_pt);
    float m_min_pt = 20; //> transverse momentum threshold [GeV]
    ROOT::VecOps::RVec<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };

  /// select MCParticles with their status
  struct sel_genStatus {
    sel_genStatus(int arg_status);
    float m_status = 1; //> Generator status
    ROOT::VecOps::RVec<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
  };

  /// select MCParticles with their PDG id
  struct sel_pdgID {
    sel_pdgID(int arg_pdg, bool arg_chargeconjugate);
    int m_pdg = 13;
    bool m_chargeconjugate = true;
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


 /// return a list of indices that correspond to a given MC decay. The list contains the index of the mother, followed by the indices of the daughters, in the order specified. In case there are several such decays in the event, keep only the first one.
  struct get_indices_ExclusiveDecay{
     get_indices_ExclusiveDecay( int pdg_mother, std::vector<int> pdg_daughters, bool stableDaughters, bool chargeConjugate ) ;
     int m_pdg_mother;
     std::vector<int> m_pdg_daughters;
     bool m_stableDaughters;
     bool m_chargeConjugate;
     ROOT::VecOps::RVec<int>   operator() ( ROOT::VecOps::RVec<edm4hep::MCParticleData> in , ROOT::VecOps::RVec<int> ind);
  };

  /// return a list of indices that correspond to a given MC decay
  ROOT::VecOps::RVec<int>  get_indices_ExclusiveDecay_MotherByIndex( int imother,
								     std::vector<int> m_pdg_daughters,
								     bool m_stableDaughters,
                                        			     ROOT::VecOps::RVec<edm4hep::MCParticleData> in ,
								     ROOT::VecOps::RVec<int> ind);


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

  /// return the end point of the input MCParticles (not using the "endpoint" that is currently not filled)
  ROOT::VecOps::RVec<edm4hep::Vector3d> get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind );

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

  /// return the angle (3D) between two MCParticles :
  ROOT::VecOps::RVec<float> AngleBetweenTwoMCParticles( ROOT::VecOps::RVec<edm4hep::MCParticleData> p1, ROOT::VecOps::RVec<edm4hep::MCParticleData> p2 );

  /// return the list of stable particles from the decay of a mother particle, looking at the full decay chain recursively. i is the mother index in the Particle block
  std::vector<int> get_list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) ;

  /// return the list of particles from the decay of a mother particle. i is the mother index in the Particle block.
  std::vector<int> get_list_of_particles_from_decay( int i,
						 ROOT::VecOps::RVec<edm4hep::MCParticleData> in,
						 ROOT::VecOps::RVec<int> ind) ;

  /// returns one MCParticle selected by its index in the particle block
  edm4hep::MCParticleData sel_byIndex( int idx, ROOT::VecOps::RVec<edm4hep::MCParticleData> in) ;

  /// obsolete: should use get_list_of_stable_particles_from_decay instead
  std::vector<int> list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) ;
  /// obsolete: should use get_list_of_particles_from_decay instead
  std::vector<int> list_of_particles_from_decay( int i,
                                                 ROOT::VecOps::RVec<edm4hep::MCParticleData> in,
                                                 ROOT::VecOps::RVec<int> ind) ;




}//#end NS MCParticle

}//end NS FCCAnalyses
#endif
