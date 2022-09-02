#include "FCCAnalyses/myFinalSel.h"

#include <iostream>
#include <cstdlib>
#include <vector>

namespace FCCAnalyses{

namespace myFinalSel{

int selTauCand(ROOT::VecOps::RVec<float> mass,
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


int selTauCandTM(ROOT::VecOps::RVec<int> mcvertex,
			     ROOT::VecOps::RVec<int> truevertex,
			     int CandInd){

  int cand = mcvertex.at(CandInd);
  for (auto &p:truevertex)
    if (p==cand)return 1;
  return 0;

}


float get_min(ROOT::VecOps::RVec<float> in,
			  float val){

  float min=99999999.;
  for (auto &p:in){
    if (abs(p-val)<0.000000001)
      continue;
    if (p<min)min=p;

  }
  return min;
}

float get_max(ROOT::VecOps::RVec<float> in,
			  float val){

  float max=-9999999.;
  for (auto &p:in){
    if (abs(p-val)<0.000000001)
      continue;
    if (p>max)max=p;

  }
  return max;
}

float get_ave(ROOT::VecOps::RVec<float> in,
			  float val){

  float ave=0.;
  float aven=0.;

  for (auto &p:in){
    if (abs(p-val)<0.000000001)
      continue;

    ave+=p;
    aven+=1.;
  }
  if (aven>0.)
    return ave/aven;
  return -999999.;
}


float get_min(ROOT::VecOps::RVec<float> in,
			  ROOT::VecOps::RVec<int> ispv,
			  int index){
  float min = 9999999.;

  for (size_t i = 0; i < in.size(); ++i){
    if (ispv.at(i)>0)continue;
    if (index==i)continue;
    if (in.at(i)<min)min=in.at(i);
  }
  return min;
}
float get_max(ROOT::VecOps::RVec<float> in,
			  ROOT::VecOps::RVec<int> ispv,
			  int index){
  float max = -9999999.;

  for (size_t i = 0; i < in.size(); ++i){
    if (ispv.at(i)>0)continue;
    if (index==i)continue;
    if (in.at(i)>max)max=in.at(i);
  }
  return max;
}


float get_ave(ROOT::VecOps::RVec<float> in,
			  ROOT::VecOps::RVec<int> ispv,
			  int index){

  float ave=0.;
  float aven=0.;
  for (size_t i = 0; i < in.size(); ++i){
    if (ispv.at(i)>0)continue;
    if (index==i)continue;

    ave+=in.at(i);
    aven+=1.;
  }
  if (aven>0.)
    return ave/aven;
  return -999999.;
}

}//end NS myFinalSel

}//end NS FCCAnalyses
