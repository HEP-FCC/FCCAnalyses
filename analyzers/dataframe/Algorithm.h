
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



/*struct ThrustFitObject {
double operator()(double* pars) { // the implementation above }
const std::vector<double>& _px;
// same for _py, _pz
};


struct selRP_pT {
  selRP_pT(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  float operator() (double *par);
};


*/

struct thrustFit {
  thrustFit(std::vector<float> arg_px, std::vector<float> arg_py, std::vector<float> arg_pz);
  std::vector<float> m_px;
  std::vector<float> m_py;
  std::vector<float> m_pz;
  float operator()(double *par);
};


double thrust(const double *par);


struct minimize_thrust {
  minimize_thrust(char *arg_minname, char* arg_algoname);
  char const *m_minname  = "Minuit2";
  char const *m_algoname = "";
  float operator()(std::vector<float> px, std::vector<float> py, std::vector<float> pz);
};


#endif
