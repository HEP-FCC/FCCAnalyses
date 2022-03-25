#ifndef analyzers_dataframe_WeaverInterface_h
#define analyzers_dataframe_WeaverInterface_h

#include "ONNXRuntime.h"
#include "ROOT/RVec.hxx"

class WeaverInterface {
public:
  static WeaverInterface& get(const std::string& onnx_filename = "", const std::string& json_filename = "");

  WeaverInterface(const WeaverInterface&) = delete;
  WeaverInterface& operator=(const WeaverInterface&) = delete;

  using CollectionVars = ROOT::VecOps::RVec<float>;

  template <typename... Args>
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > operator()(Args&&... args) {
    return run(std::vector<ROOT::VecOps::RVec<CollectionVars> >{std::forward<Args>(args)...});
  }

private:
  explicit WeaverInterface(const std::string&, const std::string&);
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > run(const std::vector<ROOT::VecOps::RVec<CollectionVars> >&);

  struct PreprocessParams {
    struct VarInfo {
      VarInfo() {}
      VarInfo(float median, float norm_factor, float replace_inf_value, float lower_bound, float upper_bound, float pad)
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
    unsigned int min_length{0};
    unsigned max_length = 0;
    std::vector<std::string> var_names;
    std::unordered_map<std::string, VarInfo> var_info_map;
    VarInfo info(const std::string& name) const { return var_info_map.at(name); }
  };

  std::unique_ptr<ONNXRuntime> onnx_;
  std::vector<std::string> input_names_;
  std::vector<std::vector<long long> > input_shapes_;
  std::vector<unsigned int> input_sizes_;
  std::unordered_map<std::string, PreprocessParams> prep_info_map_;
  ONNXRuntime::Tensor<float> data_;
};

#endif
