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

#include "MultiPlotter/ROOTUtils.h"
#include "MultiPlotter/ROOTCanvas.h"
#include "MultiPlotter/Sample.h"
#include <TGraphAsymmErrors.h>
#include <TH1.h>
#include <THStack.h>
#include <TLegend.h>
#include <algorithm>
#include <cmath>
#include <functional>
#include <ranges>

using namespace std::string_literals;

namespace mplt::root::utils {
/// Adjust x- and y-axis labels if a physical unit is specified
void adjust_labels(TH1 *histogram, std::string_view xaxis_unit) {
  if (xaxis_unit.empty())
    return;
  if (std::string hist_xlabel{histogram->GetXaxis()->GetTitle()};
      hist_xlabel.find(" (") == std::string::npos &&
      hist_xlabel.find(" [") == std::string::npos) { // not already quoted
    hist_xlabel += " ("s + std::string{xaxis_unit} + ")"s;
    histogram->GetXaxis()->SetTitle(hist_xlabel.data());
  }
  if (std::string hist_ylabel{histogram->GetYaxis()->GetTitle()};
      hist_ylabel.find(" / ") == std::string::npos) {
    if (hist_ylabel.empty())
      hist_ylabel = "Events";
    hist_ylabel +=
        Form(" / %g %s", histogram->GetBinWidth(1), xaxis_unit.data());
    histogram->GetYaxis()->SetTitle(hist_ylabel.data());
  }
}

TH1 *draw_samples_stack(ROOTCanvas &canvas, const Stack &stack, bool stacked,
                        Style_t fill_style, bool with_stat_band) {
  auto *root_stack = canvas.make<THStack>();
  for (const auto &sample : stack.samples()) {
    if (sample.histogram) // only stack if a histogram is present
      root_stack->Add(sample.histogram, sample.name.data());
  }
  TH1 *hist_merged{nullptr};
  if (with_stat_band)
    hist_merged = canvas.make<TH1D>(
        *dynamic_cast<TH1D *>(merge_samples(stack).release()));
  if (hist_merged) {
    hist_merged->SetLineWidth(0);
    hist_merged->SetFillStyle(fill_style);
    hist_merged->SetFillColor(kGray + 1);
    hist_merged->Draw("e2,same");
  }
  root_stack->Draw(("hist,same,"s + (stacked ? ""s : "nostack"s)).data());
  return hist_merged;
}

std::unique_ptr<TH1> merge_samples(const Stack &stack) {
  std::unique_ptr<TH1> hist_merged;
  for (const auto &sample : stack.samples()) {
    if (sample.histogram) { // only stack if a histogram is present
      if (!hist_merged) {
        hist_merged.reset(dynamic_cast<TH1D *>(sample.histogram->Clone()));
        hist_merged->SetDirectory(nullptr); // keep it for ourselves
      } else
        hist_merged->Add(sample.histogram);
    }
  }
  return hist_merged;
}

StackSystematics combine_systematics(const Stack &stack) {
  StackSystematics combined;
  // a given source is fully correlated between samples: linear sum of shifts
  for (const auto &sample : stack.samples()) {
    if (!sample.histogram) // not drawn, hence not accounted for
      continue;
    for (const auto &[name, shifts] : sample.systematics) {
      auto &source = combined.sources[name];
      if (source.size() < shifts.size())
        source.resize(shifts.size(), {0., 0.});
      for (size_t i = 0; i < shifts.size(); ++i) {
        source[i].first += shifts[i].first;
        source[i].second += shifts[i].second;
      }
    }
  }
  size_t num_bins = 0;
  for (const auto &source : combined.sources | std::views::values)
    num_bins = std::max(num_bins, source.size());
  // sources are uncorrelated with each other: quadratic sum, separately for
  // the upwards and downwards fluctuations of the yield
  combined.total.assign(num_bins, {0., 0.});
  for (auto &source : combined.sources | std::views::values) {
    source.resize(num_bins, {0., 0.});
    for (size_t i = 0; i < num_bins; ++i) {
      const auto upwards = std::max({source[i].first, source[i].second, 0.}),
                 downwards =
                     std::max({-source[i].first, -source[i].second, 0.});
      combined.total[i].first += upwards * upwards;
      combined.total[i].second += downwards * downwards;
    }
  }
  for (auto &[upwards, downwards] : combined.total) {
    upwards = std::sqrt(upwards);
    downwards = std::sqrt(downwards);
  }
  return combined;
}

double max_relative_systematics(const TH1 &nominal,
                                const StackSystematics &systematics) {
  double max_relative = 0.;
  for (int bin = nominal.GetXaxis()->GetFirst();
       bin <= nominal.GetXaxis()->GetLast(); ++bin) {
    const auto content = nominal.GetBinContent(bin);
    if (const size_t i = bin; content > 0. && i < systematics.total.size())
      max_relative =
          std::max({max_relative, systematics.total[i].first / content,
                    systematics.total[i].second / content});
  }
  return max_relative;
}

TH1D *book_like(ROOTCanvas &canvas, const TH1 &model, const std::string &name) {
  const auto *axis = model.GetXaxis();
  auto *histogram = axis->GetXbins()->GetSize() > 0 // variable-width bins
                        ? canvas.make<TH1D>(name.data(), "", axis->GetNbins(),
                                            axis->GetXbins()->GetArray())
                        : canvas.make<TH1D>(name.data(), "", axis->GetNbins(),
                                            axis->GetXmin(), axis->GetXmax());
  histogram->SetDirectory(nullptr); // kill garbage collector
  histogram->SetStats(false);
  histogram->GetXaxis()->SetRange(axis->GetFirst(), axis->GetLast());
  return histogram;
}

TGraphAsymmErrors *draw_uncertainty_band(ROOTCanvas &canvas, const TH1 &nominal,
                                         const StackSystematics &systematics,
                                         bool relative, double offset,
                                         bool with_stat) {
  const int num_bins = nominal.GetNbinsX();
  auto *band = canvas.make<TGraphAsymmErrors>(num_bins);
  for (int i = 0; i < num_bins; ++i) {
    const int bin = i + 1;
    const auto content = nominal.GetBinContent(bin),
               stat = nominal.GetBinError(bin),
               half_width = 0.5 * nominal.GetBinWidth(bin);
    const auto [syst_up, syst_down] =
        static_cast<size_t>(bin) < systematics.total.size()
            ? systematics.total[bin]
            : std::pair{0., 0.};
    auto central = content,
         up = with_stat ? std::hypot(stat, syst_up) : syst_up,
         down = with_stat ? std::hypot(stat, syst_down) : syst_down;
    if (relative) {     // no band for empty bins
      central = offset; // 0: relative uncertainty ; 1: ratio to nominal
      up = content > 0. ? up / content : 0.;
      down = content > 0. ? down / content : 0.;
    }
    band->SetPoint(i, nominal.GetBinCenter(bin), central);
    band->SetPointError(i, half_width, half_width, down, up);
  }
  band->SetLineWidth(0);
  band->SetMarkerSize(0);
  band->SetFillStyle(1001);
  band->SetFillColorAlpha(kBlack, 0.25);
  band->Draw("2");
  return band;
}

void draw_systematics_breakdown(ROOTCanvas &canvas, const TH1 &nominal,
                                const StackSystematics &systematics,
                                size_t max_sources, TLegend &legend,
                                double offset) {
  // rank the sources according to their overall effect on the yields
  std::vector<std::pair<double, std::string>> ranking;
  for (const auto &[name, shifts] : systematics.sources) {
    double effect = 0.;
    for (const auto &[up, down] : shifts)
      effect += std::max(std::fabs(up), std::fabs(down));
    ranking.emplace_back(effect, name);
  }
  std::ranges::sort(ranking, std::greater{});
  if (ranking.size() > max_sources)
    ranking.resize(max_sources);

  size_t i_source = 0;
  for (const auto &name : ranking | std::views::values) {
    const auto &shifts = systematics.sources.at(name);
    const auto base_name = canvas.GetName() + "_syst_"s + name;
    auto *up = book_like(canvas, nominal, base_name + "_up"),
         *down = book_like(canvas, nominal, base_name + "_down");
    for (int bin = 1; bin <= nominal.GetNbinsX(); ++bin) {
      const auto content = nominal.GetBinContent(bin);
      up->SetBinContent(bin, offset);
      down->SetBinContent(bin, offset);
      if (const size_t i = bin; content > 0. && i < shifts.size()) {
        up->SetBinContent(bin, offset + shifts[i].first / content);
        down->SetBinContent(bin, offset + shifts[i].second / content);
      }
    }
    const auto colour =
        colours.at((i_source++ % colours.size()) + 1 /*skip black*/);
    for (auto *variation : {up, down}) {
      variation->SetLineColor(colour);
      variation->SetLineWidth(2);
      variation->SetFillStyle(0);
      variation->Draw("hist,same");
    }
    down->SetLineStyle(2); // solid: +1 sigma ; dashed: -1 sigma
    legend.AddEntry(up, name.data(), "l");
  }
}
} // namespace mplt::root::utils
