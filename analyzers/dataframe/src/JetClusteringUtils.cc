
#include "JetClusteringUtils.h"
using namespace JetClusteringUtils;


ROOT::VecOps::RVec<fastjet::PseudoJet> JetClusteringUtils::get_pseudoJets(FCCAnalysesJet jets){
  return jets.jets;
}

std::vector<std::vector<int>> JetClusteringUtils::get_constituents(FCCAnalysesJet jets){
  return jets.constituents;
}

std::vector<fastjet::PseudoJet> JetClusteringUtils::set_pseudoJets(ROOT::VecOps::RVec<float> px, 
								   ROOT::VecOps::RVec<float> py, 
								   ROOT::VecOps::RVec<float> pz, 
								   ROOT::VecOps::RVec<float> e) {
  std::vector<fastjet::PseudoJet> result;
  unsigned index = 0;
  for (size_t i = 0; i < px.size(); ++i) {
    result.emplace_back(px.at(i), py.at(i), pz.at(i), e.at(i));
    result.back().set_user_index(index);
    ++index;
  }
  return result;
}

std::vector<fastjet::PseudoJet> JetClusteringUtils::set_pseudoJets_xyzm(ROOT::VecOps::RVec<float> px, 
								   ROOT::VecOps::RVec<float> py, 
								   ROOT::VecOps::RVec<float> pz, 
								   ROOT::VecOps::RVec<float> m) {
  std::vector<fastjet::PseudoJet> result;
  unsigned index = 0;
  for (size_t i = 0; i < px.size(); ++i) {
    double px_d = px.at(i);
    double py_d = py.at(i);
    double pz_d = pz.at(i);
    double  m_d =  m.at(i);
    double  E_d = sqrt(px_d*px_d + py_d*py_d + pz_d*pz_d + m_d*m_d);
    result.emplace_back(px_d, py_d, pz_d, E_d);
    result.back().set_user_index(index);
    ++index;
  }
  return result;
}


ROOT::VecOps::RVec<float> JetClusteringUtils::get_px(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.px());
  }
  return result;
}


ROOT::VecOps::RVec<float> JetClusteringUtils::get_py(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.py());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_pz(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.pz());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_e(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_pt(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.pt());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_m(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.m());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_eta(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_phi(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> JetClusteringUtils::get_theta(ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.theta());
  }
  return result;
}



FCCAnalysesJet JetClusteringUtils::initialise_FCCAnalysesJet(){
  
  JetClusteringUtils::FCCAnalysesJet result;
  ROOT::VecOps::RVec<fastjet::PseudoJet> jets;
  std::vector<std::vector<int>> constituents;

  result.jets = jets;
  result.constituents = constituents;

  return result;
};

FCCAnalysesJet JetClusteringUtils::build_FCCAnalysesJet(std::vector<fastjet::PseudoJet> in){
  JetClusteringUtils::FCCAnalysesJet result = JetClusteringUtils::initialise_FCCAnalysesJet();
  for (const auto& pjet : in) {
    result.jets.push_back(pjet);
    
    std::vector<fastjet::PseudoJet> consts = pjet.constituents();
    std::vector<int> tmpvec;
    for (const auto& constituent : consts){
      tmpvec.push_back(constituent.user_index());  
    }
    result.constituents.push_back(tmpvec);
  }
  return result;
}



std::vector<fastjet::PseudoJet> JetClusteringUtils::build_jets(fastjet::ClusterSequence & cs, int exclusive, float cut, int sorted){
  std::vector<fastjet::PseudoJet> pjets;

  if (sorted == 0){
    if(exclusive ==  0 )       pjets = fastjet::sorted_by_pt(cs.inclusive_jets(cut));
    else if( exclusive ==  1)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(cut));
    else if( exclusive ==  2)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets(int(cut)));
    else if( exclusive ==  3)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_up_to(int(cut)));
    else if( exclusive ==  4)  pjets = fastjet::sorted_by_pt(cs.exclusive_jets_ycut(cut));
  }
  else if (sorted == 1){
    if(exclusive ==  0 )       pjets = fastjet::sorted_by_E(cs.inclusive_jets(cut));
    else if( exclusive ==  1)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(cut));
    else if( exclusive ==  2)  pjets = fastjet::sorted_by_E(cs.exclusive_jets(int(cut)));
    else if( exclusive ==  3)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_up_to(int(cut)));
    else if( exclusive ==  4)  pjets = fastjet::sorted_by_E(cs.exclusive_jets_ycut(cut));
  }
  return pjets;
}


bool JetClusteringUtils::check(unsigned int n, int exclusive, float cut){
  if (exclusive>0 && n<=int(cut)) return false;
  return true;
}

fastjet::RecombinationScheme JetClusteringUtils::recomb_scheme(int recombination){
  fastjet::RecombinationScheme recomb_scheme;

  if(recombination == 0) recomb_scheme = fastjet::RecombinationScheme::E_scheme;
  else if (recombination == 1) recomb_scheme = fastjet::RecombinationScheme::pt_scheme;
  else if (recombination == 2) recomb_scheme = fastjet::RecombinationScheme::pt2_scheme;
  else if (recombination == 3) recomb_scheme = fastjet::RecombinationScheme::Et_scheme;
  else if (recombination == 4) recomb_scheme = fastjet::RecombinationScheme::Et2_scheme;
  else if (recombination == 5) recomb_scheme = fastjet::RecombinationScheme::BIpt_scheme;
  else if (recombination == 6) recomb_scheme = fastjet::RecombinationScheme::BIpt2_scheme;
  else recomb_scheme = fastjet::RecombinationScheme::external_scheme;

  return recomb_scheme;
}
