// main31.cc is a part of the PYTHIA event generator.
// Copyright (C) 2011 Mikhail Kirsanov, Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// This is a simple test program.
// It illustrates how HepMC can be interfaced to Pythia8.
// It studies the charged multiplicity distribution at the LHC.
// HepMC events are output to the hepmcout31.dat file.
// Written by Mikhail Kirsanov based on main01.cc.

// WARNING: typically one needs 25 MB/100 events at the LHC.
// Therefore large event samples may be impractical.

#include "Pythia.h"
#include "HepMCInterface.h"

#include "HepMC/GenEvent.h"
#include "HepMC/IO_GenEvent.h"

// Following line is a deprecated alternative, removed in recent versions
//#include "HepMC/IO_Ascii.h"
//#include "HepMC/IO_AsciiParticles.h"

// Following line to be used with HepMC 2.04 onwards.
#ifdef HEPMC_HAS_UNITS
#include "HepMC/Units.h"
#endif

using namespace Pythia8; 

int main() {

  // Interface for conversion from Pythia8::Event to HepMC one. 
  HepMC::I_Pythia8 ToHepMC;
  //  ToHepMC.set_crash_on_problem();

  // Specify file where HepMC events will be stored.
  HepMC::IO_GenEvent ascii_io("hepmcout31.dat", std::ios::out);
  // Following line is a deprecated alternative, removed in recent versions
  // HepMC::IO_Ascii ascii_io("hepmcout31.dat", std::ios::out);
  // Line below is an eye-readable one-way output, uncomment the include above
  // HepMC::IO_AsciiParticles ascii_io("hepmcout31.dat", std::ios::out);

  // Generator. Process selection. LHC initialization. Histogram.
  Pythia pythia;
  pythia.readString("HardQCD:all = on");    
  pythia.readString("PhaseSpace:pTHatMin = 20.");    
  pythia.init( 2212, 2212, 14000.);
  Hist mult("charged multiplicity", 100, -0.5, 799.5);

  // Begin event loop. Generate event. Skip if error. List first one.
  for (int iEvent = 0; iEvent < 100; ++iEvent) {
    if (!pythia.next()) continue;
    if (iEvent < 1) {pythia.info.list(); pythia.event.list();} 

    // Find number of all final charged particles and fill histogram.
    int nCharged = 0;
    for (int i = 0; i < pythia.event.size(); ++i) 
      if (pythia.event[i].isFinal() && pythia.event[i].isCharged()) 
        ++nCharged; 
    mult.fill( nCharged );

    // Construct new empty HepMC event. 
#ifdef HEPMC_HAS_UNITS
    // This form with arguments is only meaningful for HepMC 2.04 onwards, 
    // and even then unnecessary if HepMC was built with GeV and mm as units..
    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent( 
      HepMC::Units::GEV, HepMC::Units::MM);
#else
    // This form is needed for backwards compatibility. 
    // In HepMCInterface.cc a conversion from GeV to MeV will be done.
    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
#endif

    // Fill HepMC event, including PDF info.
    ToHepMC.fill_next_event( pythia, hepmcevt );
    // This alternative older method fills event, without PDF info.
    // ToHepMC.fill_next_event( pythia.event, hepmcevt );

    // Write the HepMC event to file. Done with it.
    ascii_io << hepmcevt;
    delete hepmcevt;

  // End of event loop. Statistics. Histogram. 
  }
  pythia.statistics();
  cout << mult; 

  // Done.
  return 0;
}
