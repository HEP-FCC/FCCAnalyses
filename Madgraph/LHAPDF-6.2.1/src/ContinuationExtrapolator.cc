// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/ContinuationExtrapolator.h"
#include "LHAPDF/GridPDF.h"

namespace LHAPDF {


  namespace { // Unnamed namespace

    // One-dimensional linear extrapolation for y(x).
    // Extrapolate in log(x) rather than just in x.
    inline double _extrapolateLinear(double x, double xl, double xh, double yl, double yh) {
      if (yl > 1e-3 && yh > 1e-3) {
	// If yl and yh are sufficiently positive, keep y positive by extrapolating log(y).
	return exp(log(yl) + (log(x) - log(xl)) / (log(xh) - log(xl)) * (log(yh) - log(yl)));
      } else {
	// Otherwise just extrapolate y itself.
	return yl + (log(x) - log(xl)) / (log(xh) - log(xl)) * (yh - yl);
      }
    }

  }
  
  
  double ContinuationExtrapolator::extrapolateXQ2(int id, double x, double q2) const {
    // The ContinuationExtrapolator provides an implementation of the extrapolation used in
    // the MSTW standalone code (and LHAPDFv5 when using MSTW sets), G. Watt, October 2014.

    const size_t nxknots = pdf().xKnots().size(); // total number of x knots (all subgrids)
    const size_t nq2knots = pdf().q2Knots().size(); // total number of q2 knots (all subgrids)

    const double xMin = pdf().xKnots()[0]; // first x knot
    const double xMin1 = pdf().xKnots()[1]; // second x knot
    const double xMax = pdf().xKnots()[nxknots-1]; // last x knot

    const double q2Min = pdf().q2Knots()[0]; // first q2 knot
    const double q2Max1 = pdf().q2Knots()[nq2knots-2]; // second-last q2 knot
    const double q2Max = pdf().q2Knots()[nq2knots-1]; // last q2 knot
    
    double fxMin, fxMin1, fq2Max, fq2Max1, fq2Min, fq2Min1, xpdf, anom;

    if (x < xMin && (q2 >= q2Min && q2 <= q2Max)) {

      // Extrapolation in small x only.
      fxMin = pdf().interpolator().interpolateXQ2(id, xMin, q2); // PDF at (xMin,q2)
      fxMin1 = pdf().interpolator().interpolateXQ2(id, xMin1, q2); // PDF at (xMin1,q2)
      xpdf = _extrapolateLinear(x, xMin, xMin1, fxMin, fxMin1); // PDF at (x,q2)

    } else if ((x >= xMin && x <= xMax) && q2 > q2Max) {

      // Extrapolation in large q2 only.
      fq2Max = pdf().interpolator().interpolateXQ2(id, x, q2Max); // PDF at (x,q2Max)
      fq2Max1 = pdf().interpolator().interpolateXQ2(id, x, q2Max1); // PDF at (x,q2Max1)
      xpdf = _extrapolateLinear(q2, q2Max, q2Max1, fq2Max, fq2Max1); // PDF at (x,q2)

    } else if (x < xMin && q2 > q2Max) {

      // Extrapolation in large q2 AND small x.
      fq2Max = pdf().interpolator().interpolateXQ2(id, xMin, q2Max); // PDF at (xMin,q2Max)
      fq2Max1 = pdf().interpolator().interpolateXQ2(id, xMin, q2Max1); // PDF at (xMin,q2Max1)
      fxMin = _extrapolateLinear(q2, q2Max, q2Max1, fq2Max, fq2Max1); // PDF at (xMin,q2)
      fq2Max = pdf().interpolator().interpolateXQ2(id, xMin1, q2Max); // PDF at (xMin1,q2Max)
      fq2Max1 = pdf().interpolator().interpolateXQ2(id, xMin1, q2Max1); // PDF at (xMin1,q2Max1)
      fxMin1 = _extrapolateLinear(q2, q2Max, q2Max1, fq2Max, fq2Max1); // PDF at (xMin1,q2)
      xpdf = _extrapolateLinear(x, xMin, xMin1, fxMin, fxMin1); // PDF at (x,q2)

    } else if (q2 < q2Min && x <= xMax) {

      // Extrapolation in small q2.

      if (x < xMin) {

	// Extrapolation also in small x.

	fxMin = pdf().interpolator().interpolateXQ2(id, xMin, q2Min); // PDF at (xMin,q2Min)
	fxMin1 = pdf().interpolator().interpolateXQ2(id, xMin1, q2Min); // PDF at (xMin1,q2Min)
	fq2Min = _extrapolateLinear(x, xMin, xMin1, fxMin, fxMin1); // PDF at (x,q2Min)
	fxMin = pdf().interpolator().interpolateXQ2(id, xMin, 1.01*q2Min); // PDF at (xMin,1.01*q2Min)
	fxMin1 = pdf().interpolator().interpolateXQ2(id, xMin1, 1.01*q2Min); // PDF at (xMin1,1.01*q2Min)
	fq2Min1 = _extrapolateLinear(x, xMin, xMin1, fxMin, fxMin1); // PDF at (x,1.01*q2Min)

      } else {

	// Usual interpolation in x.

	fq2Min = pdf().interpolator().interpolateXQ2(id, x, q2Min); // PDF at (x,q2Min)
	fq2Min1 = pdf().interpolator().interpolateXQ2(id, x, 1.01*q2Min); // PDF at (x,1.01*q2Min)

      }

      // Calculate the anomalous dimension, dlog(f)/dlog(q2),
      // evaluated at q2Min.  Then extrapolate the PDFs to low
      // q2 < q2Min by interpolating the anomalous dimension between
      // the value at q2Min and a value of 1 for q2 << q2Min.
      // If value of PDF at q2Min is very small, just set
      // anomalous dimension to 1 to prevent rounding errors.
      // Impose minimum anomalous dimension of -2.5.
      
      if (abs(fq2Min) >= 1e-5) {

	// anom = dlog(f)/dlog(q2) = q2/f * df/dq2 evaluated at q2 = q2Min,
	// where derivative df/dq2 = ( f(1.01*q2Min) - f(q2Min) ) / (0.01*q2Min).
	anom = max( -2.5, (fq2Min1 - fq2Min) / fq2Min / 0.01 );

      } else anom = 1.0;

      // Interpolates between f(q2Min)*(q2/q2Min)^anom for q2 ~ q2Min and
      // f(q2Min)*(q2/q2Min) for q2 << q2Min, i.e. PDFs vanish as q2 --> 0.
      xpdf = fq2Min * pow( q2/q2Min, anom*q2/q2Min + 1.0 - q2/q2Min );

    }

    else throw LogicError("We shouldn't be able to get here!");
  
    return xpdf;

  }


}
