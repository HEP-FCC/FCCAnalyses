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

#include "MultiPlotter/ROOTCanvas.h"
#include "MultiPlotter/ROOTUtils.h"
#include "MultiPlotter/Utils.h"
#include "MultiPlotter/plotItPlotter.h"
#include <TGraphAsymmErrors.h>
#include <THStack.h>
#include <TLatex.h>
#include <TLegend.h>
#include <TLine.h>
#include <filesystem>
#include <iostream> //FIXME
#include <pybind11/stl.h>

using namespace mplt;
namespace py = pybind11;
using namespace std::string_literals;

plotItPlotter::plotItPlotter(std::string_view experiment_name,
                             const std::vector<std::string> &extra_labels)
    : MultiPlotter(experiment_name, extra_labels) {}

void plotItPlotter::plot(std::string_view output_file,
                         std::string_view output_dir, PyObject *options_obj) {
  py::dict options;
  if (options_obj)
    options = py::reinterpret_borrow<py::dict>(options_obj);
  options["name"] = std::string{output_file};
  ROOTCanvas canvas(options);
  for (const auto &[coordinates, text] : text_boxes_)
    canvas.addTextBox(coordinates.first, coordinates.second, text);

  const auto xaxis_unit = utils::get_with_default(options, "unit", ""s);

  root::utils::StackSystematics systematics;
  if (utils::get_with_default(options, "plot-syst-unc", true) &&
      samples_.contains(Sample::Type::background))
    systematics =
        root::utils::combine_systematics(samples_.at(Sample::Type::background));
  const auto has_data = samples_.contains(Sample::Type::data) &&
                        !samples_.at(Sample::Type::data).samples().empty();
  const auto with_breakdown =
      (!systematics.empty() || has_data) &&
      utils::get_with_default(options, "syst-breakdown", true);

  // extra legend entries: stat and stat+syst uncertainty bands, and data
  prepareStacksPlotting(canvas,
                        (systematics.empty() ? 0 : 2) + (has_data ? 1 : 0));
  if (with_breakdown) // lower pad for the per-source relative uncertainties
    canvas.split(0.3);
  canvas.mainPad()->cd();

  std::unique_ptr<TH1> histogram_data{nullptr}, histogram_ref{nullptr};
  for (const auto &samples_list : samples_ | std::ranges::views::values) {
    if (histogram_ref)
      break;
    if (auto merged = root::utils::merge_samples(samples_list); merged)
      histogram_ref = std::move(merged);
  }
  if (!histogram_ref)
    throw std::runtime_error(
        "Failed to initialise a reference histogram for plot with name '"s +
        canvas.GetName() + "'."s);
  histogram_ref->SetDirectory(nullptr); // kill garbage collector
  histogram_ref->Clear();               // reset bins content
  histogram_ref->SetLineWidth(0);
  histogram_ref->SetFillStyle(0);
  histogram_ref->Draw("hist");
  root::utils::adjust_labels(histogram_ref.get(), xaxis_unit);

  if (samples_.contains(Sample::Type::data)) {
    for (const auto &sample : samples_.at(Sample::Type::data).samples()) {
      // mangle all data histograms into one stack
      if (!histogram_data) { // not yet initialised
        histogram_data.reset(dynamic_cast<TH1 *>(sample.histogram->Clone()));
        histogram_data->SetDirectory(nullptr); // kill garbage collector
        histogram_data->Sumw2(false);          // disable for data
        if (options.contains("error_options"))
          histogram_data->SetBinErrorOption(static_cast<TH1::EBinErrorOpt>(
              py::cast<int>(options["error_options"])));
      } else // no need to clone for addition
        histogram_data->Add(dynamic_cast<TH1 *>(sample.histogram));
    }
  }
  auto min_value = std::numeric_limits<double>::max(),
       max_value = std::numeric_limits<double>::min();
  // smallest strictly positive content: lower bound of a logarithmic y-axis
  auto min_positive_value = std::numeric_limits<double>::max();
  const auto update_min_positive = [&min_positive_value](const TH1 &hist) {
    for (int bin = hist.GetXaxis()->GetFirst();
         bin <= hist.GetXaxis()->GetLast(); ++bin)
      if (const auto content = hist.GetBinContent(bin); content > 0.)
        min_positive_value = std::min(min_positive_value, content);
  };
  std::unique_ptr<TH1> merged_background{nullptr};
  if (samples_.contains(Sample::Type::background)) {
    auto &stack = samples_.at(Sample::Type::background);
    auto *stat_band =
        root::utils::draw_samples_stack(canvas, stack, true, 3004);
    merged_background = root::utils::merge_samples(stack);
    min_value = std::min(min_value, merged_background->GetMinimum());
    max_value = std::max(max_value, merged_background->GetMaximum());
    update_min_positive(*merged_background);
    if (!systematics.empty() && merged_background) {
      // total uncertainty band, on top of the stack
      const auto *total_band = root::utils::draw_uncertainty_band(
          canvas, *merged_background, systematics, false);
      for (int i = merged_background->GetXaxis()->GetFirst() - 1;
           i < std::min(total_band->GetN(),
                        merged_background->GetXaxis()->GetLast());
           ++i)
        max_value = std::max(max_value, total_band->GetY()[i] +
                                            total_band->GetErrorYhigh(i));
      if (auto *legend = canvas.legend(); legend) {
        if (stat_band)
          legend->AddEntry(stat_band, "Stat. unc.", "f");
        legend->AddEntry(total_band, "Total unc.", "f");
      }
    }
  }
  if (samples_.contains(Sample::Type::signal)) {
    auto &stack = samples_.at(Sample::Type::signal);
    root::utils::draw_samples_stack(canvas, stack, false, 3005);
    const auto merged = root::utils::merge_samples(stack);
    min_value = std::min(min_value, merged->GetMinimum());
    max_value = std::max(max_value, merged->GetMaximum());
    update_min_positive(*merged);
  }
  if (histogram_data) { // data points, on top of everything else
    histogram_data->SetMarkerStyle(20);
    histogram_data->SetMarkerSize(1.);
    histogram_data->SetMarkerColor(kBlack);
    histogram_data->SetLineColor(kBlack);
    histogram_data->SetLineWidth(1);
    histogram_data->Draw("e,x0,same");
    for (int bin = histogram_data->GetXaxis()->GetFirst();
         bin <= histogram_data->GetXaxis()->GetLast(); ++bin)
      max_value = std::max(max_value, histogram_data->GetBinContent(bin) +
                                          histogram_data->GetBinError(bin));
    update_min_positive(*histogram_data);
    if (auto *legend = canvas.legend(); legend)
      legend->AddEntry(
          histogram_data.get(),
          samples_.at(Sample::Type::data).samples().front().name.data(), "pe");
  }

  if (with_breakdown && merged_background) {
    // lower pad: uncertainties relative to the total background yield
    canvas.lowerPad()->cd();
    auto *frame = root::utils::book_like(canvas, *histogram_ref,
                                         canvas.GetName() + "_syst_frame"s);
    { // the lower pad takes over the x-axis labelling
      const auto scaling =
          (1. - canvas.lowerFraction()) / canvas.lowerFraction();
      auto *ref_xaxis = histogram_ref->GetXaxis(),
           *ref_yaxis = histogram_ref->GetYaxis();
      frame->GetXaxis()->SetTitle(ref_xaxis->GetTitle());
      frame->GetXaxis()->SetTitleSize(ref_xaxis->GetTitleSize() * scaling);
      frame->GetXaxis()->SetLabelSize(ref_xaxis->GetLabelSize() * scaling);
      frame->GetXaxis()->SetTickLength(ref_xaxis->GetTickLength() * scaling);
      frame->GetYaxis()->SetTitle(histogram_data ? "Data / MC"
                                                 : "Rel. unc.");
      frame->GetYaxis()->CenterTitle();
      frame->GetYaxis()->SetTitleSize(ref_yaxis->GetTitleSize() * scaling);
      // a null offset means "automatic", which scales with the title size
      frame->GetYaxis()->SetTitleOffset((ref_yaxis->GetTitleOffset() > 0.f
                                             ? ref_yaxis->GetTitleOffset()
                                             : 1.25f) /
                                        scaling);
      frame->GetYaxis()->SetLabelSize(ref_yaxis->GetLabelSize() * scaling);
      frame->GetYaxis()->SetNdivisions(505);
      ref_xaxis->SetTitleSize(0.);
      ref_xaxis->SetLabelSize(0.);
    }
    // vertical range driven by the systematics, with room for the legend
    auto max_relative =
        root::utils::max_relative_systematics(*merged_background, systematics);
    // with data: ratio to the total background yield, centred on 1 ;
    // otherwise: relative uncertainties, centred on 0
    const auto centre = histogram_data ? 1. : 0.;
    TH1D *data_deviation{nullptr};
    if (histogram_data) {
      data_deviation = root::utils::book_like(
          canvas, *merged_background, canvas.GetName() + "_data_deviation"s);
      for (int bin = 1; bin <= merged_background->GetNbinsX(); ++bin)
        if (const auto expected = merged_background->GetBinContent(bin);
            expected > 0.) {
          const auto deviation =
              histogram_data->GetBinContent(bin) / expected - 1.;
          data_deviation->SetBinContent(bin, centre + deviation);
          data_deviation->SetBinError(bin, histogram_data->GetBinError(bin) /
                                               expected);
          if (bin >= merged_background->GetXaxis()->GetFirst() &&
              bin <= merged_background->GetXaxis()->GetLast())
            max_relative = std::max(max_relative, std::fabs(deviation));
        }
    }
    if (max_relative <= 0.)
      max_relative = 1.;
    frame->SetMinimum(centre - 1.5 * max_relative);
    frame->SetMaximum(centre + 2.4 * max_relative);
    frame->Draw("axis");

    root::utils::draw_uncertainty_band( // stat+syst
        canvas, *merged_background, systematics, true, centre);
    auto *stat_band = root::utils::draw_uncertainty_band( // stat only
        canvas, *merged_background, {}, true, centre);
    stat_band->SetFillStyle(3004);
    stat_band->SetFillColor(kGray + 1);

    const auto num_sources = std::min(
        systematics.sources.size(),
        utils::get_with_default(options, "syst-max-sources", size_t{6}));
    auto *legend = canvas.make<TLegend>(0.16, 0.76, 0.9, 0.94);
    legend->SetLineWidth(0);
    legend->SetFillStyle(0);
    legend->SetTextSize(0.09);
    legend->SetNColumns(std::clamp<int>(num_sources, 1, 3));
    root::utils::draw_systematics_breakdown(canvas, *merged_background,
                                            systematics, num_sources, *legend,
                                            centre);
    auto *zero_line = canvas.make<TLine>(
        frame->GetXaxis()->GetBinLowEdge(frame->GetXaxis()->GetFirst()), centre,
        frame->GetXaxis()->GetBinUpEdge(frame->GetXaxis()->GetLast()), centre);
    zero_line->SetLineColor(kGray + 2);
    zero_line->Draw();
    if (data_deviation) {
      data_deviation->SetMarkerStyle(20);
      data_deviation->SetMarkerSize(1.);
      data_deviation->SetMarkerColor(kBlack);
      data_deviation->SetLineColor(kBlack);
      data_deviation->Draw("e,x0,same");
    }
    legend->Draw();
    canvas.mainPad()->cd();
  }

  const auto formats = utils::get_with_default(options, "output-file-types",
                                               std::vector{"pdf"s});
  auto &experiment_label = canvas.addTextBox(
      0.9, 0.94, {"#it{"s + std::string{experiment_name_} + "}"s});
  experiment_label.SetTextAlign(31);
  experiment_label.SetTextSize(0.04);
  canvas.addTextBox(0.18, 0.82, extra_labels_);

  // particularise for lin/log axes, and final draw
  // user-defined vertical ranges, for the linear and logarithmic scales
  const auto user_range =
      [&options](std::string_view key) -> std::pair<double, double> {
    if (!options.contains(key) || options[key.data()].is_none())
      return {0., 0.};
    return py::cast<std::pair<double, double>>(options[key.data()]);
  };
  const auto y_range = user_range("y-range"),
             log_y_range = user_range("log-y-range");

  for (const auto &x_scaling : utils::get_with_default(
           options, "x-axis-scale-types", std::vector{"lin"s})) {
    canvas.setLogx(x_scaling == "log");
    const auto y_scalings = utils::get_with_default(
        options, "y-axis-scale-types", std::vector{"lin"s});
    for (const auto &y_scaling : y_scalings) {
      if (y_scaling == "log") { // logarithmic y-axis
        // empty bins cannot drive the lower bound of a logarithmic axis
        histogram_ref->SetMinimum(0.1 * (min_positive_value < max_value
                                             ? min_positive_value
                                             : 1.e-3 * max_value));
        if (max_value > std::numeric_limits<double>::min())
          histogram_ref->SetMaximum(max_value * 1.e3);
        if (log_y_range.first > 0. && log_y_range.first < log_y_range.second) {
          histogram_ref->SetMinimum(log_y_range.first);
          histogram_ref->SetMaximum(log_y_range.second);
        }
        canvas.setLogy(true);
      } else { // linear y-axis
        histogram_ref->SetMinimum(min_value);
        histogram_ref->SetMaximum(max_value * 1.4);
        if (y_range.first < y_range.second) {
          histogram_ref->SetMinimum(y_range.first);
          histogram_ref->SetMaximum(y_range.second);
        }
        canvas.setLogy(false);
      }
      // histogram_ref->GetYaxis()->SetRangeUser(min_value, max_value * 1.2);

      std::ostringstream final_output_file;
      final_output_file << output_file;
      if (y_scalings.size() > 1)
        final_output_file << "_" << y_scaling;

      // save canvas
      const auto output_path_in_dir =
          std::filesystem::path{output_dir} / final_output_file.str();
      canvas.save(formats, std::string{output_path_in_dir});
    }
  }
}

