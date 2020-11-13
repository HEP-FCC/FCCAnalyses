
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


//struct ThrustFitObject {
//double operator()(double* pars) {
//  float thrust(const double *par);
//}
//}
double thrust(const double *par);
double minimize_thrust(std::vector<double> px, std::vector<double> py, std::vector<double> pz);


//struct minimize_thrust {
//  minimize_thrust(std::);
//  float m_min_pt = 20; //> transverse momentum threshold [GeV]
//  std::vector<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
//};


#endif
