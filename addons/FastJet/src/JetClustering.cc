#include "FastJet/JetClustering.h"
#include "FastJet/ExternalRecombiner.h"

#include "FCCAnalyses/JetClusteringUtils.h"

#include "fastjet/JetDefinition.hh"
#include "fastjet/PseudoJet.hh"
#include "fastjet/Selector.hh"

namespace JetClustering {

  clustering_kt::clustering_kt(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;

    // initialize jet algorithm
    _jetAlgorithm = fastjet::JetAlgorithm::kt_algorithm;

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_kt::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    FCCAnalysesJet result = FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);

    return result;
  }

  clustering_antikt::clustering_antikt(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;

    // initialize jet algorithm
    //fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
    _jetAlgorithm = fastjet::JetAlgorithm::antikt_algorithm;

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_antikt::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    FCCAnalysesJet result = FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);

    return result;
  }

  clustering_cambridge::clustering_cambridge(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;

    // initialize jet algorithm
    _jetAlgorithm = fastjet::JetAlgorithm::cambridge_algorithm;

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_cambridge::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }

  clustering_ee_kt::clustering_ee_kt(int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination) {
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;

    // initialize jet algorithm
    _jetAlgorithm = fastjet::JetAlgorithm::ee_kt_algorithm;

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_ee_kt::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }

  clustering_ee_genkt::clustering_ee_genkt(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;
    _exponent = arg_exponent;

    // initialize jet algorithm
    _jetAlgorithm = fastjet::JetAlgorithm::ee_genkt_algorithm;

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _exponent, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_ee_genkt::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }

  clustering_genkt::clustering_genkt(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;
    _exponent = arg_exponent;

    // initialize jet algorithm
    _jetAlgorithm = fastjet::JetAlgorithm::genkt_algorithm;

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _exponent, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_genkt::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);

    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }

  clustering_valencia::clustering_valencia(float arg_radius,
                                           int arg_exclusive,
                                           float arg_cut,
                                           int arg_sorted,
                                           int arg_recombination,
                                           float arg_beta,
                                           float arg_gamma) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;
    _beta = arg_beta;
    _gamma = arg_gamma;

    // initialize jet algorithm
    _jetAlgorithm = new fastjet::contrib::ValenciaPlugin(_radius, _beta, _gamma);

    // initialize recombination scheme
    _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm);
    _def.set_recombination_scheme(_recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_valencia::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }

  clustering_jade::clustering_jade(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;

    // initialize jet algorithm
    _jetAlgorithm = new fastjet::JadePlugin();

    // initialize recombination scheme
    fastjet::RecombinationScheme _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm);
    _def.set_recombination_scheme(_recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
  }

  FCCAnalysesJet clustering_jade::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);

    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }

}  // namespace JetClustering
