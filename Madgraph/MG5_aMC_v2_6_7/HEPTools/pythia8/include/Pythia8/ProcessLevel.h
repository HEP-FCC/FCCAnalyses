// ProcessLevel.h is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// This file contains the main class for process-level event generation.
// ProcessLevel: administrates the selection of "hard" process.

#ifndef Pythia8_ProcessLevel_H
#define Pythia8_ProcessLevel_H

#include "Pythia8/Basics.h"
#include "Pythia8/BeamParticle.h"
#include "Pythia8/Event.h"
#include "Pythia8/Info.h"
#include "Pythia8/ParticleData.h"
#include "Pythia8/PartonDistributions.h"
#include "Pythia8/PhysicsBase.h"
#include "Pythia8/ProcessContainer.h"
#include "Pythia8/PythiaStdlib.h"
#include "Pythia8/ResonanceDecays.h"
#include "Pythia8/Settings.h"
#include "Pythia8/SigmaTotal.h"
#include "Pythia8/SusyCouplings.h"
#include "Pythia8/SLHAinterface.h"
#include "Pythia8/StandardModel.h"
#include "Pythia8/UserHooks.h"

namespace Pythia8 {

//==========================================================================

// The ProcessLevel class contains the top-level routines to generate
// the characteristic "hard" process of an event.

class ProcessLevel : public PhysicsBase {

public:

  // Constructor.
  ProcessLevel() = default;

  // Destructor to delete processes in containers.
  ~ProcessLevel();

  // Initialization.
  bool init(bool doLHAin, SLHAinterface* slhaInterfacePtrIn,
    vector<SigmaProcess*>& sigmaPtrs, vector<PhaseSpace*>& phaseSpacePtrs);

  // Store or replace Les Houches pointer.
  void setLHAPtr( LHAupPtr lhaUpPtrIn) {lhaUpPtr = lhaUpPtrIn;
    if (iLHACont >= 0) containerPtrs[iLHACont]->setLHAPtr(lhaUpPtr);}

  // Generate the next "hard" process.
  bool next( Event& process);

  // Special case: LHA input of resonance decay only.
  bool nextLHAdec( Event& process);

  // Accumulate and update statistics (after possible user veto).
  void accumulate( bool doAccumulate = true);

  // Print statistics on cross sections and number of events.
  void statistics(bool reset = false);

  // Reset statistics.
  void resetStatistics();

  // Add any junctions to the process event record list.
  void findJunctions( Event& junEvent);

  // Initialize and call resonance decays separately.
  void initDecays( LHAupPtr lhaUpPtrIn) {
    containerLHAdec.setLHAPtr(lhaUpPtrIn, particleDataPtr, settingsPtr,
      rndmPtr); }

  bool nextDecays( Event& process) { return resonanceDecays.next( process);}

protected:

  virtual void onInitInfoPtr() override {
    registerSubObject(resonanceDecays);
    registerSubObject(gammaKin);
  }

private:

  // Constants: could only be changed in the code itself.
  static const int MAXLOOP;

  // Generic info for process generation.
  bool   doSecondHard, doSameCuts, allHardSame, noneHardSame, someHardSame,
         cutsAgree, cutsOverlap, doResDecays, doISR, doMPI, doWt2;
  int    startColTag;
  double maxPDFreweight, mHatMin1, mHatMax1, pTHatMin1, pTHatMax1, mHatMin2,
         mHatMax2, pTHatMin2, pTHatMax2, sigmaND;

  // Info for process generation with photon beams.
  bool   beamHasGamma;
  int    gammaMode;

  // Vector of containers of internally-generated processes.
  vector<ProcessContainer*> containerPtrs;
  int    iContainer, iLHACont = -1;
  double sigmaMaxSum;

  // Ditto for optional choice of a second hard process.
  vector<ProcessContainer*> container2Ptrs;
  int    i2Container;
  double sigma2MaxSum;

  // Single half-dummy container for LHA input of resonance decay only.
  ProcessContainer containerLHAdec;

  // Pointer to SusyLesHouches object for interface to SUSY spectra.
  SLHAinterface*  slhaInterfacePtr;

  // Pointer to LHAup for generating external events.
  LHAupPtr          lhaUpPtr;

  // ResonanceDecay object does sequential resonance decays.
  ResonanceDecays resonanceDecays;

  // Samples photon kinematics from leptons.
  GammaKinematics gammaKin;

  // Generate the next event with one interaction.
  bool nextOne( Event& process);

  // Generate the next event with two hard interactions.
  bool nextTwo( Event& process);

  // Check that enough room for beam remnants in photon beam.
  bool roomForRemnants();

  // Append the second to the first process list.
  void combineProcessRecords( Event& process, Event& process2);

  // Check that colours match up.
  bool checkColours( Event& process);

  // Print statistics when two hard processes allowed.
  void statistics2(bool reset);

};

//==========================================================================

} // end namespace Pythia8

#endif // Pythia8_ProcessLevel_H
