#include "FCCAnalyses/Algorithms.h"

#include "catch2/catch_test_macros.hpp"
#include <catch2/benchmark/catch_benchmark.hpp>


TEST_CASE("calculate_thrust", "[algorithms]") {
  ROOT::VecOps::RVec<float> x {0., 1., 3., 7., 11., 3.};
  ROOT::VecOps::RVec<float> y {0., -1., 3., -7., -11., .3};
  ROOT::VecOps::RVec<float> z {5., -3., 1., 4., 2., -4};

  BENCHMARK("calculate_thrust short vector") {
        return FCCAnalyses::Algorithms::calculate_thrust()(x, y, z);
  };
}
