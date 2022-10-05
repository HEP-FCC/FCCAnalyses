// -*- C++ -*-
//
/** FCCAnalysis module: __ANALYSIS_NAME__
 *
 * \\file __SCRIPT_NAME__.cc
 * \\author __AUTHOR_NAME__ <__AUTHOR_EMAIL__>
 *
 * Description:
 *   __ANALYSIS_DESCRIPTION__
 */

#include "__SCRIPT_NAME__.h"
#include <iostream>

using namespace std;

namespace __ANALYSIS_NAME__ {
  void dummy_analysis() { cout << "Dummy analysis initialised." << endl; }

  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>& parts) {
    rv::RVec<float> output;
    for (size_t i = 0; i < parts.size(); ++i)
      output.emplace_back(parts.at(i).momentum.x);
    return output;
  }
}  // namespace __ANALYSIS_NAME__
