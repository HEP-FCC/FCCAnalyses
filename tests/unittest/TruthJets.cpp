#include "FCCAnalyses/TruthJets.h"
#include "FCCAnalyses/JetClusteringUtils.h"
#include "FastJet/JetClustering.h"

// Catch2
#include "catch2/catch_test_macros.hpp"
#include <catch2/catch_approx.hpp>

namespace {

const std::vector<std::array<float, 3>> kMomenta = {
    {40., 2., 5.},   {20., -3., 2.},  {10., 1., -4.},
    {-38., 4., -6.}, {-22., -2., 3.}, {-9., 3., 1.}};

edm4hep::MCParticleData mc_particle(const std::array<float, 3> &p, int pdg,
                                    int status) {
  edm4hep::MCParticleData d;
  d.PDG = pdg;
  d.generatorStatus = status;
  d.mass = 0.;
  d.momentum = edm4hep::Vector3d(p[0], p[1], p[2]);
  return d;
}

/// MC record: the six stable pions of the two prongs, then a neutrino and an
/// unstable particle, both of which must stay out of the truth jets.
ROOT::VecOps::RVec<edm4hep::MCParticleData> mc_record() {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc;
  for (const auto &p : kMomenta)
    mc.push_back(mc_particle(p, 211, 1));
  mc.push_back(mc_particle({30., 0., 0.}, 12, 1));
  mc.push_back(mc_particle({-30., 0., 0.}, 310, 2));
  return mc;
}

std::vector<fastjet::PseudoJet> reco_particles() {
  ROOT::VecOps::RVec<float> px, py, pz, e;
  for (const auto &p : kMomenta) {
    px.push_back(p[0]);
    py.push_back(p[1]);
    pz.push_back(p[2]);
    e.push_back(std::sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2]));
  }
  return FCCAnalyses::JetClusteringUtils::set_pseudoJets(px, py, pz, e);
}

} // namespace

TEST_CASE("truth-jet-inputs", "[TruthJets]") {
  auto inputs = FCCAnalyses::TruthJets::select_truth_jet_inputs(mc_record());
  REQUIRE(inputs == std::vector<int>{0, 1, 2, 3, 4, 5});
}

TEST_CASE("truth-jets-match-by-shared-energy", "[TruthJets]") {
  auto mc = mc_record();
  auto reco = reco_particles();
  auto clustered = JetClustering::clustering_ee_kt(2, 2, 1, 0)(reco);
  ROOT::VecOps::RVec<fastjet::PseudoJet> jets(clustered.jets.begin(),
                                              clustered.jets.end());

  // every reco particle is linked to the MC pion with the same index
  ROOT::VecOps::RVec<int> recin = {0, 1, 2, 3, 4, 5};
  ROOT::VecOps::RVec<int> mcin = {0, 1, 2, 3, 4, 5};

  auto truth = FCCAnalyses::TruthJets::cluster_truth_jets(
      JetClustering::clustering_ee_kt(2, 2, 1, 0), mc);
  REQUIRE(truth.jets.jets.size() == 2);

  auto match = FCCAnalyses::TruthJets::match_truth_jets(clustered.constituents,
                                                        recin, mcin, mc, truth);
  REQUIRE(match.size() == 2);
  REQUIRE(match[0] >= 0);
  REQUIRE(match[1] >= 0);
  REQUIRE(match[0] != match[1]);

  auto pt = FCCAnalyses::TruthJets::get_truth_jet_pt(match, truth);
  auto energy = FCCAnalyses::TruthJets::get_truth_jet_energy(match, truth);
  auto dr = FCCAnalyses::TruthJets::get_truth_jet_dr(jets, match, truth);
  auto purity = FCCAnalyses::TruthJets::get_truth_jet_purity(
      clustered.constituents, recin, mcin, mc, match, truth);
  auto completeness = FCCAnalyses::TruthJets::get_truth_jet_completeness(
      clustered.constituents, recin, mcin, mc, match, truth);
  for (std::size_t j = 0; j < 2; ++j) {
    REQUIRE(pt[j] == Catch::Approx(jets[j].pt()));
    REQUIRE(energy[j] == Catch::Approx(jets[j].e()));
    REQUIRE(dr[j] == Catch::Approx(0.).margin(1e-6));
    REQUIRE(purity[j] == Catch::Approx(1.));
    REQUIRE(completeness[j] == Catch::Approx(1.));
  }
}

TEST_CASE("unlinked-jets-stay-unmatched", "[TruthJets]") {
  auto mc = mc_record();
  auto reco = reco_particles();
  auto clustered = JetClustering::clustering_ee_kt(2, 2, 1, 0)(reco);

  auto truth = FCCAnalyses::TruthJets::cluster_truth_jets(
      JetClustering::clustering_ee_kt(2, 2, 1, 0), mc);
  ROOT::VecOps::RVec<int> none;
  auto match = FCCAnalyses::TruthJets::match_truth_jets(clustered.constituents,
                                                        none, none, mc, truth);
  auto pt = FCCAnalyses::TruthJets::get_truth_jet_pt(match, truth);

  REQUIRE(match[0] == -1);
  REQUIRE(match[1] == -1);
  REQUIRE(std::isnan(pt[0]));
  REQUIRE(std::isnan(pt[1]));
}

TEST_CASE("truth-jets-match-one-to-one", "[TruthJets]") {
  auto reco = reco_particles();
  auto clustered = JetClustering::clustering_ee_kt(2, 2, 1, 0)(reco);

  // all six linked MC particles point the same way, so they form one truth
  // jet; a seventh, unlinked particle forms the other
  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc;
  for (int i = 0; i < 6; ++i)
    mc.push_back(mc_particle({30. + i, 1., 1.}, 211, 1));
  mc.push_back(mc_particle({-30., 0., 0.}, 211, 1));
  ROOT::VecOps::RVec<int> recin = {0, 1, 2, 3, 4, 5};
  ROOT::VecOps::RVec<int> mcin = {0, 1, 2, 3, 4, 5};

  auto truth = FCCAnalyses::TruthJets::cluster_truth_jets(
      JetClustering::clustering_ee_kt(2, 2, 1, 0), mc);
  REQUIRE(truth.jets.jets.size() == 2);

  auto match = FCCAnalyses::TruthJets::match_truth_jets(clustered.constituents,
                                                        recin, mcin, mc, truth);
  REQUIRE(match.size() == 2);
  // only one reco jet may take the shared truth jet; the other shares no
  // energy with the remaining truth jet and stays unmatched
  REQUIRE(((match[0] >= 0) != (match[1] >= 0)));
}
