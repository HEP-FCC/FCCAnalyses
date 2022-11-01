// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/AlphaS.h"
#include "LHAPDF/Utils.h"

namespace LHAPDF {

  // Calculate the number of active quark flavours at energy scale Q2.
  // Respects min/max nf
  /// Currently returns the active number of flavors,
  /// not the number actually used for lambdaQCD
  /// (in case only lambda3 and lambda5 are defined and
  /// we are in the 4 flavour range, we use lambda3 but this returns 4)
  /// @todo Is this the "correct" behaviour?
  int AlphaS_Analytic::numFlavorsQ2(double q2) const {
    if ( _flavorscheme == FIXED ) return _fixflav;
    int nf = _nfmin;
    /// Use quark masses if flavour threshold not set explicitly
    if ( _flavorthresholds.empty() ) {
      for ( int it = _nfmin; it <= _nfmax; ++it ) {
        std::map<int, double>::const_iterator element = _quarkmasses.find(it);
        if ( element == _quarkmasses.end() ) continue;
        if ( sqr(element->second) < q2 ) nf = it;
      }
    } else {
      for ( int it = _nfmin; it <= _nfmax; ++it ) {
        std::map<int, double>::const_iterator element = _flavorthresholds.find(it);
        if ( element == _flavorthresholds.end() ) continue;
        if ( sqr(element->second) < q2 ) nf = it;
      }
    }
    if ( _fixflav != -1 && nf > _fixflav ) nf = _fixflav;
    return nf;
  }

  // Set lambda_i && recalculate nfmax and nfmin
  void AlphaS_Analytic::setLambda(unsigned int i, double lambda) {
    _lambdas[i] = lambda;
    _setFlavors();
  }

  // Recalculate nfmax and nfmin after a new lambda has been set
  void AlphaS_Analytic::_setFlavors() {
    for (int it = 0; it <= 6; ++it) {
      std::map<int, double>::iterator element = _lambdas.find(it);
      if ( element == _lambdas.end() ) continue;
      _nfmin = it;
      break;
    }
    for (int it = 6; it >= 0; --it) {
      std::map<int, double>::iterator element = _lambdas.find(it);
      if ( element == _lambdas.end() ) continue;
      _nfmax = it;
      break;
    }
  }

  // Return the correct lambda for a given number of active flavours
  // Uses recursion to find the closest defined-but-lower lambda for the given
  // number of active flavours
  // If a fixed flavor scheme is used, require the correct lambda to be set
  double AlphaS_Analytic::_lambdaQCD(int nf) const {
    if ( _flavorscheme == FIXED ) {
      std::map<int, double>::const_iterator lambda = _lambdas.find(_fixflav);
      if ( lambda == _lambdas.end() ) throw Exception("Set lambda(" + to_str(_fixflav) + ") when using a fixed " + to_str(_fixflav) + " flavor scheme.");
      return lambda->second;
    } else {
      if ( nf < 0 ) throw Exception("Requested lambdaQCD for " + to_str(nf) + " number of flavours.");
      std::map<int, double>::const_iterator lambda = _lambdas.find(nf);
      if ( lambda == _lambdas.end() ) return _lambdaQCD(nf-1);
      return lambda->second;
    }
  }


  // Calculate alpha_s(Q2) by an analytic approximation
  double AlphaS_Analytic::alphasQ2(double q2) const {
    /// Get the number of active flavours and corresponding LambdaQCD
    /// Should support any number of active flavors as long as the
    /// corresponding lambas are set
    if ( _lambdas.empty() ) throw Exception("You need to set at least one lambda value to calculate alpha_s by analytic means!");
    const int nf = this->numFlavorsQ2(q2);
    const double lambdaQCD = _lambdaQCD(nf);

    if (q2 <= lambdaQCD * lambdaQCD) return std::numeric_limits<double>::max();

    // Get beta coeffs for the number of active (above threshold) quark flavours at energy Q
    const std::vector<double> beta = _betas(nf);
    const double beta02 = sqr(beta[0]);
    const double beta12 = sqr(beta[1]);

    // Pre-calculate ln(Q2/lambdaQCD) and expansion term y = 1/ln(Q2/lambdaQCD)
    const double x = q2 / (lambdaQCD*lambdaQCD);
    const double lnx = log(x);
    const double lnlnx = log(lnx);
    const double lnlnx2 = lnlnx * lnlnx;
    const double lnlnx3 = lnlnx * lnlnx * lnlnx;
    const double y = 1 / lnx;

    // Calculate terms up to qcdorder = 4
    // A bit messy because the actual expressions are
    // quite messy...
    /// @todo Is it okay to use _alphas_mz as the constant value?
    if(_qcdorder == 0) return _alphas_mz;
    const double A = 1 / beta[0];
    const double a_0 = 1;
    double tmp = a_0;
    if (_qcdorder > 1) {
      const double a_1 = beta[1] * lnlnx / beta02;
      tmp -= a_1 * y;
    }
    if (_qcdorder > 2) {
      const double B = beta12 / (beta02 * beta02);
      const double a_20 = lnlnx2 - lnlnx;
      const double a_21 = beta[2] * beta[0] / beta12;
      const double a_22 = 1;
      tmp += B * y*y * (a_20 + a_21 - a_22);
    }
    if (_qcdorder > 3) {
      const double C = 1. / (beta02 * beta02 * beta02);
      const double a_30 = (beta12 * beta[1]) * (lnlnx3 - (5/2.) * lnlnx2 - 2 * lnlnx + 0.5);
      const double a_31 = 3 * beta[0] * beta[1] * beta[2] * lnlnx;
      const double a_32 = 0.5 * beta02 * beta[3];
      tmp -= C * y*y*y * (a_30 + a_31 - a_32);
    }
    const double alphaS = A * y * tmp;
    return alphaS;
  }


}
