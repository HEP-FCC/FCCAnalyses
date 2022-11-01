// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Paths_H
#define LHAPDF_Paths_H

#include "LHAPDF/Utils.h"

namespace LHAPDF {


  /// @name File searching and search path handling functions
  //@{

  /// @brief Get the ordered list of search paths, from $LHAPDF_DATA_PATH and the install location
  /// @note The install prefix will be appended *unless* $LHAPDF_DATA_PATH ends with a double colon, i.e. '::'
  std::vector<std::string> paths();

  /// Set the search paths list as a colon-separated string
  void setPaths(const std::string& pathstr);
  /// Set the search paths list
  inline void setPaths(std::vector<string> paths) {
    setPaths(join(paths, ":"));
  }


  /// Prepend to the search paths list
  inline void pathsPrepend(const std::string& p) {
    vector<string> ps = paths();
    ps.insert(ps.begin(), p);
    ps.pop_back(); //< Discard the auto-added fallback path to the installed data prefix
    setPaths(ps);
  }


  /// Append to the search paths list
  inline void pathsAppend(const std::string& p) {
    vector<string> ps = paths();
    ps.pop_back(); //< Discard the auto-added fallback path to the installed data prefix
    ps.push_back(p);
    setPaths(ps);
  }


  /// Return the first location in which a file is found
  ///
  /// If no matching file is found, return an empty path.
  std::string findFile(const std::string& target);
  //@}



  /// @name Functions for handling standard LHAPDF filename structures
  //@{

  inline std::string pdfmempath(const std::string& setname, int member) {
    const string memname = setname + "_" + to_str_zeropad(member) + ".dat";
    const string mempath = setname / memname;
    return mempath;
  }

  inline std::string findpdfmempath(const std::string& setname, int member) {
    return findFile(pdfmempath(setname, member));
  }

  inline std::string pdfsetinfopath(const std::string& setname) {
    const string infoname = setname + ".info";
    const string setinfo = setname / infoname;
    return setinfo;
  }

  inline std::string findpdfsetinfopath(const std::string& setname) {
    /// @todo Check that set info and mem=0 file are in same dir?
    return findFile(pdfsetinfopath(setname));
  }

  //@}


  /// @brief Get the names of all available PDF sets in the search path
  ///
  /// @note Taken from scanning the directories in the search path
  /// (i.e. LHAPDF_DATA_PATH) for viable PDF sets.
  ///
  /// @note The result is cached when first called, to avoid repeated filesystem
  /// walking. It's assumed that new PDFs will not appear on the filesystem
  /// during a run: please let the authors know if that's not a good assumption!
  const std::vector<std::string>& availablePDFSets();


}

#endif
