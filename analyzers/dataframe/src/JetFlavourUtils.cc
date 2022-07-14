#include "FCCAnalyses/JetFlavourUtils.h"
#include "FCCAnalyses/WeaverInterface.h"

#include <iostream>  //FIXME
#include <memory>

namespace FCCAnalyses {

  //std::unique_ptr<WeaverInterface> gWeaver;
  WeaverInterface* gWeaver;

  namespace JetFlavourUtils {
    void setup_weaver(const std::string& onnx_filename, const std::string& json_filename) {
      //gWeaver = std::make_unique<WeaverInterface>(onnx_filename, json_filename);
      gWeaver = new WeaverInterface(onnx_filename, json_filename);
      std::cout << "Weaver initialised!!\n";
    }

    ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_weights(
        const std::vector<std::vector<std::vector<float> > >& features) {
      if (!gWeaver) {
        std::cout << "prout\n";
        throw std::runtime_error("Weaver interface is not initialised!");
      }
      std::cout << "starting inference\n";
      return (*gWeaver)(features);
    }
  }  // namespace JetFlavourUtils
}  // namespace FCCAnalyses
