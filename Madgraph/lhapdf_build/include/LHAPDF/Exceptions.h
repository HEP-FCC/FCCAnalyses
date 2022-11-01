// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Exceptions_H
#define LHAPDF_Exceptions_H

#include <exception>
#include <stdexcept>

namespace LHAPDF {


  /// @name Exception classes for error handling
  //@{

  /// @brief Generic unspecialised LHAPDF runtime error.
  ///
  /// NB. We don't use "Error" because that has a physics meaning!
  class Exception : public std::runtime_error {
  public:
    /// Constructor with error description string
    Exception(const std::string& what) : std::runtime_error(what) {}
  };


  /// Error for general PDF grid problems.
  class GridError : public Exception {
  public:
    /// Constructor with error description string
    GridError(const std::string& what) : Exception(what) {}
  };


  /// Error to be thrown when out of the valid range of a PDF.
  class RangeError : public Exception {
  public:
    /// Constructor with error description string
    RangeError(const std::string& what) : Exception(what) {}
  };


  /// Error for places where it should not have been possible to get to!
  class LogicError : public Exception {
  public:
    /// Constructor with error description string
    LogicError(const std::string& what) : Exception(what) {}
  };


  /// @brief Error for unfound or broken metadata entries.
  class MetadataError : public Exception {
  public:
    /// Constructor with error description string
    MetadataError(const std::string& what) : Exception(what) {}
  };


  /// @brief Error for file reading errors.
  class ReadError : public Exception {
  public:
    /// Constructor with error description string
    ReadError(const std::string& what) : Exception(what) {}
  };


  /// @brief Error for requests for unsupported/invalid flavour PIDs.
  class FlavorError : public Exception {
  public:
    /// Constructor with error description string
    FlavorError(const std::string& what) : Exception(what) {}
  };


  /// @brief Error to be raised by object factories given invalid requests.
  class FactoryError : public Exception {
  public:
    /// Constructor with error description string
    FactoryError(const std::string& what) : Exception(what) {}
  };


  /// @brief Error to be raised when a LHAPDF ID indexing fails
  class IndexError : public Exception {
  public:
    /// Constructor with error description string
    IndexError(const std::string& what) : Exception(what) {}
  };


  /// Error for general AlphaS computation problems.
  class AlphaSError : public Exception {
  public:
    /// Constructor with error description string
    AlphaSError(const std::string& what) : Exception(what) {}
  };


  /// @brief Error to be raised when a newer LHAPDF version is needed
  class VersionError : public Exception {
  public:
    /// Constructor with error description string
    VersionError(const std::string& what) : Exception(what) {}
  };


  /// Problem exists between keyboard and chair.
  class UserError : public Exception {
  public:
    /// Constructor with error description string
    UserError(const std::string& what) : Exception(what) {}
  };


  /// This feature doesn't exist yet
  class NotImplementedError : public Exception {
  public:
    /// Constructor with error description string
    NotImplementedError(const std::string& what) : Exception(what) {}
  };

  //@}


}
#endif
