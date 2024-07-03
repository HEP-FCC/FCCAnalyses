#include "ONNXRuntime/ONNXRuntime.h"

#include <numeric>
#include <algorithm>

ONNXRuntime::ONNXRuntime(const std::string& model_path, const std::vector<std::string>& input_names)
    : env_(new Ort::Env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "onnx_runtime")),
      memoryInfo_(Ort::MemoryInfo::CreateCpu(OrtAllocatorType::OrtArenaAllocator, OrtMemTypeDefault)),
      input_names_(input_names) {
  if (model_path.empty())
    throw std::runtime_error("Path to ONNX model cannot be empty!");
  Ort::SessionOptions options;
  options.SetIntraOpNumThreads(1);
  session_ = std::make_unique<Ort::Session>(*env_, model_path.c_str(), options);

  Ort::AllocatorWithDefaultOptions allocator;
#if ORT_API_VERSION < 13
  // Before 1.13 we have to roll our own unique_ptr wrapper here
  auto allocDeleter = [&allocator](char* p) { allocator.Free(p); };
  using AllocatedStringPtr = std::unique_ptr<char, decltype(allocDeleter)>;
#endif

  // get input names and shapes
  input_node_dims_.clear();
  for (size_t i = 0; i < session_->GetInputCount(); ++i) {
#if ORT_API_VERSION < 13
  input_node_strings_.emplace_back(AllocatedStringPtr(session_->GetInputName(i, allocator), allocDeleter).release());
#else
  input_node_strings_.emplace_back(session_->GetInputNameAllocated(i, allocator).release());
#endif

    const auto& input_name = input_node_strings_[i];
    // get input shapes
    const auto nodeInfo = session_->GetInputTypeInfo(i);
    input_node_dims_[input_name] = nodeInfo.GetTensorTypeAndShapeInfo().GetShape();
  }

  // get output names and shapes
  output_node_dims_.clear();
  for (size_t i = 0; i < session_->GetOutputCount(); ++i) {
#if ORT_API_VERSION < 13
    output_node_strings_.emplace_back(AllocatedStringPtr(session_->GetOutputName(i, allocator), allocDeleter).release());
#else
    output_node_strings_.emplace_back(session_->GetOutputNameAllocated(i, allocator).release());
#endif

    // get output node names
    const auto& output_name = output_node_strings_[i];
    // get output node types
    const auto nodeInfo = session_->GetOutputTypeInfo(i);
    output_node_dims_[output_name] = nodeInfo.GetTensorTypeAndShapeInfo().GetShape();
    // the 0th dim depends on the batch size
    output_node_dims_[output_name].at(0) = -1;
  }
}

ONNXRuntime::~ONNXRuntime() {}

template <typename T>
ONNXRuntime::Tensor<T> ONNXRuntime::run(Tensor<T>& input,
                                        const Tensor<long>& input_shapes,
                                        unsigned long long batch_size) const {
  std::vector<Ort::Value> tensors_in;
  for (const auto& name : input_node_strings_) {
    auto input_pos = variablePos(name);
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
      throw std::runtime_error("Input array '" + std::string(name) + "' has a wrong size of " + std::to_string(value->size()) +
                               ", expected " + std::to_string(expected_len));
    auto input_tensor = Ort::Value::CreateTensor<float>(memoryInfo_, const_cast<float*>(value->data()), value->size(), input_dims.data(), input_dims.size());
    if (!input_tensor.IsTensor())
      throw std::runtime_error("Failed to create an input tensor for variable '" + std::string(name) + "'.");

    tensors_in.emplace_back(std::move(input_tensor));
  }

  // run the inference
  auto output_tensors = session_->Run(Ort::RunOptions{nullptr}, input_node_strings_.data(), tensors_in.data(), tensors_in.size(), output_node_strings_.data(), output_node_strings_.size());

  // convert output tensor to values
  Tensor<T> outputs;
  size_t i = 0;
  for (auto& output_tensor : output_tensors) {
    if (!output_tensor.IsTensor())
      throw std::runtime_error("(at least) inference output " + std::to_string(i) + " is not a tensor.");
    // get output shape
    auto tensor_info = output_tensor.GetTensorTypeAndShapeInfo();
    auto length = tensor_info.GetElementCount();

    auto floatarr = output_tensor.GetTensorMutableData<float>();
    outputs.emplace_back(floatarr, floatarr + length);
    ++i;
  }
  if (outputs.size() != session_->GetOutputCount())
    throw std::runtime_error("Number of outputs differ from the expected one: got " + std::to_string(outputs.size()) +
                             ", expected " + std::to_string(session_->GetOutputCount()));

  return outputs;
}

size_t ONNXRuntime::variablePos(const std::string& name) const {
  auto iter = std::find(input_names_.begin(), input_names_.end(), name);
  if (iter == input_names_.end())
    throw std::runtime_error("Input variable '" + name + " is not provided");
  return iter - input_names_.begin();
}

template ONNXRuntime::Tensor<float> ONNXRuntime::run(Tensor<float>&, const Tensor<long>&, unsigned long long) const;
