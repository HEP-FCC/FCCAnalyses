#include "ONNXRuntime.h"

#include "awkward/Content.h"
#include "awkward/io/json.h"

#include <fstream>
#include <iostream>

ONNXRuntime::ONNXRuntime(const std::string& model_path, const std::string& preprocess_json) :
    env_(new Ort::Env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "onnx_runtime")) {
  std::cout << "building new ONNXRuntime object" << std::endl;
  /*if (!preprocess_json.empty()) {
    // the preprocessing JSON was found ; extract the variables listing and all useful information
    std::ifstream json_file(preprocess_json);
    std::stringstream json_content;
    json_content << json_file.rdbuf();
    const std::shared_ptr<awkward::Form> json = awkward::Form::fromjson(json_content.str());
    for (const auto& key : json->keys())
      std::cout << ">> " << key << std::endl;
  }*/
  Ort::SessionOptions options;
  auto path = model_path;
  session_ = std::make_unique<Ort::Experimental::Session>(*env_, path, options);
  //auto mem_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeDefault);
  //alloc_ = std::make_unique<Ort::Allocator>(*session_, mem_info);
  //alloc_.reset(new Ort::AllocatorWithDefaultOptions);
  Ort::AllocatorWithDefaultOptions alloc;

  std::cout << session_->GetInputCount() << std::endl;
  for (size_t i = 0; i < session_->GetInputCount(); ++i)
    std::cout << session_->GetInputName(i, alloc) << std::endl;

  std::cout << session_->GetOutputCount() << std::endl;
  for (size_t i = 0; i < session_->GetOutputCount(); ++i)
    std::cout << session_->GetOutputName(i, alloc) << std::endl;
}

ONNXRuntime& ONNXRuntime::get(const std::string& model_path, const std::string& preprocess_json) {
  static ONNXRuntime rt(model_path, preprocess_json);
  return rt;
}

ONNXRuntime::~ONNXRuntime() {}

ROOT::VecOps::RVec<float> ONNXRuntime::operator()(std::vector<ROOT::VecOps::RVec<float> > in) const {
  ROOT::VecOps::RVec<float> out;
  if (in.empty())
    throw std::runtime_error("Invalid size for the input collection: " + std::to_string(in.size()));

  // convert the input vector{var: RVec<float>} into a vector{var: vector{part: float}}
  std::vector<std::vector<float> > input_values, input_vars;
  for (const auto& var : in) {
    std::vector<float> vals;
    for (const auto& it : var)
      vals.emplace_back(it);
    input_vars.emplace_back(vals);
  }
  for (size_t ipart = 0; ipart != in.at(0).size(); ++ipart) {
    std::vector<float> vals;
    for (const auto& var : in)
      vals.emplace_back(var.at(ipart));
    input_values.emplace_back(vals);
  }

  std::cout << "operator() -> " << input_values.size() << std::endl;

  /*std::cout << "input: \n";
  for (const auto& iv : input_vars) {
    std::cout << " >>>";
    for (const auto& v : iv)
      std::cout << " " << v;
    std::cout << "\n";
  }*/

  // convert the input values to tensors
  std::vector<Ort::Value> tensors_in;
  //for (size_t i = 0; i < session_->GetOutputCount(); ++i) {
  for (const auto& val : input_vars) {
    auto tensor = Ort::Experimental::Value::CreateTensor<float>(const_cast<float*>(val.data()), val.size(), session_->GetInputShapes()[0]);
    if (!tensor.IsTensor())
      throw std::runtime_error("Failed to create a tensor for input values");
    tensors_in.emplace_back(std::move(tensor));
  }
  std::cout << ">>> " << tensors_in.size() << std::endl;

  // run the inference
  auto tensors_out = session_->Run(session_->GetInputNames(), tensors_in, session_->GetOutputNames());

  // convert output to floats
  std::vector<std::vector<float> > output_values;
  for (auto& tensor : tensors_out) {
    if (!tensor.IsTensor())
      continue; //FIXME
    // get output shape
    const auto length = tensor.GetTensorTypeAndShapeInfo().GetElementCount();
    const auto floatarr = tensor.GetTensorMutableData<float>();
    output_values.emplace_back(floatarr, floatarr + length);
  }

  return ROOT::VecOps::RVec<float>(output_values.at(0));
}
