#ifndef analyzers_ONNXRuntime_h
#define analyzers_ONNXRuntime_h

//#include <vector>
//#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"
//#include "edm4hep/MCParticleData.h"
#include "core/session/onnxruntime_cxx_api.h"

class ONNXRuntime {
public:
  explicit ONNXRuntime(const std::string& model_path);
  ONNXRuntime(const ONNXRuntime&) = delete;
  ONNXRuntime& operator=(const ONNXRuntime&) = delete;
  ~ONNXRuntime();

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > run() const;

  //ROOT::VecOps::RVec<int> get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in, ROOT::VecOps::RVec<edm4hep::MCParticleData> MCin);
  //ROOT::VecOps::RVec<int> get_btag(ROOT::VecOps::RVec<int> in, float efficiency);
  //ROOT::VecOps::RVec<int> get_ctag(ROOT::VecOps::RVec<int> in, float efficiency);

};

#endif
