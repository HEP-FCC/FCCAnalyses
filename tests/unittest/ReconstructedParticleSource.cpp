// FCCAnalyses
#include "FCCAnalyses/ReconstructedParticleSource.h"

// Catch2
#include "catch2/catch_approx.hpp"
#include "catch2/catch_test_macros.hpp"

TEST_CASE("remove-by-id", "[ReconstructedParticleSource]") {
  edm4hep::ReconstructedParticleCollection pColl;
  edm4hep::MutableReconstructedParticle p1;
  p1.setPDG(11);
  p1.setMomentum({1., 2., 3.});
  pColl.push_back(p1);
  edm4hep::MutableReconstructedParticle p2;
  p2.setPDG(13);
  p2.setMomentum({10., 20., 30.});
  pColl.push_back(p2);
  auto res = FCCAnalyses::PodioSource::ReconstructedParticle::remove(pColl, p1);
  REQUIRE(res.size() == 1);
  REQUIRE(res[0].getPDG() == 13);
}

TEST_CASE("remove-by-id-subset-coll", "[ReconstructedParticleSource]") {
  edm4hep::ReconstructedParticleCollection pColl;
  edm4hep::MutableReconstructedParticle p1;
  p1.setPDG(11);
  p1.setMomentum({1., 2., 3.});
  pColl.push_back(p1);
  edm4hep::MutableReconstructedParticle p2;
  p2.setPDG(13);
  p2.setMomentum({10., 20., 30.});
  pColl.push_back(p2);
  edm4hep::ReconstructedParticleCollection pCollSubset;
  pCollSubset.setSubsetCollection();
  pCollSubset.push_back(pColl[0]);
  auto res = FCCAnalyses::PodioSource::ReconstructedParticle::remove(
      pColl, pCollSubset[0]);
  REQUIRE(res.size() == 1);
  REQUIRE(res[0].getPDG() == 13);
}

TEST_CASE("remove-by-matching", "[ReconstructedParticleSource]") {
  edm4hep::ReconstructedParticleCollection pColl;
  edm4hep::MutableReconstructedParticle p1;
  p1.setPDG(11);
  p1.setMomentum({1., 2., 3.});
  pColl.push_back(p1);
  edm4hep::MutableReconstructedParticle p2;
  p2.setPDG(13);
  p2.setMomentum({10., 20., 30.});
  pColl.push_back(p2);
  edm4hep::ReconstructedParticleCollection pCollRemove;
  edm4hep::MutableReconstructedParticle p3;
  p3.setPDG(11);
  p3.setMomentum({1., 2., 3.});
  pCollRemove.push_back(p3);
  auto res = FCCAnalyses::PodioSource::ReconstructedParticle::remove(
      pColl, pCollRemove, true);
  REQUIRE(res.size() == 1);
  REQUIRE(res[0].getPDG() == 13);
}

TEST_CASE("merge", "[ReconstructedParticleSource]") {
  edm4hep::ReconstructedParticleCollection pColl1;
  edm4hep::MutableReconstructedParticle p1;
  p1.setPDG(11);
  p1.setMomentum({1., 2., 3.});
  pColl1.push_back(p1);
  edm4hep::MutableReconstructedParticle p2;
  p2.setPDG(13);
  p2.setMomentum({10., 20., 30.});
  pColl1.push_back(p2);
  edm4hep::ReconstructedParticleCollection pColl2;
  edm4hep::MutableReconstructedParticle p3;
  p3.setPDG(11);
  p3.setMomentum({1., 2., 3.});
  pColl2.push_back(p3);
  auto res =
      FCCAnalyses::PodioSource::ReconstructedParticle::merge(pColl1, pColl2);
  REQUIRE(res.size() == 3);
  REQUIRE(res[0].getPDG() == 11);
  REQUIRE(res[1].getPDG() == 13);
  REQUIRE(res[2].getPDG() == 11);
}
