#ifndef FCCAnalyses_JetFlavourUtils_h
#define FCCAnalyses_JetFlavourUtils_h

#include <ROOT/RVec.hxx>

namespace FCCAnalyses {
  namespace JetFlavourUtils {
    void setup_weaver(const std::string&, const std::string&);

    using Variables = std::vector<std::vector<float> >;

    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_weights(const std::vector<Variables>&);

    template <typename... Args>
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_weights(Args&&... args) {
      printf("%s -> %zu\n", __PRETTY_FUNCTION__, std::vector<Variables>{std::forward<Args>(args)...}.size());
      return get_weights(std::vector<Variables>{std::forward<Args>(args)...});
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses

#endif
