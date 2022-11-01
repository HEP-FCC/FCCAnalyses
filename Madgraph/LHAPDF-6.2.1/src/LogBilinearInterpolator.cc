// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/LogBilinearInterpolator.h"

namespace LHAPDF {


  namespace { // Unnamed namespace

    // One-dimensional linear interpolation for y(x)
    inline double _interpolateLinear(double x, double xl, double xh, double yl, double yh)	{
      assert(x >= xl);
      assert(xh >= x);
      return yl + (x - xl) / (xh - xl) * (yh - yl);
    }

  }


  double LogBilinearInterpolator::_interpolateXQ2(const KnotArray1F& subgrid, double x, size_t ix, double q2, size_t iq2) const {
    if (subgrid.logxs().size() < 2)
      throw GridError("PDF subgrids are required to have at least 2 x-knots for use with LogBilinearInterpolator");
    if (subgrid.logq2s().size() < 2)
      throw GridError("PDF subgrids are required to have at least 2 Q2-knots for use with LogBilinearInterpolator");
    // First interpolate in x
    const double logx = log(x);
    const double logx0 = subgrid.logxs()[ix];
    const double logx1 = subgrid.logxs()[ix+1];
    const double f_ql = _interpolateLinear(logx, logx0, logx1, subgrid.xf(ix, iq2), subgrid.xf(ix+1, iq2));
    const double f_qh = _interpolateLinear(logx, logx0, logx1, subgrid.xf(ix, iq2+1), subgrid.xf(ix+1, iq2+1));
    // Then interpolate in Q2, using the x-ipol results as anchor points
    return _interpolateLinear(log(q2), subgrid.logq2s()[iq2], subgrid.logq2s()[iq2+1], f_ql, f_qh);
  }


}
