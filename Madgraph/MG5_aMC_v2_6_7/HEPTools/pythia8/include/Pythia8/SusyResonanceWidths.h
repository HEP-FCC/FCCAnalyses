// SusyResonanceWidths.h is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand
// Main author of this file: N. Desai
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Header file for SUSY resonance properties: dynamical widths etc.
// SusyResonanceWidths: base class for all SUSY resonances.

#ifndef Pythia8_SusyResonanceWidths_H
#define Pythia8_SusyResonanceWidths_H

#include "Pythia8/ParticleData.h"
#include "Pythia8/ResonanceWidths.h"
#include "Pythia8/SusyWidthFunctions.h"
#include "Pythia8/SusyCouplings.h"

namespace Pythia8 {

//==========================================================================

class SUSYResonanceWidths : public ResonanceWidths{

public:

  // Constructor
  SUSYResonanceWidths() {}

  // Destructor
  virtual ~SUSYResonanceWidths() {}

protected:

  // Virtual methods to handle model-specific (non-SM) part of initialization
  virtual bool initBSM() override;
  virtual bool allowCalc() override;
  virtual bool getChannels(int) { return false; };

  static const bool DBSUSY;

};

//==========================================================================

// The ResonanceSquark class handles the Squark resonances.

class ResonanceSquark : public SUSYResonanceWidths {

public:

  // Constructor.
  ResonanceSquark(int idResIn) : s2W() {initBasic(idResIn);}


private:

  // Locally stored properties and couplings.

  // Initialize constants.
  virtual void initConstants() override;

  // Calculate various common prefactors for the current mass.
  virtual void calcPreFac(bool = false) override;

  bool getChannels(int idPDG) override;

  // Caclulate width for currently considered channel.
  virtual void calcWidth(bool calledFromInit = false) override;

  double s2W;

};

//==========================================================================

// The ResonanceGluino class handles the Gluino resonances.

class ResonanceGluino : public SUSYResonanceWidths {

public:

  // Constructor.
  ResonanceGluino(int idResIn) {initBasic(idResIn);}

private:

  bool getChannels(int idPDG) override;

  // Locally stored properties and couplings.

  // Initialize constants.
  virtual void initConstants() override;

  // Calculate various common prefactors for the current mass.
  virtual void calcPreFac(bool = false) override;

  // Caclulate width for currently considered channel.
  virtual void calcWidth(bool calledFromInit = false) override;

};

//==========================================================================

// The ResonanceNeut class handles the Neutralino resonances.

class ResonanceNeut : public SUSYResonanceWidths {

public:

  // Constructor.
  ResonanceNeut(int idResIn) : kinFac2(), s2W() {initBasic(idResIn);}

private:

  bool getChannels(int idPDG) override;
  // Locally stored properties and couplings.
  double kinFac2;

  // Initialize constants.
  virtual void initConstants() override;

  // Calculate various common prefactors for the current mass.
  virtual void calcPreFac(bool = false) override;

  // Caclulate width for currently considered channel.
  virtual void calcWidth(bool calledFromInit = false) override;

  double s2W;

  // Functions for 3-body decays
  /* Psi psi; */
  /* Phi phi; */
  /* Upsilon upsil; */

};

//==========================================================================

// The ResonanceChar class handles the Chargino resonances.

class ResonanceChar : public SUSYResonanceWidths {

public:

  // Constructor.
  ResonanceChar(int idResIn) : kinFac2(), s2W() {initBasic(idResIn);}

private:

  bool getChannels(int idPDG) override;

  // Locally stored properties and couplings.
  double kinFac2;

  // Initialize constants.
  virtual void initConstants() override;

  // Calculate various common prefactors for the current mass.
  virtual void calcPreFac(bool = false) override;

  // Caclulate width for currently considered channel.
  virtual void calcWidth(bool calledFromInit = false) override;

  double s2W;

  //Functions for 3-body decays
  /* Psi psi; */
  /* Phi phi; */
  /* Upsilon upsil; */

};

//==========================================================================

// The ResonanceSlepton class handles the Slepton/Sneutrino resonances.

class ResonanceSlepton : public SUSYResonanceWidths {

public:

  // Constructor.
  ResonanceSlepton(int idResIn) : s2W() {initBasic(idResIn);}

private:

  bool getChannels(int idPDG) override;

  // Locally stored properties and couplings.

  // Initialize constants.
  virtual void initConstants() override;

  // Calculate various common prefactors for the current mass.
  virtual void calcPreFac(bool = false) override;

  // Calculate width for currently considered channel.
  virtual void calcWidth(bool calledFromInit = false) override;

  double s2W;

  // Three-body stau decaywidth classes
  StauWidths stauWidths;

};

//==========================================================================

} // end namespace Pythia8

#endif // end Pythia8_SusyResonanceWidths_H
