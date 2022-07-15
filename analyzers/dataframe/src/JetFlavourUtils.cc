#include "FCCAnalyses/JetFlavourUtils.h"
#include "FCCAnalyses/WeaverInterface.h"

#include <iostream>  //FIXME
#include <memory>

namespace FCCAnalyses {
  std::unique_ptr<WeaverInterface> gWeaver;

  namespace JetFlavourUtils {
    void setup_weaver(const std::string& onnx_filename, const std::string& json_filename) {
      gWeaver = std::make_unique<WeaverInterface>(onnx_filename, json_filename);
      std::cout << "Weaver initialised!!\n";
    }

    rv::RVec<rv::RVec<float> > compute_weights(const rv::RVec<Variables>& jets) {
      if (!gWeaver)
        throw std::runtime_error("Weaver interface is not initialised!");
      rv::RVec<rv::RVec<float> > out;
      if (jets.empty())
        return out;
      for (const auto& jet : jets) {
        if (jet.empty())  // no variables registered
          return out;
        Variables jet_sc_vars;
        size_t num_constits = jet.at(0).size();
        for (size_t i = 0; i < num_constits; ++i) {
          FCCAnalysesJetConstituentsData constit_vars;
          for (const auto& var : jet) {
            if (var.size() != num_constits)
              throw std::runtime_error("Invalid array of variables specified for each jet constituent!");
            constit_vars.push_back((float)var.at(i));
          }
          jet_sc_vars.push_back(constit_vars);
        }
        out.emplace_back(gWeaver->run(jet_sc_vars));
      }
      return out;
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses
