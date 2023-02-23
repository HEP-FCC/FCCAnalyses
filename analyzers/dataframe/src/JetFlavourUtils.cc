#include "FCCAnalyses/JetFlavourUtils.h"
#include "ONNXRuntime/WeaverInterface.h"

#include <memory>

namespace FCCAnalyses {
  std::vector<WeaverInterface *> gWeavers;
  bool isSetup = false;

  namespace JetFlavourUtils {
    void setup_weaver(const std::string& onnx_filename,
                      const std::string& json_filename,
                      const rv::RVec<std::string>& vars,
                      const unsigned int nSlots) {
      for(unsigned int i=0; i<nSlots; i++) {
        WeaverInterface *gWeaver = new WeaverInterface(onnx_filename, json_filename, vars);
        gWeavers.push_back(gWeaver);
      }
      isSetup = true;
    }

    rv::RVec<rv::RVec<float> > compute_weights(unsigned int slot, const rv::RVec<Variables>& vars) {
      if (!isSetup)
        throw std::runtime_error("Weaver interface is not initialised!");
      rv::RVec<rv::RVec<float> > out;
      if (vars.empty())  // no variables registered
        return out;
      size_t num_jets = vars.at(0).size();
      if (num_jets == 0)  // no jets to categorise
        return out;
      // transform a collection of {var1 -> {jet1 -> {constit1, constit2, ...}, jet2 -> {...}, ...}, var2 -> {...}}
      //      into a collection of {jet -> {var1 -> {constit1, constit2, ...}, var2 -> {...}, ...}}
      for (size_t i = 0; i < num_jets; ++i) {
        Variables jet_sc_vars;
        size_t num_constits = vars.at(0).at(i).size();
        for (size_t k = 0; k < vars.size(); ++k) {
          FCCAnalysesJetConstituentsData constit_vars;
          for (size_t j = 0; j < num_constits; ++j)
            constit_vars.push_back((float)vars.at(k).at(i).at(j));
          jet_sc_vars.push_back(constit_vars);
        }
        out.emplace_back(gWeavers.at(slot)->run(jet_sc_vars));
      }
      return out;
    }

    rv::RVec<float> get_weight(const rv::RVec<rv::RVec<float> >& jets_weights, int weight) {
      if (weight < 0)
        throw std::runtime_error("Invalid index requested for jet flavour weight.");
      rv::RVec<float> out;
      for (const auto& jet_weights : jets_weights) {
        if (weight >= jet_weights.size())
          throw std::runtime_error("Flavour weight index exceeds the number of weights registered.");
        out.emplace_back(jet_weights.at(weight));
      }
      return out;
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses
