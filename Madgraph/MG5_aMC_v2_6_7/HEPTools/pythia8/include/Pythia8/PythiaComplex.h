// PythiaComplex.h is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Header file for typedef'd double precision complex numbers.

#ifndef Pythia8_PythiaComplex_H
#define Pythia8_PythiaComplex_H

// Stdlib header for complex numbers.
# include <complex>

namespace Pythia8 {

// Convenient typedef for double precision complex numbers.
typedef std::complex<double> complex;
using std::norm;

//==========================================================================

} // end namespace Pythia8

#endif // Pythia8_PythiaComplex_H
