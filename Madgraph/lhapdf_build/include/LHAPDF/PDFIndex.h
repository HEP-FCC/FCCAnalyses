// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_PDFIndex_H
#define LHAPDF_PDFIndex_H

#include "LHAPDF/Utils.h"

namespace LHAPDF {


  /// @name Functions for PDF lookup by LHAPDF ID index file
  //@{

  /// Get the singleton LHAPDF set ID -> PDF index map
  std::map<int, std::string>& getPDFIndex();

  /// Look up a PDF set name and member ID by the LHAPDF ID code
  ///
  /// The set name and member ID are returned as an std::pair.
  /// If lookup fails, a pair ("", -1) is returned.
  std::pair<std::string, int> lookupPDF(int lhaid);

  /// @brief Decode a single PDF member ID string into a setname,memid pair
  ///
  /// @note A trivial <SET,MEM> decoding rather than a "rea; lookup", for convenience & uniformity.
  std::pair<std::string,int> lookupPDF(const std::string& pdfstr);

  /// Look up the member's LHAPDF index from the set name and member ID.
  ///
  /// If lookup fails, -1 is returned, otherwise the LHAPDF ID code.
  /// NB. This function is relatively slow, since it requires std::map reverse lookup.
  int lookupLHAPDFID(const std::string& setname, int nmem);

  /// Look up the member's LHAPDF index from a setname/member string.
  inline int lookupLHAPDFID(const std::string& setname_nmem) {
    const std::pair<string,int> idpair = lookupPDF(setname_nmem);
    return lookupLHAPDFID(idpair.first, idpair.second);
  }

  //@}


}
#endif
