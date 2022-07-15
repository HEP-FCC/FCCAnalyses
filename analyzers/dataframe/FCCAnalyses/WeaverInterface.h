#ifndef FCCAnalyses_WeaverInterface_h
#define FCCAnalyses_WeaverInterface_h

#include "FCCAnalyses/ONNXRuntime.h"
#include "ROOT/RVec.hxx"

namespace FCCAnalyses {
  namespace rv = ROOT::VecOps;

  class WeaverInterface {
  public:
    explicit WeaverInterface(const std::string& onnx_filename = "", const std::string& json_filename = "");

    using ConstituentVars = rv::RVec<float>;

    rv::RVec<float> run(const rv::RVec<ConstituentVars>&);
    /*template <typename... Args>
    rv::RVec<float> operator()(Args&&... args) {
      return run(rv::RVec<ConstituentVars>{std::forward<Args>(args)...});
    }*/

  private:
    struct PreprocessParams {
      struct VarInfo {
        VarInfo() {}
        VarInfo(
            float median, float norm_factor, float replace_inf_value, float lower_bound, float upper_bound, float pad)
            : center(median),
              norm_factor(norm_factor),
              replace_inf_value(replace_inf_value),
              lower_bound(lower_bound),
              upper_bound(upper_bound),
              pad(pad) {}

        float center{0.};
        float norm_factor{1.};
        float replace_inf_value{0.};
        float lower_bound{-5.};
        float upper_bound{5.};
        float pad{0.};
      };
      size_t min_length{0}, max_length{0};
      std::vector<std::string> var_names;
      std::unordered_map<std::string, VarInfo> var_info_map;
      VarInfo info(const std::string& name) const { return var_info_map.at(name); }
    };
    std::vector<float> center_norm_pad(const std::vector<float>& input,
                                       float center,
                                       float scale,
                                       size_t min_length,
                                       size_t max_length,
                                       float pad_value = 0,
                                       float replace_inf_value = 0,
                                       float min = 0,
                                       float max = -1);

    std::unique_ptr<ONNXRuntime> onnx_;
    std::vector<std::string> input_names_;
    ONNXRuntime::Tensor<long> input_shapes_;
    std::vector<unsigned int> input_sizes_;
    std::unordered_map<std::string, PreprocessParams> prep_info_map_;
    ONNXRuntime::Tensor<float> data_;
  };
}  // namespace FCCAnalyses

#endif
