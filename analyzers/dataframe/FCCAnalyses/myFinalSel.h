#ifndef MYFINALSEL_ANALYZERS_H
#define MYFINALSEL_ANALYZERS_H
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"

#include "TLorentzVector.h"
#include <vector>

namespace FCCAnalyses{

namespace myFinalSel{

  int selTauCand( ROOT::VecOps::RVec<float> mass,
		  ROOT::VecOps::RVec<int> vertex_ind,
		  ROOT::VecOps::RVec<float> vertex_chi2);

  int selTauCandTM(ROOT::VecOps::RVec<int> mcvertex,
		   ROOT::VecOps::RVec<int> truevertex,
		   int CandInd);

  float get_min(ROOT::VecOps::RVec<float> in,
		float val);
  float get_max(ROOT::VecOps::RVec<float> in,
		float val);
  float get_ave(ROOT::VecOps::RVec<float> in,
		float val);


  float get_min(ROOT::VecOps::RVec<float> in,
		ROOT::VecOps::RVec<int> ispv,
		int index);
  float get_max(ROOT::VecOps::RVec<float> in,
		ROOT::VecOps::RVec<int> ispv,
		int index);
  float get_ave(ROOT::VecOps::RVec<float> in,
		ROOT::VecOps::RVec<int> ispv,
		int index);

}//end NS myFinalSel

}//end NS FCCAnalyses

#endif
