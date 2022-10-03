#include "FCCAnalyses/JetClusteringUtils.h"

namespace FCCAnalyses{

namespace JetClusteringUtils{


ROOT::VecOps::RVec<fastjet::PseudoJet> get_pseudoJets(const FCCAnalysesJet &jets){
  return jets.jets;
}

std::vector<std::vector<int>> get_constituents(const FCCAnalysesJet &jets){
  return jets.constituents;
}


float get_exclusive_dmerge(const FCCAnalysesJet &in,
                                               int n) {
  float d = -1;
  if ( n >= 1 &&  n <= Nmax_dmerge) d= in.exclusive_dmerge[n-1] ;
  return d;
}

float get_exclusive_dmerge_max(const FCCAnalysesJet &in,
                                                   int n) {
  float d = -1;
  if ( n >= 1 &&  n <= Nmax_dmerge) d= in.exclusive_dmerge_max[n-1] ;
  return d;
}

std::vector<fastjet::PseudoJet> set_pseudoJets(const ROOT::VecOps::RVec<float> &px,
                                                                   const ROOT::VecOps::RVec<float> &py,
                                                                   const ROOT::VecOps::RVec<float> &pz,
                                                                   const ROOT::VecOps::RVec<float> &e){
  std::vector<fastjet::PseudoJet> result;
  unsigned index = 0;
  for (size_t i = 0; i < px.size(); ++i) {
    result.emplace_back(px[i], py[i], pz[i], e[i]);
    result.back().set_user_index(index);
    ++index;
  }
  return result;
}

std::vector<fastjet::PseudoJet> set_pseudoJets_xyzm(const ROOT::VecOps::RVec<float> &px,
                                                                        const ROOT::VecOps::RVec<float> &py,
                                                                        const ROOT::VecOps::RVec<float> &pz,
                                                                        const ROOT::VecOps::RVec<float> &m){
  std::vector<fastjet::PseudoJet> result;
  unsigned index = 0;
  for (size_t i = 0; i < px.size(); ++i) {
    double px_d = px[i];
    double py_d = py[i];
    double pz_d = pz[i];
    double  m_d =  m[i];
    double  E_d = sqrt(px_d*px_d + py_d*py_d + pz_d*pz_d + m_d*m_d);
    result.emplace_back(px_d, py_d, pz_d, E_d);
    result.back().set_user_index(index);
    ++index;
  }
  return result;
}


ROOT::VecOps::RVec<float> get_px(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.px());
  }
  return result;
}


ROOT::VecOps::RVec<float> get_py(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.py());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pz(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.pz());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_e(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.pt());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_m(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.m());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_eta(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_phi(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_theta(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.theta());
  }
  return result;
}



FCCAnalysesJet initialise_FCCAnalysesJet(){

  FCCAnalysesJet result;
  ROOT::VecOps::RVec<fastjet::PseudoJet> jets;
  std::vector<std::vector<int>> constituents;

  result.jets = jets;
  result.constituents = constituents;

  std::vector<float> exclusive_dmerge;
  std::vector<float> exclusive_dmerge_max;
  exclusive_dmerge.reserve(Nmax_dmerge);
  exclusive_dmerge_max.reserve(Nmax_dmerge);

  result.exclusive_dmerge = exclusive_dmerge;
  result.exclusive_dmerge_max = exclusive_dmerge_max;

  return result;
};

FCCAnalysesJet build_FCCAnalysesJet(const std::vector<fastjet::PseudoJet> &in,
                                                        const std::vector<float> &dmerge,
                                                        const std::vector<float> &dmerge_max){

  FCCAnalysesJet result = initialise_FCCAnalysesJet();
  for (const auto& pjet : in) {
    result.jets.push_back(pjet);

    std::vector<fastjet::PseudoJet> consts = pjet.constituents();
    std::vector<int> tmpvec;
    for (const auto& constituent : consts){
      tmpvec.push_back(constituent.user_index());
    }
    result.constituents.push_back(tmpvec);
  }
  result.exclusive_dmerge = dmerge;
  result.exclusive_dmerge_max = dmerge_max;
  return result;
}



std::vector<fastjet::PseudoJet> build_jets(fastjet::ClusterSequence &cs,
                                                               int exclusive,
                                                               float cut,
                                                               int sorted){
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

std::vector<float> exclusive_dmerge(fastjet::ClusterSequence &cs,
                                                        int do_dmarge_max) {

  const int Nmax = Nmax_dmerge;
  std::vector<float>  result;
  for (int i=1; i <= Nmax; i++) {
     	float  d;
	const int j = i;
     	if ( do_dmarge_max == 0) d = cs.exclusive_dmerge( j );
	else d = cs.exclusive_dmerge_max( j ) ;
	result.push_back( d );
  }
  return result;
}


bool check(unsigned int n,
                               int exclusive,
                               float cut){
  if (exclusive>0 && n<=int(cut)) return false;
  return true;
}

fastjet::RecombinationScheme recomb_scheme(int recombination){
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

}//end NS JetClusteringUtils

}//end NS FCCAnalyses
