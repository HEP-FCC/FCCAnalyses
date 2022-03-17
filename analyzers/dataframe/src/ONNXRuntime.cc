#include "ONNXRuntime.h"

#include "awkward/Content.h"
#include "awkward/io/json.h"

#include <fstream>

ONNXRuntime::ONNXRuntime(const std::string& model_path, const std::string& preprocess_json) :
    env_(new Ort::Env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "onnx_runtime")) {
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
  auto mem_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeDefault);
  alloc_ = std::make_unique<Ort::Allocator>(*session_, mem_info);

  std::cout << session_->GetInputCount() << std::endl;
  for (size_t i = 0; i < session_->GetInputCount(); ++i)
    std::cout << session_->GetInputName(i, *alloc_) << std::endl;

  std::cout << session_->GetOutputCount() << std::endl;
  for (size_t i = 0; i < session_->GetOutputCount(); ++i)
    std::cout << session_->GetOutputName(i, *alloc_) << std::endl;
}

ONNXRuntime& ONNXRuntime::get(const std::string& model_path, const std::string& preprocess_json) {
  static ONNXRuntime rt(model_path, preprocess_json);
  return rt;
}

ONNXRuntime::~ONNXRuntime() {}

ROOT::VecOps::RVec<float> ONNXRuntime::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) const {
  ROOT::VecOps::RVec<float> out;

  for (const auto& part : in) {
    out.push_back(0.);
  }
  return out;
}
