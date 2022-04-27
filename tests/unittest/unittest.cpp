
#include "catch2/catch_test_macros.hpp"
#include "myUtils.h"

TEST_CASE("myUtils", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, 4.5, 1e30};
  REQUIRE(myUtils::get_Npos(in1) == 3);

}

