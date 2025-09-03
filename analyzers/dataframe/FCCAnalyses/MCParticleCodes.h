
#ifndef MCPARTICLECODES_H
#define MCPARTICLECODES_H

// This file contains the particle codes used in the FCC Analyses framework.
namespace FCCAnalyses {

  /// Particle codes following the PDG Monte Carlo particle numbering scheme.
  enum PDGCode : int {

	PDG_UNKNOWN = 0,

	// Leptons
	PDG_ELECTRON = 11,
	PDG_MUON = 13,
	PDG_TAU = 15,
	PDG_E_NEUTRINO = 12,
	PDG_MU_NEUTRINO = 14,
	PDG_TAU_NEUTRINO = 16,

	// Partons
	PDG_QUARK_UP = 1,
	PDG_QUARK_DOWN = 2,
	PDG_QUARK_CHARM = 4,
	PDG_QUARK_STRANGE = 3,
	PDG_QUARK_TOP = 6,
	PDG_QUARK_BOTTOM = 5,
	PDG_GLUON = 21,

	// Bosons
	PDG_PHOTON = 22,
	PDG_Z = 23,
	PDG_W = 24,
	PDG_HIGGS = 25,

	// ...
  };

} // namespace FCCAnalyses


#endif
