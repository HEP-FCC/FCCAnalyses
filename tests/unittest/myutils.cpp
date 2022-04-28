#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>
#include "myUtils.h"

TEST_CASE("d0", "[basics]") {
  TVector3 x(1., 0., 0.);
  TVector3 p1(1., 0., 0.);
  TVector3 p2(1., 1., 0.);
  REQUIRE(myUtils::get_d0(x, p1) == Catch::Approx(0.));
  REQUIRE(myUtils::get_d0(x, p2) == Catch::Approx(-1./sqrt(2.)));
}


TEST_CASE("z0", "[basics]") {
  TVector3 x(1., 0., 0.);
  TVector3 p1(1., 0., 0.);
  TVector3 p2(1., 0., 1.);
  REQUIRE(myUtils::get_z0(x, p1) == Catch::Approx(0.));
  REQUIRE(myUtils::get_z0(x, p2) == Catch::Approx(-1.));
}


TEST_CASE("Npos", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, 4.5, 1e30};
  REQUIRE(myUtils::get_Npos(in1) == 3);
}


TEST_CASE("Nneg", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, -4.5, 1e30};
  REQUIRE(myUtils::get_Nneg(in1) == 2);
}


TEST_CASE("dPV2DV_min", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, -4.5, 1e30, 1e-30};
  REQUIRE(myUtils::get_dPV2DV_min(in1) == Catch::Approx(1e-30));
}


TEST_CASE("dPV2DV_max", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, -4.5, 1e30, 1e-30};
  REQUIRE(myUtils::get_dPV2DV_max(in1) == Catch::Approx(1e30));
}


TEST_CASE("dPV2DV_ave", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1., 2., -4., 4., 1e5, -1e5};
  REQUIRE(myUtils::get_dPV2DV_ave(in1) == Catch::Approx(.2));
}


TEST_CASE("PV_ntracks", "[basics]") {
  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vVec;

  VertexingUtils::FCCAnalysesVertex v1;
  v1.vertex.primary = 1;
  v1.ntracks = 7;
  vVec.push_back(v1);

  VertexingUtils::FCCAnalysesVertex v2;
  v2.vertex.primary = 0;
  v2.ntracks = 14;
  vVec.push_back(v2);

  VertexingUtils::FCCAnalysesVertex v3;
  v3.vertex.primary = -4;
  v3.ntracks = 21;
  vVec.push_back(v3);

  REQUIRE(myUtils::get_PV_ntracks(vVec) == 7);
  REQUIRE(myUtils::get_PV_ntracks(vVec) != 14);
  REQUIRE(myUtils::get_PV_ntracks(vVec) != 21);
}


TEST_CASE("hasPV", "[basics]") {
  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vVec1;
  VertexingUtils::FCCAnalysesVertex v1;
  v1.vertex.primary = 1;
  vVec1.push_back(v1);
  VertexingUtils::FCCAnalysesVertex v2;
  v2.vertex.primary = 0;
  vVec1.push_back(v2);

  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vVec2;
  VertexingUtils::FCCAnalysesVertex v3;
  v3.vertex.primary = 0;
  vVec2.push_back(v3);
  VertexingUtils::FCCAnalysesVertex v4;
  v4.vertex.primary = -4;
  vVec2.push_back(v4);

  REQUIRE(myUtils::hasPV(vVec1) == 1);
  REQUIRE(myUtils::hasPV(vVec2) == 0);
}
