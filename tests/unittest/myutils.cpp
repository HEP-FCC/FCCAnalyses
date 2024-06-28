#include "FCCAnalyses/myUtils.h"

#include "edm4hep/EDM4hepVersion.h"
#if __has_include("edm4hep/utils/bit_utils.h")
#include "edm4hep/utils/bit_utils.h"
#endif

#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>

TEST_CASE("d0", "[basics]") {
  TVector3 x(1., 0., 0.);
  TVector3 p1(1., 0., 0.);
  TVector3 p2(1., 1., 0.);
  REQUIRE(FCCAnalyses::myUtils::get_d0(x, p1) == Catch::Approx(0.));
  REQUIRE(FCCAnalyses::myUtils::get_d0(x, p2) == Catch::Approx(-1./sqrt(2.)));
}


TEST_CASE("z0", "[basics]") {
  TVector3 x(1., 0., 0.);
  TVector3 p1(1., 0., 0.);
  TVector3 p2(1., 0., 1.);
  REQUIRE(FCCAnalyses::myUtils::get_z0(x, p1) == Catch::Approx(0.));
  REQUIRE(FCCAnalyses::myUtils::get_z0(x, p2) == Catch::Approx(-1.));
}


TEST_CASE("Npos", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, 4.5, 1e30};
  REQUIRE(FCCAnalyses::myUtils::get_Npos(in1) == 3);
}


TEST_CASE("Nneg", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, -4.5, 1e30};
  REQUIRE(FCCAnalyses::myUtils::get_Nneg(in1) == 2);
}


TEST_CASE("dPV2DV_min", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, -4.5, 1e30, 1e-30};
  REQUIRE(FCCAnalyses::myUtils::get_dPV2DV_min(in1) == Catch::Approx(1e-30));
}


TEST_CASE("dPV2DV_max", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1, 2, -4.5, 1e30, 1e-30};
  REQUIRE(FCCAnalyses::myUtils::get_dPV2DV_max(in1) == Catch::Approx(1e30));
}


TEST_CASE("dPV2DV_ave", "[basics]") {
  ROOT::VecOps::RVec<float> in1 {-1., 2., -4., 4., 1e5, -1e5};
  REQUIRE(FCCAnalyses::myUtils::get_dPV2DV_ave(in1) == Catch::Approx(.2));
}


TEST_CASE("PV_ntracks", "[basics]") {
  ROOT::VecOps::RVec<FCCAnalyses::VertexingUtils::FCCAnalysesVertex> vVec;

  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v1;
#if EDM4HEP_BUILD_VERSION <= EDM4HEP_VERSION(0, 10, 5)
  v1.vertex.primary = 1;
#else
  v1.vertex.type = edm4hep::utils::setBit(v1.vertex.type, edm4hep::Vertex::BITPrimaryVertex, true);
#endif
  v1.ntracks = 7;
  vVec.push_back(v1);

  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v2;
#if EDM4HEP_BUILD_VERSION <= EDM4HEP_VERSION(0, 10, 5)
  v2.vertex.primary = 0;
#else
  v1.vertex.type = edm4hep::utils::setBit(v1.vertex.type, edm4hep::Vertex::BITPrimaryVertex, false);
#endif

  v2.ntracks = 14;
  vVec.push_back(v2);

  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v3;
#if EDM4HEP_BUILD_VERSION <= EDM4HEP_VERSION(0, 10, 5)
  v3.vertex.primary = -4;
#else
  v1.vertex.type = static_cast<uint32_t>(-4);
#endif

  v3.ntracks = 21;
  vVec.push_back(v3);

  REQUIRE(FCCAnalyses::myUtils::get_PV_ntracks(vVec) == 7);
  REQUIRE(FCCAnalyses::myUtils::get_PV_ntracks(vVec) != 14);
  REQUIRE(FCCAnalyses::myUtils::get_PV_ntracks(vVec) != 21);
}


TEST_CASE("hasPV", "[basics]") {
  ROOT::VecOps::RVec<FCCAnalyses::VertexingUtils::FCCAnalysesVertex> vVec1;
  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v1;
  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v2;
#if EDM4HEP_BUILD_VERSION <= EDM4HEP_VERSION(0, 10, 5)
  v1.vertex.primary = 1;
  v2.vertex.primary = 0;
#else
  v1.vertex.type = edm4hep::utils::setBit(v1.vertex.type, edm4hep::Vertex::BITPrimaryVertex, true);
  v2.vertex.type = edm4hep::utils::setBit(v2.vertex.type, edm4hep::Vertex::BITPrimaryVertex, false);
#endif
  vVec1.push_back(v1);
  vVec1.push_back(v2);

  ROOT::VecOps::RVec<FCCAnalyses::VertexingUtils::FCCAnalysesVertex> vVec2;
  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v3;
  FCCAnalyses::VertexingUtils::FCCAnalysesVertex v4;
#if EDM4HEP_BUILD_VERSION <= EDM4HEP_VERSION(0, 10, 5)
  v3.vertex.primary = 0;
  v4.vertex.primary = -4;
#else
  v3.vertex.type = edm4hep::utils::setBit(v3.vertex.type, edm4hep::Vertex::BITPrimaryVertex, false);
  v4.vertex.type = static_cast<uint32_t>(-4);
#endif

  vVec2.push_back(v4);
  vVec2.push_back(v3);

  REQUIRE(FCCAnalyses::myUtils::hasPV(vVec1) == 1);
  REQUIRE(FCCAnalyses::myUtils::hasPV(vVec2) == 0);
}


