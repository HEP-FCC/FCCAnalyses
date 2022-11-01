// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_PDFInfo_H
#define LHAPDF_PDFInfo_H

#include "LHAPDF/Info.h"
#include "LHAPDF/Factories.h"
#include "LHAPDF/PDFIndex.h"

namespace LHAPDF {


  /// Metadata class for PDF members
  class PDFInfo : public Info {
  public:

    /// @name Creation and deletion
    //@{

    /// Default constructor (for container compatibility)
    ///
    /// @note Don't use explicitly!
    ///
    /// @todo Remove?
    PDFInfo() { }

    /// Constructor from a PDF member's data path.
    ///
    /// @todo Bypasses standard path searching hence used by the path-based
    /// GridPDF constructor, for example.
    PDFInfo(const std::string& mempath);

    /// Constructor from a set name and member ID.
    PDFInfo(const std::string& setname, int member);

    /// Constructor from an LHAPDF ID code.
    PDFInfo(int lhaid);

    //@}


    /// @name Metadata accessors
    //@{

    /// Can this Info object return a value for the given key? (it may be defined non-locally)
    bool has_key(const std::string& key) const;

    /// Retrieve a metadata string by key name
    const std::string& get_entry(const std::string& key) const;

    /// Retrieve a metadata string by key name, with a fallback
    const std::string& get_entry(const std::string& key, const std::string& fallback) const {
      return Info::get_entry(key, fallback);
    }

    //@}


  private:

    /// Name of the set in which this PDF is contained (for PDFSet lookup)
    std::string _setname;

    /// Member ID in PDF set
    /// @note Not currently used, but could be useful if a memberID method is exposed.
    int _member;

  };


}
#endif
