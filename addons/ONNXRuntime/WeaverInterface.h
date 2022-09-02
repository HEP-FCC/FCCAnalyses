#ifndef ONNXRuntime_WeaverInterface_h
#define ONNXRuntime_WeaverInterface_h

#include "ONNXRuntime/ONNXRuntime.h"
#include "ROOT/RVec.hxx"

namespace rv = ROOT::VecOps;

class WeaverInterface {
public:
  using ConstituentVars = rv::RVec<float>;

  /// Initialise an inference model from Weaver output ONNX/JSON files and
  /// a list of variables to be provided for each event/jet
  explicit WeaverInterface(const std::string& onnx_filename = "",
                           const std::string& json_filename = "",
                           const rv::RVec<std::string>& vars = {});

  /// Run inference given a list of jet constituents variables
  rv::RVec<float> run(const rv::RVec<ConstituentVars>&);

private:
  struct PreprocessParams {
    struct VarInfo {
      VarInfo() {}
      VarInfo(float imedian,
              float inorm_factor,
              float ireplace_inf_value,
              float ilower_bound,
              float iupper_bound,
              float ipad)
          : center(imedian),
            norm_factor(inorm_factor),
            replace_inf_value(ireplace_inf_value),
            lower_bound(ilower_bound),
            upper_bound(iupper_bound),
            pad(ipad) {}

      float center{0.};
      float norm_factor{1.};
      float replace_inf_value{0.};
      float lower_bound{-5.};
      float upper_bound{5.};
      float pad{0.};
    };
    std::string name;
    size_t min_length{0}, max_length{0};
    std::vector<std::string> var_names;
    std::unordered_map<std::string, VarInfo> var_info_map;
    VarInfo info(const std::string& name) const { return var_info_map.at(name); }
    void dumpVars() const;
  };
  std::vector<float> center_norm_pad(const rv::RVec<float>& input,
                                     float center,
                                     float scale,
                                     size_t min_length,
                                     size_t max_length,
                                     float pad_value = 0,
                                     float replace_inf_value = 0,
                                     float min = 0,
                                     float max = -1);
  size_t variablePos(const std::string&) const;

  std::unique_ptr<ONNXRuntime> onnx_;
  std::vector<std::string> variables_names_;
  ONNXRuntime::Tensor<long> input_shapes_;
  std::vector<unsigned int> input_sizes_;
  std::unordered_map<std::string, PreprocessParams> prep_info_map_;
  ONNXRuntime::Tensor<float> data_;
};

#endif
