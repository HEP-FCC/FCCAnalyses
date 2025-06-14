
#ifndef MCPARTICLECODES_H
#define MCPARTICLECODES_H

// This file contains the particle codes used in the FCC Analyses framework.
namespace FCCAnalyses {

  /// Particle codes following the PDG Monte Carlo particle numbering scheme.
  enum class PDGCode {

	UNKNOWN = 0,

	// Leptons
	ELECTRON = 11,
	MUON = 13,
	TAU = 15,
	E_NEUTRINO = 12,
	MU_NEUTRINO = 14,
	TAU_NEUTRINO = 16,

	// Partons
	QUARK_UP = 1,
	QUARK_DOWN = 2,
	QUARK_CHARM = 4,
	QUARK_STRANGE = 3,
	QUARK_TOP = 6,
	QUARK_BOTTOM = 5,
	GLUON = 21,

	// Bosons
	PHOTON = 22,
	Z = 23,
	W = 24,
	HIGGS = 25,

	// Baryons
	PION = 211,
	KAON = 321,
	PROTON = 2212,
	NEUTRON = 2112,
  };

} // namespace FCCAnalyses


#endif
