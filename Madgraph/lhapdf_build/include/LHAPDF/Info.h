// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#pragma once
#ifndef LHAPDF_Info_H
#define LHAPDF_Info_H

#include "LHAPDF/Utils.h"
#include "LHAPDF/Paths.h"
#include "LHAPDF/Exceptions.h"
#include <fstream>

namespace LHAPDF {


  /// Get the singleton global configuration object
  ///
  /// @todo Move this out of Info. To Factories.h or SystemConfig.h?
  ///
  /// The global config is populated by reading from lhapdf.conf if it is
  /// found in the search paths.
  // class Info;
  // Info& config();



  /// Metadata base class for PDFs, PDF sets, or global configuration
  class Info {
  public:

    /// @name Creation and deletion
    //@{

    /// Default constructor
    Info() { }

    /// Constructor
    Info(const std::string& path) {
      load(path);
    }

    /// Virtual destructor to allow inheritance
    virtual ~Info() { }

    //@}


    /// @name Loading info from YAML files
    //@{

    /// Populate this info object from the specified YAML file path.
    ///
    /// This function may be called several times to read metadata from several
    /// YAML source files. Values for existing keys will be overwritten.
    void load(const std::string& filepath);

    //@}


    /// @name General metadata accessors
    //@{

    // /// Get all metadata as a map
    // const std::map<std::string, std::string>& metadata() const {
    //   return _metadict;
    // }

    // /// Get all metadata as a map (non-const)
    // std::map<std::string, std::string>& metadata() {
    //   return _metadict;
    // }


    /// Is a value defined for the given key on this specific object?
    bool has_key_local(const std::string& key) const {
      return _metadict.find(key) != _metadict.end();
    }

    /// Can this object return a value for the given key?
    ///
    /// The given key may be defined non-locally, in which case the cascading
    /// member -> set -> config info lookup is needed. These are implemented
    /// using has_key_local() and metadata_local().
    ///
    /// The default implementation is equivalent to has_key_local(). This is
    /// appropriate for Config.
    virtual bool has_key(const std::string& key) const {
      return has_key_local(key);
    }


    /// Retrieve a metadata string by key name, as defined on this specific object
    const std::string& get_entry_local(const std::string& key) const {
      if (has_key_local(key)) return _metadict.find(key)->second;
      throw MetadataError("Metadata for key: " + key + " not found.");
    }

    /// Retrieve a metadata string by key name
    ///
    /// The given key may be defined non-locally, in which case the cascading
    /// member -> set -> config info lookup is needed. These are implemented
    /// using has_key_local() and get_entry_local().
    ///
    /// The default implementation is equivalent to get_entry_local(). This is
    /// appropriate for Config.
    virtual const std::string& get_entry(const std::string& key) const {
      return get_entry_local(key);
    }


    /// Retrieve a metadata string by key name, with a default fallback
    virtual const std::string& get_entry(const std::string& key, const std::string& fallback) const {
      try {
        return get_entry(key);
      } catch (...) {
        return fallback;
      }
    }


    /// Retrieve a metadata entry by key name, with an inline type cast
    ///
    /// Specialisations are defined below for unpacking of comma-separated lists
    /// of strings, ints, and doubles.
    template <typename T>
    T get_entry_as(const std::string& key) const {
      const string& s = get_entry(key);
      return lexical_cast<T>(s);
    }


    /// Retrieve a metadata entry by key name, with an inline type cast and default fallback
    template <typename T>
    T get_entry_as(const std::string& key, const T& fallback) const {
      try {
        return get_entry_as<T>(key);
      } catch (...) {
        return fallback;
      }
    }


    /// Set a keyed value entry
    template <typename T>
    void set_entry(const std::string& key, const T& val) {
      _metadict[key] = to_str(val);
    }

    //@}


  protected:

    /// The string -> string native metadata storage container
    std::map<std::string, std::string> _metadict;

  };


  /// @name Info metadata function template specialisations
  //@{

  template <>
  inline bool Info::get_entry_as(const std::string& key) const {
    const string& s = get_entry(key);
    try {
      bool rtn = lexical_cast<bool>(s);
      return rtn;
    } catch (...) {
      if (s == "true" || s == "on" || s == "yes") return true;
      if (s == "false" || s == "off" || s == "no") return false;
    }
    throw MetadataError("'" + s + "' is not a valid string for conversion to bool type");
  }

  template <>
  inline std::vector<std::string> Info::get_entry_as(const std::string& key) const {
    static const string delim = ",";
    return split(get_entry(key), delim);
  }

  template <>
  inline std::vector<int> Info::get_entry_as(const std::string& key) const {
    const vector<string> strs = get_entry_as< vector<string> >(key);
    vector<int> rtn;
    rtn.reserve(strs.size());
    // for (const string& s : strs) rtn.push_back( lexical_cast<int>(s) ); //< @todo Restore when C++11 guaranteed
    for (size_t i = 0; i < strs.size(); ++i) rtn.push_back( lexical_cast<int>(strs[i]) );
    assert(rtn.size() == strs.size());
    return rtn;
  }

  template <>
  inline std::vector<double> Info::get_entry_as(const std::string& key) const {
    const vector<string> strs = get_entry_as< vector<string> >(key);
    vector<double> rtn;
    rtn.reserve(strs.size());
    //for (const string& s : strs) rtn.push_back( lexical_cast<double>(s) ); //< @todo Restore when C++11 guaranteed
    for (size_t i = 0; i < strs.size(); ++i) rtn.push_back( lexical_cast<double>(strs[i]) );
    assert(rtn.size() == strs.size());
    return rtn;
  }

  //@}


}
#endif
