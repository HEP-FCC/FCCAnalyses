#include "ONNXRuntime.h"

#include "awkward/Content.h"
#include "awkward/io/json.h"

#include <fstream>

ONNXRuntime::ONNXRuntime(const std::string& model_path, const std::string& preprocess_json) {
  if (!preprocess_json.empty()) {
    // the preprocessing JSON was found ; extract the variables listing and all useful information
    std::ifstream json_file(preprocess_json);
    std::stringstream json_content;
    json_content << json_file.rdbuf();
    const std::shared_ptr<awkward::Form> json = awkward::Form::fromjson(json_content.str());
    for (const auto& key : json->keys())
      std::cout << ">> " << key << std::endl;
  }
}

ONNXRuntime::~ONNXRuntime() {}

ROOT::VecOps::RVec<float> ONNXRuntime::operator()(ROOT::VecOps::RVec<int> in) {
  ROOT::VecOps::RVec<float> out;
  return out;
}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > ONNXRuntime::run() const {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > out;
  return out;
}

ClassImp(ONNXRuntime)
