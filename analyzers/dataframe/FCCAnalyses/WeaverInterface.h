#ifndef analyzers_dataframe_WeaverInterface_h
#define analyzers_dataframe_WeaverInterface_h

#include "ONNXRuntime.h"
#include "ROOT/RVec.hxx"

class WeaverInterface {
public:
  static WeaverInterface& get(const std::string& onnx_filename = "",
                              const std::string& json_filename = "",
                              int npoints = 0,
                              int nfeatures = 0);

  WeaverInterface(const WeaverInterface&) = delete;
  WeaverInterface& operator=(const WeaverInterface&) = delete;

  template <typename... Args>
  ROOT::VecOps::RVec<float> operator()(Args&&... args) {
    std::vector<ROOT::VecOps::RVec<float> > vars{std::forward<Args>(args)...};
    std::vector<ROOT::VecOps::RVec<float> > points(vars.begin(), vars.begin() + npoints_),
        features(vars.begin() + npoints_, vars.begin() + npoints_ + nfeatures_);
    return run(points, features);
  }

private:
  explicit WeaverInterface(const std::string&, const std::string&, int, int);
  ROOT::VecOps::RVec<float> run(const std::vector<ROOT::VecOps::RVec<float> >&,
                                const std::vector<ROOT::VecOps::RVec<float> >&);

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
  int npoints_;
  int nfeatures_;
};

#endif
