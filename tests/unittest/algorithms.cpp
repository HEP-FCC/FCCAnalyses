#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>
#include "Algorithms.h"

TEST_CASE("Mass", "[algorithms]") {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pVec;
  edm4hep::ReconstructedParticleData p;
  p.momentum.x = 1.;
  p.momentum.y = -1.;
  p.momentum.z = 1.;
  p.energy = 2.;
  pVec.push_back(p);
  REQUIRE(Algorithms::getMass(pVec) == Catch::Approx( 1. ));
}


TEST_CASE("AxisCosThetaInVec", "[algorithms]") {
  ROOT::VecOps::RVec<float> ax {0., 1., 0., 0., 0., 0.};
  ROOT::VecOps::RVec<float> x {1., 0., -1};
  ROOT::VecOps::RVec<float> y {0., 1., 0.};
  ROOT::VecOps::RVec<float> z {0., 0., 0.};
  ROOT::VecOps::RVec<float> res = Algorithms::getAxisCosTheta(ax, x, y, z);
  REQUIRE(res[0] == Catch::Approx( 1. ));
  REQUIRE(res[1] == Catch::Approx( 0. ));
  REQUIRE(res[2] == Catch::Approx( -1. ));
}


TEST_CASE("AxisCosTheta", "[algorithms]") {
  ROOT::VecOps::RVec<float> ax {0., 1., 0., 0., 0., 0.};
  REQUIRE(Algorithms::getAxisCosTheta(ax, 1., 0., 0.) == Catch::Approx( 1. ));
  REQUIRE(Algorithms::getAxisCosTheta(ax, 0., 1., 0.) == Catch::Approx( 0. ));
  REQUIRE(Algorithms::getAxisCosTheta(ax, -1., 0., 0.) == Catch::Approx( -1. ));
}


TEST_CASE("ThrustPointing", "[algorithms]") {
  ROOT::VecOps::RVec<float> np {1., -1., 1., -1., 1.};
  ROOT::VecOps::RVec<float> e {1., 1., 1., 1., 1.};
  ROOT::VecOps::RVec<float> t {0., -1., 0., 1., 0., -3.};
  auto res = Algorithms::getThrustPointing(np, e, t, 1.);
  REQUIRE(res[1] == Catch::Approx( 1. ));
  REQUIRE(res[3] == Catch::Approx( -1. ));
  REQUIRE(res[5] == Catch::Approx( 3. ));
}
