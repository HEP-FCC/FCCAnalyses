#ifndef FCCAnalyses_JetFlavourUtils_h
#define FCCAnalyses_JetFlavourUtils_h

#include <ROOT/RVec.hxx>

namespace FCCAnalyses {
  namespace JetFlavourUtils {
    namespace rv = ROOT::VecOps;
    using FCCAnalysesJetConstituentsData = rv::RVec<float>;
    using Variables = rv::RVec<FCCAnalysesJetConstituentsData>;

    /// Compute all weights given a collection of input variables
    /// \note This helper should not be used directly in RDataFrame examples
    rv::RVec<rv::RVec<float> > compute_weights(const rv::RVec<Variables>&);

    /// Setup the ONNXRuntime instance using Weaver-provided parameters
    void setup_weaver(const std::string&, const std::string&, const rv::RVec<std::string>&);
    /// Compute all weights given an unspecified collection of input variables
    template <typename... Args>
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_weights(Args&&... args) {
      return compute_weights(std::vector<Variables>{std::forward<Args>(args)...});
    }
    /// Get one specific weight previously computed
    rv::RVec<float> get_weight(const rv::RVec<rv::RVec<float> >&, int);
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses

#endif
