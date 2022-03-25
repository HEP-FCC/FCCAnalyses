#include "WeaverInterface.h"

#include "nlohmann/json.hpp"
#include <fstream>

WeaverInterface::WeaverInterface(const std::string& onnx_filename, const std::string& json_filename)
    : onnx_(new ONNXRuntime(onnx_filename)) {
  if (json_filename.empty())
    throw std::runtime_error("JSON preprocessed input file not specified!");

  // the preprocessing JSON was found ; extract the variables listing and all useful information
  std::ifstream json_file(json_filename);
  const auto json = nlohmann::json::parse(json_file);
  json.at("input_names").get_to(input_names_);
  for (const auto& input : input_names_) {
    const auto& group_params = json.at(input);
    auto& info = prep_info_map_[input];
    // retrieve the variables names
    group_params.at("var_names").get_to(info.var_names);
    // retrieve the shapes for all variables
    if (group_params.contains("var_length")) {
      info.min_length = group_params.at("var_length");
      info.max_length = info.min_length;
    } else {
      info.min_length = group_params.at("min_length");
      info.max_length = group_params.at("max_length");
      input_shapes_.push_back({1, (int64_t)info.var_names.size(), -1});
    }
    // for all variables, retrieve the allowed range
    const auto& var_info_params = group_params.at("var_infos");
    for (const auto& name : info.var_names) {
      const auto& var_params = var_info_params.at(name);
      info.var_info_map[name] =
          PreprocessParams::VarInfo(var_params.at("median"),
                                    var_params.at("norm_factor"),
                                    var_params.at("replace_inf_value"),
                                    var_params.at("lower_bound"),
                                    var_params.at("upper_bound"),
                                    var_params.contains("pad") ? (double)var_params.at("pad") : 0.);
    }
    // create data storage with a fixed size vector initialised with 0's
    const auto& len = input_sizes_.emplace_back(info.max_length * info.var_names.size());
    data_.emplace_back(len, 0);
  }
}

WeaverInterface& WeaverInterface::get(const std::string& onnx_filename, const std::string& json_filename) {
  static WeaverInterface interface(onnx_filename, json_filename);
  return interface;
}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > WeaverInterface::run(
    const std::vector<ROOT::VecOps::RVec<CollectionVars> >& features) {
  // features are of type {vars{jet{particles}}
  const auto& one_var = features.at(0);
  const size_t num_features = features.size(), num_jets = one_var.size();
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > output;
  output.reserve(num_jets);
  if (num_jets == 0 || one_var.empty())
    return output;

  // convert into a {jet{vars{particles}} collection
  std::vector<std::vector<std::vector<float> > > input_colls;
  input_colls.reserve(one_var.size());
  for (const auto& var : features) {
    for (size_t i = 0; i < one_var.size(); ++i) {
      auto& jet_vars = input_colls[i];  // {vars{particles}}
      jet_vars.reserve(num_features);
      for (size_t j = 0; j < num_features; ++j) {
        auto& components = jet_vars[j];  // {particles}
        components.reserve(features.at(j).at(i).size());
        for (size_t k = 0; k < features.at(j).at(i).size(); ++k)
          components[k] = features.at(j).at(i).at(k);
      }
    }
  }

  std::cout << "operator() -> " << data_.size() << std::endl;
  for (size_t i = 0; i < num_jets; ++i) {  // loop over candidates
    auto& result = output.emplace_back();
    for (size_t j = 0; j < num_features; ++j) {
      data_[j].resize(input_colls.at(i).at(j).size());
      for (size_t k = 0; k < input_colls.at(i).at(j).size(); ++k)
        data_[j][k] = input_colls.at(i).at(j).at(k);
    }
    result = onnx_->run<float>(data_)[0];
    std::cout << "(jet " << i << ") return values:";
    for (const auto& val : result)
      std::cout << " " << val;
    std::cout << std::endl;
  }
  return output;
}
