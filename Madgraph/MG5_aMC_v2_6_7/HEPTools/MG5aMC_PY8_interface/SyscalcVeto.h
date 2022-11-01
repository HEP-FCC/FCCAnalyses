
class SyscalcVeto {

public:

  SyscalcVeto(){ slowJet = NULL; };
 ~SyscalcVeto(){};

  bool doVetoProcessLevel(const Event& eventProcessSubset, double pTjetMin);

  bool doShowerKtVeto(
    const Event & eventProcessSubset,
    double qCut,
    bool exclusive,
    double pTfirst);

  int matchPartonsToJetsLight( 
    const Event & eventProcessSubset, 
    const Event & workEventJet,
    double qCut,
    bool exclusive,
    vector<double> DJR);

  bool prepare(
    SlowJet* slowJetPtrIn,
    ParticleData* particleDataPtrIn );

  SlowJet* slowJet;
  ParticleData* particleDataPtr;

  enum vetoStatus { NONE, LESS_JETS, MORE_JETS, HARD_JET, UNMATCHED_PARTON,
    SMIN_FAIL, SMAXGTSCOMP_FAIL };


  double smin() { return sminSave;}
  double smax() { return smaxSave;}
  double scomp() { return scompSave;}

  double sminSave,smaxSave,scompSave;

};


bool SyscalcVeto::prepare( SlowJet* slowJetPtrIn,
  ParticleData* particleDataPtrIn ) {
  slowJet = slowJetPtrIn;
  particleDataPtr = particleDataPtrIn;
  sminSave = smaxSave = scompSave = 0.;
  return true;
}

//--------------------------------------------------------------------------

bool SyscalcVeto::doVetoProcessLevel(const Event& eventProcessSubset, 
  double pTjetMin){

    // Initialize SlowJet jet algorithm with current working event
    if (!slowJet->setup(eventProcessSubset) ) {
      return false;
    }

    // Cluster in steps to find all hadronic jets at the scale qCutME
    while ( slowJet->sizeAll() - slowJet->sizeJet() > 0 ) {
      // Done if next step is above qCut
      if( slowJet->dNext() > pow2(pTjetMin) ) break;
      slowJet->doStep();
    }

    if (slowJet->sizeAll()-slowJet->sizeJet() < eventProcessSubset.size() ) {
      return true;
    }

    return false;

}

//--------------------------------------------------------------------------

bool SyscalcVeto::doShowerKtVeto(const Event & eventProcessSubset, double qCut, bool exclusive, double pTfirst) {

  // Structure:
  //
  // Get smax = pTfirst from workEvent.
  // Get nPartons from eventProcessSubset.size()
  // Get smin = pTminME from eventProcessSubset
  // Get scomp = pTminME or qCut from input
  // Get "exclusive" from input.

  int nParton = eventProcessSubset.size();
  double pTminME=1e10;
  //double localQcutSq = qCut*qCut;
  for ( int i = 0; i < nParton; ++i) pTminME = min(pTminME,eventProcessSubset[i].pT());

  // Postpone the veto until later!
  //if ( nParton > 0 && pow(pTminME,2) < localQcutSq ) {
  //  sminSave=-1;
  //  return true;
  //}
  //
  //// For non-highest multiplicity, veto if the hardest emission is harder
  //// than Qcut.
  //if ( exclusive && pow(pTfirst,2) > localQcutSq ) {
  //  sminSave=-1;
  //  return true;
  //// For highest multiplicity sample, veto if the hardest emission is harder
  //// than the hard process parton.
  //} else if ( !exclusive && nParton > 0 && pTfirst > pTminME ) {
  //  sminSave=-1;
  //  return true;
  //}

  sminSave=pTminME;
  smaxSave=pTfirst;
  if(exclusive){scompSave=qCut;}
  else if (nParton > 0) {scompSave=pTminME;}
  else {scompSave=10000000000000;}

  return false;
}

