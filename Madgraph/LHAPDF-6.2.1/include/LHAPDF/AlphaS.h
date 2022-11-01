// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_AlphaS_H
#define LHAPDF_AlphaS_H

#include "LHAPDF/Utils.h"
#include "LHAPDF/Exceptions.h"
#include "LHAPDF/KnotArray.h"

namespace LHAPDF {

  /// @brief Calculator interface for computing alpha_s(Q2) in various ways
  ///
  /// The design of the AlphaS classes is that they are substitutible
  /// (cf. polymorphism) and are entirely non-dependent on the PDF and Info
  /// objects: hence they can be used by external code that actually doesn't
  /// want to do anything at all with PDFs, but which just wants to do some
  /// alpha_s interpolation.
  class AlphaS {
  public:

    /// Base class constructor for default param setup
    AlphaS();

    /// Destructor
    virtual ~AlphaS() {};

    /// @name alpha_s values
    //@{

    /// Calculate alphaS(Q)
    double alphasQ(double q) const { return alphasQ2(q*q); }

    /// Calculate alphaS(Q2)
    /// @todo Throw error in this base method if Q < Lambda?
    virtual double alphasQ2(double q2) const = 0;

    //@}


    /// @name alpha_s metadata
    //@{

    /// Calculate the number of active flavours at energy scale Q
    int numFlavorsQ(double q) const { return numFlavorsQ2(q*q); }

    /// Calculate the number of active flavours at energy scale Q2
    virtual int numFlavorsQ2(double q2) const;

    /// Get a quark mass by PDG code
    double quarkMass(int id) const;

    /// @brief Set quark masses by PDG code
    ///
    /// Used in the analytic and ODE solvers.
    void setQuarkMass(int id, double value);

    /// @brief Get a flavor scale threshold by PDG code
    ///
    /// Used in the analytic and ODE solvers.
    double quarkThreshold(int id) const;

    /// @brief Set a flavor threshold by PDG code (= quark masses by default)
    ///
    /// Used in the analytic and ODE solvers.
    void setQuarkThreshold(int id, double value);

    /// Get the order of QCD (expressed as number of loops)
    ///
    /// Used explicitly in the analytic and ODE solvers.
    int orderQCD() { return _qcdorder; }

    /// @brief Set the order of QCD (expressed as number of loops)
    ///
    /// Used in the analytic and ODE solvers.
    void setOrderQCD(int order) { _qcdorder = order; }

    /// @brief Set the Z mass used in this alpha_s
    ///
    /// Used in the ODE solver.
    void setMZ(double mz) { _mz = mz; }

    /// @brief Set the alpha_s(MZ) used in this alpha_s
    ///
    /// Used in the ODE solver.
    void setAlphaSMZ(double alphas) { _alphas_mz = alphas; }

    /// @brief Set the Z mass used in this alpha_s
    ///
    /// Used in the ODE solver.
    void setMassReference(double mref) { _mreference = mref; _customref = true; }

    /// @brief Set the alpha_s(MZ) used in this alpha_s
    ///
    /// Used in the ODE solver.
    void setAlphaSReference(double alphas) { _alphas_reference = alphas; _customref = true; }

    /// @brief Set the @a {i}th Lambda constant for @a i active flavors
    ///
    /// Used in the analytic solver.
    virtual void setLambda(unsigned int, double) {};

    //@}

    /// enum of flavor schemes
    enum FlavorScheme { FIXED, VARIABLE };

    /// Get the implementation type of this AlphaS
    virtual std::string type() const = 0;

    /// Set flavor scheme of alpha_s solver
    void setFlavorScheme(FlavorScheme scheme, int nf = -1);

    /// Get flavor scheme
    FlavorScheme flavorScheme() const { return _flavorscheme; }


  protected:

    /// @name Calculating beta function values
    //@{

    /// Calculate the i'th beta function given the number of active flavours
    /// Currently limited to 0 <= i <= 3
    /// Calculated using the MSbar scheme
    double _beta(int i, int nf) const;

    /// Calculate a vector of beta functions given the number of active flavours
    /// Currently returns a 4-element vector of beta0 -- beta3
    std::vector<double> _betas(int nf) const;

    //@}


  protected:

    /// Order of QCD evolution (expressed as number of loops)
    int _qcdorder;

    /// Mass of the Z boson in GeV
    double _mz;

    /// Value of alpha_s(MZ)
    double _alphas_mz;

    /// Reference mass in GeV
    double _mreference;

    /// Value of alpha_s(reference mass)
    double _alphas_reference;

    /// Decides whether to use custom reference values or fall back on MZ/AlphaS_MZ
    bool _customref;

    /// Masses of quarks in GeV
    /// Used for working out flavor thresholds and the number of quarks that are
    /// active at energy scale Q.
    std::map<int, double> _quarkmasses, _flavorthresholds;

    /// The flavor scheme in use
    FlavorScheme _flavorscheme;

    /// The allowed numbers of flavours in a fixed scheme
    int _fixflav;

  };



  /// Calculate alpha_s(Q2) by an analytic approximation
  class AlphaS_Analytic : public AlphaS {
  public:

    /// Implementation type of this solver
    std::string type() const { return "analytic"; }

