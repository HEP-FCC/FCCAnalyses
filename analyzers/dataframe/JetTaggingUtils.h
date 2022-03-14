#ifndef  JETTAGGINGUTILS_ANALYZERS_H
#define  JETTAGGINGUTILS_ANALYZERS_H

#include <vector>
#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "fastjet/JetDefinition.hh"
#include "TRandom3.h"
#include "JetClustering.h"
#include "JetClusteringUtils.h"
#include "MCParticle.h"

/** Jet tagging utilities interface.
This represents a set functions and utilities to perfom jet tagging from a list of jets.
*/

namespace JetTaggingUtils{

  /** @name JetTaggingUtils
   *  Jet tagging interface utilities.
  */

  /** Get flavour association of jet */
  ROOT::VecOps::RVec<int> get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in, ROOT::VecOps::RVec<edm4hep::MCParticleData> MCin);

  /** structure to output the following:
   *  - vector of parton and hadron flavours
   *  - FCCAnalyses jets clustered by user defined algorithm
   *  - jet constituent indices
   *  - ghostStatus (0 = not ghost, 1 = ghost parton, 2 = ghost hadron)
   *  - MCindex vector of indices of ghosts to MC collection (and -1 if not a ghost)
   */
  struct ghostFlavour {
    std::vector<std::vector<float>> flavour;
    JetClusteringUtils::FCCAnalysesJet jets;
    std::vector<std::vector<int>> jet_constituents;
    ROOT::VecOps::RVec<float> ghostStatus;
    ROOT::VecOps::RVec<int> MCindex;
  };


  /** Get ghost flavour (MC flavour) of jet described here: ..
   *  a struct is returned containing
   *  - vector of flavours: <<partonFlav Jet 1, partonFlav Jet 2, ...>, <hadronFlav Jet 1, hadron Flav Jet 2, ...>>
   *  - FCCAnalysesJet struct containing resulting jets (on which functions defined in JetClusteringUtils.cc can be called)
   *  - vector of jet constituent indices <<constis jet 1>, <constis jet 2>, ...>
   *  - ghostStatus (0 = not ghost, 1 = ghost parton, 2 = ghost hadron)
   *  - MCindex vector of indices of ghosts to MC collection (and -1 if not a ghost) <part 1, ..., part n>
   */
  struct get_ghostFlavour {
    get_ghostFlavour(int algo, float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_add1=0, float arg_add2=0);

    int m_algo = 0; ///< flag to select jet clustering algorithm defined in JetClustering.cc (0 = kt, 1 = antikt, 2 = cambridge, 3 = eekt, 4 = ee genkt, 5 = genkt, 6 = valencia, 7 = jade) 
    float m_radius = 0.5; ///< jet cone radius (note that this variable should be passed even when not used e.g. for eekt)
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float m_add1 = 0.; /// first additional parameter (to be used in selected clustering scheme)
    float m_add2 = 0.; /// second additional parameter
    ghostFlavour operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> Particle, ROOT::VecOps::RVec<int> ind, std::vector<fastjet::PseudoJet> pseudoJets, int partonFlag);
  };

  /** get the vector of flavours: <<partonFlav Jet 1, partonFlav Jet 2, ...>, <hadronFlav Jet 1, hadron Flav Jet 2, ...>> */
  std::vector<std::vector<float>> get_flavour(ghostFlavour ghostStruct);

  /** get the FCCAnalysesJet struct containing resulting jets (on which functions defined in JetClusteringUtils.cc can be called) */
  JetClusteringUtils::FCCAnalysesJet get_jets(ghostFlavour ghostStruct);

  /** get the vector of jet constituent indices <<constis jet 1>, <constis jet 2>, ...> */
  std::vector<std::vector<int>> get_jetconstituents(ghostFlavour ghostStruct);
  
  /** get ghostStatus (0 = not ghost, 1 = ghost parton, 2 = ghost hadron) */
  ROOT::VecOps::RVec<float> get_ghostStatus(ghostFlavour ghostStruct);

  /** get the MCindex vector of indices of ghosts to MC collection (and -1 if not a ghost) <part 1, ..., part n> */
  ROOT::VecOps::RVec<int> get_MCindex(ghostFlavour ghostStruct);

  //Get b-tags with an efficiency applied
  ROOT::VecOps::RVec<int> get_btag(ROOT::VecOps::RVec<int> in, float efficiency, float mistag_c=0., float mistag_l=0., float mistag_g=0.);
  //Get c-tags with an efficiency applied
  ROOT::VecOps::RVec<int> get_ctag(ROOT::VecOps::RVec<int> in, float efficiency, float mistag_b=0., float mistag_l=0., float mistag_g=0.);
  //Get l-tags with an efficiency applied
  ROOT::VecOps::RVec<int> get_ltag(ROOT::VecOps::RVec<int> in, float efficiency, float mistag_b=0., float mistag_c=0., float mistag_g=0.);
  //Get g-tags with an efficiency applied
  ROOT::VecOps::RVec<int> get_gtag(ROOT::VecOps::RVec<int> in, float efficiency, float mistag_b=0., float mistag_c=0., float mistag_l=0.);

  /// select a list of jets depending on the status of a certain boolean flag (corresponding to its tagging state)
  struct sel_tag {
    bool m_pass; // if pass is true, select tagged jets. Otherwise select anti-tagged ones
    sel_tag(bool arg_pass);
    ROOT::VecOps::RVec<fastjet::PseudoJet> operator() (ROOT::VecOps::RVec<bool> tags, ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  };

  ///@}
}

#endif
