// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Reweighting_H
#define LHAPDF_Reweighting_H

#include "LHAPDF/PDF.h"
#include "LHAPDF/PDFSet.h"

namespace LHAPDF {


  namespace {
    inline bool _checkAlphasQ2(double Q2, const PDF& pdfa, const PDF& pdfb, double aschk) {
      if (aschk < 0) return true;
      const double as_a = pdfa.alphasQ2(Q2);
      const double as_b = pdfb.alphasQ2(Q2);
      if (2 * std::abs(as_a - as_b) / (std::abs(as_a) + std::abs(as_b)) < aschk) return true;
      std::cerr << "WARNING: alpha_s(Q2) mismatch in PDF reweighting "
                << "at Q2 = " << Q2 << " GeV2:\n  "
                << as_a << " for " << pdfa.set().name() << "/" << pdfa.memberID() << " vs. "
                << as_b << " for " << pdfb.set().name() << "/" << pdfb.memberID()
                << std::endl;
      return false;
    }
  }


  /// @name Single beam reweighting functions
  //@{

  /// Get the PDF reweighting factor for a beam with id,x,Q parameters, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  inline double weightxQ2(int id, double x, double Q2, const PDF& basepdf, const PDF& newpdf, double aschk=5e-2) {
    if (aschk >= 0) _checkAlphasQ2(Q2, basepdf, newpdf, aschk);
    const double xf_base = basepdf.xfxQ2(id, x, Q2);
    const double xf_new = newpdf.xfxQ2(id, x, Q2);
    return xf_new / xf_base;
  }

  /// Get the PDF reweighting factor for a beam with id,x,Q parameters, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  template <typename PDFPTR>
  inline double weightxQ2(int id, double x, double Q2, const PDFPTR basepdf, const PDFPTR newpdf, double aschk=5e-2) {
    return weightxQ2(id, x, Q2, *basepdf, *newpdf, aschk);
  }

  /// Get the PDF reweighting factor for a beam with id,x,Q parameters, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  inline double weightxQ(int id, double x, double Q, const PDF& basepdf, const PDF& newpdf, double aschk=5e-2) {
    return weightxQ2(id, x, sqr(Q), basepdf, newpdf, aschk);
  }

  /// Get the PDF reweighting factor for a beam with id,x,Q parameters, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  template <typename PDFPTR>
  inline double weightxQ(int id, double x, double Q, const PDFPTR basepdf, const PDFPTR newpdf, double aschk=5e-2) {
    return weightxQ(id, x, Q, *basepdf, *newpdf, aschk);
  }

  //@}


  /// @name Two-beam reweighting functions
  //@{

  /// Get the PDF reweighting factor for two beams, one with id1,x1 and the other with id2,x2, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  inline double weightxxQ2(int id1, int id2, double x1, double x2, double Q2, const PDF& basepdf, const PDF& newpdf, double aschk=5e-2) {
    if (aschk >= 0) _checkAlphasQ2(Q2, basepdf, newpdf, aschk);
    const double w1 = weightxQ2(id1, x1, Q2, basepdf, newpdf, -1);
    const double w2 = weightxQ2(id2, x2, Q2, basepdf, newpdf, -1);
    return w1 * w2;
  }

  /// Get the PDF reweighting factor for two beams, one with id1,x1 and the other with id2,x2, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  template <typename PDFPTR>
  inline double weightxxQ2(int id1, int id2, double x1, double x2, double Q2, const PDFPTR basepdf, const PDFPTR newpdf, double aschk=5e-2) {
    return weightxxQ2(id1, id2, x1, x2, Q2, *basepdf, *newpdf, aschk);
  }

  /// Get the PDF reweighting factor for two beams, one with id1,x1 and the other with id2,x2, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  inline double weightxxQ(int id1, int id2, double x1, double x2, double Q, const PDF& basepdf, const PDF& newpdf, double aschk=5e-2) {
    return weightxxQ2(id1, id2, x1, x2, sqr(Q), basepdf, newpdf, aschk);
  }

  /// Get the PDF reweighting factor for two beams, one with id1,x1 and the other with id2,x2, from basepdf to newpdf
  /// @note For NLO calculations, in general different PDF values enter for each counterterm: be careful.
  template <typename PDFPTR>
  inline double weightxxQ(int id1, int id2, double x1, double x2, double Q, const PDFPTR basepdf, const PDFPTR newpdf, double aschk=5e-2) {
    return weightxxQ(id1, id2, x1, x2, Q, *basepdf, *newpdf, aschk);
  }

  //@}


}
#endif
