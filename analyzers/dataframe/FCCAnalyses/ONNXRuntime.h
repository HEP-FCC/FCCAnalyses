#ifndef analyzers_ONNXRuntime_h
#define analyzers_ONNXRuntime_h

#include "ROOT/RVec.hxx"
#include "core/session/onnxruntime_cxx_api.h"

class ONNXRuntime {
public:
  ONNXRuntime();
  explicit ONNXRuntime(const std::string& model_path, const std::string& preprocess_json="");
  ONNXRuntime(const ONNXRuntime&) = delete;
  virtual ~ONNXRuntime();

  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  ROOT::VecOps::RVec<float> run(ROOT::VecOps::RVec<int> in) const;
};


#endif