TEST_CASE("distanceComp", "[basics]") {
  edm4hep::Vector3f v1 = {1., -2., 3.};
  TVector3 v2 = {0., 0., 0.};

  REQUIRE(FCCAnalyses::myUtils::get_distance(v1, v2, 0) == Catch::Approx(1.));
  REQUIRE(FCCAnalyses::myUtils::get_distance(v1, v2, 1) == Catch::Approx(-2.));
  REQUIRE(FCCAnalyses::myUtils::get_distance(v1, v2, 2) == Catch::Approx(3.));
  REQUIRE(FCCAnalyses::myUtils::get_distance(v1, v2, -1) == Catch::Approx(std::sqrt(14.)));
  REQUIRE(FCCAnalyses::myUtils::get_distance(v1, v2, 3) == Catch::Approx(std::sqrt(14.)));
}


TEST_CASE("distance", "[basic]") {
  TVector3 v1 = {0., 0., 0.};
  TVector3 v2 = {3., -2., 1.};

  REQUIRE(FCCAnalyses::myUtils::get_distance(v1, v2) == Catch::Approx(std::sqrt(14.)));
}


TEST_CASE("distanceVertex", "[basic]") {
  edm4hep::VertexData v1;
  v1.position = {1., -2., 3.};
  edm4hep::VertexData v2;
  v2.position = {0., 0., 0.};

  REQUIRE(FCCAnalyses::myUtils::get_distanceVertex(v1, v2, 0) == Catch::Approx(1.));
  REQUIRE(FCCAnalyses::myUtils::get_distanceVertex(v1, v2, 1) == Catch::Approx(-2.));
  REQUIRE(FCCAnalyses::myUtils::get_distanceVertex(v1, v2, 2) == Catch::Approx(3.));
  float dist = FCCAnalyses::myUtils::get_distanceVertex(v1, v2, -1);
  REQUIRE(dist == Catch::Approx(std::sqrt(14.)));
  dist = FCCAnalyses::myUtils::get_distanceVertex(v1, v2, 3);
  REQUIRE(dist == Catch::Approx(std::sqrt(14.)));
}


TEST_CASE("distanceErrorVertex", "[basic]") {
  edm4hep::VertexData v1;
  v1.covMatrix = {.1, .2, .3, .43, .67, .11};
  v1.position = {1., 2., 3.};
  edm4hep::VertexData v2;
  v2.covMatrix = {.34, .2, .46, .43, .67, .003};
  v2.position = {0., 0., 0.};

  float err = FCCAnalyses::myUtils::get_distanceErrorVertex(v1, v2, 0);
  REQUIRE(err == Catch::Approx(std::sqrt(.44)));
  err = FCCAnalyses::myUtils::get_distanceErrorVertex(v1, v2, 1);
  REQUIRE(err == Catch::Approx(std::sqrt(.76)));
  err = FCCAnalyses::myUtils::get_distanceErrorVertex(v1, v2, 2);
  REQUIRE(err == Catch::Approx(std::sqrt(.113)));
  err = FCCAnalyses::myUtils::get_distanceErrorVertex(v1, v2, -1);
  REQUIRE(err == Catch::Approx(std::sqrt(27.337/14.)));
  err = FCCAnalyses::myUtils::get_distanceErrorVertex(v1, v2, 3);
  REQUIRE(err == Catch::Approx(std::sqrt(27.337/14.)));
}


TEST_CASE("MC_parent", "[basics]") {
  edm4hep::MCParticleData p;
  ROOT::VecOps::RVec<int> ind = {5, 3, 7,};

  REQUIRE(FCCAnalyses::myUtils::getMC_parent(0, p, ind) == -999);
  REQUIRE(FCCAnalyses::myUtils::getMC_parent(5, p, ind) == -999);

  p.parents_begin = 0;
  p.parents_end = 1;
  REQUIRE(FCCAnalyses::myUtils::getMC_parent(0, p, ind) == 5);
}


TEST_CASE("FCCAnalysesComposite_N", "[basics]") {
  ROOT::VecOps::RVec<FCCAnalyses::myUtils::FCCAnalysesComposite> cVec;
  FCCAnalyses::myUtils::FCCAnalysesComposite c1;
  cVec.push_back(c1);
  FCCAnalyses::myUtils::FCCAnalysesComposite c2;
  cVec.push_back(c2);

  REQUIRE(FCCAnalyses::myUtils::getFCCAnalysesComposite_N(cVec) == 2);
}


TEST_CASE("FCCAnalysesComposite2_N", "[basics]") {
  ROOT::VecOps::RVec<FCCAnalyses::myUtils::FCCAnalysesComposite2> cVec;
  FCCAnalyses::myUtils::FCCAnalysesComposite2 c1;
  cVec.push_back(c1);
  FCCAnalyses::myUtils::FCCAnalysesComposite2 c2;
  cVec.push_back(c2);

  REQUIRE(FCCAnalyses::myUtils::getFCCAnalysesComposite_N(cVec) == 2);
}


TEST_CASE("isPV", "[basics]") {
  edm4hep::ReconstructedParticleData p;
  p.tracks_begin = 0;
  ROOT::VecOps::RVec<int> index1 = {3, 0, 7};
  ROOT::VecOps::RVec<int> index2 = {3, 1, 7};

  REQUIRE(FCCAnalyses::myUtils::isPV(p, index1));
  REQUIRE(!FCCAnalyses::myUtils::isPV(p, index2));
}


TEST_CASE("get_p", "[basics]") {
  edm4hep::ReconstructedParticleData p;
  p.momentum.x = 1.;
  p.momentum.y = 2.;
  p.momentum.z = 2.;
  p.mass = -1e3;

  REQUIRE(FCCAnalyses::myUtils::get_p(p) == Catch::Approx(3.));
}
