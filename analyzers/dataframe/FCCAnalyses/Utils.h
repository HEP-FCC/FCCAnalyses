#ifndef UTILS_ANALYZERS_H
#define UTILS_ANALYZERS_H

#include <algorithm>
#include <cmath>

namespace FCCAnalyses {
namespace Utils {

template <typename T> inline auto getsize(T &vec) { return vec.size(); };
template <typename T>
inline ROOT::VecOps::RVec<ROOT::VecOps::RVec<T>>
as_vector(const ROOT::VecOps::RVec<T> &in) {
  return ROOT::VecOps::RVec<ROOT::VecOps::RVec<T>>(1, in);
};
template <typename T>
inline ROOT::VecOps::RVec<int> index_range(const ROOT::VecOps::RVec<T> &in) {
  ROOT::VecOps::RVec<int> indices(in.size());
  std::iota(indices.begin(), indices.end(), 0);
  return indices;
};
/// @brief count the number of valid (>=0, < size of collection) indices in an
/// index list
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
/// @return A combined collection of size (x.size()+y.size()), containing the
/// content of x followed by that of y
template <typename T>
inline ROOT::VecOps::RVec<T> merge(const ROOT::VecOps::RVec<T> &x,
                                   const ROOT::VecOps::RVec<T> &y) {
  ROOT::VecOps::RVec<T> merged;
  merged.reserve(x.size() + y.size());
  merged.insert(merged.end(), x.begin(), x.end());
  merged.insert(merged.end(), y.begin(), y.end());
  return merged;
}
} // namespace Utils
} // namespace FCCAnalyses

#endif
