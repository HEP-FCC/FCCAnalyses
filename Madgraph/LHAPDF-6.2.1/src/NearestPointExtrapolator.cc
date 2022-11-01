// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/NearestPointExtrapolator.h"
#include "LHAPDF/GridPDF.h"

namespace LHAPDF {


  namespace { // Unnamed namespace

    // Return the value in the given list that best matches the target value
    double _findClosestMatch(const vector<double>& cands, double target) {
      // cout << "From NPXpol: knots = ["; for (double c : cands) cout << c << " "; cout << endl;
      vector<double>::const_iterator it = lower_bound(cands.begin(), cands.end(), target);
      const double upper = *it;
      const double lower = (it == cands.begin()) ? upper : *(--it); //< Avoid decrementing the first entry
      /// @todo Closeness in linear or log space? Hmm...
      if (fabs(target - upper) < fabs(target - lower)) return upper;
      return lower;
    }

  }


  double NearestPointExtrapolator::extrapolateXQ2(int id, double x, double q2) const {
    /// Find the closest valid x and Q2 points, either on- or off-grid, and use the current interpolator
    // cout << "From NPXpol: x = " << x << endl;
    /// @todo We should *always* interpolate x -> 1.0
    const double closestX = (pdf().inRangeX(x)) ? x : _findClosestMatch(pdf().xKnots(), x);
    const double closestQ2 = (pdf().inRangeQ2(q2)) ? q2 : _findClosestMatch(pdf().q2Knots(), q2);
    // cout << "From NPXpol: x_closest = " << closestX << ", Q2_closest = " << closestQ2 << endl;;
    return pdf().interpolator().interpolateXQ2(id, closestX, closestQ2);
  }


}
