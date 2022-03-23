#include "WeaverInterface.h"

WeaverInterface::WeaverInterface(const std::string& onnx_filename)
  : onnx_(new ONNXRuntime(onnx_filename)) {
  /*if (!preprocess_json.empty()) {
    // the preprocessing JSON was found ; extract the variables listing and all useful information
    std::ifstream json_file(preprocess_json);
    std::stringstream json_content;
    json_content << json_file.rdbuf();
    const std::shared_ptr<awkward::Form> json = awkward::Form::fromjson(json_content.str());
    for (const auto& key : json->keys())
      std::cout << ">> " << key << std::endl;
  }*/
}

WeaverInterface& WeaverInterface::get(const std::string& onnx_filename) {
  static WeaverInterface interface(onnx_filename);
  return interface;
}

ROOT::VecOps::RVec<float> WeaverInterface::operator()(std::vector<ROOT::VecOps::RVec<float> > in) const {
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

  const auto output_values = onnx_->run(input_values);

  return ROOT::VecOps::RVec<float>(output_values);
}

ROOT::VecOps::RVec<float> WeaverInterface::operator()(ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > points, ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > features, ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > mask) const {
  std::vector<std::vector<float> > input_values;
  input_values.reserve(3);
  for (const auto& point : points) {
    for (const auto& it : point)
      input_values[0].emplace_back(it);
  }
  for (const auto& feature : features) {
    for (const auto& it : feature)
      input_values[1].emplace_back(it);
  }
  for (const auto& msk : mask) {
    for (const auto& it : msk)
      input_values[2].emplace_back(it);
  }
  const auto output_values = onnx_->run(input_values);
  return ROOT::VecOps::RVec<float>(output_values);
}
