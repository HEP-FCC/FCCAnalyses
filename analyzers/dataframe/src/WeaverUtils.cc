#include "FCCAnalyses/WeaverUtils.h"
#include "ONNXRuntime/WeaverInterface.h"

#include <memory>

namespace FCCAnalyses {
  std::unique_ptr<WeaverInterface> gWeaver;

  namespace WeaverUtils {
    void setup_weaver(const std::string& onnx_filename,
                      const std::string& json_filename,
                      const rv::RVec<std::string>& vars) {
      gWeaver = std::make_unique<WeaverInterface>(onnx_filename, json_filename, vars);
    }

    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > compute_weights(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>& vars) {
      if (!gWeaver)
        throw std::runtime_error("Weaver interface is not initialised!");
      ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > out;
      if (vars.empty())  // no variables registered
        return out;
      size_t num_obj = vars.at(0).size();
      if (num_obj == 0)  // no jets to categorise
        return out;
      // transform a collection of {var1 -> {jet1 -> {constit1, constit2, ...}, jet2 -> {...}, ...}, var2 -> {...}}
      //      into a collection of {jet -> {var1 -> {constit1, constit2, ...}, var2 -> {...}, ...}}


      for (size_t i = 0; i < num_obj; ++i) {
        ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> obj_sc_vars;
        size_t num_constits = vars.at(0).at(i).size();
        for (size_t k = 0; k < vars.size(); ++k) {
            ROOT::VecOps::RVec<float> constit_vars;
          for (size_t j = 0; j < num_constits; ++j)
            constit_vars.push_back((float)vars.at(k).at(i).at(j));
          obj_sc_vars.push_back(constit_vars);
        }
        out.emplace_back(gWeaver->run(obj_sc_vars));
      }
      return out;
    }

    ROOT::VecOps::RVec<float> get_weight(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> >& jets_weights, int weight) {
      if (weight < 0)
        throw std::runtime_error("Invalid index requested for jet flavour weight.");
      ROOT::VecOps::RVec<float> out;
      for (const auto& jet_weights : jets_weights) {
        if (weight >= jet_weights.size())
          throw std::runtime_error("Flavour weight index exceeds the number of weights registered.");
        out.emplace_back(jet_weights.at(weight));
      }
      return out;
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses
