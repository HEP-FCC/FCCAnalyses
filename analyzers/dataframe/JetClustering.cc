
#include "JetClustering.h"
using namespace JetClustering;

clustering::clustering(int arg_jetalgo, float arg_radius, int arg_exclusive, float arg_cut){m_jetalgo = arg_jetalgo; m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut;}

ROOT::VecOps::RVec<fastjet::PseudoJet> clustering::operator() (ROOT::VecOps::RVec<float> p_x, ROOT::VecOps::RVec<float> p_y, ROOT::VecOps::RVec<float> p_z, ROOT::VecOps::RVec<float> E) {
  ROOT::VecOps::RVec<fastjet::PseudoJet> result;
  std::vector<fastjet::PseudoJet> input;
  unsigned index = 0;
  for (size_t i = 0; i < p_x.size(); ++i) {
    input.emplace_back(p_x.at(i), p_y.at(i), p_z.at(i), E.at(i));
    input.back().set_user_index(index);
    ++index;
  }


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
  
  fastjet::ClusterSequence* cs;
  fastjet::JetDefinition def(jetAlgorithm, m_radius, fastjet::RecombinationScheme::E_scheme);
  cs = new fastjet::ClusterSequence(input, def);
  std::vector<fastjet::PseudoJet> pjets;
  if(m_exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs->inclusive_jets(m_cut));
  else if( m_exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs->exclusive_jets(m_cut));
  else if( m_exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs->exclusive_jets(int(m_cut)));
  else if( m_exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs->exclusive_jets_up_to(int(m_cut)));
  else if( m_exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs->exclusive_jets_ycut(m_cut));
  for (const auto& pjet : pjets) {
    result.push_back(pjet);
  }
  delete cs;
  return result;
}


ROOT::VecOps::RVec<float> getJet_px(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.px());
  }
  return result;
}


ROOT::VecOps::RVec<float> getJet_py(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.py());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_pz(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.pz());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_e(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_pt(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.pt());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_m(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.m());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_eta(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_phi(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> getJet_theta(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.theta());
  }
  return result;
}

