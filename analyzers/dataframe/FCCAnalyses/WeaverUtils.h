#ifndef FCCAnalyses_WEAVERUTILS_h
#define FCCAnalyses_WEAVERUTILS_h

#include <ROOT/RVec.hxx>

namespace FCCAnalyses {
  namespace WeaverUtils {

    /// Compute all weights given a collection of input variables
    /// \note This helper should not be used directly in RDataFrame examples
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> compute_weights(
        const ROOT::VecOps::RVec<ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>>&);

    /// Setup the ONNXRuntime instance using Weaver-provided parameters
    void setup_weaver(const std::string&, const std::string&, const ROOT::VecOps::RVec<std::string>&);

    /// Compute all weights given an unspecified collection of input variables
    template <typename... Args>
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> get_weights(Args&&... args) {
      return compute_weights(std::vector<ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>>{std::forward<Args>(args)...});
    }
    /// Get one specific weight previously computed
    ROOT::VecOps::RVec<float> get_weight(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>&, int);
  }  // namespace WeaverUtils
}  // namespace FCCAnalyses

#endif
