// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/Config.h"
#include "LHAPDF/Version.h"
using namespace std;

namespace LHAPDF {


  Config::~Config() {
    // Emit citation information at the end of the job, via the Config destructor
    // std::cout << "CONFIG DESTRUCTION" << std::endl;
    if (verbosity() > 0) {
      cout << "Thanks for using LHAPDF " << version() << ". Please make sure to cite the paper:\n";
      cout << "  Eur.Phys.J. C75 (2015) 3, 132  (http://arxiv.org/abs/1412.7420)" << endl;
    }
  }



}
