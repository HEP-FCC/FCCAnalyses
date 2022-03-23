#ifndef analyzers_dataframe_WeaverInterface_h
#define analyzers_dataframe_WeaverInterface_h

#include "ONNXRuntime.h"

class WeaverInterface {
public:
  static WeaverInterface& get(const std::string& onnx_filename = "");

  WeaverInterface(const WeaverInterface&) = delete;
  WeaverInterface& operator=(const WeaverInterface&) = delete;

  template <typename... Args> ROOT::VecOps::RVec<float> operator()(Args&&... args) const {
    return operator()(std::vector<ROOT::RVec<float> >{std::forward<Args>(args)...});
  }
  ROOT::VecOps::RVec<float> operator()(std::vector<ROOT::VecOps::RVec<float> >) const;

private:
  explicit WeaverInterface(const std::string& onnx_filename);
  std::unique_ptr<ONNXRuntime> onnx_;
};

#endif
