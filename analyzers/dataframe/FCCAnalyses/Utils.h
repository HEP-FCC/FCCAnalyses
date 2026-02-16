#ifndef  UTILS_ANALYZERS_H
#define  UTILS_ANALYZERS_H

#include <cmath>
#include <algorithm>

namespace FCCAnalyses {
  namespace Utils {

    template<typename T> inline auto getsize( T& vec){ return vec.size();};
    template<typename T> inline ROOT::VecOps::RVec<ROOT::VecOps::RVec<T> >  as_vector(const ROOT::VecOps::RVec<T>& in){return ROOT::VecOps::RVec<ROOT::VecOps::RVec<T> >(1, in);};     
    template <typename T> inline ROOT::VecOps::RVec<int> index_range(const ROOT::VecOps::RVec<T> & in){
      ROOT::VecOps::RVec<int> indices(in.size()); 
      std::iota(indices.begin(),indices.end(), 0);
      return indices; 
    };  
    /// @brief count the number of valid (>=0, < size of collection) indices in an index list 
    /// @param in: index list
    /// @param ref: particle vector to which the indices refer. 
    /// @return integer count of valid indices 
    template <typename T> inline int count_valid_indices(const ROOT::VecOps::RVec<int> & in,
                                                         const ROOT::VecOps::RVec<T> & ref){
      int maxSize = ref.size(); 
      return std::count_if(in.begin(),in.end(),[maxSize](const int & i){return (i >=0 && i < maxSize);}); 
    };

    // @brief for a given list of indices, returns a list of particle (copies) 
    /// @param idx : Indices of desired particles within the full set ("in")
    /// @param in : Full set of particles 
    /// @return A vector of particles with the desired indices. 
    template <typename T> inline ROOT::VecOps::RVec<T> sel_byIndex( const ROOT::VecOps::RVec<int> & idx, const ROOT::VecOps::RVec<T> & in){
      ROOT::VecOps::RVec<T> found; 
      for (int index : idx){
        if (index < 0 || index >= in.size()) continue; 
        found.push_back(in.at(index)); 
      }
      return found; 
    }
  }
}

#endif
