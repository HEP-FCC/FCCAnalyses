#ifndef  UTILS_ANALYZERS_H
#define  UTILS_ANALYZERS_H

#include <cmath>

namespace FCCAnalyses {
  namespace Utils {

    template<typename T> inline auto getsize( T& vec){ return vec.size();};
    template<typename T> inline ROOT::VecOps::RVec<ROOT::VecOps::RVec<T> >  as_vector(const ROOT::VecOps::RVec<T>& in){return ROOT::VecOps::RVec<ROOT::VecOps::RVec<T> >(1, in);};                                                                                                                                                                              
  }
}

#endif
