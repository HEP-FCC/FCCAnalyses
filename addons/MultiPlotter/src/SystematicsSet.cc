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

#include "MultiPlotter/SystematicsSet.h"
#include <TH1.h>
#include <cmath>

using namespace mplt;

SystematicsSet::SystematicsSet(const TH1 *nominal)
    : true_nominal_shape_{static_cast<TH1 *>(nominal->Clone())},
      true_up_shape_{static_cast<TH1 *>(nominal->Clone())},
      true_down_shape_{static_cast<TH1 *>(nominal->Clone())} {}

void SystematicsSet::reset() {
  nominal_shape.reset(static_cast<TH1 *>(true_nominal_shape_->Clone()));
  up_shape.reset(static_cast<TH1 *>(true_up_shape_->Clone()));
  down_shape.reset(static_cast<TH1 *>(true_down_shape_->Clone()));
}

void SystematicsSet::scale(float factor) {
  for (auto &object : {nominal_shape, up_shape, down_shape})
    if (object)
      object->Scale(factor);
}

void SystematicsSet::rebin(size_t factor) {
  for (auto &object : {nominal_shape, up_shape, down_shape})
    if (object)
      object->Rebin(factor);
}

std::unique_ptr<TH1> SystematicsSet::shapeUp() const {
  std::unique_ptr<TH1> shape(static_cast<TH1 *>(up_shape->Clone()));
  shape->SetDirectory(nullptr); // disable ROOT storage in directory
  shape->Sumw2(false);          // disable uncertainties propagation
  shape->Add(nominal_shape.get(), -1.);
  return shape;
}

std::unique_ptr<TH1> SystematicsSet::shapeDown() const {
  std::unique_ptr<TH1> shape(static_cast<TH1 *>(nominal_shape->Clone()));
  shape->SetDirectory(nullptr); // disable ROOT storage in directory
  shape->Sumw2(false);          // disable uncertainties propagation
  shape->Add(down_shape.get(), -1.);
  return shape;
}

std::vector<float> SystematicsSet::binnedMaximumUncertainty() const {
  const auto asym_unc = binnedAsymmetricUncertainties();
  std::vector<float> syst_unc;
  syst_unc.reserve(asym_unc.size());
  for (size_t i = 0; i < asym_unc.size(); ++i)
    syst_unc.emplace_back(
        std::max(asym_unc.at(i).first, asym_unc.at(i).second));
  return syst_unc;
}

std::vector<std::pair<float, float>>
SystematicsSet::binnedAsymmetricUncertainties() const {
  std::vector<std::pair<float, float>> syst_unc;
  syst_unc.reserve(nominal_shape->GetNbinsX());
  for (int i = 1; i <= nominal_shape->GetNbinsX(); ++i)
    syst_unc.emplace_back(std::make_pair(
        std::fabs(up_shape->GetBinContent(i) - nominal_shape->GetBinContent(i)),
        std::fabs(nominal_shape->GetBinContent(i) -
                  down_shape->GetBinContent(i))));
  return syst_unc;
}

float SystematicsSet::totalUncertainty() const {
  const auto asym_unc = binnedAsymmetricUncertainties();
  float total_syst_unc2 = 0.f;
  for (size_t i = 0; i < asym_unc.size(); ++i) {
    // TODO: add support for asymmetric uncertainties
    const auto syst_unc = std::max(asym_unc.at(i).first, asym_unc.at(i).second);
    total_syst_unc2 += syst_unc * syst_unc;
  }
  return std::sqrtf(total_syst_unc2);
}
