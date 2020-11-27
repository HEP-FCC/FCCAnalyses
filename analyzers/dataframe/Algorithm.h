
#ifndef  ALGORITHM_ANALYZERS_H
#define  ALGORITHM_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"
#include "TFitter.h"


struct sphericityFit {
  sphericityFit(ROOT::VecOps::RVec<float> arg_px, ROOT::VecOps::RVec<float> arg_py, ROOT::VecOps::RVec<float> arg_pz);
  ROOT::VecOps::RVec<float> m_px;
  ROOT::VecOps::RVec<float> m_py;
  ROOT::VecOps::RVec<float> m_pz;
  float operator()(const double *par);
};


struct minimize_sphericity {
  minimize_sphericity(std::string arg_minname, std::string arg_algoname);
  char const *m_minname  = "Minuit2";
  char const *m_algoname = "";
  ROOT::VecOps::RVec<float> operator()(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz);
};



struct thrustFit {
  thrustFit(ROOT::VecOps::RVec<float> arg_px, ROOT::VecOps::RVec<float> arg_py, ROOT::VecOps::RVec<float> arg_pz);
  ROOT::VecOps::RVec<float> m_px;
  ROOT::VecOps::RVec<float> m_py;
  ROOT::VecOps::RVec<float> m_pz;
  float operator()(const double *par);
};


struct minimize_thrust {
  minimize_thrust(std::string arg_minname, std::string arg_algoname);
  char const *m_minname  = "Minuit2";
  char const *m_algoname = "";
  ROOT::VecOps::RVec<float> operator()(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz);
};


ROOT::VecOps::RVec<float> thrust_angle(ROOT::VecOps::RVec<float> thrust, ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz);

struct getThrustCharge {
  getThrustCharge(bool arg_pos);
  bool m_pos = 0;
  float operator() (ROOT::VecOps::RVec<float> thrust_angle, ROOT::VecOps::RVec<float> charge,ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz);
};


#endif
