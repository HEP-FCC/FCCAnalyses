// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/PDF.h"
#include "LHAPDF/PDFSet.h"
using namespace std;

namespace LHAPDF {


  void PDF::_loadInfo(const std::string& mempath) {
    if (mempath.empty())
      throw UserError("Tried to initialize a PDF with a null data file path... oops");
    _mempath = mempath;
    _info = PDFInfo(mempath);
    //_info = PDFInfo(_setname(), memberID());
    /// Check that this is a sufficient version LHAPDF for this PDF
    if (_info.has_key("MinLHAPDFVersion")) {
      if (_info.get_entry_as<int>("MinLHAPDFVersion") > LHAPDF_VERSION_CODE) {
        throw VersionError("Current LHAPDF version " + to_str(LHAPDF_VERSION_CODE)
                           + " less than required " + _info.get_entry("MinLHAPDFVersion"));
      }
    }
    /// Print out a banner if sufficient verbosity is enabled
    const int v = verbosity();
    if (v > 0) {
      std::cout << "LHAPDF " << version() << " loading " << mempath << std::endl;
      print(std::cout, v);
    }
    /// Print out a warning message if this PDF data is unvalidated
    if (_info.get_entry_as<int>("DataVersion", -1) <= 0) {
      std::cerr << "WARNING: This PDF is preliminary, unvalidated, and not for production use!" << std::endl;
    }
  }


  bool PDF::hasFlavor(int id) const {
    const int id2 = (id != 0) ? id : 21; //< @note Treat 0 as an alias for 21
    const vector<int>& ids = flavors();
    /// @note std::lower_bound is meant to leverage that we have a sorted list. No speed-up over find noted, though
    // return std::find(ids.begin(), ids.end(), id2) != ids.end();
    const auto it = std::lower_bound(ids.begin(), ids.end(), id2);
    return it != ids.end() && *it == id2;
  }


  double PDF::xfxQ2(int id, double x, double q2) const {
    // Physical x range check
    if (!inPhysicalRangeX(x)) {
      throw RangeError("Unphysical x given: " + to_str(x));
    }
    // Physical Q2 range check
    if (!inPhysicalRangeQ2(q2)) {
      throw RangeError("Unphysical Q2 given: " + to_str(q2));
    }
    // Treat PID = 0 as always equivalent to a gluon: query as PID = 21
    const int id2 = (id != 0) ? id : 21; //< @note Treat 0 as an alias for 21
    // Undefined PIDs
    if (!hasFlavor(id2)) return 0.0;
    // Call the delegated method in the concrete PDF object to calculate the in-range value
    double xfx = _xfxQ2(id2, x, q2);
    // Apply positivity forcing at the enabled level
    switch (forcePositive()) {
    case 0: break;
    case 1: if (xfx < 0) xfx = 0; break;
    case 2: if (xfx < 1e-10) xfx = 1e-10; break;
    default: throw LogicError("ForcePositive value not in expected range!");
    }
    // Return
    return xfx;
  }


  void PDF::xfxQ2(double x, double q2, std::map<int, double>& rtn) const {
    rtn.clear();
    for (int id : flavors()) rtn[id] = xfxQ2(id, x, q2);
  }


  void PDF::xfxQ2(double x, double q2, std::vector<double>& rtn) const {
    rtn.clear();
    rtn.resize(13);
    for (int i = 0; i < 13; ++i) {
      const int id = i-6; // PID = 0 is automatically treated as PID = 21
      rtn[i] = xfxQ2(id, x, q2);
    }
  }


  std::map<int, double> PDF::xfxQ2(double x, double q2) const {
    std::map<int, double> rtn;
    xfxQ2(x, q2, rtn);
    return rtn;
  }


  void PDF::print(std::ostream& os, int verbosity) const {
    stringstream ss;
    if (verbosity > 0) {
      ss << set().name() << " PDF set, member #" << memberID()
         << ", version " << dataversion();
      if (lhapdfID() > 0)
        ss << "; LHAPDF ID = " << lhapdfID();
    }
    if (verbosity > 2 && set().description().size() > 0)
      ss << "\n" << set().description();
    if (verbosity > 1 && description().size() > 0)
      ss << "\n" << description();
    if (verbosity > 2)
      ss << "\n" << "Flavor content = " << to_str(flavors());
    os << ss.str() << endl;
  }


  int PDF::lhapdfID() const {
    //return set().lhapdfID() + memberID()
    /// @todo Add failure tolerance if pdfsets.index not found
    try {
      return lookupLHAPDFID(_setname(), memberID());
    } catch (const Exception&) {
      return -1; //< failure
    }
  }


  double PDF::quarkMass(int id) const {
    const unsigned int aid = std::abs(id);
    if (aid == 0 || aid > 6) return -1;
    const static string QNAMES[] = {"Down", "Up", "Strange", "Charm", "Bottom", "Top"}; ///< @todo Centralise?
    const size_t qid = aid - 1;
    const string qname = QNAMES[qid];
    return info().get_entry_as<double>("M" + qname, -1);
  }


  double PDF::quarkThreshold(int id) const {
    const unsigned int aid = std::abs(id);
    if (aid == 0 || aid > 6) return -1;
    const static string QNAMES[] = {"Down", "Up", "Strange", "Charm", "Bottom", "Top"}; ///< @todo Centralise?
    const size_t qid = aid - 1;
    const string qname = QNAMES[qid];
    return info().get_entry_as<double>("Threshold" + qname, quarkMass(id));
  }


}
