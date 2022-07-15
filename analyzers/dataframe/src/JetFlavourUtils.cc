#include "FCCAnalyses/JetFlavourUtils.h"
#include "FCCAnalyses/WeaverInterface.h"

#include <iostream>  //FIXME
#include <memory>

namespace FCCAnalyses {
  std::unique_ptr<WeaverInterface> gWeaver;

  namespace JetFlavourUtils {
    void setup_weaver(const std::string& onnx_filename, const std::string& json_filename) {
      gWeaver = std::make_unique<WeaverInterface>(onnx_filename, json_filename);
    }

    rv::RVec<rv::RVec<float> > compute_weights(const rv::RVec<Variables>& vars) {
      if (!gWeaver)
        throw std::runtime_error("Weaver interface is not initialised!");
      rv::RVec<rv::RVec<float> > out;
      if (vars.empty())  // no variables registered
        return out;
      size_t num_jets = vars.at(0).size();
      if (num_jets == 0)  // no jets to categorise
        return out;
      // transform a collection of {var1 -> {jet1 -> {constit1, constit2, ...}, jet2 -> {...}, ...}, var2 -> {...}}
      //      into a collection of {jet -> {constit1 -> {var1, var2, ...}, constit2 -> {...}, ...}}
      for (size_t i = 0; i < num_jets; ++i) {
        Variables jet_sc_vars;
        size_t num_constits = vars.at(0).at(i).size();
        for (size_t j = 0; j < num_constits; ++j) {
          FCCAnalysesJetConstituentsData constit_vars;
          for (size_t k = 0; k < vars.size(); ++k)
            constit_vars.push_back((float)vars.at(k).at(i).at(j));
          jet_sc_vars.push_back(constit_vars);
        }
        out.emplace_back(gWeaver->run(jet_sc_vars));
      }
      return out;
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses
