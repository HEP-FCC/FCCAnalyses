// This program is written by Stefan Prestel and developed as part
// of the work presented in ref. hep-ph:xxx-yyy
// 
// It is used by MG5aMC to shower with PY8 the LesHouches events it generates.
// The operational modes of this interface are:
// a) Non-matched/non-merged events
// b) MLM jet-matched events (kT-MLM, shower-kT, FxFx)
// c) CKKW-L and UMEPS-merged events
// d) UNLOPS NLO merged events

#include "Pythia8Plugins/HepMC2.h"
#include "Pythia8/Pythia.h"
#include <unistd.h>

// Include UserHooks for Jet Matching.
#include "Pythia8Plugins/CombineMatchingInput.h"
// Include UserHooks for randomly choosing between integrated and
// non-integrated treatment for unitarised merging.
#include "Pythia8Plugins/aMCatNLOHooks.h"

using namespace Pythia8;

#include "SyscalcVeto.h"
#include "MultiHist.h"

// Function implementing the CKKWL veto.
double ckkwlWeight( int nHard, double tmsHard,
  int nJetsNow, int nJetMax, double tmsNow, double tms) {

  // Reject event because hard process does not pass the merging scale cut.
  if (nHard > 0 && tmsHard < tms) return 0.0;

  // Reject event because first emission is too hard.
  if (nJetsNow < nJetMax && tmsNow > tms) return 0.0;

  // Accept event.
  return 1.0;

}

// Function implementing the MLM veto.
double mlmWeight( double smin, double smax, double scomp, double qCut) {

  // Reject event.
  if(qCut > smin || smax > max(qCut, scomp)) return 0.0;

  // Accept event.
  return 1.0;

}

// Function to reject unnecessary weight groups
bool allowWeightgroup(string name) {
  // Dummy statement to avoid compiler warnings.
  if (false) cout << name << endl;
  // Examples how to disregard a weightgroup
  //if (name.compare("Central scale variation") == 0) return false;
  //if (name.compare("Emission scale variation") == 0) return false;
  //if (name.compare("CT10nlo") == 0) return false;
  return true;
}

// Function to convert aMC@NLO weight names to "HepMC convention".
string convertFromAMCATNLO( string input) {
  string output="";
  // Count number of blanks in weight name.
  int appearances = 0;
  for(int n = input.find(" ", 0); n != int(string::npos);
          n = input.find(" ", n)) {
    appearances++;
    n++;
  }
  // Cut string by position of blanks.
  vector <string> pieces;
  for(int i =0; i < appearances;++i) {
    int n = input.find(" ", 0);
    pieces.push_back(input.substr(0,n));
    input = input.substr(n+1,input.size());
  }
  // Now pieces contains the details of the weight name.
  for(int i = 4; i < int(pieces.size()); ++i) {
    // Make upper case.
    transform(pieces[i].begin(),pieces[i].end(),pieces[i].begin(), ::toupper);
    // Add piece to weight name, with "_" as separator.
    output+=pieces[i] + "_";
  }
  return output;
}

//==========================================================================

// Example main programm to illustrate merging.

