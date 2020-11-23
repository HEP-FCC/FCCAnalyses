#include "Smearing.h"

logNormmal::logNormal(float arg_a, float arg_b, float arg_c){m_a = arg_a; m_b = arg_b; m_c = arg_c;};

ROOT::VecOps::RVec<float> logNormal::operator() (ROOT::VecOps::RVec<float> in) {
  ROOT::VecOps::RVec<float> result;
  for (size_t i = 0; i < in.size(); ++i) {


    
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.push_back(p);
    }
  }
  return result;
}

