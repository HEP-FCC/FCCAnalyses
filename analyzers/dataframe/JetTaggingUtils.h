#ifndef  JETTAGGINGUTILS_ANALYZERS_H
#define  JETTAGGINGUTILS_ANALYZERS_H

#include <vector>
#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "fastjet/JetDefinition.hh"
#include "TRandom3.h"

/** Jet tagging utilities interface.
This represents a set functions and utilities to perfom jet tagging from a list of jets.
*/

namespace JetTaggingUtils{

  /** @name JetTaggingUtils
   *  Jet tagging interface utilities.
  */

  //Get flavour association of jet 
  ROOT::VecOps::RVec<int> get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in, ROOT::VecOps::RVec<edm4hep::MCParticleData> MCin);
  //Get b-tags with an efficiency applied
  ROOT::VecOps::RVec<int> get_btag(ROOT::VecOps::RVec<int> in, float efficiency);
  //Get c-tags with an efficiency applied
  ROOT::VecOps::RVec<int> get_ctag(ROOT::VecOps::RVec<int> in, float efficiency);

    ///@}                                                                                                                                                                              
}


#endif
