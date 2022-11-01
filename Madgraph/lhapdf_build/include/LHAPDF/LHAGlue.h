// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_LHAGlue_H
#define LHAPDF_LHAGlue_H

/// @file LHAGlue.h
/// A file that provides backwards compatibility for some C functions from LHAPDF 5.x

#include "LHAPDF/Version.h"
#if LHAPDF_LHA5CXX

/// A special C++ function to return the PDF name + code currently being used via LHAGlue.
std::string lhaglue_get_current_pdf(int nset=1);

// Compatibility preprocessor-based aliasing of deprecated "M" function names
#define initPDFSetM initPDFSet
#define initPDFSetByNameM initPDFSetByName
#define initPDFM initPDF
#define initPDFByNameM initPDFByName
#define getDescriptionM getDescription
#define xfxM xfx
#define xfxpM xfxp
#define xfxaM xfxa
#define xfxphotonM xfxphoton
#define numberPDFM numberPDF
#define alphasPDFM alphasPDF
#define getOrderPDFM getOrderPDF
#define getOrderAlphaSM getOrderAlphaS
#define getQMassM getQMass
#define getThresholdM getThreshold
#define getNfM getNf
#define getLam4M getLam4
#define getLam5M getLam5
#define getXminM getXmin
#define getXmaxM getXmax
#define getQ2minM getQ2min
#define getQ2maxM getQ2max

namespace LHAPDF {


  /// @brief Only Provided for LHAPDF5 compatibility. Distinction between evolution
  /// or interpolation PDF sets.
  /// Enum to choose whether evolution (i.e. @c LHpdf data file) or
  /// interpolation (i.e. @c LHgrid data file) is used.
  /// This distinction ismeaningless in LHAPDF6 interpolation is always used.
  enum SetType {
    EVOLVE = 0, LHPDF = 0,
    INTERPOLATE = 1, LHGRID = 1
  };

  /// Level of noisiness.
  enum Verbosity { SILENT=0, LOWKEY=1, DEFAULT=2 };

  /// Get LHAPDF version string (prefer LHAPDF::version())
  inline std::string getVersion() {
    return version();
  }

  /// Get max allowed number of concurrent sets (there is no limit anymore)
  inline int getMaxNumSets() { return 1000; }

  /// Global initialisation (there is none)
  inline void initLHAPDF() {}

  /// Extrapolate beyond grid edges (not an option at present)
  /// @todo Use this to set the default extrapolator when there is a physical extrapolation option
  // This form commented due to unused variable warnings, until this can actually have an effect
  // inline void extrapolate(bool extrapolate=true) {}
  inline void extrapolate(bool) {}
  inline void extrapolate() {}

  /// Choose level of noisiness.
  void setVerbosity(Verbosity noiselevel);

  /// Set a steering parameter (does nothing!)
  inline void setParameter(const std::string&) {
    std::cerr << "LHAPDF::setParameter() has no effect in LHAPDF6: "
              << "please update your code to use the native C++ interface" << std::endl;
  }

  /// Check if the PDF includes a photon member
  bool hasPhoton();

  /// Prepends path to path list
  void setPDFPath(const string& path);
  std::string pdfsetsPath();


  /// The PDF set by filename, see subdir @c PDFsets of LHAPDF for choices.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void initPDFSetByName(const std::string& filename);
  void initPDFSetByName(const std::string& filename, SetType type);

  /// The PDF set by filename, see subdir @c PDFsets of LHAPDF for choices.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void initPDFSetByName(int nset, const std::string& filename);
  void initPDFSetByName(int nset, const std::string& filename, SetType type);


  /// Number of members available in the current set.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int numberPDF();

  /// Number of members available in the current set.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int numberPDF(int nset);

  /// The choice of PDF member out of one distribution.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void initPDF(int memset);

  /// The choice of PDF member out of one distribution.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void initPDF(int nset, int memset);


  /// Nucleon PDF: returns \f$ x f(x, Q) \f$ for flavour @a fl - flavour encoding as in the LHAPDF manual.
  /// @arg -6..-1 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 0 = \f$ g \f$
  /// @arg 1..6 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double xfx(double x, double Q, int fl);

  /// Nucleon PDF: returns @c x f(x, Q) for flavour @a fl - flavour encoding as in the LHAPDF manual.
  /// @arg -6..-1 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 0 = \f$ g \f$
  /// @arg 1..6 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double xfx(int nset, double x, double Q, int fl);

  /// Nucleon PDF: fills primitive 13 element array pointed at by @a results with
  /// \f$ x f(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void xfx(double x, double Q, double* results);

  /// Nucleon PDF: fills primitive 13 element array pointed at by @a results with
  /// \f$ x f(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void xfx(int nset, double x, double Q, double* results);

  /// Nucleon PDF: returns a vector \f$ x f_i(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  std::vector<double> xfx(double x, double Q);

  /// Nucleon PDF: returns a vector @c x f_i(x, Q) with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  std::vector<double> xfx(int nset, double x, double Q);


  /// MRST QED PDF: returns a vector \f$ x f_i(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$;
  /// @arg 13 = \f$ \gamma \f$.
  ///
  /// NB. Note extra element in this set for MRST photon.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  std::vector<double> xfxphoton(double x, double Q);

