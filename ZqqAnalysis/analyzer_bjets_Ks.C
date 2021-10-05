// Studying Ks->pipi in b-jets: Multiplicity, angular distribution, etc
// Wrote for Zbb, changed to Zuds at some point (no idea why)
// No cuts

#include <iostream>
#include <cmath>
#include <vector>

#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TH2.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <TSystem.h>
#include <TInterpreter.h>

using namespace std;

int main()
{
  gInterpreter->GenerateDictionary("vector<vector<int> >","vector");

  TFile* file = new TFile("p8_ee_Zuds_ecm91.root","READ");
  TTree* tree = (TTree*) file->Get("events");
  int nEvents = tree->GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;
  
  TString histfname;
  histfname = "histZuds_Ks.root";
  TFile *histFile = new TFile(histfname,"RECREATE");

  // Hists for jet-constituents' properties
  //TH1D* h_deltaAngKl = new TH1D("h_deltaAngKl","Angle b/n K_{L} and Jet Axis",100,0.,3.15);
  
  // hists for jet angluar distributions
  /*
  TH2D* h_JetCKaonC = new TH2D("h_JetCKaonC","K^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetNKaonC = new TH2D("h_JetNKaonC","K_{L} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetCPionC = new TH2D("h_JetCPionC","#pi^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetElecC = new TH2D("h_JetElecC","e^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetMuonC = new TH2D("h_JetMuonC","#mu^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetPhotC = new TH2D("h_JetPhotC","#gamma in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetProtC = new TH2D("h_JetProtC","p in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetNeutC = new TH2D("h_JetNeutC","n in c jets",29,-0.5,0.5,29,-0.5,0.5);
  */
  TH1D* h_Ks2pipi = new TH1D("h_Ks2pipi","K_{S} #rightarrow #pi^{+}#pi^{-}",100,-0.9,0.1);
  TH1D* h_nKs = new TH1D("h_nKs","Number of K_{S} #rightarrow #pi^{+}#pi^{-}",5,0,5);
  TH1D* h_KsAngJ1 = new TH1D("h_KsAngJ1","Angle b/n K_{S} and jet1",100,0.,3.15);
  TH1D* h_KsAngJ2 = new TH1D("h_KsAngJ2","Angle b/n K_{S} and jet2",100,0.,3.15);
  
  vector<float> *MCpxF=0, *MCpyF=0, *MCpzF=0, *MCeF=0, *MCpdgF=0;
  tree->SetBranchAddress("MC_px_f", &MCpxF);
  tree->SetBranchAddress("MC_py_f", &MCpyF);
  tree->SetBranchAddress("MC_pz_f", &MCpzF);
  tree->SetBranchAddress("MC_e_f", &MCeF);
  tree->SetBranchAddress("MC_pdg_f", &MCpdgF);

  vector<float> *MCpx=0, *MCpy=0, *MCpz=0, *MCe=0, *MCpdg=0;
  tree->SetBranchAddress("MC_px", &MCpx);
  tree->SetBranchAddress("MC_py", &MCpy);
  tree->SetBranchAddress("MC_pz", &MCpz);
  tree->SetBranchAddress("MC_e", &MCe);
  tree->SetBranchAddress("MC_pdg", &MCpdg);

  vector<int> *Ks2pipi=0;
  tree->SetBranchAddress("K0spipi_indices", &Ks2pipi);
  
  vector<float> *jetE=0, *jetPx=0, *jetPy=0, *jetPz=0;
  //vector<vector<int>> *jetConst;
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

  //tree->SetBranchAddress("jetconstituents_ee_kt", &jetConst);
  tree->SetBranchAddress("jets_ee_kt_e", &jetE);
  tree->SetBranchAddress("jets_ee_kt_px", &jetPx);
  tree->SetBranchAddress("jets_ee_kt_py", &jetPy);
  tree->SetBranchAddress("jets_ee_kt_pz", &jetPz);
  
  // event loop
  for(unsigned int evt=0; evt<nEvents; evt++)
    {
      tree->GetEntry(evt);
      
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

      double mKs = 0.;
      double mpipi = 0.;
      TLorentzVector p4, p_pi;
      double px=0, py=0, pz=0, e=0;
      int nKs = 0;
      double KsAngJ1 = 0., KsAngJ2 = 0.;
      // Ks2pipi loop
      for(int iPi = 0; iPi<Ks2pipi->size(); iPi++)
	{
	  //cout<<"Idices of Ks and pi+-: "<<Ks2pipi->at(iPi)<<endl;
	  px = MCpx->at(iPi);
	  py = MCpy->at(iPi);
	  pz = MCpz->at(iPi);
	  e = MCe->at(iPi);

	  p4.SetPxPyPzE(px, py, pz, e);
	 
	  if(iPi%3 == 0)
	    {
	      mKs = p4.M();
	      nKs++;
	      KsAngJ1 = p4.Angle(p_Jet[0].Vect());
	      KsAngJ2 = p4.Angle(p_Jet[1].Vect());
	      h_KsAngJ1->Fill(KsAngJ1);
	      h_KsAngJ2->Fill(KsAngJ2);
	    }
	  else p_pi += p4;
	  
	  if(iPi%3 == 2)
	    {
	      mpipi = p_pi.M();
	      h_Ks2pipi->Fill(mKs - mpipi);
	      p_pi.SetPxPyPzE(0.,0.,0.,0.);
	    }
	}
      h_nKs->Fill(nKs);

      /*
      // jet constituents
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;

      // JET 1
      double px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
      TLorentzVector p4_j1;

      for(int ele : jet1Const)
	{
	  px_j1 = MCpxF->at(ele);
	  py_j1 = MCpyF->at(ele);
	  pz_j1 = MCpzF->at(ele);
	  e_j1 = MCeF->at(ele);

	  p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);  
	}
            
      // JET 2
      double px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      for(int ele : jet2Const)
	{
	  px_j2 = MCpxF->at(ele);
	  py_j2 = MCpyF->at(ele);
	  pz_j2 = MCpzF->at(ele);
	  e_j2 = MCeF->at(ele);

	  p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);	  
	}

      jet1Const.clear();
      jet2Const.clear();
      */
    }
      
  histFile->Write();
  histFile->Close();
      
  //delete jetConst;
  //jetConst = NULL;
  
  file->Close();
  return -1;
}
