
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
  sphericityFit(std::vector<float> arg_px, std::vector<float> arg_py, std::vector<float> arg_pz);
  std::vector<float> m_px;
  std::vector<float> m_py;
  std::vector<float> m_pz;
  float operator()(const double *par);
};


struct minimize_sphericity {
  minimize_sphericity(std::string arg_minname, std::string arg_algoname);
  char const *m_minname  = "Minuit2";
  char const *m_algoname = "";
  std::vector<float> operator()(std::vector<float> px, std::vector<float> py, std::vector<float> pz);
};



struct thrustFit {
  thrustFit(std::vector<float> arg_px, std::vector<float> arg_py, std::vector<float> arg_pz);
  std::vector<float> m_px;
  std::vector<float> m_py;
  std::vector<float> m_pz;
  float operator()(const double *par);
};


struct minimize_thrust {
  minimize_thrust(std::string arg_minname, std::string arg_algoname);
  char const *m_minname  = "Minuit2";
  char const *m_algoname = "";
  std::vector<float> operator()(std::vector<float> px, std::vector<float> py, std::vector<float> pz);
};


std::vector<float> axisCosTheta(std::vector<float> axis, std::vector<float> px, std::vector<float> py, std::vector<float> pz);

struct getAxisCharge {
  getAxisCharge(bool arg_pos);
  bool m_pos = 0;
  float operator() (std::vector<float> angle, std::vector<float> charge,std::vector<float> px, std::vector<float> py, std::vector<float> pz);
};


#endif
