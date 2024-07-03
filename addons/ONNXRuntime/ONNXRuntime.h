#ifndef ONNXRuntime_ONNXRuntime_h
#define ONNXRuntime_ONNXRuntime_h

#include "onnxruntime_cxx_api.h"

#include <string>
#include <vector>
#include <map>
#include <memory>

class ONNXRuntime {
public:
  explicit ONNXRuntime(const std::string& = "", const std::vector<std::string>& = {});
  virtual ~ONNXRuntime();

  template <typename T>
  using Tensor = std::vector<std::vector<T>>;

  ONNXRuntime(const ONNXRuntime&) = delete;
  ONNXRuntime& operator=(const ONNXRuntime&) = delete;

  const std::vector<std::string>& inputNames() const { return input_names_; }

  template <typename T>
  Tensor<T> run(Tensor<T>&, const Tensor<long>& = {}, unsigned long long = 1ull) const;

private:
  size_t variablePos(const std::string&) const;

  std::unique_ptr<Ort::Env> env_;
  std::unique_ptr<Ort::Session> session_;
  Ort::MemoryInfo memoryInfo_;

  std::vector<const char*> input_node_strings_, output_node_strings_;
  std::vector<std::string> input_names_;
  std::map<std::string, std::vector<int64_t>> input_node_dims_, output_node_dims_;
};

#endif
