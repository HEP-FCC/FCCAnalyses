#include "FCCAnalyses/ReconstructedParticle.h"

// Catch2
#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>

// EDM4hep
#include "edm4hep/EDM4hepVersion.h"

TEST_CASE("sel_type", "[ReconstructedParticle]") {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pVec;
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
  edm4hep::ReconstructedParticleData p1;
  p1.PDG = 11;
  pVec.push_back(p1);
  edm4hep::ReconstructedParticleData p2;
  p2.PDG = 13;
  pVec.push_back(p2);
  edm4hep::ReconstructedParticleData p3;
  p3.PDG = -11;
  pVec.push_back(p3);
  edm4hep::ReconstructedParticleData p4;
  p4.PDG = -13;
  pVec.push_back(p4);
#else
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
#endif
  FCCAnalyses::ReconstructedParticle::sel_type selType{11};
  auto res = selType(pVec);
  REQUIRE(res.size() == 1);
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
  REQUIRE(res[0].PDG == 11);
#else
  REQUIRE(res[0].type == 11);
#endif
}

TEST_CASE("sel_absType", "[ReconstructedParticle]") {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pVec;
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
  edm4hep::ReconstructedParticleData p1;
  p1.PDG = 11;
  pVec.push_back(p1);
  edm4hep::ReconstructedParticleData p2;
  p2.PDG = 13;
  pVec.push_back(p2);
  edm4hep::ReconstructedParticleData p3;
  p3.PDG = -11;
  pVec.push_back(p3);
  edm4hep::ReconstructedParticleData p4;
  p4.PDG = -13;
  pVec.push_back(p4);
#else
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
#endif
  FCCAnalyses::ReconstructedParticle::sel_absType selAbsType{11};
  auto res = selAbsType(pVec);
  REQUIRE(res.size() == 2);
#if edm4hep_VERSION > EDM4HEP_VERSION(0, 10, 5)
  REQUIRE(res[0].PDG == 11);
  REQUIRE(res[1].PDG == -11);
#else
  REQUIRE(res[0].type == 11);
  REQUIRE(res[1].type == -11);
#endif
}

TEST_CASE("sel_absType__neg_type", "[ReconstructedParticle]") {
  REQUIRE_THROWS_AS(FCCAnalyses::ReconstructedParticle::sel_absType(-17),
                    std::invalid_argument);
}
