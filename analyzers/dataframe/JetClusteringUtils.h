
#ifndef  JETCLUSTERINGUTILS_ANALYZERS_H
#define  JETCLUSTERINGUTILS_ANALYZERS_H

#include <vector>

#include "ROOT/RVec.hxx"

#include "fastjet/JetDefinition.hh"


/** Jet clustering utilities interface. 
This represents a set functions and utilities to perfom jet clustering from a list of.  
*/

namespace JetClusteringUtils{

  /** @name JetClusteringUtils
   *  Jet clustering interface utilities. 
  */
  ///@{
  
  /** Get fastjet pseudoJet*/
  std::vector<fastjet::PseudoJet> get_pseudoJets(ROOT::VecOps::RVec<float> px, 
						 ROOT::VecOps::RVec<float> py, 
						 ROOT::VecOps::RVec<float> pz, 
						 ROOT::VecOps::RVec<float> e);
  
  /** Get jet px. Details. */
  ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet py. Details. */
  ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet pz. Details. */
  ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet energy. Details. */
  ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet pt. Details. */
  ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet p. Details. */
  ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet mass. Details. */
  ROOT::VecOps::RVec<float> get_m(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet eta. Details. */
  ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

  /** Get jet phi. Details. */
  ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<fastjet::PseudoJet> in);
  
  /** Get jet theta. Details. */
  ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

  ///@}
}


#endif
