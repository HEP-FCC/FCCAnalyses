#include "FCCAnalyses/WeaverUtils.h"
#include "ONNXRuntime/WeaverInterface.h"

#include <memory>

namespace FCCAnalyses {
  std::unique_ptr<WeaverInterface> gWeaver2;

  namespace WeaverUtils {
    void setup_weaver(const std::string& onnx_filename,
                      const std::string& json_filename,
                      const rv::RVec<std::string>& vars) {
      gWeaver2 = std::make_unique<WeaverInterface>(onnx_filename, json_filename, vars);
    }

    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> compute_weights(
        const ROOT::VecOps::RVec<ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>>& vars) {
      if (!gWeaver2)
        throw std::runtime_error("Weaver interface is not initialised!");
      ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> out;
      if (vars.empty())  // no variables registered
        return out;
      size_t num_obj = vars.at(0).size();
      if (num_obj == 0)  // no objects to categorise
        return out;
      // transform a collection of {var1 -> {object1 -> {input1, input2, ...}, object2 -> {...}, ...}, var2 -> {...}}
      //      into a collection of {object -> {var1 -> {input1, input2, ...}, var2 -> {...}, ...}}

      for (size_t i = 0; i < num_obj; ++i) {
        ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> obj_sc_vars;
        size_t num_inputs = vars.at(0).at(i).size();
        for (size_t k = 0; k < vars.size(); ++k) {
          ROOT::VecOps::RVec<float> input_vars;
          for (size_t j = 0; j < num_inputs; ++j)
            input_vars.push_back((float)vars.at(k).at(i).at(j));
          obj_sc_vars.push_back(input_vars);
        }
        out.emplace_back(gWeaver2->run(obj_sc_vars));
      }
      return out;
    }

    ROOT::VecOps::RVec<float> get_weight(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>& objects_weights,
                                         int weight) {
      if (weight < 0)
        throw std::runtime_error("Invalid index requested for object weight " + std::to_string(weight) + ".");
      ROOT::VecOps::RVec<float> out;
      for (const auto& object_weights : objects_weights) {
        if (weight >= object_weights.size())
          throw std::runtime_error("Flavour weight index exceeds the number of weights registered.");
        out.emplace_back(object_weights.at(weight));
      }
      return out;
    }
  }  // namespace WeaverUtils
}  // namespace FCCAnalyses
