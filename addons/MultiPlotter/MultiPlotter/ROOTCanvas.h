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

#ifndef MultiPlotter_ROOTCanvas_h
#define MultiPlotter_ROOTCanvas_h

#include <TCanvas.h>

class TLatex;
namespace pybind11 {
class dict;
} // namespace pybind11

namespace mplt {
/// Enhanced ROOT TCanvas object
/// \author Laurent Forthomme <laurent.forthomme@cern.ch>
/// \date September 2026
class ROOTCanvas : public TCanvas {
public:
  using TCanvas::TCanvas;
  explicit ROOTCanvas(const pybind11::dict &);

  void save(const std::vector<std::string> &formats,
            std::string_view alternative_name = "");

  // TODO: use concepts to ensure T derives from a TObject
  template <typename T, typename... Args> T *make(Args &&...args) {
    auto *&object = objects_.emplace_back(new T(std::forward<Args>(args)...));
    return dynamic_cast<T *>(object.get());
  }
  TLatex &addTextBox(float x1, float y1, const std::vector<std::string> &);

private:
  std::vector<std::unique_ptr<TObject>> objects_;
  std::vector<std::unique_ptr<TLatex>> text_boxes_;
};
} // namespace mplt

#endif
