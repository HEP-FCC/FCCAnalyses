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

#ifndef MultiPlotter_plotItPlotter_h
#define MultiPlotter_plotItPlotter_h

#include "MultiPlotter.h"
#include <TLatex.h>
#include <pybind11/pybind11.h>

// forward definitions
class TCanvas;

namespace mplt {
/// plotIt-like plotting utility object
/// \author Laurent Forthomme <laurent.forthomme@cern.ch>
/// \date July 2026
class plotItPlotter : public MultiPlotter {
public:
  explicit plotItPlotter(std::string_view experiment_name,
                         const std::vector<std::string> &extra_labels);

  void plot(std::string_view output_file, std::string_view output_dir,
            PyObject *options) override;

private:
  /// prepare per-stack histograms before plotting
  void prepareStacksPlotting(TCanvas &) const;
};
} // namespace mplt

#endif
