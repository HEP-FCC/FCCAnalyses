// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Interpolator_H
#define LHAPDF_Interpolator_H

#include "LHAPDF/Utils.h"
#include "LHAPDF/KnotArray.h"

namespace LHAPDF {


  // Forward declaration
  class GridPDF;


  /// The general interface for interpolating between grid points
  class Interpolator {
  public:

    /// Destructor to allow inheritance
    virtual ~Interpolator() { }


    /// @name Binding to a PDF object
    //@{

    /// Bind to a GridPDF
    void bind(const GridPDF* pdf) { _pdf = pdf; }

    /// Unbind from GridPDF
    void unbind() { _pdf = 0; }

    /// Identify whether this Interpolator has an associated PDF
    bool hasPDF() { return _pdf != 0; }

    /// Get the associated GridPDF
    const GridPDF& pdf() const { return *_pdf; }

    //@}


    /// @name Interpolation methods
    //@{

    /// Interpolate a single-point in (x,Q)
    double interpolateXQ(int id, double x, double q) const {
      return interpolateXQ2(id, x, q*q);
    }

    /// Interpolate a single-point in (x,Q2)
    double interpolateXQ2(int id, double x, double q2) const;


    /// @todo Make an all-PID version of interpolateQ and Q2?


  protected:

    /// @brief Interpolate a single-point in (x,Q2), given x/Q2 values and subgrid indices.
    ///
    /// The key function to be overridden in derived classes: the subgrid and
    /// x/Q2 index lookup (and their caching) are done centrally in the
    /// Interpolator base class so do not need to be re-implemented in each
    /// flavour of interpolator.
    virtual double _interpolateXQ2(const KnotArray1F& subgrid, double x, size_t ix, double q2, size_t iq2) const = 0;

    /// @todo Implement this NF version, with a cached KnotArrayNF?
    // virtual double _interpolateXQ2(const KnotArrayNF& subgrid, int id, double x, size_t ix, double q2, size_t iq2) const;

    //@}


  private:

    const GridPDF* _pdf;

  };


}

#endif
