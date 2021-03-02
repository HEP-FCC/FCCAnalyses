
#include "JetClustering.h"
using namespace JetClustering;

clustering_kt::clustering_kt(int arg_jetalgo, float arg_radius, int arg_exclusive, float arg_cut){m_jetalgo = arg_jetalgo; m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut;}
JetClusteringUtils::FCCAnalysesJet JetClustering::clustering_kt::operator() (std::vector<fastjet::PseudoJet> input) {
  
  JetClusteringUtils::FCCAnalysesJet result;
  ROOT::VecOps::RVec<fastjet::PseudoJet> jets;
  std::vector<std::vector<int>> constituents;

  result.jets = jets;
  result.constituents = constituents;

  // initialize jet algorithm
  fastjet::JetAlgorithm jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};
  switch(m_jetalgo)
    {
    case 1:
      jetAlgorithm = fastjet::JetAlgorithm::kt_algorithm;
      break;
    case 2:
      jetAlgorithm = fastjet::JetAlgorithm::antikt_algorithm;
      break;
    case 3:
      jetAlgorithm = fastjet::JetAlgorithm::cambridge_algorithm;
      break;
    }
  
  fastjet::ClusterSequence cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, fastjet::RecombinationScheme::E_scheme);
  cs = fastjet::ClusterSequence(input, def);
  std::vector<fastjet::PseudoJet> pjets;
  if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs.inclusive_jets(m_cut));
  else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(m_cut));
  else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(int(m_cut)));
  else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_up_to(int(m_cut)));
  else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_ycut(m_cut));

  for (const auto& pjet : pjets) {
    jets.push_back(pjet);
  }

  
  for (const auto& pjet : pjets) {
    std::vector<fastjet::PseudoJet> consts = pjet.constituents();
    std::vector<int> tmpvec;
    for (const auto& constituent : consts){
      tmpvec.push_back(constituent.user_index());  
    }
    constituents.push_back(tmpvec);
  }

  result.jets = jets;
  result.constituents = constituents;

  return result;
}


