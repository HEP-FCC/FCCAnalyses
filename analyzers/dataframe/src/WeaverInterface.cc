#include "WeaverInterface.h"

#include "nlohmann/json.hpp"
#include <fstream>

WeaverInterface::WeaverInterface(const std::string& onnx_filename, const std::string& json_filename, int npoints, int nfeatures)
  : onnx_(new ONNXRuntime(onnx_filename)), npoints_(npoints), nfeatures_(nfeatures) {
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
      info.var_info_map[name] = PreprocessParams::VarInfo(var_params.at("median"),
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

WeaverInterface& WeaverInterface::get(const std::string& onnx_filename, const std::string& json_filename, int npoints, int nfeatures) {
  static WeaverInterface interface(onnx_filename, json_filename, npoints, nfeatures);
  return interface;
}

ROOT::VecOps::RVec<float> WeaverInterface::run(const std::vector<ROOT::VecOps::RVec<float> >& points, const std::vector<ROOT::VecOps::RVec<float> >& features) {
  /*input_values.reserve(3);
  for (const auto& point : points) {
    for (const auto& it : point)
      input_values[0].emplace_back(it);
  }
  for (const auto& feature : features) {
    for (const auto& it : feature)
      input_values[1].emplace_back(it);
  }
  //for (const auto& msk : mask) {
  //  for (const auto& it : msk)
  //    input_values[2].emplace_back(it);
  //}*/
  std::vector<float> output_values;
  for (size_t i = 0; i < features.at(0).size(); ++i) { // loop over candidates
    data_[i].resize(features.at(0).size());
    for (size_t j = 0; j < features.size(); ++j) {
      data_[i][j] = features.at(j).at(i);
    }
    output_values.emplace_back(onnx_->run<float>(data_)[0][0]);
  }
  return ROOT::VecOps::RVec<float>(output_values);
}