int main( int argc, char* argv[] ){

  // Check that correct number of command-line arguments
  if (argc < 2) {
    cerr << " Unexpected number of command-line arguments ("<<argc<<"). \n"
         << " You are expected to provide the arguments" << endl
         << " 1. Input file for settings" << endl
         << " Program stopped. " << endl;
    return 1;
  }

  Pythia pythia;

  // New setting to allow processing of multiple input LHEFs.
  pythia.settings.addMode("LHEFInputs:nSubruns",0,true,false,0,100);
  pythia.settings.addWord("HEPMCoutput:file","void");
  pythia.settings.addParm("HEPMCoutput:scaling",1.0,true,false,0.,0.);

  pythia.settings.addWord("HistFile:name","");

  // BEGIN aMC_MG5-specific code.
  // Add an input setting for many cut values.
  vector<double> defaults;
  defaults.resize(10,0.0);
  pythia.settings.addPVec("Syscalc:qCutList",defaults,false,false,0.,0.);
  pythia.settings.addPVec("Syscalc:tmsList",defaults,false,false,0.,0.);
  pythia.settings.addFlag("Syscalc:fullCutVariation",false);
  pythia.settings.addParm("SysCalc:qWeed",0.0,true,false,0.,0.);
  // END aMC_MG5-specific code.

  // Input parameters:
  pythia.readFile(argv[1],0);

  string hepmcfile = pythia.settings.word("HEPMCoutput:file");
  bool hasHepMC =
    !(pythia.settings.word("HEPMCoutput:file").compare("void")==0);
  if (!hasHepMC) hepmcfile= "/dev/null";
  if (hepmcfile == "/dev/null") hasHepMC = false;

  // Get number of subruns.
  int nRun = pythia.mode("LHEFInputs:nSubruns");

  // Interface for conversion from Pythia8::Event to HepMC one.
  HepMC::Pythia8ToHepMC ToHepMC;
  // Specify file where HepMC events will be stored.
  HepMC::IO_GenEvent evt(hepmcfile, std::ios::out);
  // Switch off warnings for parton-level events.
  ToHepMC.set_print_inconsistency(false);
  ToHepMC.set_free_parton_exception(false);
  // Do not store cross section information, as this will be done manually.
  ToHepMC.set_store_pdf(false);
  ToHepMC.set_store_proc(false);
  ToHepMC.set_store_xsec(false);

  // Check if jet matching should be applied.
  bool doMatch   = pythia.settings.flag("JetMatching:merge");

  // Check if internal merging should be applied.
  bool doMerge   =
    !(pythia.settings.word("Merging:Process").compare("void")==0);

  // Currently, only one scheme at a time is allowed.
  if (doMatch && doMerge) {
    cerr << " Jet matching and merging cannot be used simultaneously.\n"
         << " Program stopped.";
  }

  // BEGIN comment of aMC_MG5-specific code.
  // For jet matching, initialise the respective user hooks code.
  //CombineMatchingInput* combined = NULL;
  //UserHooks* matching            = NULL;
  // END comment of aMC_MG5-specific code.

  // BEGIN aMC_MG5-specific code.
  shared_ptr<JetMatchingMadgraph> matching;
  // END aMC_MG5-specific code.

  // Allow to set the number of addtional partons dynamically.
  shared_ptr<amcnlo_unitarised_interface> setting;
  if ( doMerge ) {
    // Store merging scheme.
    int scheme = ( pythia.settings.flag("Merging:doUMEPSTree")
                || pythia.settings.flag("Merging:doUMEPSSubt")) ?
                1 :
                 ( ( pythia.settings.flag("Merging:doUNLOPSTree")
                || pythia.settings.flag("Merging:doUNLOPSSubt")
                || pythia.settings.flag("Merging:doUNLOPSLoop")
                || pythia.settings.flag("Merging:doUNLOPSSubtNLO")) ?
                2 :
                0 );
    setting = make_shared<amcnlo_unitarised_interface>(scheme);
    pythia.setUserHooksPtr(setting);
  }

  // For jet matching, initialise the respective user hooks code.
  if (doMatch) {
    // BEGIN comment of aMC_MG5-specific code.
    //matching = combined->getHook(pythia);
    // END comment of aMC_MG5-specific code.

    // BEGIN aMC_MG5-specific code.
    matching = make_shared<JetMatchingMadgraph>();
    // END aMC_MG5-specific code.

    if (!matching) {
      cerr << " Failed to initialise jet matching structures.\n"
           << " Program stopped.";
      return 1;
    }
    pythia.setUserHooksPtr(matching);
  }

  // BEGIN aMC_MG5-specific code.
  // Initialise DJR-histograms. These histograms are used as quick check
  // of the quality of the merging.
  vector< vector< MultiHist > > d01_multiweight, d12_multiweight,
                                d23_multiweight, d34_multiweight;
  vector< vector< MultiHist > > pt1_multiweight, pt2_multiweight,
                                pt3_multiweight, pt4_multiweight;
  vector<int> nJetsInRun;
  bool fullCutVariation = pythia.settings.flag("Syscalc:fullCutVariation");

  // Specify files where HepMC events will be stored.
#ifndef HEPMC2HACK
  double nMaxFiles = 20;
  vector< HepMC::IO_GenEvent* > ev;
#endif

  // Cross section an error.
  vector<vector<double> > sigmaTot;
  vector<vector<double> > errorTot;
  // Headers for output files.
  vector<string> headers;
  vector<vector<string> > xsecnames;

  // Store number of events.
  vector<int> nEvents;

  for (int iRun=0; iRun < nRun; ++iRun){

    // Read in name of LHE file for current subrun and initialize.
    pythia.readFile(argv[1], iRun);

    // If the process string is "guess", temporarily set it to something safe
    // for initialization.
    if (doMerge && pythia.settings.word("Merging:process") == "guess")
      pythia.settings.word("Merging:process","pp>e+e-");

    // Initialise.
    pythia.init();

    // Reset the process string to "guess" if necessary.
    if (doMerge && pythia.settings.word("Merging:process") == "guess")
      pythia.settings.word("Merging:process","guess");


    int nEvent = pythia.settings.mode("Main:numberOfEvents");

    // Get the number of events by pre-parsing the lhe if it is negative
    // otherwise take the user-input value as it is
    if (nEvent < 1) {
      cout << "Counting events in input LHEF, please wait." << endl;
      // File reader.
      Reader reader(pythia.word("Beams:LHEF"));
      long nEventNow = 0;
      // Read each event and write them out again, also in reclustered form. 
      while ( reader.readEvent() ) ++nEventNow;
      nEvents.push_back(nEventNow);
      cout << "Found " << nEventNow << " events in input LHEF." << endl;
    } else {
      cout << "Considering "<< nEvent <<" events. Make sure that there is"
            <<" enough events in the input event files, otherwise "
            <<" normalization is likely to be wrong."<<endl;
       nEvents.push_back(nEvent);
    }

    // Get maximal number of partons in the input. This will set the number
    // of sub-histograms that will sum to the full inclusive MLM-matched result.
    int nJets = 0;
    if (doMatch) nJets = pythia.settings.mode("JetMatching:nJetMax");
    else {
      // Default to tree-level CKKW-L counting.
      nJets = pythia.settings.mode("Merging:nJetMax");

      if (pythia.settings.flag("Merging:doUMEPSSubt") )
        nJets = pythia.settings.mode("Merging:nJetMax")-1;
      if ( pythia.settings.flag("Merging:doUNLOPSSubt") )
        nJets = pythia.settings.mode("Merging:nJetMax")-1;
      if ( pythia.settings.flag("Merging:doUNLOPSLoop") )
        nJets = pythia.settings.mode("Merging:nJetMaxNLO");
      if ( pythia.settings.flag("Merging:doUNLOPSSubtNLO") )
        nJets = pythia.settings.mode("Merging:nJetMaxNLO")-1;
    }

    nJetsInRun.push_back(nJets);

    // Get "central" cut.
    double cut = (doMatch)
               ? pythia.settings.parm("JetMatching:qCut")
               : (doMerge) ? pythia.settings.parm("Merging:TMS") : 0.0;

    // Multiple cut values.
    vector<double> cuts;
    cuts.push_back(cut);
    vector<double> cutValues =
      (doMatch) ? pythia.settings.pvec("Syscalc:qCutList")
         : (doMerge) ? pythia.settings.pvec("Syscalc:tmsList")
           : vector<double>();
    for (int iCut = 0; iCut < int(cutValues.size()); ++iCut)
      if (cutValues[iCut] > 0.0) cuts.push_back(cutValues[iCut]);

    vector<string> xsecnamesNow;
    vector<double> sigmaTotNow;
    vector<double> errorTotNow;

    // Construct a header for the run
    ostringstream head;
    head << " xmin; xmax; Weight";
    head << "_MERGING=" << cut << ";";
    ostringstream xsname;
    xsname << "Weight_MERGING=" << cut;
    //xsecnames.push_back(xsname.str());
    xsecnamesNow.push_back(xsname.str());
    head << " WeightError;";
    for (int iCut = 1; iCut < int(cuts.size()); ++iCut) {
      head << " Weight";
      head << "_MERGING=" << cuts[iCut] << ";";
      ostringstream xsn;
      xsn << "Weight_MERGING=" << cuts[iCut];
      //xsecnames.push_back(xsn.str());
      xsecnamesNow.push_back(xsn.str());
    }

    // Count number of histograms.
    int nhist = 0;
    // First count the cut variation for the event weight.
    nhist    += cuts.size();
    // Now count additional weights in acceptable weightgruops,
    // possibly for a series of cut values.
    //if (pythia.info.rwgt && pythia.info.weights_detailed) { 
    if (pythia.info.weightgroups) { 
      // Loop through cuts.
      for (int iCut = 0; iCut < int(cuts.size()); ++iCut) {
        // Do nothing fore restricted set of variations.
        if (iCut > 0 && !fullCutVariation) continue;
        // Loop through weightgroups.
        for ( std::map<std::string,LHAweightgroup>::const_iterator
          it_wg  = pythia.info.weightgroups->begin();
          it_wg != pythia.info.weightgroups->end(); ++it_wg ) {
          // Only count allowed weightgroups.
          if (!allowWeightgroup(it_wg->first)) continue;
          // Loop through weights in the weightgroup.
          for ( std::map<std::string,LHAweight>::const_iterator
            it_w  = it_wg->second.weights.begin();
            it_w != it_wg->second.weights.end();    ++it_w ) {
            // Increase the number of histograms.
            nhist++;
            // Get name.
            string name;
            for ( std::map<string,string>::const_iterator
              it_att  = it_w->second.attributes.begin();
              it_att != it_w->second.attributes.end();    ++it_att)
              name += it_att->first + "=" + it_att->second + "_";

            // In aMC@NLO, the weight names should be extracted from the
            // weight tag contents, not its attributes.
            if (it_w->second.attributes.size()==0)
              name = convertFromAMCATNLO(it_w->second.contents);

            head << " " << name << "MERGING=" << cuts[iCut] << ";";
            ostringstream xsn;
            xsn << name << "MERGING=" << cuts[iCut];
            xsecnamesNow.push_back(xsn.str());
          } // Done looping through weights.
        } // Done looping through weight groups.
      } // Done looping through cuts.
    }
    headers.push_back(head.str());

    // Prepare book-keeping of cross sections and event files.
    for (int i=0; i < nhist; ++i) {
      sigmaTotNow.push_back(0.0);
      errorTotNow.push_back(0.0);
#ifndef HEPMC2HACK
      // Create multiple output HepMC files.
      if (i >= nMaxFiles ) continue;
      ostringstream c; c << i;
	  string newfile;
	  if (i == 0) {
        newfile = (hasHepMC) ? hepmcfile : "/dev/null";
	  } else {
        newfile = (hasHepMC) ? hepmcfile + c.str() : "/dev/null";
	  }
      ev.push_back( new HepMC::IO_GenEvent(newfile, std::ios::out));
#endif
    }

    // Dummy temporary map.
    vector< MultiHist > d01_temp, d12_temp, d23_temp, d34_temp;
    vector< MultiHist > pt1_temp, pt2_temp, pt3_temp, pt4_temp;

    for (int j=0; j <= nJets; ++j){
      // Dummy temporary map.
      d01_temp.push_back(MultiHist("d01",100.,0.,3.,nhist));
      d12_temp.push_back(MultiHist("d12",100.,0.,3.,nhist));
      d23_temp.push_back(MultiHist("d23",100.,0.,3.,nhist));
      d34_temp.push_back(MultiHist("d34",100.,0.,3.,nhist));
      pt1_temp.push_back(MultiHist("pt1",100.,0.,1000.,nhist));
      pt2_temp.push_back(MultiHist("pt2",100.,0.,1000.,nhist));
      pt3_temp.push_back(MultiHist("pt3",100.,0.,500.,nhist));
      pt4_temp.push_back(MultiHist("pt4",100.,0.,500.,nhist));
    }

    // Store histograms.
    d01_multiweight.push_back(d01_temp);
    d12_multiweight.push_back(d12_temp);
    d23_multiweight.push_back(d23_temp);
    d34_multiweight.push_back(d34_temp);
    pt1_multiweight.push_back(pt1_temp);
    pt2_multiweight.push_back(pt2_temp);
    pt3_multiweight.push_back(pt3_temp);
    pt4_multiweight.push_back(pt4_temp);

    sigmaTot.push_back(sigmaTotNow);
    errorTot.push_back(errorTotNow);
    xsecnames.push_back(xsecnamesNow);

  }
  // END aMC_MG5-specific code.

  // Jet finder for some of the histograms.
  double ptprint = pythia.settings.parm("Syscalc:qWeed");
  //double ptmin = (doMerge) ? pythia.settings.parm("Merging:TMS") : 10.0;
  SlowJet* slowJet = new SlowJet(1, 0.4, ptprint, 4.4, 2, 2, NULL, false);

  // Cross section an error.
  double sigmaTotal = 0.;
  double errorTotal = 0.;

  cout << endl << endl << endl;
  cout << "Start generating events" << endl;

  bool doInternalMLMvetoes = pythia.settings.flag("JetMatching:doVeto");
  bool doShowerKt = pythia.settings.flag("JetMatching:doShowerKt");
  SyscalcVeto* syscalc = NULL;
  if (!doInternalMLMvetoes) syscalc = new SyscalcVeto();

  bool doInternalCKKWLvetoes = pythia.settings.flag("Merging:applyVeto");

  // Loop over subruns with varying number of jets.
  for (int iRun = 0; iRun < nRun; ++iRun) {

    // Cross section an error.
    double sigmaSample = 0.;
    double errorSample = 0.;

    // Read in name of LHE file for current subrun and initialize.
    pythia.readFile(argv[1], iRun);

    // If the process string is "guess", temporarily set it to something safe
    // for initialization.
    if (doMerge && pythia.settings.word("Merging:process") == "guess")
      pythia.settings.word("Merging:process","pp>e+e-");

    // Initialise.
    pythia.init();

    // Reset the process string to "guess" if necessary.
    if (doMerge && pythia.settings.word("Merging:process") == "guess")
      pythia.settings.word("Merging:process","guess");

    // Prepare syscalcveto.
    if ( doMatch && !doInternalMLMvetoes)
      syscalc->prepare( matching->slowJetDJR, &pythia.particleData);

    // Get the inclusive x-section by summing over all process x-sections.
    double xs = 0.;
    for (int i=0; i < pythia.info.nProcessesLHEF(); ++i)
      xs += pythia.info.sigmaLHEF(i);

    // Additional user-defined scaling factor for weights printed into HEPMC
    // events. This is useful if users do not want the output events to be
    // normalized in milli-barn.
    double hepmcWeightRescaling = pythia.settings.parm("HEPMCOutput:scaling");

    // Get "central" cut.
    double cut = (doMatch)
               ? pythia.settings.parm("JetMatching:qCut")
               : (doMerge) ? pythia.settings.parm("Merging:TMS") : 0.0;

    // Multiple cut values.
    vector<double> cuts;
    cuts.push_back(cut);
    vector<double> cutValues =
      (doMatch) ? pythia.settings.pvec("Syscalc:qCutList")
         : (doMerge) ? pythia.settings.pvec("Syscalc:tmsList")
           : vector<double>();
    for (int iCut = 0; iCut < int(cutValues.size()); ++iCut)
      if (cutValues[iCut] > 0.0) cuts.push_back(cutValues[iCut]);

    // Check number of events.
    int nEvent = pythia.settings.mode("Main:numberOfEvents");	
    if (nEvent < 1) {
      nEvent = nEvents[iRun];
    } else if (nEvent > nEvents[iRun]) {
      cout << "Warning in MG5aMC_PY8_interface.cc: Required " << nEvent << " events,"
           << " while LHEF contained only " << nEvents[iRun] << " events."
           << " Normalisation of the events likely to be be corrupted." << endl;
    }

    // Start generation loop
    while( pythia.info.nSelected() < nEvent ){

        // Generate next event
        if( !pythia.next() ) {

        if( pythia.info.atEndOfFile() ) {
          if (pythia.info.nSelected() < nEvent){
              cerr << "WARNING in MG5aMC_PY8_interface.cc: Reached end of LHEF "
                   << " after " << pythia.info.nSelected()
                   <<" Normalisation will be decreased by" << (pythia.info.nSelected() - nEvent)/(nEvent*0.010)<<"%."
                   << endl;
          }
	      if ((pythia.info.nSelected() - nEvent)/(1.0*nEvent) > 0.02){ 
		    cerr << "ERROR: More than 2% of the events fails to be showered by pythia. Stopping" << endl;
            exit(1);
	      }
          break;
        }
        else continue;
      }

      double norm_event_wgt = xs / double(1e9*nEvent);
      if ( abs(pythia.info.lhaStrategy()) == 4)
        norm_event_wgt = 1 / double(1e9*nEvent);

      double central_weight = pythia.info.weight();
      // Additional PDF/alphaS weight for internal merging.
      double merging_weight = 1.;
      if (doMerge) merging_weight  *= pythia.info.mergingWeightNLO()
      // Additional weight due to random choice of reclustered/non-reclustered
      // treatment. Also contains additional sign for subtractive samples.
                                    * setting->getNormFactor();
      central_weight *= merging_weight;

      bool printEvent = true;

      if (doMatch && !doInternalMLMvetoes) {
        // record mlm vetoes.
        bool exclusive = matching->getExclusive();
        double pTfirst = matching->getPTfirst();
        vector<double> djr = matching->getDJR();

        // Weeding of events with very small parton separation, which 
        // would yield a vanishing weight, and thus might not be desirable 
        // print-out because of file size issues.
        printEvent = !syscalc->doVetoProcessLevel(matching->getProcessSubset(),
                                                  ptprint);

        // Find minimal cut value, used to calculate smin, smax, scomp. 
        double qCutMin = 1e15;
        for (int iCut = 0; iCut < int(cuts.size()); ++iCut )
          qCutMin = min(qCutMin,cuts[iCut]);
        if (ptprint > 0.0) qCutMin = min(qCutMin, ptprint);

        if(doShowerKt){
          syscalc->doShowerKtVeto( matching->getProcessSubset(),
            qCutMin, exclusive, pTfirst);
        } else {
          syscalc->matchPartonsToJetsLight( matching->getProcessSubset(),
            matching->getWorkEventJet(), qCutMin, exclusive, djr);
        }

      } else if (doMerge && !doInternalCKKWLvetoes) {

        // Weeding of events with very small parton separation, which 
        // would yield a vanishing weight, and thus might not be desirable 
        // print-out because of file size issues.
        double tmsnow = pythia.mergingHooksPtr->tmsNow(
          pythia.mergingHooksPtr->bareEvent(pythia.process,false)); 
        printEvent = (tmsnow > ptprint); 
        if (pythia.mergingHooksPtr->nHardNow() == 0 ) printEvent = true;

      }

      if (!printEvent) continue;

      // Handling of multiple cut values.
      vector<double> vetoWeights;
      // Multiple cut values for MLM.
      if (doMatch && !doInternalMLMvetoes) {
        // Check multiple vetoes.
        for (int iCut = 0; iCut < int(cuts.size()); ++iCut) {
          // Check veto, store veto weight.
          vetoWeights.push_back( mlmWeight( 
                                   syscalc->smin(),
                                   syscalc->smax(),
                                   syscalc->scomp(),
                                   cuts[iCut]));
        }

      // Multiple cut values for CKKWL.
      } else if (doMerge && !doInternalCKKWLvetoes){
        // Check multiple vetoes.
        for (int iCut = 0; iCut < int(cuts.size()); ++iCut) {
          // Check veto, store veto weight.
          vetoWeights.push_back( ckkwlWeight( 
                                   pythia.mergingHooksPtr->nHardNow(),
                                   pythia.mergingHooksPtr->tmsHardNow(),
                                   pythia.mergingHooksPtr->nJetsNow(),
                                   pythia.mergingHooksPtr->nMaxJets(),
                                   pythia.mergingHooksPtr->tmsNow(),
                                   cuts[iCut]));
        }

      // No multiple values for everything else so far.
      } else {
        for (int iCut = 0; iCut < int(cuts.size()); ++iCut)
          vetoWeights.push_back(1.0);
      }

      // Add the weight of the current event to the cross section.
      sigmaTotal  += central_weight*norm_event_wgt;
      sigmaSample += central_weight*norm_event_wgt;
      errorTotal  += pow2(central_weight*norm_event_wgt);
      errorSample += pow2(central_weight*norm_event_wgt);

#ifdef HEPMC2HACK

      // Construct new empty HepMC event.
      HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
      hepmcevt->set_signal_process_id(pythia.info.code());
      // Attach weight of central prediction to HepMC event.
      for (int iCut = 0; iCut < int(vetoWeights.size()); ++iCut) {
        ostringstream convert;
        convert << fixed << setprecision(3) << cuts[iCut];
        string cutTag = "_MERGING=" + convert.str();
        double w = central_weight*norm_event_wgt*vetoWeights[iCut];
        w *=hepmcWeightRescaling;
        // Attach new weight to HepMC event.
        hepmcevt->weights().push_back(w, "Weight"+cutTag);
        // Update cross section.
        sigmaTot[iRun][iCut] += w;
        errorTot[iRun][iCut] += pow2(w);
      } // Done looping through cuts.

      // Get additional LHEF v3 event weight information, directly from
      // the iterator, and fill the event weights.
      if (pythia.info.rwgt ) { 
        int nWeights = pythia.info.initrwgt->size();
        // Loop through cuts.
        for (int iCut = 0; iCut < int(vetoWeights.size()); ++iCut) {
          // Do nothing fore restricted set of variations.
          if (iCut > 0 && !fullCutVariation) continue;
          int k = iCut*nWeights + int(vetoWeights.size());
          ostringstream convert;
          convert << fixed << setprecision(3) << cuts[iCut];
          string cutTag = "MERGING=" + convert.str();
          // Loop through weightgroups.
          for ( std::map<std::string,LHAweightgroup>::const_iterator
            it_wg  = pythia.info.weightgroups->begin();
            it_wg != pythia.info.weightgroups->end(); ++it_wg ) {

            if (!allowWeightgroup(it_wg->first)) continue;

            // Loop through weights in the weightgroup.
            for ( std::map<std::string,LHAweight>::const_iterator
              it_w  = it_wg->second.weights.begin();
              it_w != it_wg->second.weights.end();    ++it_w ) {
              // Get value of weight indexed by the present key.
              std::map<std::string,double>::const_iterator it_value
                = pythia.info.weights_detailed->find(it_w->first);
              double w = it_value->second*merging_weight*vetoWeights[iCut];
              // Get name.
              string name;
              for ( std::map<string,string>::const_iterator
                it_att  = it_w->second.attributes.begin();
                it_att != it_w->second.attributes.end();    ++it_att)
                name += it_att->first + "=" + it_att->second + "_";

              // In aMC@NLO, the weight names should be extracted from the
              // weight tag contents, not its attributes.
              if (it_w->second.attributes.size()==0)
                name = convertFromAMCATNLO(it_w->second.contents);

              if (pythia.info.lhaStrategy() == 3)
                w *= norm_event_wgt / pythia.info.eventWeightLHEF;
              // Weighted events.
              else w *= 1 / double(1e9*nEvent);

              w *=hepmcWeightRescaling;

              // Add event weight.
              hepmcevt->weights().push_back(w, name+cutTag);
              // Update cross section.

              sigmaTot[iRun][k] += w;
              errorTot[iRun][k] += pow2(w);
              k++;
            } // Done looping through weights.
          } // Done looping through weight groups.
        } // Done looping through cuts.
      }

      // Here attach three syscalc numbers to end of weights.
      // smin, smax, scomp
      if (doMatch && !doInternalMLMvetoes) {
        // In HepMC, "weights" is a map, which means that it will internally
        // always be ordered as below (because of the string key comparison
        // operator). Thus, we have to either live with this ordering, or
        // encode smin, smax, scomp cleverly...
        ostringstream convert;
        convert << scientific << setprecision(10) << syscalc->scomp();
        string tag = "scomp=" + convert.str();
        hepmcevt->weights().push_back(syscalc->scomp(), tag);
        convert.str("");
        convert << scientific << setprecision(10) << syscalc->smax();
        tag = "smax=" + convert.str();
        hepmcevt->weights().push_back(syscalc->smax(), tag);
        convert.str("");
        convert << scientific << setprecision(10) << syscalc->smin();
        tag = "smin=" + convert.str();
        hepmcevt->weights().push_back(syscalc->smin(), tag);
      }

      // Fill HepMC event
      ToHepMC.fill_next_event( pythia, hepmcevt );

      // Report cross section calculated from central weights to hepmc.
      // This cross section is only correct for the central weight, i.e. if
      // this is used (by e.g. Rivet) to set the normalisation of a plot for an
      // additional weight, this will not give the correct result.
      HepMC::GenCrossSection xsec;
      xsec.set_cross_section( sigmaTotal*1e9,
        pythia.info.sigmaErr()*1e9 );
      hepmcevt->set_cross_section( xsec );
      // Write the HepMC event to file. Done with it.
      if (printEvent) evt << hepmcevt;
      delete hepmcevt;

#else

      // Write HepMC events.
      for (int iCut = 0; iCut < int(vetoWeights.size()); ++iCut) {
        if (iCut >= nMaxFiles ) break;
        HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
	hepmcevt->set_signal_process_id(pythia.info.code());

        // Set event weight
        double w = central_weight*norm_event_wgt*vetoWeights[iCut];
        w *=hepmcWeightRescaling;
        hepmcevt->weights().push_back(w);
        // Fill HepMC event
        ToHepMC.fill_next_event( pythia, hepmcevt );
        // Add the weight of the current event to the cross section.
        sigmaTot[iRun][iCut]  += w;
        errorTot[iRun][iCut]  += pow2(w);
        // Report cross section to hepmc
        HepMC::GenCrossSection xsec;
        //xsec.set_cross_section( sigmaTot[iCut]*1e9,
        xsec.set_cross_section( sigmaTot[iRun][iCut]*1e9,
          pythia.info.sigmaErr()*1e9 );
        hepmcevt->set_cross_section( xsec );
        // Write the HepMC event to file. Done with it.
        if (printEvent) *ev[iCut] << hepmcevt;
        delete hepmcevt;
      }

      // Get additional LHEF v3 event weight information, directly from
      // the iterator, and fill the events.
      if (pythia.info.rwgt ) { 
        int nWeights = pythia.info.initrwgt->size();
        // Loop through cuts.
        for (int iCut = 0; iCut < int(vetoWeights.size()); ++iCut) {
          // Do nothing fore restricted set of variations.
          if (iCut > 0 && !fullCutVariation) continue;
          int k = iCut*nWeights + int(vetoWeights.size());
          // Loop through weightgroups.
          for ( std::map<std::string,LHAweightgroup>::const_iterator
            it_wg  = pythia.info.weightgroups->begin();
            it_wg != pythia.info.weightgroups->end(); ++it_wg ) {

            if (!allowWeightgroup(it_wg->first)) continue;

            // Loop through weights in the weightgroup.
            for ( std::map<std::string,LHAweight>::const_iterator
              it_w  = it_wg->second.weights.begin();
              it_w != it_wg->second.weights.end();    ++it_w ) {
              // Get value of weight indexed by the present key.
              std::map<std::string,double>::const_iterator it_value
                = pythia.info.weights_detailed->find(it_w->first);
              double w = it_value->second*merging_weight*vetoWeights[iCut];
              if (pythia.info.lhaStrategy() == 3)
                w *= norm_event_wgt / pythia.info.eventWeightLHEF;
              // Weighted events.
              else w *= 1 / double(1e9*nEvent);
              // Fill events.
              if (k >= nMaxFiles ) break;
              HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
              // Set event weight
              w *=hepmcWeightRescaling;
              hepmcevt->weights().push_back(w);
              // Fill HepMC event
              ToHepMC.fill_next_event( pythia, hepmcevt );
              // Add the weight of the current event to the cross section.
              sigmaTot[iRun][k]  += w;
              errorTot[iRun][k]  += pow2(w);
              // Report cross section to hepmc
              HepMC::GenCrossSection xsec;
              xsec.set_cross_section( sigmaTot[iRun][k]*1e9,
                pythia.info.sigmaErr()*1e9 );
              hepmcevt->set_cross_section( xsec );
              // Write the HepMC event to file. Done with it.
              if (printEvent) *ev[k] << hepmcevt;
              delete hepmcevt;
              k++;
            } // Done looping through weights.
          } // Done looping through weight groups.
        } // Done looping through cuts.
      }

#endif

      // BEGIN aMC_MG5-specific code.

      // Now calculate all the jet separations. Note: For kt-MLM, the
      // output will not strictly coincide with the jet separations used
      // in the jet matching procedure - which are kt-MLM-specific. Here,
      // we want an observable that is defined identically for all merging
      // schemes, including stand-alone Pytiha8 runs.

      int njetNow = 0;
      vector<double> dijVec;
      // Construct input for jet algorithm.
      Event jetInput;
      jetInput.init("jet input",&pythia.particleData);
      jetInput.clear();
      for (int i =0; i < pythia.event.size(); ++i)
        if (  pythia.event[i].isFinal()
          && (pythia.event[i].colType() != 0 || pythia.event[i].isHadron()))
          jetInput.append(pythia.event[i]);
      slowJet->setup(jetInput);
      // Run jet algorithm.
      vector<double> result;
      while ( slowJet->sizeAll() - slowJet->sizeJet() > 0 ) {
        result.push_back(sqrt(slowJet->dNext()));
        slowJet->doStep();
      }
      // Reorder by decreasing multiplicity.
      for (int i=int(result.size())-1; i >= 0; --i)
        dijVec.push_back(result[i]);

      // Now get the "number of partons" in the input event, so that
      // we may tag this event accordingly when histogramming. Note
      // that for MLM jet matching, this might not coincide with the
      // actual number of partons in the input LH event, since some
      // partons may be excluded from the matching.
      if (doMatch && !doShowerKt)
        njetNow = matching->nMEpartons().first;
      else if (doMatch && doShowerKt)
        njetNow = matching->getProcessSubset().size(); 
      else if (doMerge){
        njetNow = pythia.settings.mode("Merging:nRequested");
        if ( pythia.settings.flag("Merging:doUMEPSSubt")
          || pythia.settings.flag("Merging:doUNLOPSSubt")
          || pythia.settings.flag("Merging:doUNLOPSSubtNLO") )
          njetNow--;
      }

      // Inclusive jet pTs as further validation plot.
      vector<double> ptVec;
      // Run jet algorithm.
      slowJet->analyze(jetInput);
      for (int i = 0; i < slowJet->sizeJet(); ++i)
        ptVec.push_back(slowJet->pT(i) );

      // Fill the histograms with the "central" value.
      int ihist = 0;
      for (int iCut = 0; iCut < int(vetoWeights.size()); ++iCut) {
        double w = central_weight*norm_event_wgt*vetoWeights[iCut];

        if (dijVec.size() > 0)
          d01_multiweight[iRun][njetNow].fill(log10(dijVec[0]), w, ihist);
        if (dijVec.size() > 1)
          d12_multiweight[iRun][njetNow].fill(log10(dijVec[1]), w, ihist);
        if (dijVec.size() > 2)
          d23_multiweight[iRun][njetNow].fill(log10(dijVec[2]), w, ihist);
        if (dijVec.size() > 3)
          d34_multiweight[iRun][njetNow].fill(log10(dijVec[3]), w, ihist);

        if (ptVec.size() > 0)
            pt1_multiweight[iRun][njetNow].fill(ptVec[0], w, ihist);
        if (ptVec.size() > 1)
            pt2_multiweight[iRun][njetNow].fill(ptVec[1], w, ihist);
        if (ptVec.size() > 2)
            pt3_multiweight[iRun][njetNow].fill(ptVec[2], w, ihist);
        if (ptVec.size() > 3)
            pt4_multiweight[iRun][njetNow].fill(ptVec[3], w, ihist);

        ihist++;
      } // Done looping through cuts.

      // Get additional LHEF v3 event weight information, directly from
      // the iterator, and fill the additional histograms.
      if (pythia.info.rwgt ) {
        // Loop through cuts.
        for (int iCut = 0; iCut < int(vetoWeights.size()); ++iCut) {
          // Do nothing fore restricted set of variations.
          if (iCut > 0 && !fullCutVariation) continue;
          // Loop through weightgroups.
          for ( std::map<std::string,LHAweightgroup>::const_iterator
            it_wg  = pythia.info.weightgroups->begin();
            it_wg != pythia.info.weightgroups->end(); ++it_wg ) {

            if (!allowWeightgroup(it_wg->first)) continue;

            // Loop through weights in the weightgroup.
            for ( std::map<std::string,LHAweight>::const_iterator
              it_w  = it_wg->second.weights.begin();
              it_w != it_wg->second.weights.end();    ++it_w ) {
              // Get value of weight indexed by the present key.
              std::map<std::string,double>::const_iterator it_value
                = pythia.info.weights_detailed->find(it_w->first);
              double w = it_value->second*merging_weight*vetoWeights[iCut];
              // Ensure correct normalisation.
              // Unweighted events (event weight = 1.0, extra weights O(1))
              // Normalise like the event weight, and divide by "unit weight".
              if (pythia.info.lhaStrategy() == 3)
                w *= norm_event_wgt / pythia.info.eventWeightLHEF;
              // Weighted events.
              else w *= 1 / double(1e9*nEvent);
              // Fill histograms.
              if (dijVec.size() > 0)
                d01_multiweight[iRun][njetNow].fill(log10(dijVec[0]), w, ihist);
              if (dijVec.size() > 1)
                d12_multiweight[iRun][njetNow].fill(log10(dijVec[1]), w, ihist);
              if (dijVec.size() > 2)
                d23_multiweight[iRun][njetNow].fill(log10(dijVec[2]), w, ihist);
              if (dijVec.size() > 3)
                d34_multiweight[iRun][njetNow].fill(log10(dijVec[3]), w, ihist);

              if (ptVec.size() > 0)
                pt1_multiweight[iRun][njetNow].fill(ptVec[0], w, ihist);
              if (ptVec.size() > 1)
                pt2_multiweight[iRun][njetNow].fill(ptVec[1], w, ihist);
              if (ptVec.size() > 2)
                pt3_multiweight[iRun][njetNow].fill(ptVec[2], w, ihist);
              if (ptVec.size() > 3)
                pt4_multiweight[iRun][njetNow].fill(ptVec[3], w, ihist);

              ihist++;
            } // Done looping through weights.
          } // Done looping through weight groups.
        } // Done looping through cuts.
      }
      // END aMC_MG5-specific code.

    } // end loop over events to generate

    // print cross section, errors
    pythia.stat();

    cout << endl << " Contribution of sample " << iRun
         << " to the inclusive cross section : "
         << scientific << setprecision(8)
         << sigmaSample << "  +-  " << sqrt(errorSample)  << endl; 

  }

  cout << endl << endl << endl;
  cout << "Inclusive cross section: " << scientific << setprecision(8)
       << sigmaTotal << "  +-  " << sqrt(errorTotal) << " mb " << endl;
  cout << endl << endl << endl;

  // BEGIN aMC_MG5-specific code.
  // Print histograms.
  ofstream output;
  string name = pythia.settings.word("HistFile:name");
  output.open( (char*)(name + "djrs.dat").c_str());
  output << "<histfile>\n";
  for (int i=0; i < nRun; ++i){

    // Construct a header for the run
    output << "<run id=\"" << i << "\""
           << " header=\"" << headers[i] <<"\">\n";

    // Construct the cross section tags.
    for (int ixs = 0; ixs < int(xsecnames[i].size()); ++ixs) {
      output << "<xsection name=\"" << xsecnames[i][ixs] << "\">";
      output << sigmaTot[i][ixs] << " " << sqrt(errorTot[i][ixs]);
      output << "</xsection>\n";
    }

    // Print histograms.
    int njNow = nJetsInRun[i];
    for (int j=0; j <= njNow; ++j){

      output << "<jethistograms njet=\"" << j << "\">\n";

      output << "<histogram name=\"" << "log10d01" << "\""
        << " unit=\"" << "[]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      d01_multiweight[i][j].table(output, false, false);
      //// Print histogram with over/underflow
      //d01_multiweight[i][j].table(output, true, false);
      output << "</histogram>\n";

      output << "<histogram name=\"" << "log10d12" << "\""
        << " unit=\"" << "[]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      d12_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "<histogram name=\"" << "log10d23" << "\""
        << " unit=\"" << "[]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      d23_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "<histogram name=\"" << "log10d34" << "\""
        << " unit=\"" << "[]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      d34_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "</jethistograms>\n";
    }
    output << "</run>\n";
  }
  output << "</histfile>\n";
  output.close();

  // BEGIN aMC_MG5-specific code.
  // Print histograms.
  name = pythia.settings.word("HistFile:name");
  output.open( (char*)(name + "pts.dat").c_str());
  output << "<histfile>\n";
  for (int i=0; i < nRun; ++i){

    // Construct a header for the run
    output << "<run id=\"" << i << "\""
           << " header=\"" << headers[i] <<"\">\n";

    // Construct the cross section tags.
    for (int ixs = 0; ixs < int(xsecnames[i].size()); ++ixs) {
      output << "<xsection name=\"" << xsecnames[i][ixs] << "\">";
      output << sigmaTot[i][ixs] << " " << sqrt(errorTot[i][ixs]);
      output << "</xsection>\n";
    }

    // Print histograms.
    int njNow = nJetsInRun[i];
    for (int j=0; j <= njNow; ++j){

      output << "<jethistograms njet=\"" << j << "\">\n";

      output << "<histogram name=\"" << "pt1" << "\""
        << " unit=\"" << "[GeV]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      pt1_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "<histogram name=\"" << "pt2" << "\""
        << " unit=\"" << "[GeV]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      pt2_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "<histogram name=\"" << "pt3" << "\""
        << " unit=\"" << "[GeV]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      pt3_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "<histogram name=\"" << "pt4" << "\""
        << " unit=\"" << "[GeV]" << "\""
        << " weight=\"" << "all" << "\">\n";
      // Print histogram without over/underflow
      pt4_multiweight[i][j].table(output, false, false);
      output << "</histogram>\n";

      output << "</jethistograms>\n";
    }
    output << "</run>\n";
  }
  output << "</histfile>\n";
  output.close();

  // END aMC_MG5-specific code.

  // BEGIN aMC_MG5-specific code.
  if (!doInternalMLMvetoes) delete syscalc;
  // END aMC_MG5-specific code.

  // Clean up
#ifndef HEPMC2HACK
  for (unsigned int i=0; i < ev.size(); ++i) delete ev[i];
#endif

  // Done
  return 0;

}
