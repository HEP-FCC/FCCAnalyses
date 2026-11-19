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

#ifndef MultiPlotter_MultiPlotter_h
#define MultiPlotter_MultiPlotter_h

#include "MultiPlotter/Sample.h"
#include <memory>

namespace mplt {
/// Base, virtual plotting utility object
/// \author Laurent Forthomme <laurent.forthomme@cern.ch>
/// \date June 2026
class MultiPlotter {
public:
  explicit MultiPlotter(std::string_view experiment_name,
                        const std::vector<std::string> &extra_labels);
  virtual ~MultiPlotter() = default;

  /// Add a new sample (and its attributes) to a given samples category
  Sample &addSample(Sample &sample);
  /// Generate a data sample out of the background-only hypothesis
  /// \param[in] fluctuate Poisson fluctuation, or Asimov dataset
  Sample &addPseudoData(bool fluctuate = true, unsigned int seed = 42,
                        const std::string &name = "Pseudo-data");
  void sortSamples(SortingType, bool reverse = false);
  void rebin(int factor);                 ///< Apply x-axis rebinning
  void setXRange(double min, double max); ///< Set x-axis range
  void addOverflow(); ///< Add the x-axis (under/over)flow bins
  /// List of samples registered for a given category
  const std::vector<Sample> &samples(Sample::Type) const;

  /// Add a visual text box of a given size at a given position into the canvas
  /// (units: normalised to 1 ; 0=leftmost/bottommost, 1=rightmost/topmost)
  virtual void addTextBox(float x1, float y1, const std::vector<std::string> &);
  /// Core method: perform the plotting operation using all samples, with a
  /// given set of user-defined options
  virtual void plot(std::string_view output_file, std::string_view output_dir,
                    PyObject *options) = 0;

  std::string yieldsTable() const;

protected:
  const std::string experiment_name_;
  const std::vector<std::string> extra_labels_;
  std::unordered_map<Sample::Type, Stack> samples_;

  std::vector<std::shared_ptr<TH1>> pseudo_data_; ///< generated pseudo-data
  bool binning_frozen_{false}; ///< x-axis range or overflow already set?

  using BoxCoordinates = std::pair<float, float>;
  std::vector<std::pair<BoxCoordinates, std::vector<std::string>>> text_boxes_;
};
} // namespace mplt

#endif
