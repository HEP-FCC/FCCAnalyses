
#include "JetClustering.h"
using namespace JetClustering;

clustering_kt::clustering_kt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted){m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_kt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::initialise_FCCAnalysesJet();
  if (input.size()<2) return result;

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::kt_algorithm;

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, fastjet::RecombinationScheme::E_scheme);
  cs = fastjet::ClusterSequence(input, def);

  //std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);

  std::vector<fastjet::PseudoJet> pjets;

  if (m_sorted == 0){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_ycut(m_cut));
  }
  else if (m_sorted == 1){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_E(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_ycut(m_cut));
  }
  
  JetClusteringUtils::FCCAnalysesJet result2 = JetClusteringUtils::build_FCCAnalysesJet(pjets);

  return result2;
}


clustering_antikt::clustering_antikt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted){m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_antikt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::initialise_FCCAnalysesJet();
  if (input.size()<2) return result;

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::antikt_algorithm;

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, fastjet::RecombinationScheme::E_scheme);
  cs = fastjet::ClusterSequence(input, def);

  //std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);

  std::vector<fastjet::PseudoJet> pjets;

  if (m_sorted == 0){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_ycut(m_cut));
  }
  else if (m_sorted == 1){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_E(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_ycut(m_cut));
  }
  
  JetClusteringUtils::FCCAnalysesJet result2 = JetClusteringUtils::build_FCCAnalysesJet(pjets);

  return result2;
}

clustering_cambridge::clustering_cambridge(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted){m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_cambridge::operator() (std::vector<fastjet::PseudoJet> input) {
  
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::initialise_FCCAnalysesJet();
  if (input.size()<2) return result;

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::cambridge_algorithm;

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, fastjet::RecombinationScheme::E_scheme);
  cs = fastjet::ClusterSequence(input, def);

  //std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);

  std::vector<fastjet::PseudoJet> pjets;

  if (m_sorted == 0){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_ycut(m_cut));
  }
  else if (m_sorted == 1){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_E(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_ycut(m_cut));
  }
  
  JetClusteringUtils::FCCAnalysesJet result2 = JetClusteringUtils::build_FCCAnalysesJet(pjets);

  return result2;
}



clustering_ee_kt::clustering_ee_kt(int arg_exclusive, float arg_cut, int arg_sorted){m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_ee_kt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::initialise_FCCAnalysesJet();
  if (input.size()<2) return result;

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  jetAlgorithm = fastjet::JetAlgorithm::ee_kt_algorithm;

  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, fastjet::RecombinationScheme::E_scheme);
  cs = fastjet::ClusterSequence(input, def);

  //std::vector<fastjet::PseudoJet> pjets = JetClusteringUtils::build_jets(cs, m_exclusive, m_cut, m_sorted);

  std::vector<fastjet::PseudoJet> pjets;

  if (m_sorted == 0){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_ycut(m_cut));
  }
  else if (m_sorted == 1){
    if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_E(cs.inclusive_jets(m_cut));
    else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(m_cut));
    else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(int(m_cut)));
    else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_up_to(int(m_cut)));
    else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_ycut(m_cut));
  }
  
  JetClusteringUtils::FCCAnalysesJet result2 = JetClusteringUtils::build_FCCAnalysesJet(pjets);

  return result2;
}

