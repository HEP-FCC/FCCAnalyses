#ifndef  SMEARING_ANALYZERS_H
#define  SMEARING_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"



///LogNormal smearing in the form of sqrt(aX^2 + bX + c)
struct logNormal {
  logNormal(float arg_a, float arg_b, float arg_c);
  float m_a = 0.;
  float m_b = 0.;
  float m_c = 0.;
  ROOT::VecOps::RVec<float>  operator() (ROOT::VecOps::RVec<float> in);
};

#endif
