// -*- C++ -*-
// LHAPDFv5/v6 compatibility example

#include "LHAPDF/LHAPDF.h"
#include <iostream>


int main() {
  const double x = 1e-3, Q = 200;

  #if LHAPDF_MAJOR_VERSION == 6
  LHAPDF::PDF* pdf = LHAPDF::mkPDF("CT10nlo", 0);
  std::cout << "xf_g = " << pdf->xfxQ(21, x, Q) << std::endl;
  delete pdf;
  #else
  LHAPDF::initPDFSet("CT10nlo", LHAPDF::LHGRID, 0);
  std::cout << "xf_g = " << LHAPDF::xfx(x, Q, 0) << std::endl;
  #endif

  return 0;
}