    /// Calculate alphaS(Q2)
    double alphasQ2(double q2) const;

    /// Analytic has its own numFlavorsQ2 which respects the min/max nf set by the Lambdas
    int numFlavorsQ2(double q2) const;

    /// Set lambda_i (for i = flavour number)
    void setLambda(unsigned int i, double lambda);


  private:

    /// Get lambdaQCD for nf
    double _lambdaQCD(int nf) const;

    /// Recalculate min/max flavors in case lambdas have changed
    void _setFlavors();


    /// LambdaQCD values.
    std::map<int, double> _lambdas;

    /// Max number of flavors
    int _nfmax;
    /// Min number of flavors
    int _nfmin;

  };



  /// Interpolate alpha_s from tabulated points in Q2 via metadata
  ///
  /// @todo Extrapolation: log-gradient xpol at low Q, const at high Q?
  class AlphaS_Ipol : public AlphaS {
  public:

    /// Implementation type of this solver
    std::string type() const { return "ipol"; }

    /// Calculate alphaS(Q2)
    double alphasQ2(double q2) const;

    /// Set the array of Q values for interpolation
    ///
    /// Writes to the same internal arrays as setQ2Values, appropriately transformed.
    void setQValues(const std::vector<double>& qs);

    /// Set the array of Q2 values for interpolation
    ///
    /// Subgrids are represented by repeating the values which are the end of
    /// one subgrid and the start of the next. The supplied vector must match
    /// the layout of alpha_s values.
    void setQ2Values(const std::vector<double>& q2s) { _q2s = q2s; }

    /// Set the array of alpha_s(Q2) values for interpolation
    ///
    /// The supplied vector must match the layout of Q2 knots.  Subgrids may
    /// have discontinuities, i.e. different alpha_s values on either side of a
    /// subgrid boundary (for the same Q values).
    void setAlphaSValues(const std::vector<double>& as) { _as = as; }


  private:

    /// Standard cubic interpolation formula
    double _interpolateCubic(double T, double VL, double VDL, double VH, double VDH) const;
    /// Get the gradient for a patch in the middle of the grid
    double _ddq_central( size_t i ) const;
    /// Get the gradient for a patch at the low end of the grid
    double _ddq_forward( size_t i ) const;
    /// Get the gradient for a patch at the high end of the grid
    double _ddq_backward( size_t i ) const;

    /// Synchronise the contents of the single Q2 / alpha_s vectors into subgrid objects
    /// @note This is const so it can be called silently from a const method
    void _setup_grids() const;


    /// Map of AlphaSArrays "binned" for lookup by low edge in (log)Q2
    /// @note This is mutable so it can be initialized silently from a const method
    mutable std::map<double, AlphaSArray> _knotarrays;

    /// Array of ipol knots in Q2
    std::vector<double> _q2s;
    /// Array of alpha_s values for the Q2 knots
    std::vector<double> _as;

  };



  /// Solve the differential equation in alphaS using an implementation of RK4
  class AlphaS_ODE : public AlphaS {
  public:

    /// Implementation type of this solver
    std::string type() const { return "ode"; }

    /// Calculate alphaS(Q2)
    double alphasQ2( double q2 ) const;

    /// Set MZ, and also the caching flag
    void setMZ( double mz ) { _mz = mz; _calculated = false; }

    /// Set alpha_s(MZ), and also the caching flag
    void setAlphaSMZ( double alphas ) { _alphas_mz = alphas; _calculated = false; }

    /// Set reference mass, and also the caching flag
    void setMassReference( double mref ) { _mreference = mref; _calculated = false; _customref = true; }

    /// Set alpha_s(MZ), and also the caching flag
    void setAlphaSReference( double alphas ) { _alphas_reference = alphas; _calculated = false; _customref = true; }

    /// Set the array of Q values for interpolation, and also the caching flag
    void setQValues(const std::vector<double>& qs);

    /// @brief Set the array of Q2 values for interpolation, and also the caching flag
    ///
    /// Writes to the same internal array as setQValues, appropriately transformed.
    void setQ2Values( std::vector<double> q2s ) { _q2s = q2s; _calculated = false; }


  private:

    /// Calculate the derivative at Q2 = t, alpha_S = y
    double _derivative(double t, double y, const std::vector<double>& beta) const;

    /// Calculate the decoupling relation when going from num. flav. = ni -> nf
    /// abs(ni - nf) must be = 1
    double _decouple(double y, double t, unsigned int ni, unsigned int nf) const;

    /// Calculate the next step using RK4 with adaptive step size
    void _rk4(double& t, double& y, double h, const double allowed_change, const vector<double>& bs) const;

    /// Solve alpha_s for q2 using RK4
    void _solve(double q2, double& t, double& y, const double& allowed_relative, double h, double accuracy) const;

    /// Create interpolation grid
    void _interpolate() const;


    /// Vector of Q2s in case specific anchor points are used
    mutable std::vector<double> _q2s;

    /// Whether or not the ODE has been solved yet
    mutable bool _calculated;

    /// The interpolation used to get Alpha_s after the ODE has been solved
    mutable AlphaS_Ipol _ipol;

  };


}
#endif
