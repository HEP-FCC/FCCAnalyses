#include "FCCAnalyses/JetClusteringUtilsSource.h"

// Catch2
#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>

TEST_CASE("create-pseudojets", "[JetClusteringUtilsSource]") {
  edm4hep::ReconstructedParticleCollection pColl;
  edm4hep::MutableReconstructedParticle p1;
  p1.setPDG(11);
  p1.setMomentum({20., 30., 40.});
  p1.setMass(5.486e-4);
  p1.setEnergy(53.85164807);
  pColl.push_back(p1);
  edm4hep::MutableReconstructedParticle p2;
  p2.setPDG(13);
  p2.setMomentum({10., 20., 30.});
  p2.setMass(1.05658e-1);
  p2.setEnergy(37.416723);
  pColl.push_back(p2);
  auto res = FCCAnalyses::PodioSource::JetClustering::createPseudoJets(pColl);
  REQUIRE(res.size() == 2);
  REQUIRE(res[0].px() == Catch::Approx(p1.getMomentum().x));
  REQUIRE(res[0].py() == Catch::Approx(p1.getMomentum().y));
  REQUIRE(res[0].pz() == Catch::Approx(p1.getMomentum().z));
  REQUIRE(res[0].e() == Catch::Approx(p1.getEnergy()));
  REQUIRE(res[0].m2() ==
          Catch::Approx(p1.getMass() * p1.getMass()).margin(1.e-3));
  REQUIRE(res[1].px() == Catch::Approx(p2.getMomentum().x));
  REQUIRE(res[1].py() == Catch::Approx(p2.getMomentum().y));
  REQUIRE(res[1].pz() == Catch::Approx(p2.getMomentum().z));
  REQUIRE(res[1].e() == Catch::Approx(p2.getEnergy()));
  REQUIRE(res[1].m2() ==
          Catch::Approx(p2.getMass() * p2.getMass()).margin(1.e-3));
}
