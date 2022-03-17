#ifndef analyzers_ONNXRuntime_h
#define analyzers_ONNXRuntime_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "core/session/experimental_onnxruntime_cxx_api.h"

namespace Ort {
  class Allocator;
  class Env;
  class Session;
}

class ONNXRuntime {
public:
  static ONNXRuntime& get(const std::string& model_path = "", const std::string& preprocess_json = "");
  ONNXRuntime(const ONNXRuntime&) = delete;
  virtual ~ONNXRuntime();

  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  ROOT::VecOps::RVec<float> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>) const;

private:
  explicit ONNXRuntime(const std::string& model_path = "", const std::string& preprocess_json = "");

  std::unique_ptr<Ort::Env> env_;
  std::unique_ptr<Ort::Experimental::Session> session_;
  std::unique_ptr<Ort::Allocator> alloc_;
};


#endif
