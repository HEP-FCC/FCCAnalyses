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
#include "MultiPlotter/Utils.h"
#include <TFrame.h>
#include <TGaxis.h>
#include <TLatex.h>
#include <TLegend.h>
#include <iostream>

using namespace mplt;
using namespace std::string_literals;
namespace py = pybind11;

ROOTCanvas::ROOTCanvas(const py::dict &options)
    : TCanvas(py::cast<std::string>(options["name"]).data(), "",
              utils::get_with_default(options, "width", 800),
              utils::get_with_default(options, "height", 800)) {
  if (utils::get_with_default(options, "transparent",
                              false)) { // transparent background
    SetFillStyle(4000);
    SetFrameFillStyle(4000);
  }

  // logarithmic axes
  SetTicks(1, 1);
  TGaxis::SetExponentOffset(-0.06, 0, "y"); // move exponent label if shown
  // external margins
  SetLeftMargin(utils::get_with_default(options, "margin_left", 0.14));
  SetRightMargin(utils::get_with_default(options, "margin_right", 0.08));
  if (options.contains("margin_top"))
    SetTopMargin(py::cast<double>(options["margin_top"]));
  if (options.contains("margin_bottom"))
    SetBottomMargin(py::cast<double>(options["margin_bottom"]));
  cd();
}

TLatex &ROOTCanvas::addTextBox(float x1, float y1,
                               const std::vector<std::string> &lines) {
  // recursive function to split lines according to the cardinality of the
  // multi-lines box
  std::function<std::string(const std::vector<std::string> &)> combine_lines;
  combine_lines =
      [&combine_lines](
          const std::vector<std::string> &remaining_lines) -> std::string {
    if (remaining_lines.empty())
      return ""s;
    if (remaining_lines.size() == 1)
      return remaining_lines.at(0);
    std::ostringstream os;
    os << "#splitline{" << remaining_lines.at(0) << "}{"
       << combine_lines(
              std::vector(remaining_lines.begin() + 1, remaining_lines.end()))
       << "}";
    return os.str();
  };
  const auto &box = text_boxes_.emplace_back(
      std::make_unique<TLatex>(x1, y1, combine_lines(lines).data()));
  box->SetNDC(true);
  box->SetTextAlign(12);
  box->SetTextFont(42); // Helvetica, normal weight
  box->SetTextSize(0.04);
  return *box;
}

TLegend &ROOTCanvas::addLegend(float x1, float y1, float x2, float y2) {
  if (legend_) {
    std::cout << "Replacing pre-existing legend for canvas with name '"
              << GetName() << "'.";
    legend_.reset();
  }
  legend_ = std::make_unique<TLegend>(x1, y1, x2, y2);
  legend_->SetLineWidth(0);
  legend_->SetFillStyle(0);
  return *legend_;
}

void ROOTCanvas::split(float lower_fraction) {
  if (upper_pad_) // already split
    return;
  lower_fraction_ = lower_fraction;
  cd();
  upper_pad_ =
      new TPad((GetName() + "_upper"s).data(), "", 0., lower_fraction, 1., 1.);
  lower_pad_ =
      new TPad((GetName() + "_lower"s).data(), "", 0., 0., 1., lower_fraction);
  for (auto *pad : {upper_pad_, lower_pad_}) { // inherit the canvas attributes
    pad->SetFillStyle(GetFillStyle());
    pad->SetFrameFillStyle(GetFrameFillStyle());
    pad->SetTicks(1, 1);
    pad->SetLeftMargin(GetLeftMargin());
    pad->SetRightMargin(GetRightMargin());
  }
  upper_pad_->SetTopMargin(GetTopMargin());
  upper_pad_->SetBottomMargin(0.02);
  lower_pad_->SetTopMargin(0.04);
  // keep the same absolute room for the x-axis labels and title
  lower_pad_->SetBottomMargin(
      std::min(0.45f, GetBottomMargin() / lower_fraction));
  for (auto *pad : {upper_pad_, lower_pad_}) {
    cd(); // sub-pads are attached to the canvas
    pad->Draw();
  }
  upper_pad_->cd();
}

void ROOTCanvas::setLogx(bool log) {
  SetLogx(log);
  for (auto *pad : {upper_pad_, lower_pad_})
    if (pad)
      pad->SetLogx(log);
}

void ROOTCanvas::setLogy(bool log) { mainPad()->SetLogy(log); }

void ROOTCanvas::save(const std::vector<std::string> &formats,
                      std::string_view alternative_name) {
  auto *main_pad = mainPad();
  if (lower_pad_) {
    lower_pad_->cd();
    lower_pad_->RedrawAxis();
    lower_pad_->Modified();
  }
  main_pad->cd();
  main_pad->RedrawAxis();
  main_pad->GetFrame()->SetBorderSize(12);
  main_pad->Modified();
  Modified();
  Update();

  main_pad->cd();  // legend and text boxes belong to the main pad
  if (legend_)
    legend_->Draw();
  for (const auto &text_box : text_boxes_) // add registered text boxes
    text_box->Draw("same");
  for (const auto &format : formats) {
    const auto filename =
        (alternative_name.empty() ? std::string{GetName()}
                                  : std::string{alternative_name}) +
        "." + format;
    SaveAs(filename.data());
  }
}
