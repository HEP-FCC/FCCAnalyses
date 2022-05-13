#include "FCCAnalyses/myUtils.h"

#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>
#include <catch2/benchmark/catch_benchmark.hpp>

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


TEST_CASE("distanceComp", "[basics]") {
  edm4hep::Vector3f v1 = {1., -2., 3.};
  TVector3 v2 = {0., 0., 0.};

  REQUIRE(myUtils::get_distance(v1, v2, 0) == Catch::Approx(1.));
  REQUIRE(myUtils::get_distance(v1, v2, 1) == Catch::Approx(-2.));
  REQUIRE(myUtils::get_distance(v1, v2, 2) == Catch::Approx(3.));
  REQUIRE(myUtils::get_distance(v1, v2, -1) == Catch::Approx(std::sqrt(14.)));
  REQUIRE(myUtils::get_distance(v1, v2, 3) == Catch::Approx(std::sqrt(14.)));
}


TEST_CASE("distance", "[basic]") {
  TVector3 v1 = {0., 0., 0.};
  TVector3 v2 = {3., -2., 1.};

  REQUIRE(myUtils::get_distance(v1, v2) == Catch::Approx(std::sqrt(14.)));
}


TEST_CASE("distanceVertex", "[basic]") {
  edm4hep::VertexData v1;
  v1.position = {1., -2., 3.};
  edm4hep::VertexData v2;
  v2.position = {0., 0., 0.};

  REQUIRE(myUtils::get_distanceVertex(v1, v2, 0) == Catch::Approx(1.));
  REQUIRE(myUtils::get_distanceVertex(v1, v2, 1) == Catch::Approx(-2.));
  REQUIRE(myUtils::get_distanceVertex(v1, v2, 2) == Catch::Approx(3.));
  float dist = myUtils::get_distanceVertex(v1, v2, -1);
  REQUIRE(dist == Catch::Approx(std::sqrt(14.)));
  dist = myUtils::get_distanceVertex(v1, v2, 3);
  REQUIRE(dist == Catch::Approx(std::sqrt(14.)));
}


TEST_CASE("distanceErrorVertex", "[basic]") {
  edm4hep::VertexData v1;
  v1.covMatrix = {.1, .2, .3, .43, .67, .11};
  v1.position = {1., 2., 3.};
  edm4hep::VertexData v2;
  v2.covMatrix = {.34, .2, .46, .43, .67, .003};
  v2.position = {0., 0., 0.};

  float err = myUtils::get_distanceErrorVertex(v1, v2, 0);
  REQUIRE(err == Catch::Approx(std::sqrt(.44)));
  err = myUtils::get_distanceErrorVertex(v1, v2, 1);
  REQUIRE(err == Catch::Approx(std::sqrt(.76)));
  err = myUtils::get_distanceErrorVertex(v1, v2, 2);
  REQUIRE(err == Catch::Approx(std::sqrt(.113)));
  err = myUtils::get_distanceErrorVertex(v1, v2, -1);
  REQUIRE(err == Catch::Approx(std::sqrt(27.337/14.)));
  err = myUtils::get_distanceErrorVertex(v1, v2, 3);
  REQUIRE(err == Catch::Approx(std::sqrt(27.337/14.)));
}


TEST_CASE("MC_parent", "[basics]") {
  edm4hep::MCParticleData p;
  ROOT::VecOps::RVec<int> ind = {5, 3, 7,};

  REQUIRE(myUtils::getMC_parent(0, p, ind) == -999);
  REQUIRE(myUtils::getMC_parent(5, p, ind) == -999);

  p.parents_begin = 0;
  p.parents_end = 1;
  REQUIRE(myUtils::getMC_parent(0, p, ind) == 5);
}


TEST_CASE("FCCAnalysesComposite_N", "[basics]") {
  ROOT::VecOps::RVec<myUtils::FCCAnalysesComposite> cVec;
  myUtils::FCCAnalysesComposite c1;
  cVec.push_back(c1);
  myUtils::FCCAnalysesComposite c2;
  cVec.push_back(c2);

  REQUIRE(myUtils::getFCCAnalysesComposite_N(cVec) == 2);
}


TEST_CASE("FCCAnalysesComposite2_N", "[basics]") {
  ROOT::VecOps::RVec<myUtils::FCCAnalysesComposite2> cVec;
  myUtils::FCCAnalysesComposite2 c1;
  cVec.push_back(c1);
  myUtils::FCCAnalysesComposite2 c2;
  cVec.push_back(c2);

  REQUIRE(myUtils::getFCCAnalysesComposite_N(cVec) == 2);
}


TEST_CASE("isPV", "[basics]") {
  edm4hep::ReconstructedParticleData p;
  p.tracks_begin = 0;
  ROOT::VecOps::RVec<int> index1 = {3, 0, 7};
  ROOT::VecOps::RVec<int> index2 = {3, 1, 7};

  REQUIRE(myUtils::isPV(p, index1));
  REQUIRE(!myUtils::isPV(p, index2));

  BENCHMARK("isPV bench") {
        return myUtils::isPV(p, index1);
  };
}
