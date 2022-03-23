#ifndef analyzers_ONNXRuntime_h
#define analyzers_ONNXRuntime_h

#include "ROOT/RVec.hxx"
//#include "edm4hep/ReconstructedParticleData.h"

namespace Ort {
  class Env;
  namespace Experimental {
    class Session;
  }
}

class ONNXRuntime {
public:
  explicit ONNXRuntime(const std::string& model_path = "");
  virtual ~ONNXRuntime();

  ONNXRuntime(const ONNXRuntime&) = delete;
  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  std::vector<float> run(const std::vector<std::vector<float> >& input) const;

private:
  std::unique_ptr<Ort::Env> env_;
  std::unique_ptr<Ort::Experimental::Session> session_;
};


#endif
