#ifndef JETTAGGINGUTILS_ANALYZERS_H
#define JETTAGGINGUTILS_ANALYZERS_H

#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"
#include "TRandom3.h"
#include "edm4hep/MCParticleData.h"
#include "fastjet/JetDefinition.hh"
#include <vector>

/** Jet tagging utilities interface.
This represents a set functions and utilities to perfom jet tagging from a list
of jets.
*/
namespace FCCAnalyses {

namespace JetTaggingUtils {

/** @name JetTaggingUtils
 *  Jet tagging interface utilities.
 */

// Get flavour association of jet
ROOT::VecOps::RVec<int>
get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in,
            ROOT::VecOps::RVec<edm4hep::MCParticleData> MCin);
// Get b-tags with an efficiency applied
ROOT::VecOps::RVec<int> get_btag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_c = 0., float mistag_l = 0.,
                                 float mistag_g = 0.);
// Get c-tags with an efficiency applied
ROOT::VecOps::RVec<int> get_ctag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_b = 0., float mistag_l = 0.,
                                 float mistag_g = 0.);
// Get l-tags with an efficiency applied
ROOT::VecOps::RVec<int> get_ltag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_b = 0., float mistag_c = 0.,
                                 float mistag_g = 0.);
// Get g-tags with an efficiency applied
ROOT::VecOps::RVec<int> get_gtag(ROOT::VecOps::RVec<int> in, float efficiency,
                                 float mistag_b = 0., float mistag_c = 0.,
                                 float mistag_l = 0.);

/// select a list of jets depending on the status of a certain boolean flag
/// (corresponding to its tagging state)
struct sel_tag {
  bool m_pass; // if pass is true, select tagged jets. Otherwise select
               // anti-tagged ones
  sel_tag(bool arg_pass);
  ROOT::VecOps::RVec<fastjet::PseudoJet>
  operator()(ROOT::VecOps::RVec<bool> tags,
             ROOT::VecOps::RVec<fastjet::PseudoJet> in);
};

///@}
} // namespace JetTaggingUtils

} // namespace FCCAnalyses

#endif
