#include "FCCAnalyses/ONNXRuntime.h"

#include "core/session/experimental_onnxruntime_cxx_api.h"

#include <fstream>
#include <cassert>
#include <numeric>
#include <algorithm>

ONNXRuntime::ONNXRuntime(const std::string& model_path)
    : env_(new Ort::Env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "onnx_runtime")) {
  Ort::SessionOptions options;
  options.SetIntraOpNumThreads(1);
  session_ = std::make_unique<Ort::Session>(*env_, model_path.data(), options);
  Ort::AllocatorWithDefaultOptions allocator;

  // get input names and shapes
  const auto num_input_nodes = session_->GetInputCount();
  input_node_strings_.resize(num_input_nodes);
  input_node_names_.resize(num_input_nodes);
  input_node_dims_.clear();
  for (size_t i = 0; i < num_input_nodes; ++i) {
    const std::string input_name(session_->GetInputName(i, allocator));
    //const auto input_name = session_->GetInputNames()[i];
    input_node_strings_[i] = input_name;
    input_node_names_[i] = input_node_strings_[i].data();
    // get input shapes
    auto tensor_info = session_->GetInputTypeInfo(i).GetTensorTypeAndShapeInfo();
    const size_t num_dims = tensor_info.GetDimensionsCount();
    input_node_dims_[input_name].resize(num_dims);
    tensor_info.GetDimensions(input_node_dims_[input_name].data(), num_dims);
  }

  // get output names and shapes
  const auto num_output_nodes = session_->GetOutputCount();
  output_node_strings_.resize(num_output_nodes);
  output_node_names_.resize(num_output_nodes);
  output_node_dims_.clear();
  for (size_t i = 0; i < num_output_nodes; i++) {
    // get output node names
    const std::string output_name(session_->GetOutputName(i, allocator));
    //const auto& output_name = session_->GetOutputNames()[i];
    output_node_strings_[i] = output_name;
    output_node_names_[i] = output_node_strings_[i].data();

    // get output node types
    auto type_info = session_->GetOutputTypeInfo(i);
    auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
    size_t num_dims = tensor_info.GetDimensionsCount();
    output_node_dims_[output_name].resize(num_dims);
    tensor_info.GetDimensions(output_node_dims_[output_name].data(), num_dims);

    // the 0th dim depends on the batch size
    output_node_dims_[output_name].at(0) = -1;
  }
}

ONNXRuntime::~ONNXRuntime() {}

template <typename T>
ONNXRuntime::Tensor<T> ONNXRuntime::run(const std::vector<std::string>& input_names,
                                        Tensor<T>& input,
                                        const Tensor<long>& input_shapes,
                                        const std::vector<std::string>& output_names,
                                        unsigned long long batch_size) const {
  std::vector<Ort::Value> tensors_in;
  auto mem_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);

  //auto& input_dims = session_->GetInputShapes()[0];
  for (const auto& name : input_node_strings_) {
    auto iter = std::find(input_names.begin(), input_names.end(), name);
    if (iter == input_names.end())
      throw std::runtime_error("Input '" + name + " is not provided");
    auto input_pos = iter - input_names.begin();
    auto value = input.begin() + input_pos;
    std::vector<int64_t> input_dims;
    if (input_shapes.empty()) {
      input_dims = input_node_dims_.at(name);
      input_dims[0] = batch_size;
    } else {
      input_dims = input_shapes[input_pos];
      // rely on the given input_shapes to set the batch size
      if (input_dims[0] != batch_size)
        throw std::runtime_error("The first element of `input_shapes` (" + std::to_string(input_dims[0]) +
                                 ") does not match the given `batch_size` (" + std::to_string(batch_size) + ")");
    }
    auto expected_len = std::accumulate(input_dims.begin(), input_dims.end(), 1, std::multiplies<int64_t>());
    if (expected_len != (int64_t)value->size())
      throw std::runtime_error("Input array '" + name + "' has a wrong size of " + std::to_string(value->size()) +
                               ", expected " + std::to_string(expected_len));
    auto input_tensor =
        Ort::Value::CreateTensor<float>(mem_info, value->data(), value->size(), input_dims.data(), input_dims.size());
    assert(input_tensor.IsTensor());
    tensors_in.emplace_back(std::move(input_tensor));
  }

  // set output node names; will get all outputs if `output_names` is not provided
  std::vector<const char*> run_output_node_names;
  if (output_names.empty())
    run_output_node_names = output_node_names_;
  else
    for (const auto& name : output_names)
      run_output_node_names.push_back(name.data());

  // run
  auto output_tensors = session_->Run(Ort::RunOptions{nullptr},
                                      input_node_names_.data(),
                                      tensors_in.data(),
                                      tensors_in.size(),
                                      run_output_node_names.data(),
                                      run_output_node_names.size());

  // convert output to floats
  Tensor<T> outputs;
  for (auto& output_tensor : output_tensors) {
    assert(output_tensor.IsTensor());
    // get output shape
    auto tensor_info = output_tensor.GetTensorTypeAndShapeInfo();
    auto length = tensor_info.GetElementCount();

    auto floatarr = output_tensor.GetTensorMutableData<float>();
    outputs.emplace_back(floatarr, floatarr + length);
  }
  assert(outputs.size() == run_output_node_names.size());

  return outputs;
}

template ONNXRuntime::Tensor<float> ONNXRuntime::run(const std::vector<std::string>&,
                                                     Tensor<float>&,
                                                     const Tensor<long>&,
                                                     const std::vector<std::string>&,
                                                     unsigned long long) const;
