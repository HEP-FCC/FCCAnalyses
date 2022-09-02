#include "FCCAnalyses/myUtils.h"

#include <catch2/catch_test_macros.hpp>
#include <catch2/benchmark/catch_benchmark.hpp>

TEST_CASE("isPV", "[basics]") {
  edm4hep::ReconstructedParticleData p;
  p.tracks_begin = 0;
  ROOT::VecOps::RVec<int> index1 = {3, 0, 7};
  ROOT::VecOps::RVec<int> index2 = {3, 1, 7};

  BENCHMARK("isPV") {
        return FCCAnalyses::myUtils::isPV(p, index1);
  };
}
