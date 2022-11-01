// BeamRemnants.h is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Header file for beam-remnants handling.
// BeamRemnants: matches the remnants between the two beams.

#ifndef Pythia8_BeamRemnants_H
#define Pythia8_BeamRemnants_H

#include "Pythia8/Basics.h"
#include "Pythia8/BeamParticle.h"
#include "Pythia8/ColourReconnection.h"
#include "Pythia8/Event.h"
#include "Pythia8/FragmentationFlavZpT.h"
#include "Pythia8/Info.h"
#include "Pythia8/JunctionSplitting.h"
#include "Pythia8/ParticleData.h"
#include "Pythia8/PartonDistributions.h"
#include "Pythia8/PartonSystems.h"
#include "Pythia8/PartonVertex.h"
#include "Pythia8/PhysicsBase.h"
#include "Pythia8/PythiaStdlib.h"
#include "Pythia8/Settings.h"
#include "Pythia8/StringLength.h"

namespace Pythia8 {

//==========================================================================

// This class matches the kinematics of the hard-scattering subsystems
// (with primordial kT added) to that of the two beam remnants.

class BeamRemnants : public PhysicsBase {

public:

  // Constructor.
  BeamRemnants() : doPrimordialKT(), allowRescatter(), doRescatterRestoreY(),
    doReconnect(), primordialKTsoft(), primordialKThard(),
    primordialKTremnant(), halfScaleForKT(), halfMassForKT(),
    reducedKTatHighY(), remnantMode(), reconnectMode(), isDIS(), doMPI(),
    beamA2gamma(), beamB2gamma(), nSys(), oldSize(), iDS(0), eCM(), sCM(),
    colourReconnectionPtr(), partonVertexPtr(), doPartonVertex() { }

  // Initialization.
  bool init( PartonVertexPtr partonVertexPtrIn,
    ColRecPtr colourReconnectionPtrIn);

  // New beams possible for handling of hard diffraction.
  void reassignBeamPtrs( BeamParticle* beamAPtrIn, BeamParticle* beamBPtrIn,
    int iDSin) {beamAPtr = beamAPtrIn; beamBPtr = beamBPtrIn; iDS = iDSin;}

  // Select the flavours/kinematics/colours of the two beam remnants.
  bool add( Event& event, int iFirst = 0, bool doDiffCR = false);

protected:

  virtual void onInitInfoPtr() override {
    registerSubObject(junctionSplitting); }

private:

  // Constants: could only be changed in the code itself.
  static const bool   ALLOWCOLOURTWICE, CORRECTMISMATCH;
  static const int    NTRYCOLMATCH, NTRYKINMATCH;

  // Initialization data, read from Settings.
  bool   doPrimordialKT, allowRescatter, doRescatterRestoreY, doReconnect;
  double primordialKTsoft, primordialKThard, primordialKTremnant,
         halfScaleForKT, halfMassForKT, reducedKTatHighY;
  int    remnantMode, reconnectMode;

  // Information set for events.
  bool   isDIS, doMPI, beamA2gamma, beamB2gamma;
  int    nSys, oldSize, iDS;
  double eCM, sCM;

  // Colour collapses (when one colour is mapped onto another).
  vector<int> colFrom, colTo;

  // Pointer to the colour reconnection class.
  ColRecPtr colourReconnectionPtr;

  // StringLength class.
  StringLength stringLength;

  // Junction splitting class.
  JunctionSplitting junctionSplitting;

  // Select the flavours/kinematics/colours of the two beam remnants.
  bool addOld( Event& event);

  // Select the flavours/kinematics/colours of the two beam remnants.
  bool addNew( Event& event);

  // Pointer to assign space-time information.
  PartonVertexPtr partonVertexPtr;
  bool doPartonVertex;

  // Do the kinematics of the collision subsystems and two beam remnants.
  bool setKinematics( Event& event);

  // Special beam remnant kinematics when only one remnant system added.
  // This is the case e.g for Deeply Inelastic Scattering and photon
  // collisions with other side ended up to beam photon by ISR.
  bool setOneRemnKinematics( Event& event);

  // Update colours of outgoing particles in the event.
  void updateColEvent( Event& event, vector<pair <int,int> > colChanges);

  // Check that colours are consistent.
  bool checkColours( Event& event);

  // Find junction chains.
  vector <vector<int> > findJunChains(vector<vector <int> > iPartonJun,
    vector<vector<int> > iPartonAjun);

  // Split junction configuration into smaller parts.
  bool splitJunChains(Event& event, vector<vector<int > >& iPartonJun,
    vector<vector< int > >& ipartonAntiJun);

  // Get junction chains.
  vector<vector<int > > getJunChains(Event& event);

};

//==========================================================================

} // end namespace Pythia8

#endif // Pythia8_BeamRemnants_H
