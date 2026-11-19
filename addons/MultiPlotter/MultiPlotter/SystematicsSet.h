/*
 *  MultiPlotter: a standalone tool for the prettification of plots
 *  Copyright (C) 2026  Laurent Forthomme <laurent.forthomme@cern.ch>
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef MultiPlotter_SystematicsSet_h
#define MultiPlotter_SystematicsSet_h

#include <memory>
#include <string>
#include <vector>

// forward declarations
class TH1; // still ROOT-based

namespace mplt {
/// Systematics distributions: nominal, +1sigma, and -1sigma shapes
/// \author Laurent Forthomme <laurent.forthomme@cern.ch>
/// \date July 2026
class SystematicsSet {
public:
  explicit SystematicsSet(const TH1 *);

  void reset();       ///< restore the nominal shape to the one provided
  void scale(float);  ///< rescale all shapes by a given factor
  void rebin(size_t); ///< rebin all shapes histograms by a given factor

  using Values = std::pair<float, float>;

  /// Maximum (between upper and lower) uncertainty for each bin
  std::vector<float> binnedMaximumUncertainty() const;
  /// Independent upper/lower uncertainty for each bin
  std::vector<Values> binnedAsymmetricUncertainties() const;
  std::vector<Values> binnedShifts() const; ///< Signed, binned shifts
  float totalUncertainty() const; ///< Total uncertainty from binned shape

  std::unique_ptr<TH1> shapeUp() const;
  std::unique_ptr<TH1> shapeDown() const;

  std::shared_ptr<TH1> nominal_shape;
  std::shared_ptr<TH1> up_shape;
  std::shared_ptr<TH1> down_shape;

private:
  // do not expose the true distributions, only used for bookkeeping/reset
  std::shared_ptr<TH1> true_nominal_shape_;
  std::shared_ptr<TH1> true_up_shape_;
  std::shared_ptr<TH1> true_down_shape_;
};
} // namespace mplt

#endif
