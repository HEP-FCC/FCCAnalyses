// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/ErrExtrapolator.h"
#include "LHAPDF/Exceptions.h"

namespace LHAPDF {


  double ErrExtrapolator::extrapolateXQ2(int id, double x, double q2) const {
    throw RangeError("Point x=" + to_str(x) + ", Q2=" + to_str(q2) +
                     " is outside the PDF grid boundaries");
  }


}
