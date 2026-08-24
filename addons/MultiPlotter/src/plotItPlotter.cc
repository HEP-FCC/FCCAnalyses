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
#include <TH1.h>
#include <THStack.h>
#include <TLatex.h>
#include <TLegend.h>
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
  /*for sig_stacking in config['stack-sig']:
      plot_params = {'stack-sig': sig_stacking}
      for xaxis_scaling in config['x-axis-scale-types']:
          plot_params_x = {**plot_params, 'xaxis': xaxis_scaling}
          for yaxis_scaling in config['y-axis-scale-types']:
              plot_params_x_y = {**plot_params_x, 'yaxis': yaxis_scaling}
              plot_name = var
              if len(config['stack-sig']) > 1:
                  plot_name += '_' + sig_stacking
              if len(config['x-axis-scale-types']) > 1:
                  plot_name += '_' + xaxis_scaling + 'x'
              if len(config['y-axis-scale-types']) > 1:
                  plot_name += '_' + yaxis_scaling + 'y'*/
  options["name"] = std::string{output_file};
  ROOTCanvas canvas(options);
  for (const auto &[coordinates, text] : text_boxes_)
    canvas.addTextBox(coordinates.first, coordinates.second, text);

  const auto xaxis_unit = utils::get_with_default(options, "unit", ""s);

  const auto rebinning_factor = utils::get_with_default(options, "rebin", 1.);
  if (const auto sorting_method =
          utils::get_with_default(options, "sorting", ""s);
      sorting_method == "yields") { // TODO
  }

  prepareStacksPlotting(canvas);

  if (samples_.contains(Sample::Type::background))
    for (const auto &sample : samples_.at(Sample::Type::background).samples()) {
      auto *histogram = dynamic_cast<TH1 *>(sample.histogram->Clone());
      histogram->Scale(sample.weight);
      double rescaled_integral_uncertainty = 0.,
             rescaled_integral =
                 histogram->IntegralAndError(histogram->GetXaxis()->GetFirst(),
                                             histogram->GetXaxis()->GetLast(),
                                             rescaled_integral_uncertainty);
      if (rebinning_factor != 1.) // FIXME float comparisons
        histogram->Rebin(rebinning_factor);
    }
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
  if (samples_.contains(Sample::Type::background)) {
    auto &stack = samples_.at(Sample::Type::background);
    root::utils::draw_samples_stack(canvas, stack, true, 3004);
    const auto merged = root::utils::merge_samples(stack);
    min_value = std::min(min_value, merged->GetMinimum());
    max_value = std::max(max_value, merged->GetMaximum());
  }
  if (samples_.contains(Sample::Type::signal)) {
    auto &stack = samples_.at(Sample::Type::signal);
    root::utils::draw_samples_stack(canvas, stack, false, 3005);
    const auto merged = root::utils::merge_samples(stack);
    min_value = std::min(min_value, merged->GetMinimum());
    max_value = std::max(max_value, merged->GetMaximum());
  }

  const auto formats = utils::get_with_default(options, "output-file-types",
                                               std::vector{"pdf"s});
  auto &experiment_label = canvas.addTextBox(
      0.9, 0.94, {"#it{"s + std::string{experiment_name_} + "}"s});
  experiment_label.SetTextAlign(31);
  experiment_label.SetTextSize(0.04);
  canvas.addTextBox(0.18, 0.82, extra_labels_);

  // particularise for lin/log axes, and final draw
  for (const auto &x_scaling : utils::get_with_default(
           options, "x-axis-scale-types", std::vector{"lin"s})) {
    canvas.SetLogx(x_scaling == "log");
    const auto y_scalings = utils::get_with_default(
        options, "y-axis-scale-types", std::vector{"lin"s});
    for (const auto &y_scaling : y_scalings) {
      if (y_scaling == "log") { // logarithmic y-axis
        if (min_value > 0.)
          histogram_ref->SetMinimum(min_value * 0.1);
        if (max_value > std::numeric_limits<double>::min())
          histogram_ref->SetMaximum(max_value * 1.e3);
        canvas.SetLogy(true);
      } else { // linear y-axis
        histogram_ref->SetMinimum(min_value);
        histogram_ref->SetMaximum(max_value * 1.4);
        canvas.SetLogy(false);
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

void plotItPlotter::prepareStacksPlotting(ROOTCanvas &canvas) const {
  canvas.cd();
  size_t num_drawable_histograms = 0;
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
