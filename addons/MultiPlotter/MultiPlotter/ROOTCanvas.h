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
class TLegend;
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
    const std::unique_ptr<TObject> &object =
        objects_.emplace_back(new T(std::forward<Args>(args)...));
    return dynamic_cast<T *>(object.get());
  }
  TLatex &addTextBox(float x1, float y1, const std::vector<std::string> &);
  TLegend &addLegend(float x1, float y1, float x2, float y2);
  TLegend *legend() { return legend_.get(); }

  /// Split the canvas into main/secondary pads
  void split(float lower_fraction = 0.3);
  /// Pad hosting the distributions (the canvas itself if not split)
  TPad *mainPad() { return upper_pad_ ? upper_pad_ : this; }
  /// Secondary pad (null if the canvas was not split)
  TPad *lowerPad() { return lower_pad_; }
  /// Fraction of the canvas height covered by the secondary pad
  float lowerFraction() const { return lower_fraction_; }
  void setLogx(bool); ///< x-axis scaling for all pads
  void setLogy(bool); ///< y-axis scaling for the main pad only

private:
  TPad *upper_pad_{nullptr};
  TPad *lower_pad_{nullptr};
  float lower_fraction_{0.f};
  std::unique_ptr<TLegend> legend_;
  std::vector<std::unique_ptr<TObject>> objects_;
  std::vector<std::unique_ptr<TLatex>> text_boxes_;
};
} // namespace mplt

#endif
