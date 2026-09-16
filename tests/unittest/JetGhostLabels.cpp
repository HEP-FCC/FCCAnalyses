#include "FCCAnalyses/JetGhostLabels.h"
#include "FCCAnalyses/JetClusteringUtils.h"
#include "FastJet/JetClustering.h"

// Catch2
#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>

using FCCAnalyses::JetGhostLabels::GhostParticles;

namespace {

/// Two well separated back-to-back sprays of particles.
std::vector<fastjet::PseudoJet> two_prong_event() {
  ROOT::VecOps::RVec<float> px, py, pz, e;
  auto add = [&](float x, float y, float z) {
    px.push_back(x);
    py.push_back(y);
    pz.push_back(z);
    e.push_back(std::sqrt(x * x + y * y + z * z));
  };
  add(40., 2., 5.);
  add(20., -3., 2.);
  add(10., 1., -4.);
  add(-38., 4., -6.);
  add(-22., -2., 3.);
  add(-9., 3., 1.);
  return FCCAnalyses::JetClusteringUtils::set_pseudoJets(px, py, pz, e);
}

GhostParticles make_ghost(double x, double y, double z, int pdg) {
  GhostParticles g;
  g.p.emplace_back(x, y, z, std::sqrt(x * x + y * y + z * z));
  g.pdg.push_back(pdg);
  g.mc_index.push_back(0);
  return g;
}

} // namespace

TEST_CASE("ghosts-do-not-move-jets", "[JetGhostLabels]") {
  auto parts = two_prong_event();
  auto clustered = JetClustering::clustering_ee_kt(2, 2, 1, 0)(parts);
  REQUIRE(clustered.jets.size() == 2);

  // a ghost along each prong
  GhostParticles ghosts = make_ghost(40., 2., 5., 511);
  ghosts.p.emplace_back(-38., 4., -6., std::sqrt(38. * 38. + 16. + 36.));
  ghosts.pdg.push_back(-511);
  ghosts.mc_index.push_back(1);

  std::vector<fastjet::PseudoJet> input = parts;
  for (const auto &g : ghosts.p) {
    double mag = std::sqrt(g.px() * g.px() + g.py() * g.py() + g.pz() * g.pz());
    double s = 1e-18 / mag;
    input.emplace_back(g.px() * s, g.py() * s, g.pz() * s, mag * s);
  }
  auto with_ghosts = JetClustering::clustering_ee_kt(2, 2, 1, 0)(input);
  REQUIRE(with_ghosts.jets.size() == 2);

  for (std::size_t j = 0; j < 2; ++j) {
    REQUIRE(with_ghosts.jets[j].px() == Catch::Approx(clustered.jets[j].px()));
    REQUIRE(with_ghosts.jets[j].py() == Catch::Approx(clustered.jets[j].py()));
    REQUIRE(with_ghosts.jets[j].pz() == Catch::Approx(clustered.jets[j].pz()));
    REQUIRE(with_ghosts.jets[j].e() == Catch::Approx(clustered.jets[j].e()));
  }
}

TEST_CASE("ghosts-land-in-their-own-jet", "[JetGhostLabels]") {
  auto parts = two_prong_event();
  auto clustered = JetClustering::clustering_ee_kt(2, 2, 1, 0)(parts);

  GhostParticles ghosts = make_ghost(40., 2., 5., 511);
  ghosts.p.emplace_back(-38., 4., -6., std::sqrt(38. * 38. + 16. + 36.));
  ghosts.pdg.push_back(-511);
  ghosts.mc_index.push_back(1);

  auto assoc = FCCAnalyses::JetGhostLabels::associate_ghosts(
      JetClustering::clustering_ee_kt(2, 2, 1, 0), parts,
      clustered.constituents, ghosts);

  REQUIRE(assoc.size() == 2);
  REQUIRE(assoc[0] >= 0);
  REQUIRE(assoc[1] >= 0);
  // the two ghosts follow opposite prongs, so they cannot share a jet
  REQUIRE(assoc[0] != assoc[1]);
}
