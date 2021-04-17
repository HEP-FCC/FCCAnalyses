#include <iostream>
#include <cstdlib>
#include <vector>

#include "myFinalSel.h"

using namespace myFinalSel;

int myFinalSel::selTauCand( ROOT::VecOps::RVec<float> mass,
			    ROOT::VecOps::RVec<int> vertex_ind,
			    ROOT::VecOps::RVec<float> vertex_chi2){
  float bestchi2=9999999.;
  int indbestchi2=-999;
  for (size_t i = 0; i < mass.size(); ++i){
    if (mass.at(i)>2.)  continue;
    if (mass.at(i)<0.6) continue;
    if (vertex_chi2.at(vertex_ind.at(i))<0.) continue;
    if (vertex_chi2.at(vertex_ind.at(i))>10.) continue;
    //if (fabs(vertex_chi2.at(vertex_ind.at(i))-1.)<bestchi2)bestchi2=vertex_chi2.at(vertex_ind.at(i));
    if (vertex_chi2.at(vertex_ind.at(i)) < bestchi2) {bestchi2=vertex_chi2.at(vertex_ind.at(i)); indbestchi2=i;}
    
  }
  return indbestchi2;
}


int myFinalSel::selTauCandTM(ROOT::VecOps::RVec<int> mcvertex,
			     ROOT::VecOps::RVec<int> truevertex,
			     int CandInd){

  int cand = mcvertex.at(CandInd);
  for (auto &p:truevertex)
    if (p==cand)return 1;
  return 0;
  
}
