// studying Zuds events to study the distribution of the jets - multiplicities of the categories being used in the network
// also makes pie charts of the jet distribution - jet flavours are the MC truth flavours
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

  cout<<"MC Truth Tagging"<<endl;
  cout<<"================"<<endl;

  TFile *file = TFile::Open("p8_ee_Zuds_ecm91.root");
  TTreeReader tree("events", file);
  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  // All particles                                                       
  
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpx(tree, "MC_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpy(tree, "MC_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpz(tree, "MC_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCe(tree, "MC_e");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpdg(tree, "MC_pdg");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCstatus(tree, "MC_status");
  
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
  //TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_ee_kt_flavour");

  TString histfname;
  histfname = "histZuds_truthtag.root";
  TFile histFile(histfname,"RECREATE");
  
  // event counter
  int evt = 0;

  // jet flavour counters
  int nS=0, nU=0, nD=0;

  // particle counters
  double nPiS=0, nKS=0, nKlS=0, nNS=0, nPS=0, nLeptonS=0, nPhotonS=0, nOthersS=0;
  double nPiD=0, nKD=0, nKlD=0, nND=0, nPD=0, nLeptonD=0, nPhotonD=0, nOthersD=0;
  double nPiU=0, nKU=0, nKlU=0, nNU=0, nPU=0, nLeptonU=0, nPhotonU=0, nOthersU=0;

  // event loop
  while(tree.Next())
    {
      if(evt%10000==0) cout<<evt<<" events processed"<<endl;

      vector<int> jetFlavour;

      for(unsigned int ipar=0; ipar<MCpdg->size(); ipar++)
	{
	  if(MCstatus->at(ipar)==23) jetFlavour.push_back(MCpdg->at(ipar));
	}

      if(abs(jetFlavour[0])==3) nS += jetFlavour.size();
      if(abs(jetFlavour[0])==1) nD += jetFlavour.size();
      if(abs(jetFlavour[0])==2) nU += jetFlavour.size();

      // extract jet constituents
      //int nJetC = jetConst->size();
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;
      
      // JET 1
      for(int ele : jet1Const) 
	{
	  if(abs(jetFlavour[0])==3)
	    {
	      if(abs(MCpdgF->at(ele))==211) nPiS++;
	      if(abs(MCpdgF->at(ele))==321) nKS++;
	      //if(abs(MCpdgF->at(ele))==310) nKsS++;
	      if(abs(MCpdgF->at(ele))==130) nKlS++;
	      if(abs(MCpdgF->at(ele))==2212) nPS++;
	      if(abs(MCpdgF->at(ele))==2112) nNS++;
	      //if(abs(MCpdgF->at(ele))==3122) nNSBS++;
	      //if(abs(MCpdgF->at(ele))==3212) nNSBS++;
	      if(abs(MCpdgF->at(ele))==11) nLeptonS++;
	      if(abs(MCpdgF->at(ele))==13) nLeptonS++;
	      if(abs(MCpdgF->at(ele))==22) nPhotonS++;
	    }

	  if(abs(jetFlavour[0])==1)
	    {
	      if(abs(MCpdgF->at(ele))==211) nPiD++;
	      if(abs(MCpdgF->at(ele))==321) nKD++;
	      //if(abs(MCpdgF->at(ele))==310) nKsD++;
	      if(abs(MCpdgF->at(ele))==130) nKlD++;
	      if(abs(MCpdgF->at(ele))==2212) nPD++;
	      if(abs(MCpdgF->at(ele))==2112) nND++;
	      //if(abs(MCpdgF->at(ele))==3122) nNSBD++;
	      //if(abs(MCpdgF->at(ele))==3212) nNSBD++;
	      if(abs(MCpdgF->at(ele))==11) nLeptonD++;
	      if(abs(MCpdgF->at(ele))==13) nLeptonD++;
	      if(abs(MCpdgF->at(ele))==22) nPhotonD++;
	    }

	  if(abs(jetFlavour[0])==2)
	    {
	      if(abs(MCpdgF->at(ele))==211) nPiU++;
	      if(abs(MCpdgF->at(ele))==321) nKU++;
	      //if(abs(MCpdgF->at(ele))==310) nKsU++;
	      if(abs(MCpdgF->at(ele))==130) nKlU++;
	      if(abs(MCpdgF->at(ele))==2212) nPU++;
	      if(abs(MCpdgF->at(ele))==2112) nNU++;
	      //if(abs(MCpdgF->at(ele))==3122) nNSBU++;
	      //if(abs(MCpdgF->at(ele))==3212) nNSBU++;
	      if(abs(MCpdgF->at(ele))==11) nLeptonU++;
	      if(abs(MCpdgF->at(ele))==13) nLeptonU++;
	      if(abs(MCpdgF->at(ele))==22) nPhotonU++;
	    }
	}
      
      // JET 2
      for(int ele : jet2Const) 
	{
	  if(abs(jetFlavour[1])==3)
	    {
	      if(abs(MCpdgF->at(ele))==211) nPiS++;
	      if(abs(MCpdgF->at(ele))==321) nKS++;
	      //if(abs(MCpdgF->at(ele))==310) nKsS++;
	      if(abs(MCpdgF->at(ele))==130) nKlS++;
	      if(abs(MCpdgF->at(ele))==2212) nPS++;
	      if(abs(MCpdgF->at(ele))==2112) nNS++;
	      //if(abs(MCpdgF->at(ele))==3122) nNSBS++;
	      //if(abs(MCpdgF->at(ele))==3212) nNSBS++;
	      if(abs(MCpdgF->at(ele))==11) nLeptonS++;
	      if(abs(MCpdgF->at(ele))==13) nLeptonS++;
	      if(abs(MCpdgF->at(ele))==22) nPhotonS++;
	    }

	  if(abs(jetFlavour[1])==1)
	    {
	      if(abs(MCpdgF->at(ele))==211) nPiD++;
	      if(abs(MCpdgF->at(ele))==321) nKD++;
	      //if(abs(MCpdgF->at(ele))==310) nKsD++;
	      if(abs(MCpdgF->at(ele))==130) nKlD++;
	      if(abs(MCpdgF->at(ele))==2212) nPD++;
	      if(abs(MCpdgF->at(ele))==2112) nND++;
	      //if(abs(MCpdgF->at(ele))==3122) nNSBD++;
	      //if(abs(MCpdgF->at(ele))==3212) nNSBD++;
	      if(abs(MCpdgF->at(ele))==11) nLeptonD++;
	      if(abs(MCpdgF->at(ele))==13) nLeptonD++;
	      if(abs(MCpdgF->at(ele))==22) nPhotonD++;
	    }

	  if(abs(jetFlavour[1])==2)
	    {
	      if(abs(MCpdgF->at(ele))==211) nPiU++;
	      if(abs(MCpdgF->at(ele))==321) nKU++;
	      //if(abs(MCpdgF->at(ele))==310) nKsU++;
	      if(abs(MCpdgF->at(ele))==130) nKlU++;
	      if(abs(MCpdgF->at(ele))==2212) nPU++;
	      if(abs(MCpdgF->at(ele))==2112) nNU++;
	      //if(abs(MCpdgF->at(ele))==3122) nNSBU++;
	      //if(abs(MCpdgF->at(ele))==3212) nNSBU++;
	      if(abs(MCpdgF->at(ele))==11) nLeptonU++;
	      if(abs(MCpdgF->at(ele))==13) nLeptonU++;
	      if(abs(MCpdgF->at(ele))==22) nPhotonU++;
	    }
	}
      
      jet1Const.clear();
      jet2Const.clear();
      jetFlavour.clear();

      evt++;
    }

  cout<<"processed all events"<<endl;

  cout<<"There are "<<nS<<" true s-jets"<<endl;
  cout<<"There are "<<nD<<" true d-jets"<<endl;
  cout<<"There are "<<nU<<" true u-jets"<<endl;
  cout<<"All summed together give "<<nS+nD+nU<<" , which is twice the number of events: "<<2*nEvents<<endl;

  // subtract all categories from the total and put in "others" category- expecting it to contain only neutrinos [yes, they are]
  //nOthersS = nOthersS -nPiS-nKS-nKlS-nPS-nNS-nLeptonS-nPhotonS;
  //nOthersU = nOthersU -nPiU-nKU-nKlU-nPU-nNU-nLeptonU-nPhotonU;
  //nOthersD = nOthersD -nPiD-nKD-nKlD-nPD-nND-nLeptonD-nPhotonD;
  
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

  sJets->Write();
  dJets->Write();
  uJets->Write();
  histFile.Close();
  cout<<"pie charts written and file closed"<<endl;

  //delete jetConst;
  //jetConst = NULL;

  return -1;
}
