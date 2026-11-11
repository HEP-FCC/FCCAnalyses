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

#ifndef MultiPlotter_Binning_h
#define MultiPlotter_Binning_h

#include <algorithm>
#include <cstddef>
#include <utility>
#include <vector>

/// Operations on per-bin (up, down) shifts indexed by histogram bin number,
namespace mplt::binning {
using Shifts = std::vector<std::pair<float, float>>;

/// Apply rebinning
inline Shifts rebin(const Shifts &shifts, size_t factor) {
  if (shifts.size() < 2 || factor < 2)
    return shifts;
  const size_t num_bins = shifts.size() - 2, new_num_bins = num_bins / factor;
  Shifts rebinned(new_num_bins + 2, {0.f, 0.f});
  // little lambda to account for shifts
  const auto add = [&rebinned](size_t to, const Shifts::value_type &shift) {
    rebinned[to].first += shift.first;
    rebinned[to].second += shift.second;
  };
  add(0, shifts.front());                      // start with underflow bin
  for (size_t bin = 1; bin <= num_bins; ++bin) // bins in "normal" range
    add(std::min((bin - 1) / factor + 1, new_num_bins + 1), shifts[bin]);
  add(new_num_bins + 1, shifts.back()); // end with overflow bin
  return rebinned;
}

/// Move everything below/above the [first, last] bins range into its edges
inline Shifts fold_overflow(const Shifts &shifts, size_t first, size_t last) {
  Shifts folded(shifts);
  if (first > last || last >= shifts.size())
    return folded;
  for (size_t bin = 0; bin < shifts.size(); ++bin) {
    if (bin >= first && bin <= last)
      continue;
    auto &edge = folded[bin < first ? first : last];
    edge.first += shifts[bin].first;
    edge.second += shifts[bin].second;
    folded[bin] = {0.f, 0.f};
  }
  return folded;
}
} // namespace mplt::binning

#endif
