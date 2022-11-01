#ifndef VECTOR_CONVERSION_H
#define VECTOR_CONVERSION_H
//////////////////////////////////////////////////////////////////////////
// garren@fnal.gov, January 2007
//
// This example converts from ThreeVector and FourVector to 
// CLHEP::Hep3Vector and CLHEP::HepLorentzVector
// Similar (or perhaps templated) conversion methods could be added to
// any vector class.
//
//////////////////////////////////////////////////////////////////////////

#include "HepMC/SimpleVector.h"
#include "CLHEP/Vector/LorentzVector.h"
///
/// \namespace CLHEP
/// CLHEP Vector classes are used in one of the examples
///

/// Convert from HepMC::ThreeVector to CLHEP::Hep3Vector
inline CLHEP::Hep3Vector convertTo( const HepMC::ThreeVector& v )
     { return CLHEP::Hep3Vector( v.x(), v.y(), v.z() ); }

/// Convert from HepMC::FourVector to CLHEP::HepLorentzVector
inline CLHEP::HepLorentzVector convertTo( const HepMC::FourVector& v )
     { return CLHEP::HepLorentzVector( v.x(), v.y(), v.z(), v.t() ); }
 
#endif  // VECTOR_CONVERSION_H
