#include "FCCAnalyses/JetFlavourUtils.h"

#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>

// macros for input test files, can be moved in an external include
#define _STR(x) #x
#define TOKENISE(x) _STR(x)
#define TEST_FILE(file) TOKENISE(TEST_INPUT_DATA_DIR) "/" file

TEST_CASE("flavtagging", "[onnx]") {
  FCCAnalyses::JetFlavourUtils::setup_weaver(TEST_FILE("fccee_flavtagging_dummy.onnx"),
                                             TEST_FILE("preprocess.json"),
                                             {"pfcand_e", "pfcand_theta", "pfcand_phi", "pfcand_pid", "pfcand_charge"}, 1);

  unsigned int slot = 0;
  const auto out = FCCAnalyses::JetFlavourUtils::compute_weights(slot, 
      {{{1.38285, 19.3685}}, {{1.97631, 1.7312}}, {{-1.50803, -1.36646}}, {{0, 0}}, {{1, -1}}});

  REQUIRE(out.size() == 1);                                    // single jet -> single collection of weights
  REQUIRE(out.at(0).size() == 5);                              // weaver model-specific feature
  REQUIRE(ROOT::VecOps::Sum(out.at(0)) == Catch::Approx(1.));  // all weights should add up to unity
}
