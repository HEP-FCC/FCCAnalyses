#include "FCCAnalyses/ReconstructedParticle.h"

// Catch2
#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>

TEST_CASE("sel_type", "[ReconstructedParticle]") {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pVec;
  edm4hep::ReconstructedParticleData p1;
  p1.type = 11;
  pVec.push_back(p1);
  edm4hep::ReconstructedParticleData p2;
  p2.type = 13;
  pVec.push_back(p2);
  edm4hep::ReconstructedParticleData p3;
  p3.type = -11;
  pVec.push_back(p3);
  edm4hep::ReconstructedParticleData p4;
  p4.type = -13;
  pVec.push_back(p4);
  FCCAnalyses::ReconstructedParticle::sel_type selType{11};
  auto res = selType(pVec);
  REQUIRE(res.size() == 1);
  REQUIRE(res[0].type == 11);
}

TEST_CASE("sel_absType", "[ReconstructedParticle]") {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pVec;
  edm4hep::ReconstructedParticleData p1;
  p1.type = 11;
  pVec.push_back(p1);
  edm4hep::ReconstructedParticleData p2;
  p2.type = 13;
  pVec.push_back(p2);
  edm4hep::ReconstructedParticleData p3;
  p3.type = -11;
  pVec.push_back(p3);
  edm4hep::ReconstructedParticleData p4;
  p4.type = -13;
  pVec.push_back(p4);
  FCCAnalyses::ReconstructedParticle::sel_absType selAbsType{11};
  auto res = selAbsType(pVec);
  REQUIRE(res.size() == 2);
  REQUIRE(res[0].type == 11);
  REQUIRE(res[1].type == -11);
}

TEST_CASE("sel_absType__neg_type", "[ReconstructedParticle]") {
  REQUIRE_THROWS_AS(FCCAnalyses::ReconstructedParticle::sel_absType(-17),
                    std::invalid_argument);
}
