// -*- C++ -*-
//
/** FCCAnalysis module: __pkgname__
 *
 * \file __name__.h
 * \author __author__
 *
 * Description:
 *   __pkgdesc__
 */

#ifndef __pkgname_____name___h
#define __pkgname_____name___h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace __pkgname__ {
  namespace rv = ROOT::VecOps;

  void dummy_analysis();
  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>&);
}  // namespace __pkgname__

#endif
