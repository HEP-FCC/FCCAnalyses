// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/BicubicInterpolator.h"
#include <iostream>

namespace LHAPDF {


  namespace { // Unnamed namespace

    // One-dimensional linear interpolation for y(x)
    inline double _interpolateLinear(double x, double xl, double xh, double yl, double yh)	{
      assert(x >= xl);
      assert(xh >= x);
      return yl + (x - xl) / (xh - xl) * (yh - yl);
    }

    // One-dimensional cubic interpolation
    inline double _interpolateCubic(double T, double VL, double VDL, double VH, double VDH) {
      // Pre-calculate powers of T
      const double t2 = T*T;
      const double t3 = t2*T;

      // Calculate left point
      const double p0 = (2*t3 - 3*t2 + 1)*VL;
      const double m0 = (t3 - 2*t2 + T)*VDL;

      // Calculate right point
      const double p1 = (-2*t3 + 3*t2)*VH;
      const double m1 = (t3 - t2)*VDH;

      return p0 + m0 + p1 + m1;
    }


    // Provides d/dx at all grid locations
    double _ddx(const KnotArray1F& subgrid, size_t ix, size_t iq2) {
      /// @todo Re-order this if so that branch prediction will favour the "normal" central case
      if (ix == 0) { //< If at leftmost edge, use forward difference
        return (subgrid.xf(ix+1, iq2) - subgrid.xf(ix, iq2)) / (subgrid.xs()[ix+1] - subgrid.xs()[ix]);
      } else if (ix == subgrid.xs().size() - 1) { //< If at rightmost edge, use backward difference
        return (subgrid.xf(ix, iq2) - subgrid.xf(ix-1, iq2)) / (subgrid.xs()[ix] - subgrid.xs()[ix-1]);
      } else { //< If central, use the central difference
        const double lddx = (subgrid.xf(ix, iq2) - subgrid.xf(ix-1, iq2)) / (subgrid.xs()[ix] - subgrid.xs()[ix-1]);
        const double rddx = (subgrid.xf(ix+1, iq2) - subgrid.xf(ix, iq2)) / (subgrid.xs()[ix+1] - subgrid.xs()[ix]);
        return (lddx + rddx) / 2.0;
      }
    }

  }



  double BicubicInterpolator::_interpolateXQ2(const KnotArray1F& subgrid, double x, size_t ix, double q2, size_t iq2) const {
    if (subgrid.logxs().size() < 4)
      throw GridError("PDF subgrids are required to have at least 4 x-knots for use with BicubicInterpolator");
    if (subgrid.logq2s().size() < 4) {
      if (subgrid.logq2s().size() > 1) {
	// Fallback to BilinearInterpolator if either 2 or 3 Q2-knots
	// First interpolate in x
	const double f_ql = _interpolateLinear(x, subgrid.xs()[ix], subgrid.xs()[ix+1], subgrid.xf(ix, iq2), subgrid.xf(ix+1, iq2));
	const double f_qh = _interpolateLinear(x, subgrid.xs()[ix], subgrid.xs()[ix+1], subgrid.xf(ix, iq2+1), subgrid.xf(ix+1, iq2+1));
	// Then interpolate in Q2, using the x-ipol results as anchor points
	return _interpolateLinear(q2, subgrid.q2s()[iq2], subgrid.q2s()[iq2+1], f_ql, f_qh);
      } else throw GridError("PDF subgrids are required to have at least 2 Q2-knots for use with BicubicInterpolator");
    }

    /// @todo Allow interpolation right up to the borders of the grid in Q2 and x... the last inter-knot range is currently broken

    /// @todo Also treat the x top/bottom edges carefully, cf. the Q2 ones

    // Distance parameters
    const double dx = subgrid.xs()[ix+1] - subgrid.xs()[ix];
    const double tx = (x - subgrid.xs()[ix]) / dx;
    /// @todo Only compute these if the +1 and +2 indices are guaranteed to be valid
    const double dq_0 = subgrid.q2s()[iq2] - subgrid.q2s()[iq2-1];
    const double dq_1 = subgrid.q2s()[iq2+1] - subgrid.q2s()[iq2];
    const double dq_2 = subgrid.q2s()[iq2+2] - subgrid.q2s()[iq2+1];
    const double dq = dq_1;
    const double tq = (q2 - subgrid.q2s()[iq2]) / dq;

    // Points in Q2
    double vl = _interpolateCubic(tx, subgrid.xf(ix, iq2), _ddx(subgrid, ix, iq2) * dx,
                                      subgrid.xf(ix+1, iq2), _ddx(subgrid, ix+1, iq2) * dx);
    double vh = _interpolateCubic(tx, subgrid.xf(ix, iq2+1), _ddx(subgrid, ix, iq2+1) * dx,
                                      subgrid.xf(ix+1, iq2+1), _ddx(subgrid, ix+1, iq2+1) * dx);

    // Derivatives in Q2
    double vdl, vdh;
    if (iq2 == 0) {
      // Forward difference for lower q
      vdl = (vh - vl) / dq_1;
      // Central difference for higher q
      double vhh = _interpolateCubic(tx, subgrid.xf(ix, iq2+2), _ddx(subgrid, ix, iq2+2) * dx,
                                         subgrid.xf(ix+1, iq2+2), _ddx(subgrid, ix+1, iq2+2) * dx);
      vdh = (vdl + (vhh - vh)/dq_2) / 2.0;
    }
    else if (iq2+1 == subgrid.q2s().size()-1) {
      // Backward difference for higher q
      vdh = (vh - vl) / dq_1;
      // Central difference for lower q
      double vll = _interpolateCubic(tx, subgrid.xf(ix, iq2-1), _ddx(subgrid, ix, iq2-1) * dx,
                                         subgrid.xf(ix+1, iq2-1), _ddx(subgrid, ix+1, iq2-1) * dx);
      vdl = (vdh + (vl - vll)/dq_0) / 2.0;
    }
    else {
      // Central difference for both q
      double vll = _interpolateCubic(tx, subgrid.xf(ix, iq2-1), _ddx(subgrid, ix, iq2-1) * dx,
                                         subgrid.xf(ix+1, iq2-1), _ddx(subgrid, ix+1, iq2-1) * dx);
      vdl = ( (vh - vl)/dq_1 + (vl - vll)/dq_0 ) / 2.0;
      double vhh = _interpolateCubic(tx, subgrid.xf(ix, iq2+2), _ddx(subgrid, ix, iq2+2) * dx,
                                         subgrid.xf(ix+1, iq2+2), _ddx(subgrid, ix+1, iq2+2) * dx);
      vdh = ( (vh - vl)/dq_1 + (vhh - vh)/dq_2 ) / 2.0;
    }

    vdl *= dq;
    vdh *= dq;

    return _interpolateCubic(tq, vl, vdl, vh, vdh);
  }


}
