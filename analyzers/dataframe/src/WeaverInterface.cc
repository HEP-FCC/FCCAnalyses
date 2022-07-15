#include "FCCAnalyses/WeaverInterface.h"

#include "nlohmann/json.hpp"
#include <fstream>
#include <iostream>

namespace FCCAnalyses {
  WeaverInterface* gWeaverInterface = nullptr;

  WeaverInterface::WeaverInterface(const std::string& onnx_filename,
                                   const std::string& json_filename,
                                   const rv::RVec<std::string>& vars)
      : onnx_(new ONNXRuntime(onnx_filename)), variables_names_(vars.begin(), vars.end()) {
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
      if (group_params.contains("var_length"))
        info.min_length = info.max_length = group_params.at("var_length");
      else {
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
    std::cout << __PRETTY_FUNCTION__ << std::endl;
  }

  std::vector<float> WeaverInterface::center_norm_pad(const rv::RVec<float>& input,
                                                      float center,
                                                      float scale,
                                                      size_t min_length,
                                                      size_t max_length,
                                                      float pad_value,
                                                      float replace_inf_value,
                                                      float min,
                                                      float max) {
    if (min > pad_value || pad_value > max)
      throw std::runtime_error("Pad value not within (min, max) range");
    if (min_length > max_length)
      throw std::runtime_error("Variable length mismatch (min_length >= max_length)");

    auto ensure_finitude = [](const float in, const float replace_val) {
      if (!std::isfinite(in))
        return replace_val;
      return in;
    };

    size_t target_length = std::clamp(input.size(), min_length, max_length);
    std::vector<float> out(target_length, pad_value);
    for (size_t i = 0; i < input.size() && i < target_length; ++i)
      out[i] = std::clamp((ensure_finitude(input[i], replace_inf_value) - center) * scale, min, max);
    return out;
  }

  rv::RVec<float> WeaverInterface::run(const rv::RVec<ConstituentVars>& constituents) {
    rv::RVec<float> output;
    for (size_t i = 0; i < input_names_.size(); ++i) {
      const auto& name = input_names_.at(i);
      const auto& params = prep_info_map_.at(name);
      std::cout << ">>>> nm " << i << "=" << name << std::endl;
      auto& values = data_[i];
      values.resize(input_sizes_.at(i));
      std::fill(values.begin(), values.end(), 0);
      size_t k = 0;
      size_t it_pos = 0;
      params.dumpVars();
      for (const auto& var_name : params.var_names) {  // transform and add the proper amount of padding
        const auto& var_info = params.info(var_name);
        auto val = center_norm_pad(constituents.at(k),
                                   var_info.center,
                                   var_info.norm_factor,
                                   params.min_length,
                                   params.max_length,
                                   var_info.pad,
                                   var_info.replace_inf_value,
                                   var_info.lower_bound,
                                   var_info.upper_bound);
        std::copy(val.begin(), val.end(), values.begin() + it_pos);
        it_pos += val.size();
        if (k == 0 && !input_shapes_.empty())
          input_shapes_[i][2] = val.size();
        ++k;
      }
      values.resize(it_pos);
    }
    std::cout << "before running for jet " << i << std::endl;
    result = onnx_->run<float>(data_, input_shapes_)[0];
    std::cout << "after running for jet " << i << ", result: " << result << std::endl;
  }

  // convert into a {jet{vars{particles}} collection
  /*for (size_t i = 0; i < num_jets; ++i) {  // loop over candidates
    auto& result = output.emplace_back();
    for (size_t j = 0; j < num_features; ++j) {
      data_[j].resize(features.at(j).at(i).size());
      for (size_t k = 0; k < features.at(j).at(i).size(); ++k)
        data_[j][k] = features.at(j).at(i).at(k);
    }
    result = onnx_->run<float>(data_)[0];
    std::cout << "(jet " << i << ") return values:";
    for (const auto& val : result)
      std::cout << " " << val;
    std::cout << std::endl;
  }*/
    return output;
  }

  void WeaverInterface::PreprocessParams::dumpVars() const {
    std::cout << "List of variables for this preprocessing parameter: ";
    for (size_t i = 0; i < var_names.size(); ++i)
      std::cout << (i > 0 ? ", " : "") << var_names.at(i);
    std::cout << std::endl;
  }
}  // namespace FCCAnalyses
