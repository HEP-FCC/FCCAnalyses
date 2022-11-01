// main333.cc is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Authors: Christian Bierlich <christian.bierlich@thep.lu.se>.

// Keywords: userhooks; performance; jets; hadronic rescattering;

// This main program illustrates the use of UserHooks to veto events
// after hadronization, but before any subsequent processes such as
// rescattering or Bose-Einstein.

#include "Pythia8/Pythia.h"
using namespace Pythia8;

//==========================================================================

// Write own derived UserHooks class.

class HadronUserHooks : public UserHooks {

public:

  bool canVetoAfterHadronization() override {return true;}

  bool doVetoAfterHadronization(const Event& e) override {
    // This illustrates the use by requiring the presence of
    // a high pT track central in eta.
    for (const Particle& p : e) {
      // If a trigger particle is found, do not veto.
      if (p.isFinal() && p.isCharged() && p.pT() > 7 && abs(p.eta()) < 1.0)
        return false;
    }
    // This info message will be printed in the stat summary.
    infoPtr->errorMsg("Info: Event vetoed by HadronUserHooks");
    // If no trigger particle is found, veto the event.
    return true;
  }


};

//==========================================================================

int main() {

  // Generator.
  Pythia pythia;
  // Make a histogram of the leading track.
  Hist leadingTrack("pTleading", 20, 0, 20);
  pythia.readString("HardQCD:all = on");
  // Select the parton-level pTHatMin below the cut on track-level.
  pythia.readString("PhaseSpace:pTHatMin = 5.");
  // Add a process after hadronization to motivate the veto.
  pythia.readString("Fragmentation:setVertices = on");
  pythia.readString("PartonVertex:setVertex = on");
  pythia.readString("HadronLevel:Rescatter = on");
  pythia.readString("MultipartonInteractions:pT0Ref = 2.345");

  auto hadronUserHooks = make_shared<HadronUserHooks>();
  pythia.setUserHooksPtr( hadronUserHooks);

  pythia.readString("Beams:eCM = 7000");

  pythia.init();

  // Collect sum of weights of accepted events.
  double sumW = 0.;
  // Begin event loop.
  for (int iEvent = 0; iEvent < 10000; ++iEvent) {

    // Generate events.
    if (!pythia.next()) continue;
    sumW+=pythia.info.weight();
    double pTmax = 0;
    for (int i = 0, N = pythia.event.size(); i < N; ++i) {
      Particle& p = pythia.event[i];
      if (p.isFinal() && p.isCharged() && abs(p.eta()) < 0.8)
        if (p.pT() > pTmax) pTmax = p.pT();
    }
    leadingTrack.fill(pTmax);
  // End of event loop.
  }

  // Statistics.
  pythia.stat();
  leadingTrack/=sumW;
  HistPlot hpl("test333plot");
  hpl.frame("fig", "Leading track pT", "$p_{\\perp}$", "Prob");
  hpl.add( leadingTrack, "-,black" , "");
  hpl.plot();
  // Done.
  return 0;
}
