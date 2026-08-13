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

#ifndef MultiPlotter_Utils_h
#define MultiPlotter_Utils_h

#include <pybind11/pybind11.h>
#include <string_view>

namespace mplt::utils {
/// Retrieve a parameter from a Python dictionary (from its key), and replace it
/// with a default value if the key is not found
template <typename T>
T get_with_default(const pybind11::dict &dict, std::string_view key,
                   T default_value = T()) {
  if (dict.contains(key))
    return pybind11::cast<T>(dict[key.data()]);
  return default_value;
}
} // namespace mplt::utils

#endif
