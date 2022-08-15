#ifndef analysis_example_DummyAnalysis_h
#define analysis_example_DummyAnalysis_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace analysis_example {
  namespace rv = ROOT::VecOps;

  void dummy_analysis();

  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>&);
}  // namespace analysis_example

#endif
