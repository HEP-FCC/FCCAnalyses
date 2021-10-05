// copy of the summed b-jet images with names changed to get hists for c
// no updates except closing event file before writing hists, may even have segmentation fault (unlikely but didn't check)
// no cuts

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

  TFile* file = new TFile("p8_ee_Zcc_ecm91.root","READ");
  TTree* tree = (TTree*) file->Get("events");
  int nEvents = tree->GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;
  
  TString histfname;
  histfname = "histZcc_jets.root";
  TFile *histFile = new TFile(histfname,"RECREATE");

  // Hists for jet-constituents' properties
  //TH1D* h_deltaAngKl = new TH1D("h_deltaAngKl","Angle b/n K_{L} and Jet Axis",100,0.,3.15);
  
  // hists for jet angluar distributions
  TH2D* h_JetCKaonC = new TH2D("h_JetCKaonC","K^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetNKaonC = new TH2D("h_JetNKaonC","K_{L} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetCPionC = new TH2D("h_JetCPionC","#pi^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetElecC = new TH2D("h_JetElecC","e^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetMuonC = new TH2D("h_JetMuonC","#mu^{+/-} in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetPhotC = new TH2D("h_JetPhotC","#gamma in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetProtC = new TH2D("h_JetProtC","p in c jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetNeutC = new TH2D("h_JetNeutC","n in c jets",29,-0.5,0.5,29,-0.5,0.5);
  
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
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;

      // JET 1
      double px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
      TLorentzVector p4_j1;

      double p_norm1 = 0.;
      double delta_theta1 = 0., delta_phi1 = 0.;

      //double delta_ang1=0.;
      for(int ele : jet1Const)
	{
	  px_j1 = MCpxF->at(ele);
	  py_j1 = MCpyF->at(ele);
	  pz_j1 = MCpzF->at(ele);
	  e_j1 = MCeF->at(ele);

	  p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);

	  p_norm1 = p4_j1.P()/p_Jet[0].P();
	  delta_theta1 = p4_j1.Theta() - p_Jet[0].Theta();
	  delta_phi1 = p4_j1.Phi() - p_Jet[0].Phi();
	  /*
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130)
	    {
	      delta_ang1 = p4_j1.Angle(p_Jet[0].Vect());
	      h_deltaAngKl->Fill(delta_ang1);
	    }
	  */
	  // K+-
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // Kl
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // K+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // Muon
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // p
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // n
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutC->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	}
            
      // JET 2
      double px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      double p_norm2 = 0.;
      double delta_theta2 = 0., delta_phi2 = 0.;

      //double delta_ang2=0.;
      for(int ele : jet2Const)
	{
	  px_j2 = MCpxF->at(ele);
	  py_j2 = MCpyF->at(ele);
	  pz_j2 = MCpzF->at(ele);
	  e_j2 = MCeF->at(ele);

	  p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);

	  p_norm2 = p4_j2.P()/p_Jet[1].P();
	  delta_theta2 = p4_j2.Theta() - p_Jet[1].Theta();
	  delta_phi2 = p4_j2.Phi() - p_Jet[1].Phi();
	  /*
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130)
	    {
	      delta_ang2 = p4_j2.Angle(p_Jet[1].Vect());
	      h_deltaAngKl->Fill(delta_ang2);
	    }
	  */
	  // K+-
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // Kl
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // K+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // Muon
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // p
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // n
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutC->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	}

      jet1Const.clear();
      jet2Const.clear();
    }
  
  file->Close();
    
  histFile->Write();
  histFile->Close();
      
  delete jetConst;
  jetConst = NULL;
  
  return -1;
}
