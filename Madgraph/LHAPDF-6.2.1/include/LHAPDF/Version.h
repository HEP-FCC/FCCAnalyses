/* include/LHAPDF/Version.h.  Generated from Version.h.in by configure.  */
// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Version_H
#define LHAPDF_Version_H

#include <string>

/* "LHAPDF version string" */
#define LHAPDF_VERSION "6.2.1"

/* "LHAPDF version as an int" */
#define LHAPDF_VERSION_CODE 60201

/* "Whether PDFLIB Fortran compatibility is available" */
#define LHAPDF_PDFLIB 1

/* "Whether LHAPDF5 C++ compatibility is available" */
#define LHAPDF_LHA5CXX 1

// Separate int-valued macro for conditional compilation. Doesn't exist in LHAPDF5.
// Use like "#if defined LHAPDF_MAJOR_VERSION && LHAPDF_MAJOR_VERSION == 6 ..."
#define LHAPDF_MAJOR_VERSION 6

namespace LHAPDF {


  /// Get the LHAPDF library version code (as a string)
  inline std::string version() {
    return LHAPDF_VERSION;
  }


}
#endif
