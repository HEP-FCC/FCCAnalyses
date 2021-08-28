#include <iostream>
#include <cmath>
#include <vector>

#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <TSystem.h>
#include <TInterpreter.h>

using namespace std;

int main()
{
  gInterpreter->GenerateDictionary("vector<vector<int> >","vector");

  TFile* file = new TFile("p8_ee_Zbb_ecm91.root","READ");
  TTree* tree = (TTree*) file->Get("events");
  int nEvents = tree->GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;
  
  TString histfname;
  histfname = "histZbb_jets.root";
  TFile *histFile = new TFile(histfname,"RECREATE");

  TH1D* h_deltaAngKl = new TH1D("h_deltaAngKl","Angle b/n K_{L} and Jet Axis",100,0.,3.15);
  
  vector<float> *MCpxF=0, *MCpyF=0, *MCpzF=0, *MCeF=0, *MCpdgF=0;
  tree->SetBranchAddress("MC_px_f", &MCpxF);
  tree->SetBranchAddress("MC_py_f", &MCpyF);
  tree->SetBranchAddress("MC_pz_f", &MCpzF);
  tree->SetBranchAddress("MC_e_f", &MCeF);
  tree->SetBranchAddress("MC_pdg_f", &MCpdgF);
  
  vector<float> *jetE=0, *jetPx=0, *jetPy=0, *jetPz=0;
  vector<vector<int>> *jetConst;
  //tree->SetBranchAddress("jetconstituents_ee_genkt", &jetConst);
  //tree->SetBranchAddress("jets_ee_genkt_e", &jetE);
  //tree->SetBranchAddress("jets_ee_genkt_px", &jetPx);
  //tree->SetBranchAddress("jets_ee_genkt_py", &jetPy);
  //tree->SetBranchAddress("jets_ee_genkt_pz", &jetPz);

  //tree->SetBranchAddress("jetconstituents_kt", &jetConst);
  //tree->SetBranchAddress("jets_kt_e", &jetE);
  //tree->SetBranchAddress("jets_kt_px", &jetPx);
  //tree->SetBranchAddress("jets_kt_py", &jetPy);
  //tree->SetBranchAddress("jets_kt_pz", &jetPz);

  tree->SetBranchAddress("jetconstituents_ee_kt", &jetConst);
  tree->SetBranchAddress("jets_ee_kt_e", &jetE);
  tree->SetBranchAddress("jets_ee_kt_px", &jetPx);
  tree->SetBranchAddress("jets_ee_kt_py", &jetPy);
  tree->SetBranchAddress("jets_ee_kt_pz", &jetPz);
  
  // event loop
  for(unsigned int evt=0; evt<nEvents; evt++)
    {
      tree->GetEntry(evt);
      /*
      if(evt%10000 == 0)
	{
	  cout<<"Final Particle Indices: ";
	  for(int par=0; par<MCpdgF->size(); par++)
	    {
	      cout<<par<<"\t";
	    }
	  cout<<endl<<"===================="<<endl;
	  cout<<endl<<"Total per event = "<<MCpdgF->size()<<endl<<endl<<"===================="<<endl<<endl;
	}
      */
      double jPx=0., jPy=0., jPz=0., jE=0., invMjet=0.;
      int nJet = jetE->size();
      TLorentzVector p_Jet[nJet], p_Jets;
      
      // jet loop
      for(unsigned int j=0; j<nJet; j++)
	{
	  jE = jetE->at(j);
	  jPx = jetPx->at(j);
	  jPy = jetPy->at(j);
	  jPz = jetPz->at(j);

	  p_Jet[j].SetPxPyPzE(jPx, jPy, jPz, jE);

	  // sum of all jets' momenta
	  p_Jets += p_Jet[j];
	}

      // jet constituents
      //int nJetC = jetConst->size();
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;
      /*cout<<"Jet constituent vector "<<jetConst->size()<<endl;
      cout<<"vector in vector : "<<jet1Const.size()<<endl;
      cout<<"vector in vector : "<<jet2Const.size()<<endl;*/

      // JET 1
      double px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
      TLorentzVector p4_j1;

      double delta_ang1=0.;
      for(int ele : jet1Const)
	{
	  px_j1 = MCpxF->at(ele);
	  py_j1 = MCpyF->at(ele);
	  pz_j1 = MCpzF->at(ele);
	  e_j1 = MCeF->at(ele);

	  p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);

	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130)
	    {
	      delta_ang1 = p4_j1.Angle(p_Jet[0].Vect());
	      h_deltaAngKl->Fill(delta_ang1);
	    }
	}
      
      /*
      if(evt%10000 == 0)
	{
	  cout<<"Jet 1 Constituent Indices: ";
	  for(int ele : jet1Const) 
	    {
	      cout<<ele<<"\t";
	    }
	  cout<<endl<<"=========="<<endl;
	  cout<<endl<<"Total in Jet 1 = "<<jet1Const.size()<<endl<<endl<<"=========="<<endl<<endl;
	}
      */
      
      // JET 2
      double px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      double delta_ang2=0.;
      for(int ele : jet2Const)
	{
	  px_j2 = MCpxF->at(ele);
	  py_j2 = MCpyF->at(ele);
	  pz_j2 = MCpzF->at(ele);
	  e_j2 = MCeF->at(ele);

	  p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);

	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130)
	    {
	      delta_ang2 = p4_j2.Angle(p_Jet[1].Vect());
	      h_deltaAngKl->Fill(delta_ang2);
	    }
	}

      /*
      if(evt%10000 == 0)
	{
	  cout<<"Jet 2 Constituent Indices ";
	  for(int ele : jet2Const) 
	    {
	      cout<<ele<<"\t";
	    }
	  cout<<endl<<"=========="<<endl;
	  cout<<endl<<"Total in Jet 2 = "<<jet2Const.size()<<endl<<endl<<"=========="<<endl<<endl;
	}
      */
      
      jet1Const.clear();
      jet2Const.clear();
    }
      
  histFile->Write();
  histFile->Close();
      
  delete jetConst;
  jetConst = NULL;
  
  file->Close();
  return -1;
}
