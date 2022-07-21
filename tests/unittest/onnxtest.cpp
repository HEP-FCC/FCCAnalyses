#include "FCCAnalyses/JetFlavourUtils.h"

#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>

TEST_CASE("flavtagging", "[onnx]") {
  FCCAnalyses::JetFlavourUtils::setup_weaver(
      "/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx",
      "/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/preprocess.json",
      {"pfcand_e", "pfcand_theta", "pfcand_phi", "pfcand_pid", "pfcand_charge"});

  const auto out = FCCAnalyses::JetFlavourUtils::compute_weights(
      {{{1.38285, 19.3685}}, {{1.97631, 1.7312}}, {{-1.50803, -1.36646}}, {{0, 0}}, {{1, -1}}});

  REQUIRE(out.size() == 1);                                    // single jet -> single collection of weights
  REQUIRE(out.at(0).size() == 5);                              // weaver model-specific feature
  REQUIRE(ROOT::VecOps::Sum(out.at(0)) == Catch::Approx(1.));  // all weights should add up to unity
}
