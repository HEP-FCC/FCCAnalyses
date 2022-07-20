#ifndef FCCAnalyses_ONNXRuntime_h
#define FCCAnalyses_ONNXRuntime_h

#include <string>
#include <vector>
#include <map>
#include <memory>

namespace Ort {
  class Env;
  namespace Experimental {
    class Session;
  }
  class Session;
}  // namespace Ort

class ONNXRuntime {
public:
  explicit ONNXRuntime(const std::string& model_path = "");
  virtual ~ONNXRuntime();

  template <typename T>
  using Tensor = std::vector<std::vector<T>>;

  ONNXRuntime(const ONNXRuntime&) = delete;
  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  template <typename T>
  Tensor<T> run(const std::vector<std::string>&,
                Tensor<T>&,
                const Tensor<long>& = {},
                const std::vector<std::string>& = {},
                unsigned long long = 1ull) const;

private:
  std::unique_ptr<Ort::Env> env_;
  //std::unique_ptr<Ort::Experimental::Session> session_;
  std::unique_ptr<Ort::Session> session_;

  std::vector<std::string> input_node_strings_;
  std::vector<const char*> input_node_names_;
  std::map<std::string, std::vector<int64_t>> input_node_dims_;

  std::vector<std::string> output_node_strings_;
  std::vector<const char*> output_node_names_;
  std::map<std::string, std::vector<int64_t>> output_node_dims_;
};

#endif
