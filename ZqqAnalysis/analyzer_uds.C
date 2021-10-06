// studying Zuds events to study the distribution of the jets - multiplicities of the categories being used in the network
// also makes pie charts of the jet distribution - jet flavours are the ones you get from jettagging tool in FCCAnalyses, not MC truth
// no cuts

#include <iostream>
#include <cmath>
#include <vector>

#include <TObject.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include "ROOT/RVec.hxx"
#include <TFile.h>
#include <TTree.h>
#include <TH1I.h>
#include <TPie.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <TSystem.h>
#include <TInterpreter.h>

using namespace std;

int main()
{
  gInterpreter->GenerateDictionary("vector<vector<int> >","vector");

  TFile *file = TFile::Open("p8_ee_Zuds_ecm91.root");
  TTreeReader tree("events", file);
  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  // All particles                                                       
  /*
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpx(tree, "MC_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpy(tree, "MC_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpz(tree, "MC_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCe(tree, "MC_e");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpdg(tree, "MC_pdg");
  */
  // final particles   
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpxF(tree, "MC_px_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpyF(tree, "MC_py_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpzF(tree, "MC_pz_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCeF(tree, "MC_e_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpdgF(tree, "MC_pdg_f");

  //jet constituents      
  TTreeReaderValue<vector<vector<int>>> jetConst(tree, "jetconstituents_ee_kt");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_ee_kt_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_ee_kt_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_ee_kt_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree, "jets_ee_kt_e");
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_ee_kt_flavour");

  TString histfname;
  histfname = "histZuds.root";
  TFile histFile(histfname,"RECREATE");

  // hists for the particle loop
  
  // hists for final particles
  
  // hists for the jet loop
  
  // hists for the jet constituents
  
  TH1I* h_nKl = new TH1I("h_nKl", "No. of K_{L} in jets", 8, 0, 8);
  TH1I* h_nN = new TH1I("h_nN", "No. of n in jets", 8, 0, 8);
  TH1I* h_nLambda = new TH1I("h_nLambda", "No. of #Lambda in jets", 5, 0, 5);
  TH1I* h_nSigma = new TH1I("h_nSigma", "No. of #Sigma in jets", 5, 0, 5);
  TH1I* h_nKs = new TH1I("h_nKs", "No. of k_{S} in jets", 5, 0, 5);
  TH1I* h_nE = new TH1I("h_nE", "No. of e in jets", 8, 0, 8);
  TH1I* h_nMu = new TH1I("h_nMu", "No. of #mu in jets", 5, 0, 5);
  TH1I* h_nPhoton = new TH1I("h_nPhoton", "No. of #gamma in jets", 45, 0, 45);

  TH1I* h_nNu = new TH1I("h_nNu", "No. of #nu in jets", 7, 0, 7);
  
  // event counter
  int evt = 0;

  // flavour counter
  int nU=0, nD=0, nS=0;

  // particle counters
  double nPiS=0, nKS=0, nKlS=0, nNS=0, nPS=0, nLeptonS=0, nPhotonS=0, nOthersS=0;
  double nPiD=0, nKD=0, nKlD=0, nND=0, nPD=0, nLeptonD=0, nPhotonD=0, nOthersD=0;
  double nPiU=0, nKU=0, nKlU=0, nNU=0, nPU=0, nLeptonU=0, nPhotonU=0, nOthersU=0;

  int nNu_max=0, nNuS=0, nNuD=0, nNuU=0;

  // event loop
  while(tree.Next())
    {
      if(evt%10000==0) cout<<evt<<" events processed"<<endl<<"jet flavours: "<<jetFlavour->at(0)<<" & "<<jetFlavour->at(1)<<endl;

      // Neutrinos
      int nNu=0;
      for(unsigned int iNu=0; iNu<MCpdgF->size(); iNu++)
	{
	  if(abs(MCpdgF->at(iNu)) == 12 || abs(MCpdgF->at(iNu)) == 14 || abs(MCpdgF->at(iNu)) == 16) nNu++;
	}
      h_nNu->Fill(nNu);
      if(nNu>nNu_max) nNu_max=nNu;

      // extract jet constituents
      //int nJetC = jetConst->size();
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;

      // only use events with both jets tagged as s, d, or u (to avoid having to loop over jets)
      // s-jets
      if(jetFlavour->at(0)==3 && jetFlavour->at(1)==3)
	{
	  nS++;

	  for(int ipar=0; ipar<MCpdgF->size(); ipar++)
	    {
	      if(abs(MCpdgF->at(ipar))==211) nPiS++;
	      if(abs(MCpdgF->at(ipar))==321) nKS++;
	      //if(abs(MCpdgF->at(ipar))==310) nKsS++;
	      if(abs(MCpdgF->at(ipar))==130) nKlS++;
	      if(abs(MCpdgF->at(ipar))==2212) nPS++;
	      if(abs(MCpdgF->at(ipar))==2112) nNS++;
	      //if(abs(MCpdgF->at(ipar))==3122) nNSBS++;
	      //if(abs(MCpdgF->at(ipar))==3212) nNSBS++;
	      if(abs(MCpdgF->at(ipar))==11) nLeptonS++;
	      if(abs(MCpdgF->at(ipar))==13) nLeptonS++;
	      if(abs(MCpdgF->at(ipar))==22) nPhotonS++;

	      if(abs(MCpdgF->at(ipar)) == 12 || abs(MCpdgF->at(ipar)) == 14 || abs(MCpdgF->at(ipar)) == 16) nNuS++;
	    }

	  // add all final particles to get the total and subtract all the categories outside the event loop
	  nOthersS += MCpdgF->size();
	}

      // u-jets
      if(jetFlavour->at(0)==2 && jetFlavour->at(1)==2)
	{
	  nU++;

	  for(int ipar=0; ipar<MCpdgF->size(); ipar++)
	    {
	      if(abs(MCpdgF->at(ipar))==211) nPiU++;
	      if(abs(MCpdgF->at(ipar))==321) nKU++;
	      //if(abs(MCpdgF->at(ipar))==310) nKsU++;
	      if(abs(MCpdgF->at(ipar))==130) nKlU++;
	      if(abs(MCpdgF->at(ipar))==2212) nPU++;
	      if(abs(MCpdgF->at(ipar))==2112) nNU++;
	      //if(abs(MCpdgF->at(ipar))==3122) nNSBU++;
	      //if(abs(MCpdgF->at(ipar))==3212) nNSBU++;
	      if(abs(MCpdgF->at(ipar))==11) nLeptonU++;
	      if(abs(MCpdgF->at(ipar))==13) nLeptonU++;
	      if(abs(MCpdgF->at(ipar))==22) nPhotonU++;

	      if(abs(MCpdgF->at(ipar)) == 12 || abs(MCpdgF->at(ipar)) == 14 || abs(MCpdgF->at(ipar)) == 16) nNuU++;
	    }

	  nOthersU += MCpdgF->size();
	}

      // d-jets
      if(jetFlavour->at(0)==1 && jetFlavour->at(1)==1)
	{
	  nD++;

	  for(int ipar=0; ipar<MCpdgF->size(); ipar++)
	    {
	      if(abs(MCpdgF->at(ipar))==211) nPiD++;
	      if(abs(MCpdgF->at(ipar))==321) nKD++;
	      //if(abs(MCpdgF->at(ipar))==310) nKsD++;
	      if(abs(MCpdgF->at(ipar))==130) nKlD++;
	      if(abs(MCpdgF->at(ipar))==2212) nPD++;
	      if(abs(MCpdgF->at(ipar))==2112) nND++;
	      //if(abs(MCpdgF->at(ipar))==3122) nNSBD++;
	      //if(abs(MCpdgF->at(ipar))==3212) nNSBD++;
	      if(abs(MCpdgF->at(ipar))==11) nLeptonD++;
	      if(abs(MCpdgF->at(ipar))==13) nLeptonD++;
	      if(abs(MCpdgF->at(ipar))==22) nPhotonD++;

	      if(abs(MCpdgF->at(ipar)) == 12 || abs(MCpdgF->at(ipar)) == 14 || abs(MCpdgF->at(ipar)) == 16) nNuD++;
	    }

	  nOthersD += MCpdgF->size();
	}

      // without discriminating among uds

      // JET 1
      int nKl=0, nN=0, nKs=0, nLambda=0, nSigma=0, nE=0, nMu=0, nPhoton=0;
      
      for(int ele : jet1Const) 
	{
	  if(abs(MCpdgF->at(ele))==130) nKl++;
	  if(abs(MCpdgF->at(ele))==2112) nN++;
	  if(abs(MCpdgF->at(ele))==310) nKs++;
	  if(abs(MCpdgF->at(ele))==3122) nLambda++;
	  if(abs(MCpdgF->at(ele))==3212) nSigma++;
	  if(abs(MCpdgF->at(ele))==11) nE++;
	  if(abs(MCpdgF->at(ele))==13) nMu++;
	  if(abs(MCpdgF->at(ele))==22) nPhoton++;
	}
            
      h_nKl->Fill(nKl);
      h_nN->Fill(nN);
      h_nKs->Fill(nKs);
      h_nLambda->Fill(nLambda);
      h_nSigma->Fill(nSigma);
      h_nE->Fill(nE);
      h_nMu->Fill(nMu);
      h_nPhoton->Fill(nPhoton);
      
      // JET 2
      // need counts for each jet separately so zeroed all counters
      nKl=0, nN=0, nKs=0, nLambda=0, nSigma=0, nE=0, nMu=0, nPhoton=0;
      
      for(int ele : jet2Const) 
	{
	  if(abs(MCpdgF->at(ele))==130) nKl++;
	  if(abs(MCpdgF->at(ele))==2112) nN++;
	  if(abs(MCpdgF->at(ele))==310) nKs++;
	  if(abs(MCpdgF->at(ele))==3122) nLambda++;
	  if(abs(MCpdgF->at(ele))==3212) nSigma++;
	  if(abs(MCpdgF->at(ele))==11) nE++;
	  if(abs(MCpdgF->at(ele))==13) nMu++;
	  if(abs(MCpdgF->at(ele))==22) nPhoton++;
	}
      
      h_nKl->Fill(nKl);
      h_nN->Fill(nN);
      h_nKs->Fill(nKs);
      h_nLambda->Fill(nLambda);
      h_nSigma->Fill(nSigma);
      h_nE->Fill(nE);
      h_nMu->Fill(nMu);
      h_nPhoton->Fill(nPhoton);
      
      jet1Const.clear();
      jet2Const.clear();

      evt++;
    }

  cout<<"processed all events"<<endl;

  cout<<"There are "<<nS<<" events with both jets tagged as s"<<endl;
  cout<<"There are "<<nD<<" events with both jets tagged as d"<<endl;
  cout<<"There are "<<nU<<" events with both jets tagged as u"<<endl;

  cout<<"Max number of neutrinos per event among "<< nEvents <<" events is "<<nNu_max<<endl;

  // subtract all categories from the total and put in "others" category- expecting it to contain only neutrinos [yes, they are]
  nOthersS = nOthersS -nPiS-nKS-nKlS-nPS-nNS-nLeptonS-nPhotonS;
  nOthersU = nOthersU -nPiU-nKU-nKlU-nPU-nNU-nLeptonU-nPhotonU;
  nOthersD = nOthersD -nPiD-nKD-nKlD-nPD-nND-nLeptonD-nPhotonD;

  cout<<"Number of neutrinos in events with both s-jets is "<<nNuS<<endl;
  cout<<"Number of neutrinos in events with both d-jets is "<<nNuD<<endl;
  cout<<"Number of neutrinos in events with both u-jets is "<<nNuU<<endl;

  cout<<"Other particles in events with both s-jets is "<<nOthersS<<endl;
  cout<<"Other particles in events with both d-jets is "<<nOthersD<<endl;
  cout<<"Other particles in events with both u-jets is "<<nOthersU<<endl;

  double valsS[] = {nPiS,nKS,nKlS,nPS,nNS,nLeptonS,nPhotonS};
  double valsD[] = {nPiD,nKD,nKlD,nPD,nND,nLeptonD,nPhotonD};
  double valsU[] = {nPiU,nKU,nKlU,nPU,nNU,nLeptonU,nPhotonU};
  int colors[] = {46,32,42,9,34,45,38};
  int nvals = sizeof(valsS)/sizeof(valsS[0]);
  //const char labels[] = {"#pi^{+-}","K^{+-}","K_{S}","K_{L}","p","n","NSB","e^{+-}","#mu^{+-}","#gamma"};
  
  // pie charts
  TPie* sJets = new TPie("sJets","distribution of s-jets",nvals,valsS,colors);
  TPie* dJets = new TPie("dJets","distribution of d-jets",nvals,valsD,colors);
  TPie* uJets = new TPie("uJets","distribution of u-jets",nvals,valsU,colors);

  cout<<"made pie charts"<<endl;

  file->Close();

  h_nKl->Write();
  h_nN->Write();
  h_nKs->Write();
  h_nLambda->Write();
  h_nSigma->Write();
  h_nE->Write();
  h_nMu->Write();
  h_nPhoton->Write();
  h_nNu->Write();
  sJets->Write();
  dJets->Write();
  uJets->Write();
  histFile.Close();
  cout<<"hists written and file closed"<<endl;

  //delete jetConst;
  //jetConst = NULL;

  return -1;
}
