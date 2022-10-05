// -*- C++ -*-
//
/** FCCAnalysis module: __ANALYSIS_NAME__
 *
 * \\file __SCRIPT_NAME__.h
 * \\author __AUTHOR_NAME__ <__AUTHOR_EMAIL__>
 *
 * Description:
 *   __ANALYSIS_DESCRIPTION__
 */

#ifndef __ANALYSIS_NAME_____SCRIPT_NAME___h
#define __ANALYSIS_NAME_____SCRIPT_NAME___h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace __ANALYSIS_NAME__ {
  namespace rv = ROOT::VecOps;

  void dummy_analysis();
  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>&);
}  // namespace __ANALYSIS_NAME__

#endif
