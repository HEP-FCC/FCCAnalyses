#include "catch2/catch_test_macros.hpp"
#include "FCCAnalyses/JetFlavourUtils.h"

#include <iostream>

TEST_CASE("flavtagging", "") {
  FCCAnalyses::JetFlavourUtils::setup_weaver(
      "/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx",
      "/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/preprocess.json");

  const auto out = FCCAnalyses::JetFlavourUtils::compute_weights(
      {{{1.2707, 19.1198}, {1.38285, 19.3685}, {1.97631, 1.7312}, {-1.50803, -1.36646}, {0., 0.}, {1., -1.}}});

  std::cout << "out: " << out.size() << " := " << out << std::endl;
}
