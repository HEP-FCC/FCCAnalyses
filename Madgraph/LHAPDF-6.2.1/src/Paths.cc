// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/Paths.h"
#include "LHAPDF/Info.h"
#include "LHAPDF/Config.h"
#include <dirent.h>

namespace LHAPDF {


  std::vector<std::string> paths() {
    // Use LHAPDF_DATA_PATH for all path storage
    char* pathsvar = getenv("LHAPDF_DATA_PATH");
    // But fall back to looking in LHAPATH if the preferred var is not defined
    if (pathsvar == 0) pathsvar = getenv("LHAPATH");
    const string spathsvar = (pathsvar != 0) ? pathsvar : "";
    // Split the paths variable as usual
    vector<string> rtn = split(spathsvar, ":");
    // Look in the install prefix after other paths are exhausted, if not blocked by a trailing ::
    if (spathsvar.length() < 2 || spathsvar.substr(spathsvar.length()-2) != "::") {
      const string datadir = string(LHAPDF_DATA_PREFIX) / "LHAPDF";
      rtn.push_back(datadir );
    }
    return rtn;
  }


  void setPaths(const std::string& pathstr) {
    setenv("LHAPDF_DATA_PATH", pathstr.c_str(), 1);
  }


  string findFile(const string& target) {
    if (target.empty()) return "";
    for (const string& base : paths()) {
      const string p = (startswith(target, "/") || startswith(target, ".")) ? target : base / target;
      // if (verbosity() > 2) cout << "Trying file: " << p << endl;
      if (file_exists(p)) {
        // if (verbosity() > 1) cout << "Found file: " << p << endl;
        return p;
      }
    }
    return "";
  }


  const std::vector<std::string>& availablePDFSets() {
    // Cached path list
    static vector<string> rtn;
    // Return cached list if valid
    if (!rtn.empty()) return rtn;
    // Otherwise this is the first time: populate the list
    for (const string& p : paths()) {
      if (!dir_exists(p)) continue;
      DIR* dir;
      struct dirent* ent;
      if ((dir = opendir(p.c_str())) != NULL) {
        while ((ent = readdir(dir)) != NULL) {
          const string d = ent->d_name;
          const string infopath = p / d / d + ".info";
          if (file_exists(infopath)) {
            if (!contains(rtn, d)) {
              // cout << "@" << d << "@" << endl;
              rtn.push_back(d); //< add if a set with this name isn't already known
            }
          }
        }
        closedir(dir);
      }
      sort(rtn.begin(), rtn.end());
    }
    return rtn;
  }


}
