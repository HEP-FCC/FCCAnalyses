// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/AlphaS.h"
#include "LHAPDF/Utils.h"

namespace LHAPDF {


  void AlphaS_ODE::setQValues(const std::vector<double>& qs) {
    vector<double> q2s;
    for (double q : qs) q2s.push_back(q*q);
    setQ2Values(q2s);
  }


  // Calculate first order derivative, dy/dt, as it appears in the differential equation
  double AlphaS_ODE::_derivative(double t, double y, const vector<double>& beta) const {
    if ( _qcdorder == 0 ) return 0;
    const double b0 = beta[0];
    double d = (b0*y*y);
    if ( _qcdorder == 1 ) return - d / t;
    const double b1 = beta[1];
    d += (b1*y*y*y);
    if ( _qcdorder == 2 ) return - d / t;
    const double b2 = beta[2];
    d += (b2*y*y*y*y);
    if ( _qcdorder == 3 ) return - d / t;
    const double b3 = beta[3];
    d += (b3*y*y*y*y*y);
    if ( _qcdorder == 4 ) return - d / t;
    const double b4 = beta[4];
    d += (b4*y*y*y*y*y*y);
    return - d / t;
  }

  // Calculate decoupling for transition from num. flavour = ni -> nf
  double AlphaS_ODE::_decouple(double y, double t, unsigned int ni, unsigned int nf) const {
    if ( ni == nf || _qcdorder == 0 ) return 1.;
    double as = y / M_PI;
    unsigned int heavyQuark = nf > ni ? nf : ni;
    std::map<int, double>::const_iterator quark = _quarkmasses.find(heavyQuark);
    if ( quark == _quarkmasses.end() ) throw AlphaSError("Quark masses are not set, required for using the ODE solver with a variable flavor scheme.");
    const double qmass = quark->second;
    double lnmm = log(t/sqr(qmass));
    double as1 = 0, as2 = 0, as3 = 0, as4 = 0;
    if ( ni > nf ) {
      as1 = - 0.166666*lnmm*as;
      as2 = (0.152778 - 0.458333*lnmm + 0.0277778*lnmm*lnmm)*as*as;
      as3 = (0.972057 - 0.0846515*nf + (- 1.65799 + 0.116319*nf)*lnmm +
        (0.0920139 - 0.0277778*nf)*lnmm*lnmm - 0.00462963*lnmm*lnmm*lnmm)*as*as*as;
      as4 = (5.17035 - 1.00993*nf - 0.0219784*nf*nf + (- 8.42914 + 1.30983*nf + 0.0367852*nf*nf)*lnmm +
        (0.629919 - 0.143036*nf + 0.00371335*nf*nf)*lnmm*lnmm + (-0.181617 - 0.0244985*nf + 0.00308642*nf*nf)*lnmm*lnmm*lnmm +
        0.000771605*lnmm*lnmm*lnmm*lnmm)*as*as*as*as;
    } else {
      as1 = 0.166667*lnmm*as;
      as2 = (- 0.152778 + 0.458333*lnmm + 0.0277778*lnmm*lnmm)*as*as;
      as3 = (- 0.972057 + 0.0846515*ni + (1.53067 - 0.116319*ni)*lnmm +
        (0.289931 + 0.0277778*ni)*lnmm*lnmm + 0.00462963*lnmm*lnmm*lnmm)*as*as*as;
      as4 = (- 5.10032 + 1.00993*ni + 0.0219784*ni*ni + (7.03696 - 1.22518*ni - 0.0367852*ni*ni)*lnmm +
        (1.59462 + 0.0267168*ni + 0.00371335*ni*ni)*lnmm*lnmm + (0.280575 + 0.0522762*ni - 0.00308642*ni*ni)*lnmm*lnmm*lnmm +
        0.000771605*lnmm*lnmm*lnmm*lnmm)*as*as*as*as;
    }
    double decoupling = 1.;
    decoupling += as1;
    if ( _qcdorder == 1 ) return decoupling;
    decoupling += as2;
    if ( _qcdorder == 2 ) return decoupling;
    decoupling += as3;
    if ( _qcdorder == 3 ) return decoupling;
    decoupling += as4;
    return decoupling;
  }


  // Calculate the next step, using recursion to achieve
  // adaptive step size. Passing by reference explained
  // below.
  void AlphaS_ODE::_rk4(double& t, double& y, double h,
                        const double allowed_change, const vector<double>& bs) const {

    // Determine increments in y based on the slopes of the function at the
    // beginning, midpoint, and end of the interval
    const double k1 = h * _derivative(t, y, bs);
    const double k2 = h * _derivative(t + h/2.0, y + k1/2.0, bs);
    const double k3 = h * _derivative(t + h/2.0, y + k2/2.0, bs);
    const double k4 = h * _derivative(t + h, y + k3, bs);
    const double change = (k1 + 2*k2 + 2*k3 + k4) / 6.0;

    // Only call recursively if Q2 > 1 GeV (constant step
    // size after this)
    if (t > 1. && fabs(change) > allowed_change) {
      _rk4(t, y, h/2., allowed_change, bs);
    } else {
      y += change;
      t += h;
    }
  }


