// studying the performance of jet tagging algorithm used in FCCAnalyses by analysing the angular distributions of jets, partons and their ngular separations
// also separates the u/d/s events plus gets the statistics of the 3
// Note: planning to use the MC truth parton for the label instead of the output of jettagging tool from FCCAnalyses - debatable
// still don't understand the distributions entirely
// No cuts

#include <iostream>
#include <cmath>
#include <vector>

#include <TObject.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include "ROOT/RVec.hxx"
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
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

  // jet constituents      
  TTreeReaderValue<vector<vector<int>>> jetConst(tree, "jetconstituents_ee_kt");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_ee_kt_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_ee_kt_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_ee_kt_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree, "jets_ee_kt_e");
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_ee_kt_flavour");

  TString histfname;
  histfname = "histZuds_jettagging.root";
  TFile histFile(histfname,"RECREATE");

  // histograms
  TH1F* h_angJP = new TH1F("h_angJP","Angle between the parton and the corresponding jet",100,0,1.6);
  TH1F* h_angJPs = new TH1F("h_angJPs","Angle between the parton and the corresponding jet (s-jets)",100,0,1.6);
  TH1F* h_angJPd = new TH1F("h_angJPd","Angle between the parton and the corresponding jet (d-jets)",100,0,1.6);
  TH1F* h_angJPu = new TH1F("h_angJPu","Angle between the parton and the corresponding jet (u-jets)",100,0,1.6);

  // event counter
  int evt = 0;

  // flavour counter
  int s_jets=0, u_jets=0, d_jets=0;
       
  // event loop
  while(tree.Next())
    {
      if(evt%10000==0) cout<<evt<<" events processed"<<endl;

      // jet loop
      float px_Jet=0, py_Jet=0, pz_Jet=0, e_Jet=0; // partons
      TLorentzVector p4_Jet[2];
      for(unsigned int ij=0 ; ij<jetE->size(); ij++)
	{
	  px_Jet = jetPx->at(ij);
	  py_Jet = jetPy->at(ij);
	  pz_Jet = jetPz->at(ij);
	  e_Jet = jetE->at(ij);
	  p4_Jet[ij].SetPxPyPzE(px_Jet,py_Jet,pz_Jet,e_Jet);
	}

      // particle loop
      float px_p=0, py_p=0, pz_p=0, e_p=0; // partons
      TLorentzVector p4_p[2];
      //int flavour[2];
      float angJ1=0,angJ2=0; // angles between the jets and partons
      int iq=0; // parton counter
      for(unsigned int ip=0; ip<MCpdg->size(); ip++)
	{
	  if(MCstatus->at(ip)<20 || MCstatus->at(ip)>30) continue;
	  if(abs(MCpdg->at(ip))!=3 && abs(MCpdg->at(ip))!=2 && abs(MCpdg->at(ip))!=1) continue;
	  
	  px_p = MCpx->at(ip);
	  py_p = MCpy->at(ip);
	  pz_p = MCpz->at(ip);
	  e_p = MCe->at(ip);
	  p4_p[iq].SetPxPyPzE(px_p,py_p,pz_p,e_p);

	  // angle between the jet and the parton
	  angJ1 = p4_p[iq].Angle(p4_Jet[0].Vect());
	  angJ2 = p4_p[iq].Angle(p4_Jet[1].Vect());
	  h_angJP->Fill(min(angJ1,angJ2));
	  if(abs(MCpdg->at(ip))==3)
	    {
	      h_angJPs->Fill(min(angJ1,angJ2));
	      s_jets++;
	    }
	  if(abs(MCpdg->at(ip))==1)
	    {
	      h_angJPd->Fill(min(angJ1,angJ2));
	      d_jets++;
	    }
	  if(abs(MCpdg->at(ip))==2)
	    {
	      h_angJPu->Fill(min(angJ1,angJ2));
	      u_jets++;
	    }

	  iq++;
	}

      evt++;
    }

  cout<<"processed all events"<<endl<<"there are "<<s_jets<<" s-jets, "<<d_jets<<" d-jets, and "<<u_jets<<" u-jets"<<endl;

  file->Close();
  cout<<"closed the event file"<<endl;

  h_angJP->Write();
  h_angJPs->Write();
  h_angJPd->Write();
  h_angJPu->Write();
  histFile.Close();
  cout<<"hists written and file closed"<<endl;

  //delete jetConst;
  //jetConst = NULL;

  return -1;
}
