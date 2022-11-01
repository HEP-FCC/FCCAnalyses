// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_ContinuationExtrapolator_H
#define LHAPDF_ContinuationExtrapolator_H

#include "LHAPDF/Extrapolator.h"

namespace LHAPDF {


  /// The ContinuationExtrapolator provides an implementation of the extrapolation used in
  /// the MSTW standalone code (and LHAPDFv5 when using MSTW sets), G. Watt, October 2014.
  class ContinuationExtrapolator : public Extrapolator {
  public:

    double extrapolateXQ2(int id, double x, double q2) const;

  };


}
#endif