  // Solve for alpha_s(q2) using alpha_s = y and Q2 = t as starting points
  // Pass y and t by reference and change them to avoid having to
  // return them in a container -- bit confusing but should be more
  // efficient
  void AlphaS_ODE::_solve(double q2, double& t, double& y,
                          const double& allowed_relative, double h, double accuracy) const {
    if ( q2 == t ) return;
    while (fabs(q2 - t) > accuracy) {
      /// Can make the allowed change smaller as the q2 scale gets greater, does not seem necessary
      const double allowed_change = allowed_relative;

      /// Mechanism to shrink the steps if accuracy < stepsize and we are close to Q2
      if (fabs(h) > accuracy && fabs(q2 - t)/h < 10 && t > 1.) h = accuracy/2.1;
      /// Take constant steps for Q2 < 1 GeV
      if (fabs(h) > 0.01 && t < 1.) { accuracy = 0.0051; h = 0.01; }
      // Check if we are going to run forward or backwards in energy scale towards target Q2.
      /// @todo C++11's std::copysign would be perfect here
      if ((q2 < t && sgn(h) > 0) || (q2 > t && sgn(h) < 0)) h *= -1;

      // Get beta coefficients
      const vector<double> bs = _betas(numFlavorsQ2(t));

      // Calculate next step
      _rk4(t, y, h, allowed_change, bs);

      if (y > 2.) { y = std::numeric_limits<double>::max(); break; }
    }
  }


  /// Interpolate to get Alpha_S if the ODE has been solved,
  /// otherwise solve ODE from scratch
  double AlphaS_ODE::alphasQ2(double q2) const {
    // Tabulate ODE solutions for interpolation and return interpolated value
    _interpolate();
    return _ipol.alphasQ2(q2);
    // // Or directly return the ODE result (for testing)
    // double h = 2;
    // const double allowed_relative = 0.01;
    // const double faccuracy = 0.01;
    // double accuracy = faccuracy;
    // double t = sqr(_mz); // starting point
    // double y = _alphas_mz; // starting value
    // _solve(q2, t, y, allowed_relative, h, accuracy); // solve ODE
    // return y;
  }


