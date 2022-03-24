#ifndef analyzers_ONNXRuntime_h
#define analyzers_ONNXRuntime_h

#include <vector>
#include <memory>

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

  template<typename T>
  using Tensor = std::vector<std::vector<T> >;

  ONNXRuntime(const ONNXRuntime&) = delete;
  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  template<typename T>
  Tensor<T> run(const Tensor<T>& input) const;

private:
  std::unique_ptr<Ort::Env> env_;
  std::unique_ptr<Ort::Experimental::Session> session_;
};


#endif
