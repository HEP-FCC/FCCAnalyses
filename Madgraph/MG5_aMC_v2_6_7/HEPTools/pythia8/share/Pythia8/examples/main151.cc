// main151.cc is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Authors: Torbjorn Sjostrand <torbjorn.sjostrand@thep.lu.se>.

// Keywords: rescattering; low energy; multiplicities;

// Compare charged multiplicity energy dependence in various treatments,
// specifically the simplified one used for low-energy collisions in
// rescattering with the full-fledged standard based on an MPI framework.

#include "Pythia8/Pythia.h"
using namespace Pythia8;

//--------------------------------------------------------------------------

int main() {

  // Number of events per energy point.
  int nEvent = 10000;

  // All subprocesses (0), nondiffractive (1) or single diffractive (2).
  int pick = 2;

  // Histograms.
  Hist multCh0("n_charged(e_CM), simple",      32, 1., 10000., true);
  Hist multCh1("n_charged(e_CM), interpolate", 32, 1., 10000., true);
  Hist multCh2("n_charged(e_CM), full MPI",    32, 1., 10000., true);

  // Loop over the three scenarios at fifteen energies.
  for (int ic = 0; ic < 3; ++ic) {

    // First scenario: low-energy handling asin rescattering.
    // Second scenario: variable-energy interpolating description.
    if (ic < 2) {

      // Create Pythia instance and set it up.
      Pythia pythia;
      Event& event = pythia.event;
      pythia.readString("Beams:allowVariableEnergy = on");
      pythia.readString("Beams:eCM = 10000.");
      // A raised eMinPert recovers the simple framework below new value.
      if (ic == 0) pythia.readString("Beams:eMinPert = 9900.");
      // Switch on all processes, nondiffractive or single diffractive.
      if (pick == 0) {
        pythia.readString("LowEnergyQCD:all = on");
        pythia.readString("SoftQCD:all = on");
      } else if (pick == 1) {
        pythia.readString("LowEnergyQCD:nonDiffractive = on");
        pythia.readString("SoftQCD:nonDiffractive = on");
      } else {
        pythia.readString("LowEnergyQCD:singleDiffractiveXB = on");
        pythia.readString("LowEnergyQCD:singleDiffractiveAX = on");
        pythia.readString("SoftQCD:singleDiffractive = on");
      }
      pythia.init();

      // Iterate over thirty energies.
      for (int ie = 2; ie < 32; ++ie) {
        double eCM = pow( 10., (ie + 0.5) / 8.);

        // Generate events. Update charged multiplicity.
        long nSuccess = 0;
        long nCharged = 0;
        for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
          if (!pythia.next(eCM)) continue;
          ++nSuccess;
          nCharged += event.nFinal(true);
        }
        if (nSuccess == 0);
        else if (ic == 0) multCh0.fill(eCM, double(nCharged)/double(nSuccess));
        else              multCh1.fill(eCM, double(nCharged)/double(nSuccess));
      }

    // Third scenario: full generation energy by energy (only above 10 GeV).
    } else {
      for (int ie = 8; ie < 32; ++ie) {
        double eCM = pow( 10., (ie + 0.5) / 8.);

        // Create Pythia instance and set it up.
        Pythia pythia;
        Event& event = pythia.event;
        if (pick == 0) pythia.readString("SoftQCD:all = on");
        else if (pick == 1)  pythia.readString("SoftQCD:nonDiffractive = on");
        else pythia.readString("SoftQCD:singleDiffractive = on");
        pythia.settings.parm("Beams:eCM", eCM);
        pythia.init();

        // Generate events. Update charged multiplicity.
        long nSuccess = 0;
        long nCharged = 0;
        for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
          if (!pythia.next()) continue;
          ++nSuccess;
          nCharged += event.nFinal(true);
        }
        multCh2.fill( eCM, double(nCharged) / double(nSuccess) );
      }
    }
  }

  // Plot histograms.
  cout << multCh0 << multCh1 << multCh2;
  HistPlot hpl("main151plot");
  hpl.frame("out151plot", "Rise of charged multiplicity with energy",
    "eCM", "<n_charged>");
  hpl.add( multCh0, "-", "low-energy model");
  hpl.add( multCh1, "-", "interpolation");
  hpl.add( multCh2, "-", "high-energy model");
  hpl.plot();

  // Done.
  return 0;
}
