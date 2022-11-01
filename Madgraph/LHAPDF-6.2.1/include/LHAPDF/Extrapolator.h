// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Extrapolator_H
#define LHAPDF_Extrapolator_H

#include "LHAPDF/Utils.h"

namespace LHAPDF {


  // Forward declaration
  class GridPDF;


  /// The general interface for extrapolating beyond grid boundaries
  class Extrapolator {
  public:

    /// Destructor to allow inheritance
    virtual ~Extrapolator() { }


    /// @name Binding to a PDF object
    //@{

    /// Bind to a GridPDF
    void bind(const GridPDF* pdf) { _pdf = pdf; }

    /// Unbind from GridPDF
    void unbind() { _pdf = 0; }

    /// Identify whether this Extrapolator has an associated PDF
    bool hasPDF() { return _pdf != 0; }

    /// Get the associated GridPDF
    const GridPDF& pdf() const { return *_pdf; }

    //@}


    /// @name Extrapolation methods
    //@{

    /// Extrapolate a single-point in (x,Q)
    ///
    /// @param id PDG parton ID
    /// @param x Momentum fraction
    /// @param q Energy scale
    /// @return The xf value at (x,q2)
    double extrapolateXQ(int id, double x, double q) const {
      return extrapolateXQ2(id, x, q*q );
    }

    /// Extrapolate a single-point in (x,Q2)
    ///
    /// @param id PDG parton ID
    /// @param x Momentum fraction
    /// @param q2 Squared energy scale
    /// @return The xf value at (x,q2)
    virtual double extrapolateXQ2(int id, double x, double q2) const = 0;


    /// @todo Make an all-PID version of extrapolateQ and Q2?

    //@}


  private:

    const GridPDF* _pdf;

  };


}
#endif
