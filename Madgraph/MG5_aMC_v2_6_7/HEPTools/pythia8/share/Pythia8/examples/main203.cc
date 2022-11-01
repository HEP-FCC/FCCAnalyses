// main203.cc is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Example showing how to run Vincia's electroweak shower, for the example
// process pp > dijets (with pThat >= 2000 GeV) at eCM = 14000 GeV.
// The Vincia EW shower requires hard-process partons with assigned
// helicities. This is done via Pythia's MG5 matrix-element interface.

// Requires Pythia to be configured using the --with-mg5mes option.
// For example (in main pythia83 directory): ./configure --with-mg5mes

// Note: emitted weak bosons decay inclusively; it would be up to the user
// themselves to filter events with decays to specific channels if desired.

// Authors: Peter Skands <peter.skands@monash.edu>

// Keywords: madgraph; Vincia; weak showers;

// Include Pythia8 header(s) and namespace.
#include "Pythia8/Pythia.h"
using namespace Pythia8;

// Main Program
int main() {

  //************************************************************************

  // Number of events and number of aborts to accept before stopping.
  int    nEvent      = 500;
  int    nAbort      = 2;

  //**********************************************************************
  // Define Pythia 8 generator

  Pythia pythia;

  //**********************************************************************

  // Shorthands
  Event& event = pythia.event;

  // Define settings common to all runs.
  // We will print the event record ourselves (with helicities)
  pythia.readString("Next:numberShowEvent  = 0");

  // Beams and CM energy.
  pythia.readString("Beams:idA  =  2212");
  pythia.readString("Beams:idB  =  2212");
  pythia.readString("Beams:eCM = 14000.0");
  pythia.readString("Next:numberCount = 100");

  // Process and MG5 library (see plugins/mg5mes/).
  pythia.readString("HardQCD:all = on");
  pythia.readString("PhaseSpace:pThatMin = 2000.0");
  pythia.readString("Vincia:mePlugin = procs_qcd_sm");

  // VINCIA settings
  pythia.readString("PartonShowers:model   = 2");
  pythia.readString("Vincia:helicityShower = on");
  pythia.readString("Vincia:ewMode         = 3");
  pythia.readString("Vincia:verbose        = 1");

  // Switch off MPI and hadronisation (to speed things up).
  pythia.readString("PartonLevel:MPI = off");
  pythia.readString("HadronLevel:all = off");

  // Initialize
  if(!pythia.init()) { return EXIT_FAILURE; }

  // Define counters and PYTHIA histograms.
  double nGamSum   = 0.0;
  double nWeakSum  = 0.0;
  double nFinalSum = 0.0;
  Hist histNFinal("nFinal", 100, -0.5, 99.5);
  Hist histNGam("nPhotons", 20, -0.5, 19.5);
  Hist histNWeak("nWeakBosons", 10, -0.5, 9.5);

  //************************************************************************

  // EVENT GENERATION LOOP.
  // Generation, event-by-event printout, analysis, and histogramming.

  // Counter for negative-weight events
  double weight=1.0;
  double sumWeights = 0.0;

  // Begin event loop
  int iAbort = 0;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {

    bool aborted = !pythia.next();
    if(aborted){
      event.list();
      if (++iAbort < nAbort){
        continue;
      }
      cout << " Event generation aborted prematurely, owing to error!\n";
      cout<< "Event number was : "<<iEvent<<endl;
      break;
    }

    // Check for weights
    weight = pythia.info.weight();
    sumWeights += weight;

    // Print event with helicities
    if (iEvent == 0) event.list(true);

    // Count FS final-state particles, weak bosons, and photons.
    double nFinal = 0;
    double nWeak  = 0;
    double nGam   = 0;
    for (int i=5;i<event.size();i++) {
      // Count up final-state charged hadrons
      if (event[i].isFinal()) {
        ++nFinal;
        // Final-state photons that are not from hadron decays
        if (event[i].id() == 22 && event[i].status() < 90) ++nGam;
      }
      // Weak bosons (not counting hard process)
      else if (event[i].idAbs() == 23 || event[i].idAbs() == 24) {
        // Find weak bosons that were radiator or emitter.
        if (event[i].status() != -51) continue;
        nWeak += 0.5;
      }
    }
    histNWeak.fill(nWeak,weight);
    histNFinal.fill(nFinal,weight);
    histNGam.fill(nGam,weight);
    nGamSum   += nGam * weight;
    nWeakSum  += nWeak * weight;
    nFinalSum += nFinal * weight;

  }

  //**********************************************************************

  // POST-RUN FINALIZATION

  // Print out end-of-run information.
  pythia.stat();

  // Normalization.
  double normFac = 1./sumWeights;

  cout<< histNWeak << histNGam << histNFinal;

  cout<<endl;
  cout<<fixed;
  cout<< " <nFinal>   = "<<num2str(nFinalSum * normFac)<<endl;
  cout<< " <nPhotons> = "<<num2str(nGamSum * normFac)<<endl;
  cout<< " <nZW>      = "<<num2str(nWeakSum * normFac)<<endl;
  cout<<endl;

  // Done.
  return 0;
}