  /// MRST QED PDF: returns a vector \f$ x f_i(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$;
  /// @arg 13 = \f$ \gamma \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  std::vector<double> xfxphoton(int nset, double x, double Q);

  /// MRST QED PDF: fills primitive 14 element array pointed at by @a results with
  /// \f$ x f(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @arg 13 = \f$ \gamma \f$.
  ///
  /// NB. Note extra element in this set for MRST photon.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void xfxphoton(double x, double Q, double* results);

  /// MRST QED PDF: fills primitive 14 element array pointed at by @a results with
  /// \f$ x f(x, Q) \f$ with index \f$ 0 < i < 12 \f$.
  /// @arg 0..5 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 6 = \f$ g \f$;
  /// @arg 7..12 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$.
  /// @arg 13 = \f$ \gamma \f$.
  ///
  /// NB. Note extra element in this set for MRST photon.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void xfxphoton(int nset, double x, double Q, double* results);

  /// MRST QED PDF: returns \f$ x f(x, Q) \f$ for flavour @a fl - this time the flavour encoding
  /// is as in the LHAPDF manual.
  /// @arg -6..-1 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 0 = \f$ g \f$
  /// @arg 1..6 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$;
  /// @arg 7 = \f$ \gamma \f$.
  ///
  /// NB. Note extra element in this set for MRST photon.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double xfxphoton(double x, double Q, int fl);

  /// MRST QED PDF: returns \f$ x f(x, Q) \f$ for flavour @a fl - this time the flavour encoding
  /// is as in the LHAPDF manual.
  /// @arg -6..-1 = \f$ \bar{t} \f$, ..., \f$ \bar{u} \f$, \f$ \bar{d} \f$;
  /// @arg 0 = \f$ g \f$
  /// @arg 1..6 = \f$ d \f$, \f$ u \f$, ..., \f$ t \f$;
  /// @arg 7 = \f$ \gamma \f$.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double xfxphoton(int nset, double x, double Q, int fl);


  /// Print PDF description to stdout
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void getDescription();

  /// Print PDF description to stdout
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void getDescription(int nset);


  /// Order of \f$ \alpha_\mathrm{s} \f$ used by the current PDF.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int getOrderAlphaS();

  /// Order of \f$ \alpha_\mathrm{s} \f$ used by the current PDF.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int getOrderAlphaS(int nset);


  /// Order of QCD used by the current PDF.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int getOrderPDF();

  /// Order of QCD used by the current PDF.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int getOrderPDF(int nset);


  /// Number of flavours used in current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int getNf(int nset);

  /// Number of flavours used in current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  int getNf();


  /// 4-flavour LambdaQCD used in current PDF, if available else -1.0
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getLam4(int nset);

  /// 4-flavour LambdaQCD used in current PDF, if available else -1.0
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getLam4(int nset, int nmem);


  /// 5-flavour LambdaQCD used in current PDF, if available else -1.0
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getLam5(int nset);

  /// 5-flavour LambdaQCD used in current PDF, if available else -1.0
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getLam5(int nset, int nmem);


  /// Minimum X for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getXmin(int nmem);

  /// Minimum X for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 -instead!
  double getXmin(int nset, int nmem);

  /// Maximum X for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getXmax(int nset, int nmem);

  /// Maximum X for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getXmax(int nmem);


  /// Minimum Q2 for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getQ2min(int nset, int nmem);

  /// Minimum Q2 for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getQ2min(int nmem);

  /// Maximum Q2 for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getQ2max(int nset, int nmem);

  /// Maximum Q2 for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getQ2max(int nmem);


  /// Mass of quarks for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getQMass(int nset, int nf);

  /// Mass of quarks for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getQMass(int nf);


  /// Mass of quarks for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getThreshold(int nset, int nf);

  /// Mass of quarks for current PDF
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double getThreshold(int nf);


  /// \f$ \alpha_\mathrm{s} \f$ used by the current PDF.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double alphasPDF(double Q);

  /// \f$ \alpha_\mathrm{s} \f$ used by the current PDF.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  double alphasPDF(int nset, double Q);

  /// @brief Use @a member in current PDF set.
  /// This operation is computationally cheap.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void usePDFMember(int member);

  /// @brief Use @a member in PDF set @a nset (multi-set version).
  /// This operation is computationally cheap.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void usePDFMember(int nset, int member);

  /// Initialise @a member in PDF set @a setid.
  /// @deprecated Use the proper C++ interface of LHAPDF6 instead!
  void initPDFSet(const std::string& name, int member=0);
  void initPDFSet(int nset ,const std::string& name, int nmem=0);
  void initPDFSet(int setid, int member=0);
  void initPDFSet(int nset , int setid, int nmem=0);
  /// Initialise @a member in PDF set @a name, of type @a type. - LHAPDF5 compatibility
  void initPDFSet(const std::string& name, SetType type, int member=0);
  /// Initialise @a member in PDF set @a name, of type @a type (multi-set version) - LHAPDF5 compatibility
  void initPDFSet(int nset, const std::string& name, SetType type, int member=0);

}

#endif
#endif
