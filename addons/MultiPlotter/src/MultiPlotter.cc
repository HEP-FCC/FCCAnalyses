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

#include "MultiPlotter/MultiPlotter.h"

#include <TH1.h>

using namespace mplt;

MultiPlotter::MultiPlotter(std::string_view experiment_name,
                           const std::vector<std::string> &extra_labels)
    : experiment_name_{experiment_name}, extra_labels_{extra_labels} {}

Sample &MultiPlotter::addSample(Sample &sample) {
  return samples_[sample.type].add(sample);
}

std::string MultiPlotter::yieldsTable() const {
  std::ostringstream table;
  // TODO: implement the table creation
  //  potentially, create a base table creation object that can be specialised
  //  for (LaTeX, Markdown, ...) output type
  return table.str();
}
