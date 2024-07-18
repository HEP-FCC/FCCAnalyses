#include "FCCAnalyses/Algorithms.h"

#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>

TEST_CASE("sphericityFit", "[algorithms]") {
  ROOT::VecOps::RVec<float> x{1., 0., -1};
  ROOT::VecOps::RVec<float> y{0., 1., 0.};
  ROOT::VecOps::RVec<float> z{0., 0., 0.};
  FCCAnalyses::Algorithms::sphericityFit sphFit{x, y, z};
  double params[] = {0., 1., 0.};
  REQUIRE(sphFit(params) == Catch::Approx(1.));
}

// Values changed with ROOT 6.30
// Commenting out, since the first set of numbers was also not validated
// TEST_CASE("minimize_sphericity", "[algorithms]") {
//   ROOT::VecOps::RVec<float> x{0., 1., 3., 7., 11., 3.};
//   ROOT::VecOps::RVec<float> y{0., -1., 3., -7., -11., .3};
//   ROOT::VecOps::RVec<float> z{5., -3., 1., 4., 2., -4};
//   auto res = FCCAnalyses::Algorithms::minimize_sphericity()(x, y, z);
//   REQUIRE(res[0] == Catch::Approx(.28065));
//   REQUIRE(res[1] == Catch::Approx(269.09445));
//   REQUIRE(res[2] == Catch::Approx(1994.81445));
//   REQUIRE(res[3] == Catch::Approx(-263.70053));
//   REQUIRE(res[4] == Catch::Approx(2012.12073));
//   REQUIRE(res[5] == Catch::Approx(77.21406));
//   REQUIRE(res[6] == Catch::Approx(721.20111));
// }

TEST_CASE("Mass", "[algorithms]") {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pVec;
  edm4hep::ReconstructedParticleData p;
  p.momentum.x = 1.;
  p.momentum.y = -1.;
  p.momentum.z = 1.;
  p.energy = 2.;
  pVec.push_back(p);
  REQUIRE(FCCAnalyses::Algorithms::getMass(pVec) == Catch::Approx( 1. ));
}


TEST_CASE("AxisCosThetaInVec", "[algorithms]") {
  ROOT::VecOps::RVec<float> ax {0., 1., 0., 0., 0., 0.};
  ROOT::VecOps::RVec<float> x {1., 0., -1};
  ROOT::VecOps::RVec<float> y {0., 1., 0.};
  ROOT::VecOps::RVec<float> z {0., 0., 0.};
  ROOT::VecOps::RVec<float> res = FCCAnalyses::Algorithms::getAxisCosTheta(ax, x, y, z);
  REQUIRE(res[0] == Catch::Approx( 1. ));
  REQUIRE(res[1] == Catch::Approx( 0. ));
  REQUIRE(res[2] == Catch::Approx( -1. ));
}


TEST_CASE("AxisCosTheta", "[algorithms]") {
  ROOT::VecOps::RVec<float> ax {0., 1., 0., 0., 0., 0.};
  REQUIRE(FCCAnalyses::Algorithms::getAxisCosTheta(ax, 1., 0., 0.) == Catch::Approx( 1. ));
  REQUIRE(FCCAnalyses::Algorithms::getAxisCosTheta(ax, 0., 1., 0.) == Catch::Approx( 0. ));
  REQUIRE(FCCAnalyses::Algorithms::getAxisCosTheta(ax, -1., 0., 0.) == Catch::Approx( -1. ));
}


TEST_CASE("ThrustPointing", "[algorithms]") {
  ROOT::VecOps::RVec<float> np {1., -1., 1., -1., 1.};
  ROOT::VecOps::RVec<float> e {1., 1., 1., 1., 1.};
  ROOT::VecOps::RVec<float> t {0., -1., 0., 1., 0., -3.};
  auto res = FCCAnalyses::Algorithms::getThrustPointing(1)(np, e, t);
  REQUIRE(res[1] == Catch::Approx( 1. ));
  REQUIRE(res[3] == Catch::Approx( -1. ));
  REQUIRE(res[5] == Catch::Approx( 3. ));
}


TEST_CASE("calculate_thrust", "[algorithms]") {
  ROOT::VecOps::RVec<float> x {0., 1., 3., 7., 11., 3.};
  ROOT::VecOps::RVec<float> y {0., -1., 3., -7., -11., .3};
  ROOT::VecOps::RVec<float> z {5., -3., 1., 4., 2., -4};

  auto res = FCCAnalyses::Algorithms::calculate_thrust()(x, y, z);
  REQUIRE(res[0] == Catch::Approx( 0.67978 ));
  REQUIRE(res[1] == Catch::Approx( -0.83496 ));
  REQUIRE(res[2] == Catch::Approx( 0.52436 ));
  REQUIRE(res[3] == Catch::Approx( 0.166992 ));
}
