// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/AlphaS.h"
#include "LHAPDF/Utils.h"

namespace LHAPDF {


  // Base class constructor for default param setup
  AlphaS::AlphaS() {
    _qcdorder = 5;
    _mz = 91.1876;
    _alphas_mz = 0.118;
    _flavorscheme = VARIABLE;
    _fixflav = -1;
    _customref = false;
  }


  // Calculate the number of active quark flavours at energy scale Q2
  int AlphaS::numFlavorsQ2(double q2) const {
    if ( _flavorscheme == FIXED ) return _fixflav;
    int nf = 0;
    /// Use quark masses if flavour threshold not set explicitly
    if ( _flavorthresholds.empty() ) {
      for (int it = 1; it <= 6; ++it) {
        std::map<int, double>::const_iterator element = _quarkmasses.find(it);
        if ( element == _quarkmasses.end() ) continue;
        if ( sqr(element->second) < q2 ) nf = it;
      }
    } else {
      for (int it = 1; it <= 6; ++it) {
        std::map<int, double>::const_iterator element = _flavorthresholds.find(it);
        if ( element == _flavorthresholds.end() ) continue;
        if ( sqr(element->second) < q2 ) nf = it;
      }
    }
    if ( _fixflav != -1 && nf > _fixflav ) nf = _fixflav;
    return nf;
  }


  // Calculate a beta function given the number of active flavours
  double AlphaS::_beta(int i, int nf) const {
    if (i == 0) return (double) 0.875352187 - 0.053051647*nf; //(33 - 2*nf)/(12*M_PI)
    if (i == 1) return (double) 0.6459225457 - 0.0802126037*nf; //(153 - 19*nf)/(24*sqr(M_PI))
    if (i == 2) return (double) 0.719864327 - 0.140904490*nf + 0.00303291339*nf*nf; //(2857 - (5033 / 9.0)*nf + (325 / 27.0)*sqr(nf))/(128*sqr(M_PI)*M_PI)
    if (i == 3) return (double) 1.172686 - 0.2785458*nf + 0.01624467*nf*nf + 0.0000601247*nf*nf*nf;
    // ( (149753/6.) + 3564*ZETA_3 - ((1078361/162.) + (6502/27.)*ZETA_3)*nf +
    // ((50065/162.) + (6472/81.)*ZETA_3)*sqr(nf) + (1093/729.)*sqr(nf)*nf)/(256*sqr(M_PI)*sqr(M_PI))
    if (i == 4) return (double) 1.714138 - 0.5940794*nf + 0.05607482*nf*nf - 0.0007380571*nf*nf*nf - 0.00000587968*nf*nf*nf*nf;
    // ... if you want the analytic form just look them up in hep-ph/1606.08659


    throw Exception("Invalid index " + to_str(i) + " for requested beta function");
  }


  // Calculate beta functions given the number of active flavours
  vector<double> AlphaS::_betas(int nf) const {
    vector<double> rtn; rtn.reserve(4);
    for (int i = 0; i < 5; ++i) rtn.push_back(_beta(i, nf));
    return rtn;
  }

  // Set a quark mass, explicitly giving its ID
  void AlphaS::setQuarkMass(int id, double value) {
    if (abs(id) > 6 || id == 0)
      throw Exception("Invalid ID " + to_str(id) + " for quark given (should be 1-6).");
    _quarkmasses[abs(id)] = value;
  }

    // Set a flavour threshold, explicitly giving its ID
  void AlphaS::setQuarkThreshold(int id, double value) {
    if (abs(id) > 6 || id == 0)
      throw Exception("Invalid ID " + to_str(id) + " for flavour threshold given (should be 1-6).");
    _flavorthresholds[abs(id)] = value;
  }

  // Get a quark mass by ID
  double AlphaS::quarkMass(int id) const {
    std::map<int, double>::const_iterator quark = _quarkmasses.find(abs(id));
    if ( quark == _quarkmasses.end() )
       throw Exception("Quark mass " + to_str(id) + " not set!");
    return quark->second;
  }

    // Get a quark mass by ID
  double AlphaS::quarkThreshold(int id) const {
    std::map<int, double>::const_iterator threshold = _flavorthresholds.find(abs(id));
    if ( threshold == _flavorthresholds.end() )
       throw Exception("Flavour threshold " + to_str(id) + " not set!");
    return threshold->second;
  }

  void AlphaS::setFlavorScheme(FlavorScheme scheme, int nf) {
    if( scheme == FIXED && nf == -1 ) throw Exception("You need to define the number of flavors when using a fixed scheme!");
    _flavorscheme = scheme;
    _fixflav = nf;
  }

}
