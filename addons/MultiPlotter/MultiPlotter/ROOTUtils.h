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

#include <string_view>

class TH1;
namespace mplt {
class ROOTCanvas;
class Stack;
} // namespace mplt

namespace mplt::root::utils {
/// Adjust x- and y-axis labels if a physical unit is specified
void adjust_labels(TH1 *histogram, std::string_view xaxis_unit);
/// Add pre/post-range bins to a given histogram
void add_underflow_overflow_bins(
    TH1 *histogram, const std::pair<double, double> &range = std::pair(0., 0.),
    bool propagate_unc = true);
/// Draw a stack of multiple samples
void draw_samples_stack(ROOTCanvas &, const Stack &, bool stacked,
                        Style_t fill_style);
/// Merge all histograms in a sample into one single histogram
/// (with error propagation)
std::unique_ptr<TH1> merge_samples(const Stack &);
} // namespace mplt::root::utils
