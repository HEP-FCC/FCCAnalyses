// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/AlphaS.h"
#include "LHAPDF/Utils.h"

namespace LHAPDF {


  void AlphaS_Ipol::setQValues(const std::vector<double>& qs) {
    vector<double> q2s;
    for (double q : qs) q2s.push_back(q*q);
    setQ2Values(q2s);
  }


  /// @note This is const so it can be called silently from a const method
  void AlphaS_Ipol::_setup_grids() const {
    if (!_knotarrays.empty())
      throw LogicError("AlphaS interpolation subgrids being initialized a second time!");

    if (_q2s.size() != _as.size())
      throw MetadataError("AlphaS value and Q interpolation arrays are differently sized");

    // Walk along the Q2 vector, making subgrids at each boundary
    double prevQ2 = _q2s.front();
    vector<double> q2s, as;
    size_t combined_lenq2s = 0; //< For consistency checking
    for (size_t i = 0; i <= _q2s.size(); ++i) { //< The iteration to len+1 is intentional
      // Get current Q2 and alpha_s points, faked if i > vector to force syncing
      const double currQ2 = (i != _q2s.size()) ? _q2s[i] : _q2s.back();
      const double currAS = (i != _q2s.size()) ? _as[i] : -1;
      // If the Q2 value is repeated, sync the current subgrid and start a new one.
      // Note special treatment for the first and last points in q2s.
      if (abs(currQ2 - prevQ2) < numeric_limits<double>::epsilon()) {
        // Sync current subgrid as as AlphaSArray
        if (i != 0) {
          _knotarrays[q2s.front()] = AlphaSArray(q2s, as);
          combined_lenq2s += q2s.size();
        }
        // Reset temporary vectors
        q2s.clear(); q2s.reserve(_q2s.size() - i);
        as.clear(); as.reserve(_q2s.size() - i);
      }
      // Append current value to temporary vectors
      q2s.push_back(currQ2);
      as.push_back(currAS);
      prevQ2 = currQ2;
    }
    if (combined_lenq2s != _q2s.size())
      throw AlphaSError("Sum of alpha_s subgrid sizes does not match input knot array ("
                        + to_str(combined_lenq2s) + " vs. " + to_str(_q2s.size()) + ")");
  }


  double AlphaS_Ipol::_interpolateCubic(double T, double VL, double VDL, double VH, double VDH) const {
    // Pre-calculate powers of T
    const double t2 = T*T;
    const double t3 = t2*T;

    // Calculate left point
    const double p0 = (2*t3 - 3*t2 + 1)*VL;
    const double m0 = (t3 - 2*t2 + T)*VDL;

    // Calculate right point
    const double p1 = (-2*t3 + 3*t2)*VH;
    const double m1 = (t3 - t2)*VDH;

    return abs(p0 + m0 + p1 + m1) < 2. ? p0 + m0 + p1 + m1 : std::numeric_limits<double>::max();
  }


  // Interpolate alpha_s from tabulated points in Q2 via metadata
  double AlphaS_Ipol::alphasQ2(double q2) const {
    assert(q2 >= 0);

    // Using base 10 for logs to get constant gradient extrapolation in
    // a log 10 - log 10 plot
    if (q2 < _q2s.front()) {
      // Remember to take situations where the first knot also is a
      // flavor threshold into account
      double dlogq2, dlogas;
      unsigned int next_point = 1;
      while ( _q2s[0] == _q2s[next_point] ) next_point++;
      dlogq2  = log10( _q2s[next_point] / _q2s[0] );
      dlogas  = log10( _as[next_point]  / _as[0]  );
      const double loggrad = dlogas / dlogq2;
      return _as[0] * pow( q2/_q2s[0] , loggrad );
    }

    if (q2 > _q2s.back()) return _as.back();

    // If this is the first valid query, set up the ipol grids
    if (_knotarrays.empty()) _setup_grids();

    // Retrieve the appropriate subgrid
    map<double, AlphaSArray>::const_iterator it = --(_knotarrays.upper_bound(q2));
    const AlphaSArray& arr = it->second;

    // Get the Q/alpha_s index on this array which is *below* this Q point
    const size_t i = arr.iq2below(q2);

    // Calculate derivatives
    double didlogq2, di1dlogq2;
    if ( i == 0 ) {
      didlogq2 = arr.ddlogq_forward(i);
      di1dlogq2 = arr.ddlogq_central(i+1);
    } else if ( i == arr.logq2s().size()-2 ) {
      didlogq2 = arr.ddlogq_central(i);
      di1dlogq2 = arr.ddlogq_backward(i+1);
    } else {
      didlogq2 = arr.ddlogq_central(i);
      di1dlogq2 = arr.ddlogq_central(i+1);
    }

    // Calculate alpha_s
    const double dlogq2 = arr.logq2s()[i+1] - arr.logq2s()[i];
    const double tlogq2 = (log(q2) - arr.logq2s()[i]) / dlogq2;
    return _interpolateCubic( tlogq2,
                              arr.alphas()[i], didlogq2*dlogq2,
                              arr.alphas()[i+1], di1dlogq2*dlogq2 );
  }


}
