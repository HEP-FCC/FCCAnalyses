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

#include <TH1.h>
#include <cmath>

using namespace std::string_literals;

namespace mplt::root::utils {
/// Adjust x- and y-axis labels if a physical unit is specified
void adjust_labels(TH1 *histogram, std::string_view xaxis_unit) {
  if (xaxis_unit.empty())
    return;
  if (std::string hist_xlabel{histogram->GetXaxis()->GetTitle()};
      hist_xlabel.find(" (") == std::string::npos) {
    hist_xlabel += " ("s + std::string{xaxis_unit} + ")"s;
    histogram->GetXaxis()->SetTitle(hist_xlabel.data());
  }
  if (std::string hist_ylabel{histogram->GetYaxis()->GetTitle()};
      hist_ylabel.find(" / ") == std::string::npos) {
    hist_ylabel +=
        Form(" / %g %s", histogram->GetBinWidth(1), xaxis_unit.data());
    histogram->GetYaxis()->SetTitle(hist_ylabel.data());
  }
}

/// Add pre/post-range bins to a given histogram
void add_underflow_overflow_bins(TH1 *histogram,
                                 std::pair<double, double> range,
                                 bool propagate_unc) {
  int first_bin = 1, last_bin = histogram->GetNbinsX();
  if (range != std::make_pair(0., 0.)) {
    histogram->GetXaxis()->SetRangeUser(range.first, range.second);
    first_bin = histogram->GetXaxis()->GetFirst(); // range's first/last bins
    last_bin = histogram->GetXaxis()->GetLast();
  }

  // GetBinError returns sqrt(SumW2) for a given bin
  // SetBinError updates SumW2 for a given bin with error*error
  float underflow = 0.f, underflow_sumw2 = 0.f;
  for (int i = 0; i < first_bin; ++i) {
    underflow += histogram->GetBinContent(i);
    underflow_sumw2 += histogram->GetBinError(i) * histogram->GetBinError(i);
  }
  float overflow = 0.f, overflow_sumw2 = 0;
  for (int i = last_bin + 1; i <= histogram->GetNbinsX() + 1; ++i) {
    overflow += histogram->GetBinContent(i);
    overflow_sumw2 += (histogram->GetBinError(i) * histogram->GetBinError(i));
  }
  // Clear out-of-range bin content so that Integral() still returns the right
  // value
  for (int i = 1; i < first_bin; i++)
    histogram->SetBinContent(i, 0);
  for (int i = last_bin + 1; i < histogram->GetNbinsX() + 1; i++)
    histogram->SetBinContent(i, 0);
  // Clear also underflow and overflow bins
  // (SetBinContent on these may try to extend the axes)
  histogram->ClearUnderflowAndOverflow();

  float first_bin_content = histogram->GetBinContent(first_bin),
        first_bin_sumw2 = histogram->GetBinError(first_bin) *
                          histogram->GetBinError(first_bin);
  float last_bin_content = histogram->GetBinContent(last_bin),
        last_bin_sumw2 =
            histogram->GetBinError(last_bin) * histogram->GetBinError(last_bin);

  histogram->SetBinContent(first_bin, first_bin_content + underflow);
  histogram->SetBinContent(last_bin, last_bin_content + overflow);
  if (propagate_unc) {
    histogram->SetBinError(first_bin,
                           std::sqrt(underflow_sumw2 + first_bin_sumw2));
    histogram->SetBinError(last_bin,
                           std::sqrt(overflow_sumw2 + last_bin_sumw2));
  }
}
} // namespace mplt::root::utils
