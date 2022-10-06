// -*- C++ -*-
//
/** FCCAnalysis module: __pkgname__
 *
 * \file __name__.cc
 * \author __author__
 */

#include "__name__.h"
#include <iostream>

using namespace std;

namespace __pkgname__ {
  void dummy_analysis() { cout << "Dummy analysis initialised." << endl; }

  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>& parts) {
    rv::RVec<float> output;
    for (size_t i = 0; i < parts.size(); ++i)
      output.emplace_back(parts.at(i).momentum.x);
    return output;
  }
}  // namespace __pkgname__
