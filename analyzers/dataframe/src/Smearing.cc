#include "FCCAnalyses/Smearing.h"

logNormal::logNormal(float arg_a, float arg_b, float arg_c){m_a = arg_a; m_b = arg_b; m_c = arg_c;};

ROOT::VecOps::RVec<float> logNormal::operator() (ROOT::VecOps::RVec<float> in) {
  ROOT::VecOps::RVec<float> result;

  return result;
}
