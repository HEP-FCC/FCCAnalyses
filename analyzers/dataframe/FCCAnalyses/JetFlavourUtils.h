#ifndef FCCAnalyses_JetFlavourUtils_h
#define FCCAnalyses_JetFlavourUtils_h

#include <ROOT/RVec.hxx>

namespace FCCAnalyses {
  namespace JetFlavourUtils {
    namespace rv = ROOT::VecOps;
    using FCCAnalysesJetConstituentsData = rv::RVec<float>;
    using Variables = rv::RVec<FCCAnalysesJetConstituentsData>;

    void setup_weaver(const std::string&, const std::string&, const rv::RVec<std::string>&);

    rv::RVec<rv::RVec<float> > compute_weights(const rv::RVec<Variables>&);

    template <typename... Args>
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_weights(Args&&... args) {
      return compute_weights(std::vector<Variables>{std::forward<Args>(args)...});
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses

#endif