void plotItPlotter::prepareStacksPlotting(
    ROOTCanvas &canvas, size_t num_extra_legend_entries) const {
  canvas.cd();
  size_t num_drawable_histograms = num_extra_legend_entries;
  for (const auto &[sample_type, stack] : samples_)
    if (sample_type == Sample::Type::background ||
        sample_type == Sample::Type::signal)
      num_drawable_histograms += stack.samples().size();
  auto &legend =
      canvas.addLegend(0.68, 0.86 - 0.04 * num_drawable_histograms, 0.96, 0.88);
  for (const auto &[sample_type, stack] : samples_) { // set colours
    int i = 0;
    for (const auto &sample : stack.samples()) {
      if (auto *histogram = dynamic_cast<TH1 *>(sample.histogram); histogram) {
        histogram->SetLineColor(sample.colour);
        histogram->SetLineWidth(3);
        if (sample_type == Sample::Type::signal) {
          histogram->SetLineStyle(i + 2); // TODO: list of fallback line styles
          legend.AddEntry(histogram, sample.name.data(), "l");
          ++i;
        } else if (sample_type == Sample::Type::background) {
          histogram->SetFillColorAlpha(sample.colour, 0.5);
          legend.AddEntry(histogram, sample.name.data(), "lf");
        }
      }
    }
  }
}