int SyscalcVeto::matchPartonsToJetsLight( 
  const Event & eventProcessSubset, 
  const Event & workEventJet, double qCut, bool exclusive, vector<double> DJR ) {

  double localQcutSq = qCut*qCut;
  int nParton = eventProcessSubset.size();
  sminSave=0.0;
  smaxSave=0.0;
  scompSave=qCut;
  double pTminME=1e10;


  for ( int i = 0; i < nParton; ++i){
    pTminME = min(pTminME,eventProcessSubset[i].pT());
  }

  // scomp: quantity which represent the ME/PS cutoff.
  // Definition varies depending on the case
  // a) Qcut for exclusive case
  // b) pt of the softest ME radiation for inclusive case with more than 1 parton
  // c) infinity for inclusive and 0-parton case.

  if(exclusive){		scompSave=qCut;}
  else if (nParton>0){	scompSave=pTminME;} 
  else{					scompSave= 10000000000;}
  
  // smin: quantity which represents the softest ME radiation scale
  // and must be compared with the merging scale (Qcut)
  // a) infinity if no parton (no ME radiation)
  // b) Clustering scale d(nParton->nParton-1). 
  // one remark, we use DJR[nParton-1] because of the 
  // first vector index which is equal to zero.
  if (nParton==0) { 
    sminSave=100000000000;
  } else {
    if (int(DJR.size()) >= nParton) sminSave=DJR[nParton-1];
  }
  
  if(sminSave < qCut ) {
	sminSave=-2.0; // will fail when scanning the Qcut choices	
	return SMIN_FAIL;
  }
  // smax: quantity which represents the hardest emission from the parton shower.
  // First, initialize slowJet on the list of showered partons
  if (!slowJet->setup(workEventJet) ) {
      cout << "Warning in JetMatchingMadgraph:matchPartonsToJetsLight: the SlowJet algorithm failed on setup" << endl;
      return NONE;
    }

  int nCjets=0;
//  double dOld = 0.0
  // Cluster in steps to find all hadronic jets at the scale qCut
  while ( slowJet->sizeAll() - slowJet->sizeJet() > 0 ) {
    if( slowJet->dNext() > localQcutSq ) break;
//    dOld = slowJet->dNext();
    slowJet->doStep();
  }
  int nJets = slowJet->sizeJet();
  int nClus = slowJet->sizeAll();
  nCjets=nClus-nJets;
    // If the number of partons (nParton) is larger than zero, recluster in steps to find 
    // all hadronic jets at the scale Y(nParton-1).
  if(nParton>0){
        double dNow = int(DJR.size()) >= nParton ? pow(DJR[nParton],2) : 0.0;
        while ( slowJet->sizeAll() - slowJet->sizeJet() > 0 ) {
        	if(slowJet->dNext() > dNow ) break;
        	slowJet->doStep();
  	}
	nCjets = slowJet->sizeAll() - slowJet->sizeJet();
  }

 // Now decides what value to assign to smax:
 // a) either Y(nParton-1) if the number of remaining hadronic jets is >0
 // and if not the highest partonic multiplicity
 // b) scomp if inclusive or no hadronic jet left
  if(nCjets>0 && exclusive){
        smaxSave = int(DJR.size()) > nParton ? DJR[nParton] : 0.0;
  }
  else{
        smaxSave=scompSave;
  }


  // Get number of partons. Different for MLM and FxFx schemes.
  int nRequested = nParton;
/*  if ( exclusive ) {
//    ;
  } else {*/

    // Now continue in inclusive mode.
    // In inclusive mode, there can be more hadronic jets than partons,
    // provided that all partons are properly matched to hadronic jets.
    // Start by setting up the jet algorithm.
    if (!slowJet->setup(workEventJet) ) {
      return NONE;
    }

    while ( slowJet->sizeAll() - slowJet->sizeJet() > nParton ){
      slowJet->doStep();
    }

    nJets = slowJet->sizeJet();
    nClus = slowJet->sizeAll();
//}

// only needed for special scale rescaling factor?
//  // Update scale if clustering factor is non-zero
//  if ( clFact != 0. ) localQcutSq *= pow2(clFact);


  Event tempEvent;
  tempEvent.init( "(tempEvent)", particleDataPtr);
  int nPass = 0;
  double pTminEstimate = -1.;
  // Construct a master copy of the event containing only the
  // hardest nParton hadronic clusters. While constructing the event,
  // the parton type (21) and status (98,99) are arbitrary.
  for (int i = nJets; i < nClus; ++i) {
    tempEvent.append( 21, 98, 0, 0, 0, 0, 0, 0, slowJet->p(i).px(),
      slowJet->p(i).py(), slowJet->p(i).pz(), slowJet->p(i).e() );
    ++nPass;
    pTminEstimate = max( pTminEstimate, slowJet->pT(i));
    if(nPass == nRequested) break;
  }
  int tempSize = tempEvent.size();
  // This keeps track of which hadronic jets are matched to parton
  vector<bool> jetAssigned;
  jetAssigned.assign( tempSize, false);

  // Do jet matching for MLM.
  // Take the list of unmatched hadronic jets and append a parton, one at
  // a time. The parton will be clustered with the "closest" hadronic jet
  // or the beam if the distance measure is below the cut. When a hadronic
  // jet is matched to a parton, it is removed from the list of unmatched
  // hadronic jets. This process continues until all hadronic jets are
  // matched to partons or it is not possible to make a match.
  int iNow = 0;
  while (iNow < nParton ) {
    Event tempEventJet;
    tempEventJet.init("(tempEventJet)", particleDataPtr);
    for (int i = 0; i < tempSize; ++i) {
      if (jetAssigned[i]) continue;
      Vec4 pIn = tempEvent[i].p();
      // Append unmatched hadronic jets
      tempEventJet.append( 21, 98, 0, 0, 0, 0, 0, 0,
        pIn.px(), pIn.py(), pIn.pz(), pIn.e() );
    }
    Vec4 pIn = eventProcessSubset[iNow].p();
    // Append the current parton
    tempEventJet.append( 21, 99, 0, 0, 0, 0, 0, 0,
      pIn.px(), pIn.py(), pIn.pz(), pIn.e() );

    if (!slowJet->setup(tempEventJet) ) {
       return NONE;
    }
    if ( slowJet->iNext() == tempEventJet.size() - 1 && slowJet->jNext() > -1){
          smaxSave=max(smaxSave,sqrt(slowJet->dNext()));
          int iKnt = -1;
          for (int i = 0; i != tempSize; ++i) {
            if (jetAssigned[i]) continue;
            ++iKnt;
            // Identify the hadronic jet that matches the parton
            if (iKnt == slowJet->jNext() ) jetAssigned[i] = true;
    }
  } else {
     sminSave=-1;
     return UNMATCHED_PARTON;
  }
   
    ++iNow;
  }

// not needed!
//  // Minimal eT/pT (CellJet/SlowJet) of matched light jets.
//  // Needed later for heavy jet vetos in inclusive mode.
//  // This information is not used currently.
//  if (nParton > 0 && pTminEstimate > 0) eTpTlightMin = pTminEstimate;
//  else eTpTlightMin = -1.;
 
  //// Record smin, scomp and smax. 
  //// To use these numbers with an a posteriori-chosen merging scale (postQcut),
  //// apply a weight 1 to events with smin>postQcut && smax<max(postQcut,scomp).
  //// Make sure that this routine is used with a minimal Qcut, so that postQcut can hold any value > Qcut. 
  //SetSNumbers(smin,smax,scomp);
  //// Reset the clustering scales.
  //SetDJR(workEventJet);

  // No veto
  return NONE;


}