  // Solve the differential equation in alphaS using an implementation of RK4
  void AlphaS_ODE::_interpolate() const {
    if ( _calculated ) return;

    // Initial step size
    double h = 2.0;
    /// This the the relative error allowed for the adaptive step size.
    const double allowed_relative = 0.01;

    /// Accuracy of Q2 (error in Q2 within this / 2)
    double accuracy = 0.001;

    // Run in Q2 using RK4 algorithm until we are within our defined accuracy
    double t;
    double y;

    if (_customref) {
      t = sqr(_mreference); // starting point
      y = _alphas_reference; // starting value
    } else {
      t = sqr(_mz); // starting point
      y = _alphas_mz; // starting value
    }

    // If a vector of knots in q2 has been given, solve for those.
    // This creates a default grid which should be overkill for most
    // purposes
    if ( _q2s.empty() ) {
      for (int q = 1; (q/10.) < 1; ++q) {
        _q2s.push_back(sqr(q/10.));
      }
      for (int q = 4; (q/4.) < _mz; ++q) {
        _q2s.push_back(sqr(q/4.));
      }
      for (int q = ceil(_mz/4); (4*q) < 1000; ++q) {
        _q2s.push_back(sqr(4*q));
      }
      for (int q = (1000/50); (50*q) < 2000; ++q) {
        _q2s.push_back(sqr(50*q));
      }

      if ( _flavorthresholds.empty() ) {
        for (int it = 4; it <= 6; ++it) {
          std::map<int, double>::const_iterator element = _quarkmasses.find(it);
          if ( element == _quarkmasses.end() ) continue;
          _q2s.push_back(sqr(element->second)); _q2s.push_back(sqr(element->second));
        }
      } else {
        for (int it = 4; it <= 6; ++it) {
          std::map<int, double>::const_iterator element = _flavorthresholds.find(it);
          if ( element == _flavorthresholds.end() ) continue;
          _q2s.push_back(sqr(element->second)); _q2s.push_back(sqr(element->second));
        }
      }
      sort(_q2s.begin(),_q2s.end());
    }
    // If for some reason the highest q2 knot is below m_{Z},
    // force a knot there anyway (since we know it, might as well
    // use it)
    if ( _q2s[_q2s.size()-1] < sqr(_mz) ) _q2s.push_back(sqr(_mz));

    // Find the index of the knot right below m_{Z}
    unsigned int index_of_mz_lower = 0;

    while ( _q2s[index_of_mz_lower + 1] < sqr(_mz) ) {
      if ( index_of_mz_lower == _q2s.size() -1 ) break;
      index_of_mz_lower++;
    }

    vector<pair<int, double> > grid; // for storing in correct order
    grid.reserve(_q2s.size());
    double low_lim = 0;
    double last_val = -1;
    bool threshold = false;

    // We do this by starting from m_{Z}, going down to the lowest q2,
    // and then jumping back up to m_{Z} to avoid calculating things twice
    for ( int ind = index_of_mz_lower; ind >= 0; --ind) {
      const double q2 = _q2s[ind];
      // Deal with cases with two identical adjacent points (thresholds) by decreasing step size,
      // allowed errors, and accuracy.
      if ( ind != 0 && ind != 1 ) {
        if ( q2 == _q2s[ind-1] ) {
          last_val = q2;
          threshold = true;
          _solve(q2, t, y, allowed_relative/5, h/5, accuracy/5);
          grid.push_back(make_pair(ind, y));
          y = y * _decouple(y, t, numFlavorsQ2(_q2s[ind+1]), numFlavorsQ2(_q2s[ind-2]));
          // Define divergence after y > 2. -- we have no accuracy after that any way
          if ( y > 2. ) { low_lim = q2; }
          continue;
        }
      }
      // If q2 is lower than a value that already diverged, it will also diverge
      if ( q2 < low_lim ) {
        grid.push_back(make_pair(ind, std::numeric_limits<double>::max()));
        continue;
      // If last point was the same we don't need to recalculate
      } else if ( q2 == last_val ) {
        grid.push_back(make_pair(ind, y));
        continue;
      // Else calculate
      } else {
        last_val = q2;
        if ( threshold ) { _solve(q2, t, y, allowed_relative/5, h/5, accuracy/5); threshold = false; }
        else { _solve(q2, t, y, allowed_relative, h, accuracy); }
        grid.push_back(make_pair(ind, y));
        // Define divergence after y > 2. -- we have no accuracy after that any way
        if ( y > 2. ) { low_lim = q2; }
      }
    }

    if (_customref) {
      t = sqr(_mreference); // starting point
      y = _alphas_reference; // starting value
    } else {
      t = sqr(_mz); // starting point
      y = _alphas_mz; // starting value
    }

    for ( size_t ind = index_of_mz_lower + 1; ind < _q2s.size(); ++ind) {
      double q2 = _q2s[ind];
      // Deal with cases with two identical adjacent points (thresholds) by decreasing step size,
      // allowed errors, and accuracy.
      if ( ind != _q2s.size() - 1 && ind != _q2s.size() - 2 ) {
        if ( q2 == _q2s[ind+1] ) {
          last_val = q2;
          _solve(q2, t, y, allowed_relative/5, h/5, accuracy/5);
          grid.push_back(make_pair(ind, y));
          y = y * _decouple(y, t, numFlavorsQ2(_q2s[ind-1]), numFlavorsQ2(_q2s[ind+2]));
          // Define divergence after y > 2. -- we have no accuracy after that any way
          if ( y > 2. ) { low_lim = q2; }
          continue;
        }
      }
      // If q2 is lower than a value that already diverged, it will also diverge
      if ( q2 < low_lim ) {
        grid.push_back(make_pair(ind, std::numeric_limits<double>::max()));
        continue;
      // If last point was the same we don't need to recalculate
      } else if ( q2 == last_val ) {
        grid.push_back(make_pair(ind, y));
        continue;
      // Else calculate
      } else {
        last_val = q2;
        _solve(q2, t, y, allowed_relative, h, accuracy);
        grid.push_back(make_pair(ind, y));
        // Define divergence after y > 2. -- we have no accuracy after that any way
        if ( y > 2. ) { low_lim = q2; }
      }
    }

    std::sort(grid.begin(), grid.end(), [](const pair<int, double>& a, const pair<int, double>& b) { return a.first < b.first; });
    /// @todo auto lambda args need C++14: std::sort(grid.begin(), grid.end(), [](const auto& a, const auto& b) { return a.first < b.first; });

    vector<double> alphas;
    alphas.reserve(_q2s.size());

    for ( size_t x = 0; x < grid.size(); ++x ) {
      // cout << sqrt(_q2s.at(x)) << "       " << grid.at(x).second << endl;
       alphas.push_back(grid.at(x).second);
    }

    _ipol.setQ2Values(_q2s);
    _ipol.setAlphaSValues(alphas);

    _calculated = true;
  }


}
