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

#ifndef MultiPlotter_Sample_h
#define MultiPlotter_Sample_h

#include <pybind11/pybind11.h>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

#include "MultiPlotter/Systematics.h"

// forward definitions
class TH1;
class THStack;

namespace mplt {
/// Ordering method for samples inside categories
enum SortingType { none = -1, yield, weight, name };

struct Sample {
  /// Samples categories, defining the plotting strategy
  enum struct Type { unknown = -1, background, signal, data } type;
  std::string name;        ///< human-friendly sample name
  TH1 *histogram{nullptr}; ///< base ROOT distribution object
  float weight{1.};        ///< cross-section * L, with additional weightings
  int colour{0};           ///< for now, ROOT colours are handled
  std::unordered_map<std::string, std::vector<float>> systematics{};

  void addSystematics(std::string_view, SystematicsType, PyObject * = nullptr);
};

class Stack {
public:
  Stack();

  Sample &add(Sample &);

  const std::vector<Sample> &samples() const { return samples_; }

  /// Order a given samples category according to a sorting strategy
  void sort(SortingType, bool reverse = false);

  const std::shared_ptr<THStack> &stack() const;
  const std::shared_ptr<TH1> &merged() const;

private:
  std::vector<Sample> samples_;
  std::shared_ptr<TH1> hist_merged_{nullptr};
  std::shared_ptr<THStack> stack_{nullptr};
};
} // namespace mplt

#endif
