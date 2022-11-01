// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Factories_H
#define LHAPDF_Factories_H

#include <string>

namespace LHAPDF {


  // Forward declarations to avoid circular dependencies
  class PDF;
  class Info;
  class PDFSet;
  class PDFInfo;
  class Config;
  class Interpolator;
  class Extrapolator;
  class AlphaS;


  /// @name Factory functions for various Info objects
  //@{

  /// Get the global configuration object
  ///
  /// The global config is populated by reading from lhapdf.conf if it is found
  /// in the search paths. It is a singleton, hence the 'get' rather than 'mk'
  /// function name.
  ///
  /// @note The LHAPDF system is responsible for deletion of the returned
  /// object. Do NOT delete it yourself! Hence the return by reference rather
  /// than pointer.
  // Config& getConfig();
  Info& getConfig();


  /// Get the PDFSet with the given set name.
  ///
  /// Returns a PDFSet by reference. When this function is used for
  /// access, only one PDFSet object is made per set name... hence the
  /// 'get' rather than 'mk' function name.
  ///
  /// This function is intended particularly for use where it would be
  /// inefficient to have to repeatedly construct a PDFSet by name. The
  /// canonical use case is internal: the Info system uses this to ensure that
  /// cascading of config settings is efficient, and also allows the automatic
  /// application of set-level changes to all PDF member objects in that set.
  ///
  /// @note The LHAPDF system is responsible for deletion of the returned
  /// object. Do NOT delete it yourself! Hence the return by reference rather
  /// than pointer.
  PDFSet& getPDFSet(const std::string& setname);


  /// Create a new Info object for the given set name and member number.
  ///
  /// Returns a 'new'ed Info by pointer.
  /// The caller is responsible for deletion of the created object.
  PDFInfo* mkPDFInfo(const std::string& setname, int member);

  /// Create a new Info object with the given LHAPDF ID code.
  ///
  /// Returns a 'new'ed Info by pointer.
  /// The caller is responsible for deletion of the created object.
  PDFInfo* mkPDFInfo(int lhaid);

  //@}


  /// @name Factory functions for making single PDF members
  //@{

  /// Create a new PDF with the given PDF set name and member ID.
  ///
  /// Returns a 'new'ed PDF by pointer.
  /// The caller is responsible for deletion of the created object.
  PDF* mkPDF(const std::string& setname, int member);

  /// Create a new PDF with the given LHAPDF ID code.
  ///
  /// Returns a 'new'ed PDF by pointer.
  /// The caller is responsible for deletion of the created object.
  PDF* mkPDF(int lhaid);

  /// Create a new PDF with the given PDF set name and member ID as a single string.
  ///
  /// The format of the @a setname_nmem string is <setname>/<nmem>
  /// where <nmem> must be parseable as a positive integer. The /
  /// character is not permitted in set names due to clashes with
  /// Unix filesystem path syntax.
  ///
  /// If no /<nmem> is given, member number 0 will be used.
  ///
  /// Returns a 'new'ed PDF by pointer.
  /// The caller is responsible for deletion of the created object.
  PDF* mkPDF(const std::string& setname_nmem);

  //@}


  /// @name Factory functions for making all PDF members in a set
  //@{

  /// Get all PDFs in a named set (return by filling the supplied vector).
  void mkPDFs(const std::string& setname, std::vector<PDF*>& pdfs);

  /// Get all PDFs in a named set (return by a new vector).
  std::vector<PDF*> mkPDFs(const std::string& setname);

  /// Get all PDFs in a named set (return by filling the supplied vector).
  ///
  /// This is a templated version for returning a vector of smart ptrs
  template <typename PTR>
  void mkPDFs(const std::string& setname, std::vector<PTR>& pdfs) {
    std::vector<PDF*> rawptrs;
    mkPDFs(setname, rawptrs);
    pdfs.clear();
    pdfs.reserve(rawptrs.size());
    // for (const PDF* p : rawptrs) pdfs.push_back(PTR(p)); //< Reinstate when C++11 is guaranteed, without flags
    for (size_t i = 0; i < rawptrs.size(); ++i) pdfs.push_back(PTR(rawptrs[i]));
  }

  //@}


  /// @name Factory functions for making grid interpolators/extrapolators
  //@{

  /// Interpolator factory
  ///
  /// Returns a 'new'ed Interpolator by pointer. Unless passed to a GridPDF,
  /// the caller is responsible for deletion of the created object.
  Interpolator* mkInterpolator(const std::string& name);


  /// Extrapolator factory
  ///
  /// Returns a 'new'ed Extrapolator by pointer. Unless passed to a GridPDF,
  /// the caller is responsible for deletion of the created object.
  Extrapolator* mkExtrapolator(const std::string& name);


  /// @name Factory functions for making AlphaS objects
  //@{

  /// @brief Make an AlphaS object from an Info object
  ///
  /// The type and configuration of the returned AlphaS is chosen based on the
  /// PDF metadata Info object given as the argument.
  ///
  /// Returns a 'new'ed AlphaS by pointer. Unless attached to a PDF,
  /// the caller is responsible for deletion of the created object.
  AlphaS* mkAlphaS(const Info& info);

  /// @brief Make an AlphaS object for the named PDF set
  ///
  /// The type and configuration of the returned AlphaS is chosen based on the
  /// named PDFSet's metadata.
  ///
  /// Returns a 'new'ed AlphaS by pointer. Unless attached to a PDF,
  /// the caller is responsible for deletion of the created object.
  AlphaS* mkAlphaS(const std::string& setname);

  /// @brief Make an AlphaS object for the specified PDF
  ///
  /// The type and configuration of the returned AlphaS is chosen based on the
  /// named PDFSet's nth member's metadata.
  ///
  /// Returns a 'new'ed AlphaS by pointer. Unless attached to a PDF,
  /// the caller is responsible for deletion of the created object.
  AlphaS* mkAlphaS(const std::string& setname, int member);

  /// @brief Make an AlphaS object for the specified PDF
  ///
  /// The type and configuration of the returned AlphaS is chosen based on the
  /// numbered PDF's metadata.
  ///
  /// Returns a 'new'ed AlphaS by pointer. Unless attached to a PDF,
  /// the caller is responsible for deletion of the created object.
  AlphaS* mkAlphaS(int lhaid);

  /// @brief Make an AlphaS object of the requested type without a PDF reference
  ///
  /// No values are initialised and have to be configured by the caller.
  ///
  /// The caller is responsible for deletion of the created object.
  ///
  /// @todo Actually, should we just make this mkAlphaS(0)?
  AlphaS* mkBareAlphaS(const std::string& type);

  //@}


}
#endif
