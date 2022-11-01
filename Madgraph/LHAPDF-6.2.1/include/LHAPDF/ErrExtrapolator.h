// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_ErrExtrapolator_H
#define LHAPDF_ErrExtrapolator_H

#include "LHAPDF/Extrapolator.h"

namespace LHAPDF {

  /// Extrapolates using the closest point on the Grid.
  class ErrExtrapolator : public Extrapolator {
  public:

    double extrapolateXQ2(int id, double x, double q2) const;

  };


}
#endif
