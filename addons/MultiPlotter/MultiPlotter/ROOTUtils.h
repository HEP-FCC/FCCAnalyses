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

#ifndef MultiPlotter_ROOTUtils_h
#define MultiPlotter_ROOTUtils_h

#include <memory>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

class TGraphAsymmErrors;
class TH1;
class TH1D;
class TLegend;
namespace mplt {
class ROOTCanvas;
class Stack;
} // namespace mplt

namespace mplt::root::utils {
static constexpr std::array<Color_t, 9> colours = {
    kBlack,      kRed + 1,  kAzure + 1,  kGreen + 2, kMagenta + 1,
    kOrange + 7, kCyan + 2, kViolet + 5, kPink + 6};

/// Adjust x- and y-axis labels if a physical unit is specified
void adjust_labels(TH1 *histogram, std::string_view xaxis_unit);
/// Add pre/post-range bins to a given histogram
void add_underflow_overflow_bins(
    TH1 *histogram, const std::pair<double, double> &range = std::pair(0., 0.),
    bool propagate_unc = true);
/// Draw a stack of multiple samples
/// \return Statistical uncertainty band of the merged samples (if any)
TH1 *draw_samples_stack(ROOTCanvas &, const Stack &, bool stacked,
                        Style_t fill_style);
std::unique_ptr<TH1> merge_samples(const Stack &); ///< Merge all histograms

/// Systematic uncertainties on the total yield of a stack of samples
struct StackSystematics {
  using Binned = std::vector<std::pair<double, double>>;
  std::unordered_map<std::string, Binned> sources; ///< Total yield shifts
  Binned total; ///< Total (upwards, downwards) uncertainty
  bool empty() const { return sources.empty(); }
};
/// Combine the systematic uncertainties of all samples in a stack
StackSystematics combine_systematics(const Stack &);
/// Largest systematic uncertainty relative to the nominal yield, among all
/// visible bins
double max_relative_systematics(const TH1 &nominal, const StackSystematics &);
/// Book an empty histogram with the same binning as a model, in a canvas
TH1D *book_like(ROOTCanvas &, const TH1 &model, const std::string &name);
/// Draw the stat+syst uncertainty band
TGraphAsymmErrors *draw_uncertainty_band(ROOTCanvas &, const TH1 &nominal,
                                         const StackSystematics &,
                                         bool relative);
/// Draw the up/down shifts of systematic uncertainty sources
/// \param[in] max_sources Maximum number of (leading) sources to be drawn
void draw_systematics_breakdown(ROOTCanvas &, const TH1 &nominal,
                                const StackSystematics &, size_t max_sources,
                                TLegend &);
} // namespace mplt::root::utils

#endif
