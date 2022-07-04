#ifndef FCCAnalyses_ONNXRuntime_h
#define FCCAnalyses_ONNXRuntime_h

#include <string>
#include <vector>
#include <memory>

namespace Ort {
  class Env;
  namespace Experimental {
    class Session;
  }
}  // namespace Ort

class ONNXRuntime {
public:
  explicit ONNXRuntime(const std::string& model_path = "");
  virtual ~ONNXRuntime();

  template <typename T>
  using Tensor = std::vector<std::vector<T> >;

  ONNXRuntime(const ONNXRuntime&) = delete;
  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  template <typename T>
  Tensor<T> run(Tensor<T>& input, const Tensor<long>& input_shapes) const;

private:
  std::unique_ptr<Ort::Env> env_;
  std::unique_ptr<Ort::Experimental::Session> session_;
};

#endif
