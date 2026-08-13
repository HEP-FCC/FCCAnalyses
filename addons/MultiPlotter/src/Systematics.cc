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
                            const TH1 *down_shape)
      : Systematics(SystematicsType::shape, _name),
        up_shape_{static_cast<TH1 *>(up_shape->Clone())},
        down_shape_{static_cast<TH1 *>(down_shape->Clone())} {}

  void apply(SystematicsSet &set) const override {
    set.up_shape.reset(static_cast<TH1 *>(up_shape_->Clone()));
    set.down_shape.reset(static_cast<TH1 *>(down_shape_->Clone()));
    // TODO: verify the validity/scaling/...
  }

private:
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
        py::cast<float>(options["postFit"]),
        py::cast<float>(options["postFitErrorUp"]),
        py::cast<float>(options["postFitErrorDown"]));
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
    return std::make_unique<ShapeSystematics>(
        name,
        input_file->Get<TH1>(py::cast<std::string>(options["shapeUp"]).data()),
        input_file->Get<TH1>(
            py::cast<std::string>(options["shapeDown"]).data()));
  }
  }
  throw std::runtime_error(
      "Failed to build a systematics evaluator object with type=" +
      std::to_string(syst_type) + " and name='" + std::string{name} + "'.");
}
