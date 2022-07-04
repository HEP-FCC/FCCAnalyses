#include "FCCAnalyses/ONNXRuntime.h"

#include "core/session/experimental_onnxruntime_cxx_api.h"

#include <fstream>
#include <iostream>

ONNXRuntime::ONNXRuntime(const std::string& model_path)
    : env_(new Ort::Env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "onnx_runtime")) {
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

template <typename T>
ONNXRuntime::Tensor<T> ONNXRuntime::run(Tensor<T>& input, const Tensor<long>& input_shapes) const {
  std::vector<Ort::Value> tensors_in;
  std::cout << __PRETTY_FUNCTION__ << ">> " << input.size() << std::endl;
  auto mem_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);

  //auto& input_dims = session_->GetInputShapes()[0];
  std::cout << "input shapes mult: " << input_shapes.size() << std::endl;
  auto shapes = input_shapes;
  if (shapes.empty()) {
    for (size_t i = 0; i < input.size(); ++i) {
      shapes.emplace_back();
      auto type_info = session_->GetInputTypeInfo(i);
      auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
      size_t num_dims = tensor_info.GetDimensionsCount();
      shapes.back().resize(num_dims);
      tensor_info.GetDimensions(shapes.back().data(), num_dims);
    }
  }
  shapes = session_->GetInputShapes();
  for (size_t i = 0; i < shapes.size(); ++i) {
    std::cout << "shape --> " << i << std::endl;
    for (size_t j = 0; j < shapes.at(i).size(); ++j)
      std::cout << " >>>>>>> " << j << ": " << shapes.at(i).at(j) << std::endl;
  }
  auto input_dims = shapes[1];
  for (size_t i = 0; i < input_dims.size(); ++i)
    std::cout << "shape#" << i << ": " << input_dims.at(i) << std::endl;

  for (auto& val : input) {
    std::cout << "Tensor to be created: " << val.size() << std::endl;
    for (size_t i = 0; i < val.size(); ++i)
      std::cout << ":::: " << i << " = " << val.at(i) << std::endl;
    auto tensor = Ort::Value::CreateTensor<T>(mem_info, val.data(), val.size(), input_dims.data(), input_dims.size());
    //auto tensor = Ort::Value::CreateTensor<T>(val.data(), val.size(), session_->GetInputShapes()[0]);
    //auto tensor = Ort::Experimental::Value::CreateTensor<T>(val.data(), val.size(), input_shapes[0]);
    std::cout << "Tensor created: " << val.size() << std::endl;
    if (!tensor.IsTensor())
      throw std::runtime_error("Failed to create a tensor for input values");
    tensors_in.emplace_back(std::move(tensor));
  }
  std::cout << ">>> " << tensors_in.size() << std::endl;

  // run the inference
  /*auto tensors_out = session_->Run(session_->GetInputNames(), tensors_in, session_->GetOutputNames());

  std::cout << "after inference" << std::endl;

  // convert output to floats
  Tensor<T> output_values;
  for (auto& tensor : tensors_out) {
    if (!tensor.IsTensor())
      throw std::runtime_error("(At least) one of the inference outputs is not a tensor.");
    // recast the output given its shape/arrays length
    const auto length = tensor.GetTensorTypeAndShapeInfo().GetElementCount();
    const auto data = tensor.GetTensorMutableData<T>();
    output_values.emplace_back(data, data + length);
  }*/
  Tensor<T> output_values(tensors_in.size());
  return output_values;
}

template ONNXRuntime::Tensor<float> ONNXRuntime::run(Tensor<float>&, const Tensor<long>&) const;
