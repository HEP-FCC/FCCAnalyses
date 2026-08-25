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

#include "MultiPlotter/Systematics.h"
#include "MultiPlotter/SystematicsSet.h"
#include "MultiPlotter/Utils.h"
#include <TFile.h>
#include <TH1.h>
#include <pybind11/pybind11.h>

using namespace mplt;
namespace py = pybind11;

class ConstantSystematics : public Systematics {
public:
  explicit ConstantSystematics(std::string_view _name, float value)
      : Systematics(SystematicsType::constant, _name), value_{value} {}

  void apply(SystematicsSet &set) const override {
    set.up_shape->Scale(value_);
    set.down_shape->Scale(2 - value_);
  }

private:
  const float value_;
};

class LogNormalSystematics : public Systematics {
public:
  explicit LogNormalSystematics(std::string_view _name, float prior,
                                float post_fit, float post_fit_error_up,
                                float post_fit_error_down)
      : Systematics(SystematicsType::log_normal, _name), prior_{prior},
        post_fit_{post_fit}, post_fit_error_up_{post_fit_error_up},
        post_fit_error_down_{post_fit_error_down},
        value_{std::exp(post_fit_ * std::log(prior_))},
        value_up_{
            std::exp((post_fit_ + post_fit_error_up_) * std::log(prior_))},
        value_down_{
            std::exp((post_fit_ - post_fit_error_down_) * std::log(prior_))} {}

  void apply(SystematicsSet &set) const override {
    set.up_shape->Scale(value_up_);
    set.down_shape->Scale(value_down_);
  }

private:
  // parameterised values
  const float prior_;
  const float post_fit_;
  const float post_fit_error_up_;
  const float post_fit_error_down_;
  // pre-computed values
  const float value_;
  const float value_up_;
  const float value_down_;
};

class ShapeSystematics : public Systematics {
public:
  explicit ShapeSystematics(std::string_view _name, const TH1 *up_shape,
                            const TH1 *down_shape, float scale, int rebin)
      : Systematics(SystematicsType::shape, _name),
        up_shape_{prepare(up_shape, scale, rebin)},
        down_shape_{prepare(down_shape, scale, rebin)} {}

  void apply(SystematicsSet &set) const override {
    for (const auto *shape : {up_shape_, down_shape_})
      if (shape->GetNbinsX() != set.nominal_shape->GetNbinsX())
        throw std::runtime_error(
            "Shape systematics with name '" + name + "' has " +
            std::to_string(shape->GetNbinsX()) +
            " bins, while the nominal distribution has " +
            std::to_string(set.nominal_shape->GetNbinsX()) +
            ": check the 'scale' and 'rebin' parameters.");
    set.up_shape.reset(prepare(up_shape_));
    set.down_shape.reset(prepare(down_shape_));
  }

private:
  static TH1 *prepare(const TH1 *shape, float scale = 1.f, int rebin = 1) {
    auto *clone = static_cast<TH1 *>(shape->Clone());
    clone->SetDirectory(nullptr);
    if (scale != 1.f)
      clone->Scale(scale);
    if (rebin > 1)
      clone->Rebin(rebin);
    return clone;
  }

  const TH1 *up_shape_;
  const TH1 *down_shape_;
};

std::unique_ptr<Systematics> Systematics::build(SystematicsType syst_type,
                                                std::string_view name,
                                                py::dict &options) {
  switch (syst_type) {
  case SystematicsType::constant:
    return std::make_unique<ConstantSystematics>(
        name, py::cast<float>(options["value"]));
  case SystematicsType::log_normal:
    return std::make_unique<LogNormalSystematics>(
        name, py::cast<float>(options["prior"]),
        utils::get_with_default(options, "postFit", 0.f),
        utils::get_with_default(options, "postFitErrorUp", 1.f),
        utils::get_with_default(options, "postFitErrorDown", 1.f));
  case SystematicsType::shape: {
    std::unique_ptr<TFile> input_file;
    const auto input_filename = py::cast<std::string>(options["inputFilename"]);
    if (!input_filename.empty())
      input_file = std::make_unique<TFile>(input_filename.data());
    if (!input_file || input_file->IsZombie())
      throw std::runtime_error(
          "Failed to open the shapes file for systematics with name '" +
          std::string{name} + "': check your input with filename='" +
          input_filename + "'.");
    const auto up_name = py::cast<std::string>(options["shapeUp"]),
               down_name = py::cast<std::string>(options["shapeDown"]);
    const auto *up_shape = input_file->Get<TH1>(up_name.data()),
               *down_shape = input_file->Get<TH1>(down_name.data());
    if (!up_shape || !down_shape)
      throw std::runtime_error(
          "Failed to retrieve the shapes '" + up_name + "' and/or '" +
          down_name + "' for systematics with name '" + std::string{name} +
          "' from file '" + input_filename + "'.");
    return std::make_unique<ShapeSystematics>(
        name, up_shape, down_shape,
        utils::get_with_default(options, "scale", 1.f),
        utils::get_with_default(options, "rebin", 1));
  }
  }
  throw std::runtime_error(
      "Failed to build a systematics evaluator object with type=" +
      std::to_string(syst_type) + " and name='" + std::string{name} + "'.");
}
