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

#include "MultiPlotter/Binning.h"
#include "MultiPlotter/MultiPlotter.h"

#include <TH1.h>
#include <TRandom3.h>
#include <ranges>
#include <stdexcept>

using namespace mplt;

MultiPlotter::MultiPlotter(std::string_view experiment_name,
                           const std::vector<std::string> &extra_labels)
    : experiment_name_{experiment_name}, extra_labels_{extra_labels} {}

Sample &MultiPlotter::addSample(Sample &sample) {
  return samples_[sample.type].add(sample);
}

Sample &MultiPlotter::addPseudoData(bool fluctuate, unsigned int seed,
                                    const std::string &name) {
  std::shared_ptr<TH1> histogram;
  for (const auto &sample : samples(Sample::Type::background)) {
    if (!sample.histogram)
      continue;
    if (!histogram) {
      histogram.reset(static_cast<TH1 *>(sample.histogram->Clone()));
      histogram->SetDirectory(nullptr);
    } else
      histogram->Add(sample.histogram);
  }
  if (!histogram)
    throw std::runtime_error("No background sample to generate pseudo-data.");
  TRandom3 generator(seed);
  for (int bin = 0; bin <= histogram->GetNbinsX() + 1; ++bin) {
    const auto expected = std::max(0., histogram->GetBinContent(bin)),
               observed = fluctuate ? generator.PoissonD(expected) : expected;
    histogram->SetBinContent(bin, observed);
    histogram->SetBinError(bin, std::sqrt(observed));
  }
  pseudo_data_.emplace_back(histogram);

  Sample sample;
  sample.type = Sample::Type::data;
  sample.name = name;
  sample.histogram = histogram.get();
  sample.colour = kBlack;
  return addSample(sample);
}

void MultiPlotter::sortSamples(SortingType sorting_type, bool reverse) {
  for (auto &[sample_type, stack] : samples_)
    if (sample_type != Sample::Type::data)
      stack.sort(sorting_type, reverse);
}

void MultiPlotter::rebin(int factor) {
  if (factor < 2)
    return;
  for (auto &stack : samples_ | std::views::values)
    for (auto &sample : stack.samples()) {
      if (!sample.histogram)
        continue;
      sample.histogram->Rebin(factor);
      for (auto &shifts : sample.systematics | std::views::values)
        shifts = binning::rebin(shifts, factor);
    }
}

void MultiPlotter::setXRange(double min, double max) {
  if (!(min < max))
    throw std::runtime_error("Invalid x-axis range: [" + std::to_string(min) +
                             ", " + std::to_string(max) + "].");
  for (auto &stack : samples_ | std::views::values)
    for (auto &sample : stack.samples())
      if (sample.histogram)
        sample.histogram->GetXaxis()->SetRangeUser(min, max);
}

void MultiPlotter::addOverflow() {
  for (auto &stack : samples_ | std::views::values)
    for (auto &sample : stack.samples()) {
      auto *histogram = sample.histogram;
      if (!histogram)
        continue;
      const int first = histogram->GetXaxis()->GetFirst(),
                last = histogram->GetXaxis()->GetLast(),
                num_bins = histogram->GetNbinsX();
      double under = 0., under_sumw2 = 0., over = 0., over_sumw2 = 0.;
      for (int bin = 0; bin <= num_bins + 1; ++bin) {
        if (bin >= first && bin <= last)
          continue;
        const auto content = histogram->GetBinContent(bin),
                   error = histogram->GetBinError(bin);
        (bin < first ? under : over) += content;
        (bin < first ? under_sumw2 : over_sumw2) += error * error;
        if (bin >= 1 && bin <= num_bins) {
          histogram->SetBinContent(bin, 0.);
          histogram->SetBinError(bin, 0.);
        }
      }
      // not through SetBinContent, which may try to extend the axis
      histogram->ClearUnderflowAndOverflow();
      const auto add = [&histogram](int bin, double content, double sumw2) {
        const auto error = histogram->GetBinError(bin);
        histogram->SetBinContent(bin, histogram->GetBinContent(bin) + content);
        histogram->SetBinError(bin, std::sqrt(error * error + sumw2));
      };
      add(first, under, under_sumw2);
      add(last, over, over_sumw2);
      for (auto &shifts : sample.systematics | std::views::values)
        shifts = binning::fold_overflow(shifts, first, last);
    }
}

const std::vector<Sample> &MultiPlotter::samples(Sample::Type type) const {
  static const std::vector<Sample> no_samples;
  if (const auto it = samples_.find(type); it != samples_.end())
    return it->second.samples();
  return no_samples;
}

std::string MultiPlotter::yieldsTable() const {
  std::ostringstream table;
  // TODO: implement the table creation
  //  potentially, create a base table creation object that can be specialised
  //  for (LaTeX, Markdown, ...) output type
  return table.str();
}

void MultiPlotter::addTextBox(float x1, float y1,
                              const std::vector<std::string> &text) {
  text_boxes_.emplace_back(std::make_pair(std::make_pair(x1, y1), text));
}
