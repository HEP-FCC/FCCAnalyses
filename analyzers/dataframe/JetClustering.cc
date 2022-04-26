
#include "JetClustering.h"

#include "fastjet/JetDefinition.hh"
#include "fastjet/PseudoJet.hh"
#include "fastjet/Selector.hh"
#include "ValenciaPlugin.h"
#include "fastjet/EECambridgePlugin.hh"
#include "fastjet/JadePlugin.hh"

#include "ExternalRecombiner.h"

using namespace JetClustering;

clustering_kt::clustering_kt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination){m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_kt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::kt_algorithm;

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);
  
  fastjet::ClusterSequence cs;  
  fastjet::JetDefinition def(jetAlgorithm, m_radius, recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
  
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}


clustering_antikt::clustering_antikt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination){m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_antikt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::antikt_algorithm;

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);
  
  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
 
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}

clustering_cambridge::clustering_cambridge(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination){m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_cambridge::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::cambridge_algorithm;

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);  

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
  
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}



clustering_ee_kt::clustering_ee_kt(int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination)
{m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_ee_kt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::ee_kt_algorithm;

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);  

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
 
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}


clustering_ee_genkt::clustering_ee_genkt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent)
{m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination; m_exponent = arg_exponent;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_ee_genkt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::ee_genkt_algorithm;

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);  

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, m_exponent, recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
 
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}

clustering_genkt::clustering_genkt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent)
{m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination; m_exponent = arg_exponent;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_genkt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::genkt_algorithm;

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);  

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, m_exponent, recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
 
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}


clustering_valencia::clustering_valencia(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted,int arg_recombination, float arg_beta, float arg_gamma)
{m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination; m_beta = arg_beta; m_gamma = arg_gamma;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_valencia::operator() (std::vector<fastjet::PseudoJet> input) {
  
  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::contrib::ValenciaPlugin * jetAlgorithm = new fastjet::contrib::ValenciaPlugin(m_radius, m_beta, m_gamma); 

   // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm);
  def.set_recombination_scheme(recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);
 
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);

  delete static_cast<fastjet::JetDefinition::Plugin *>(jetAlgorithm);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}

clustering_jade::clustering_jade(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination)
{m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_jade::operator() (std::vector<fastjet::PseudoJet> input) {

  if (JetClusteringUtils::check(input.size(),m_exclusive, m_cut)==false) return JetClusteringUtils::initialise_FCCAnalysesJet();

  // initialize jet algorithm
  fastjet::JadePlugin * jetAlgorithm = new fastjet::JadePlugin();

  // initialize recombination scheme
  fastjet::RecombinationScheme recomb_scheme = JetClusteringUtils::recomb_scheme(m_recombination);
  
  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm);
  def.set_recombination_scheme(recomb_scheme);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.set_recombiner(new ExternalRecombiner(m_recombination));
  cs = fastjet::ClusterSequence(input, def);

  std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);

  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::build_FCCAnalysesJet(pjets);
  
  delete static_cast<fastjet::JetDefinition::Plugin *>(jetAlgorithm);
  if (recomb_scheme == fastjet::RecombinationScheme::external_scheme) def.delete_recombiner_when_unused();
  return result;
}



