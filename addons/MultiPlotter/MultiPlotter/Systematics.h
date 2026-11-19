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

#ifndef MultiPlotter_Systematics_h
#define MultiPlotter_Systematics_h

#include <memory>
#include <string>

// forward declarations
namespace mplt {
class SystematicsSet;
} // namespace mplt
namespace pybind11 {
class dict;
} // namespace pybind11

namespace mplt {
enum SystematicsType { constant, log_normal, shape };

/// Systematics computation object
/// \author Laurent Forthomme <laurent.forthomme@cern.ch>
/// \date July 2026
class Systematics {
public:
  static std::unique_ptr<Systematics>
  build(SystematicsType, std::string_view name, pybind11::dict &);

  virtual void apply(SystematicsSet &set) const = 0;

  const SystematicsType type;
  const std::string name;

protected:
  explicit Systematics(SystematicsType _type, std::string_view _name)
      : type{_type}, name{_name} {}
};
} // namespace mplt

#endif
