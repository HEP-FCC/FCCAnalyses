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

#include "MultiPlotter/Sample.h"
#include "MultiPlotter/SystematicsSet.h"

#include <TH1.h>
#include <THStack.h>
#include <iostream> //TODO: replace with multithreading-compatible equivalent

using namespace mplt;
namespace py = pybind11;

void Sample::addSystematics(std::string_view syst_name,
                            SystematicsType syst_type, PyObject *params_obj) {
  // first cast the Python object into a parseable dictionary to extract
  // parameters conveniently
  auto params = py::reinterpret_borrow<py::dict>(params_obj);
  if (systematics.contains(std::string{syst_name}))
    std::cout << "Warning: systematics with name '" << syst_name
              << "' was already booked/computed. Clearing any recorded value "
                 "by default.";
  auto &systematics_values = systematics[std::string{syst_name}];
  systematics_values.clear(); // clear any previous computation
  systematics_values.resize(histogram->GetNbinsX());

  const auto systematics_builder =
      Systematics::build(syst_type, syst_name, params);

  SystematicsSet set(histogram);
  systematics_builder->apply(set);
  const auto up_shape = set.shapeUp(), down_shape = set.shapeDown();
}

Stack::Stack() : stack_{std::make_shared<THStack>()} {}

Sample &Stack::add(Sample &sample) {
  auto &added_sample = samples_.emplace_back(sample);
  if (added_sample.histogram) { // only stack if a histogram is present
    if (!hist_merged_) {
      hist_merged_.reset(static_cast<TH1 *>(added_sample.histogram->Clone()));
      hist_merged_->SetDirectory(nullptr); // keep it for ourselves
    } else
      hist_merged_->Add(added_sample.histogram);
    stack_->Add(added_sample.histogram, added_sample.name.data());
  }
  return added_sample;
}

void Stack::sort(SortingType sorting_type, bool reverse) {
  if (sorting_type == SortingType::none)
    return; // trivial operation
  std::ranges::sort(samples_, [&sorting_type, &reverse](auto &lhs, auto &rhs) {
    switch (sorting_type) {
    case SortingType::yield:
      return reverse ? lhs.histogram->Integral() > rhs.histogram->Integral()
                     : lhs.histogram->Integral() < rhs.histogram->Integral();
    case SortingType::weight:
      return reverse ? lhs.weight > rhs.weight : lhs.weight < rhs.weight;
    case SortingType::name:
      return reverse ? lhs.name > rhs.name : lhs.name < rhs.name;
    default:
      throw std::runtime_error("Invalid sorting method (" +
                               std::to_string(sorting_type) + ").");
    }
  });
}

const std::shared_ptr<THStack> &Stack::stack() const { return stack_; }

const std::shared_ptr<TH1> &Stack::merged() const { return hist_merged_; }
