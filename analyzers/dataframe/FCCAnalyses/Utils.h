#ifndef  UTILS_ANALYZERS_H
#define  UTILS_ANALYZERS_H

#include <algorithm>
#include <cmath>
#include "ROOT/RVec.hxx"

namespace FCCAnalyses {
  namespace Utils {


  /// @brief Helper struct to select entries matching a certain predicate.
  /// When instantiated with a function that gives a "yes / no" decision
  /// based on an input object, will support three functionalities: 
  /// - select accepted objects from a list of inputs, return as list
  /// - select indices of selected objects from list of inputs and indices to study,
  ///   return index ist 
  /// - select indicises of objects passing for a set of input lists (nested selection) 
  /// This allows to consistently apply the same selection in multiple ways,
  /// and to easily write new cuts without having to write a lot of 
  /// boilerplate code. 
  /// @tparam thingToSelect: The type of object our decision will be based on 
  /// For example: edm4hep::MCParticleData (for selecting MC particles).
  /// 
  /// One pattern is to create a selector class inheriting from `selByPredicate`, 
  /// where the selection function is specified within the constructor.
  /// Constructor arguments can be passed via lambda capture or `std::bind`
  /// to parametrise cuts where needed. 
  /// This can look like 
  /// @code
  /// struct myPtCut : selByPredicate<edm4hep::MCParticleData>{///
  ///     myPtCut(double ptCutVal): selByPredicate<edm4hep::MCParticleData>(
  ///        [ptCutVal](const edm4hep::MCParticleData & mc){
  ///            return mc.pt() > ptCutVal;
  ///        }){
  ///     }
  /// };
  /// @endcode 
  /// Or, assuming you have an existing selection function 
  /// `doesThisPass(const edm4hep::MCParticleData &, double, int)`
  ///  with some customizable cut parameters
  /// @code
  /// struct myDoesThisPass : selByPredicate<edm4hep::MCParticleData>{///
  ///     myPtCut(double par1, int par2): selByPredicate<edm4hep::MCParticleData>(
  ///        std::bind(doesThisPass,std::placeholders::_1, par1, par2)){
  ///     }
  /// };
  /// @endcode 
  /// Examples for practical usage can be found in `MCParticle.h`, see for example #sel_pt. 
  /// In the python steering, you would then typically instantiate the
  /// derived cut classes, for example
  /// @code
  /// df = df.Define("particles_passing","myPtCut(10)(particles_to_check)")
  /// @endcode 
  /// or (for indices)
  /// @code
  /// df = df.Define("particle_indices_passing","myPtCut(10)(particle_indices_to_check, allParticles)")
  /// @endcode 
  template <class thingToSelect> 
  struct selByPredicate {
    /// @brief constructor - instantiate by passing a selection function. 
    /// For implementing selections with configurable parameters
    /// (e.g. cut values), look at lambda captures or `std::bind`. 
    selByPredicate(
        std::function<bool(const thingToSelect &)> thePredicate)
        : m_predicate(thePredicate){}

    /// @brief Select passing objects from a list of candidates,
    /// return by (deep-)copy 
    /// @param in: List of candidates to run the selection on 
    /// @return A list of candidates for which `m_predicate` evaluates
    /// as `true`. 
    ROOT::VecOps::RVec<thingToSelect>
    operator()(const ROOT::VecOps::RVec<thingToSelect> &in){
      ROOT::VecOps::RVec<thingToSelect> result;
      result.reserve(in.size());
      for (auto & p : in) {
        if (m_predicate(p)) result.emplace_back(p);
      } 
      return result; 
    }

