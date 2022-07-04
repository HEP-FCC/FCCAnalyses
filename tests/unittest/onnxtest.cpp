#include "catch2/catch_test_macros.hpp"
#include "FCCAnalyses/WeaverInterface.h"

#include <iostream>

TEST_CASE("flavtagging", "") {
  WeaverInterface::get("/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx",
                       "/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/preprocess.json");
  std::vector<std::vector<float> > in;

  auto out = WeaverInterface::get()(in);
  std::cout << out.size() << std::endl;
}
