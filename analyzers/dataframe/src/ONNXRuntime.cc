#include "ONNXRuntime.h"

#include "core/session/experimental_onnxruntime_cxx_api.h"

#include <fstream>
#include <iostream>

ONNXRuntime::ONNXRuntime(const std::string& model_path) :
    env_(new Ort::Env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "onnx_runtime")) {
  std::cout << "building new ONNXRuntime object" << std::endl;
  Ort::SessionOptions options;
  auto path = model_path;
  session_ = std::make_unique<Ort::Experimental::Session>(*env_, path, options);

  std::cout << session_->GetInputCount() << std::endl;
  for (size_t i = 0; i < session_->GetInputCount(); ++i)
    std::cout << session_->GetInputNames()[i] << ": " << session_->GetInputShapes()[i].size() << std::endl;

  std::cout << "overridable:" << std::endl;
  for (const auto& name : session_->GetOverridableInitializerNames())
    std::cout << ">> " << name << std::endl;

  std::cout << session_->GetOutputCount() << std::endl;
  for (size_t i = 0; i < session_->GetOutputCount(); ++i)
    std::cout << session_->GetOutputNames()[i] << ": " << session_->GetOutputShapes()[i].size() << std::endl;
}

ONNXRuntime::~ONNXRuntime() {}

template<typename T>
ONNXRuntime::Tensor<T> ONNXRuntime::run(const Tensor<T>& input) const {
  std::vector<Ort::Value> tensors_in;
  for (const auto& val : input) {
    auto tensor = Ort::Experimental::Value::CreateTensor<T>(const_cast<T*>(val.data()), val.size(), session_->GetInputShapes()[0]);
    if (!tensor.IsTensor())
      throw std::runtime_error("Failed to create a tensor for input values");
    tensors_in.emplace_back(std::move(tensor));
  }
  std::cout << ">>> " << tensors_in.size() << std::endl;

  // run the inference
  auto tensors_out = session_->Run(session_->GetInputNames(), tensors_in, session_->GetOutputNames());

  // convert output to floats
  Tensor<T> output_values;
  for (auto& tensor : tensors_out) {
    if (!tensor.IsTensor())
      throw std::runtime_error("(At least) one of the inference outputs is not a tensor.");
    // recast the output given its shape/arrays length
    const auto length = tensor.GetTensorTypeAndShapeInfo().GetElementCount();
    const auto data = tensor.GetTensorMutableData<T>();
    output_values.emplace_back(data, data + length);
  }
  return output_values;
}