    /// @brief Select passing objects from a list of candidates,
    /// return by index
    /// @param indices: List of indices of candidates within `in` 
    //                  to consider for selection 
    /// @param in: List of candidates to which indices in `indices` refer. 
    /// @return A list of indices of candidates within the `in` 
    //          vector for which `m_predicate` evaluates as `true`. 
    ROOT::VecOps::RVec<int> operator() (const ROOT::VecOps::RVec<int> & indices, const ROOT::VecOps::RVec<thingToSelect> & in){
      ROOT::VecOps::RVec<int> result;
      result.reserve(in.size());
      for (int index : indices) {
        if (index < 0 || index >= in.size()) continue; 
        if (m_predicate(in[index])) result.emplace_back(index);
      } 
      return result; 
    }

    /// @brief Select (several) lists of passing objects from (several) lists of candidates,
    /// return by lists of indices. Used to select on several (similar) lists at once. 
    /// For example: Track selection within (many) vertex candidates. 
    /// @param setsOfIndices: Multiple lists of indices referring to `in`  
    /// @param in: List of candidates to which indices in `setsOfIndices` refer. 
    /// @return A list of index lists of similar size as `setsOfIndices`. 
    ///         For each element, the list contains the output of `operator()`
    ///         run on the indices of the given element of `setsOfIndices`. 
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> operator() (
      const ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> & setsOfIndices, 
      const ROOT::VecOps::RVec<thingToSelect> & in){
      ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result(setsOfIndices.size());
      for (int elem = 0; elem <  setsOfIndices.size(); ++elem){
        result[elem] = this->operator()(setsOfIndices[elem], in); 
      }
      return result; 
    }
    private: 
    /// Stored selection function.
    std::function<bool(const thingToSelect &)> m_predicate; 
  };


    template<typename T> inline auto getsize( T& vec){ return vec.size();};
    template <typename T>
    inline ROOT::VecOps::RVec<ROOT::VecOps::RVec<T>>
    as_vector(const ROOT::VecOps::RVec<T> &in) {
      return ROOT::VecOps::RVec<ROOT::VecOps::RVec<T>>(1, in);
    };
    template <typename T>
    inline ROOT::VecOps::RVec<int>
    index_range(const ROOT::VecOps::RVec<T> &in) {
      ROOT::VecOps::RVec<int> indices(in.size());
      std::iota(indices.begin(), indices.end(), 0);
      return indices;
    };
    /// @brief count the number of valid (>=0, < size of collection) indices in
    /// an index list
    /// @param in: index list
    /// @param ref: particle vector to which the indices refer.
    /// @return integer count of valid indices
    template <typename T>
    inline int count_valid_indices(const ROOT::VecOps::RVec<int> &in,
                                   const ROOT::VecOps::RVec<T> &ref) {
      int maxSize = ref.size();
      return std::count_if(in.begin(), in.end(), [maxSize](const int &i) {
        return (i >= 0 && i < maxSize);
      });
    };

    // @brief for a given list of indices, returns a list of particle (copies)
    /// @param idx : Indices of desired particles within the full set ("in")
    /// @param in : Full set of particles
    /// @return A vector of particles with the desired indices.
    template <typename T>
    inline ROOT::VecOps::RVec<T> sel_byIndex(const ROOT::VecOps::RVec<int> &idx,
                                             const ROOT::VecOps::RVec<T> &in) {
      ROOT::VecOps::RVec<T> found;
      for (int index : idx) {
        if (index < 0 || index >= in.size())
          continue;
        found.push_back(in.at(index));
      }
      return found;
    }
    // @brief merge (concatenate) two collections of arbitrary content
    /// @param x : first collection - entries will be copied in-order
    /// @param y : second collection - entries will be copied in-order after the
    /// last element of the first
    /// @return A combined collection of size (x.size()+y.size()), containing
    /// the content of x followed by that of y
    template <typename T>
    inline ROOT::VecOps::RVec<T> merge(const ROOT::VecOps::RVec<T> &x,
                                       const ROOT::VecOps::RVec<T> &y) {
      ROOT::VecOps::RVec<T> merged;
      merged.reserve(x.size() + y.size());
      merged.insert(merged.end(), x.begin(), x.end());
      merged.insert(merged.end(), y.begin(), y.end());
      return merged;
    }
  }
}

#endif
