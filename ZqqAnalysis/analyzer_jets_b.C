// Summed histograms for b-jets, includes Ks but not pi0
// Note: Prefer using "TTreeReader" and "TTreeReaderValue" instead of "SetBranchAddress" - include the library "ROOT/RVec.hxx" while using TTreeReader 
// No cuts

#include <iostream>
#include <cmath>
#include <vector>

#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TH2D.h>
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
  
  // hists for jet angluar distributions
  TH2D* h_JetCKaonB = new TH2D("h_JetCKaonB","K^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetNKaonB = new TH2D("h_JetNKaonB","K_{L} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetCPionB = new TH2D("h_JetCPionB","#pi^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetElecB = new TH2D("h_JetElecB","e^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetMuonB = new TH2D("h_JetMuonB","#mu^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetPhotB = new TH2D("h_JetPhotB","#gamma in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetProtB = new TH2D("h_JetProtB","p in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetNeutB = new TH2D("h_JetNeutB","n in b jets",29,-0.5,0.5,29,-0.5,0.5);

  TH2D* h_JetKs2pipiB = new TH2D("h_JetKs2pipiB","K_{S} #rightarrow #pi^{+}#pi^{-} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2D* h_JetKs2pipiPiB = new TH2D("h_JetKs2pipiPiB","#pi's from K_{S} #rightarrow #pi^{+}#pi^{-} in b jets",29,-0.5,0.5,29,-0.5,0.5);
  
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
  vector<vector<int>> *jetConst;
  
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

      // Ks->pipi loop
      double px=0., py=0., pz=0., e=0.;
      TLorentzVector p4;
      double KsAngJ1=0., KsAngJ2=0.;
      double PiAngJ1=0., PiAngJ2=0.;
      double p_normKsJ1=0., KsThetaJ1=0., KsPhiJ1=0.;
      double p_normKsJ2=0., KsThetaJ2=0., KsPhiJ2=0.;
      double p_normPiJ1=0., PiThetaJ1=0., PiPhiJ1=0.;
      double p_normPiJ2=0., PiThetaJ2=0., PiPhiJ2=0.;
      for(int iKP=0; iKP<Ks2pipi->size(); iKP++)
	{
	  px = MCpx->at(Ks2pipi->at(iKP));
	  py = MCpy->at(Ks2pipi->at(iKP));
	  pz = MCpz->at(Ks2pipi->at(iKP));
	  e = MCe->at(Ks2pipi->at(iKP));
	  
	  p4.SetPxPyPzE(px, py, pz, e);
	  
	  //cout<<MCpdg->at(Ks2pipi->at(iKP))<<endl;
	  
	  if(iKP%3 == 0)
	    {
	      KsAngJ1 = p4.Angle(p_Jet[0].Vect());
	      KsAngJ2 = p4.Angle(p_Jet[1].Vect());
	      
	      p_normKsJ1 = p4.P()/p_Jet[0].P();
	      KsThetaJ1 = p4.Theta() - p_Jet[0].Theta();
	      KsPhiJ1 = p4.DeltaPhi(p_Jet[0]);
	      
	      p_normKsJ2 = p4.P()/p_Jet[1].P();
	      KsThetaJ2 = p4.Theta() - p_Jet[1].Theta();
	      KsPhiJ2 = p4.DeltaPhi(p_Jet[1]);

	      if(KsAngJ1<0.5) h_JetKs2pipiB->Fill(KsThetaJ1, KsPhiJ1, p_normKsJ1);
	      else if(KsAngJ2<0.5) h_JetKs2pipiB->Fill(KsThetaJ2, KsPhiJ2, p_normKsJ2);
	    }
	  
	  if(abs(MCpdg->at(Ks2pipi->at(iKP))) == 211)
	    {
	      PiAngJ1 = p4.Angle(p_Jet[0].Vect());
	      PiAngJ2 = p4.Angle(p_Jet[1].Vect());
	      
	      p_normPiJ1 = p4.P()/p_Jet[0].P();
	      PiThetaJ1 = p4.Theta() - p_Jet[0].Theta();
	      PiPhiJ1 = p4.DeltaPhi(p_Jet[0]);
	      
	      p_normPiJ2 = p4.P()/p_Jet[1].P();
	      PiThetaJ2 = p4.Theta() - p_Jet[1].Theta();
	      PiPhiJ2 = p4.DeltaPhi(p_Jet[1]);

	      if(abs(PiThetaJ1)<0.5 && abs(PiPhiJ1)<0.5) h_JetKs2pipiPiB->Fill(PiThetaJ1, PiPhiJ1, p_normPiJ1);
	      else if(abs(PiThetaJ2)<0.5 && abs(PiPhiJ2)<0.5) h_JetKs2pipiPiB->Fill(PiThetaJ2, PiPhiJ2, p_normPiJ2);
	    }
	  
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
	  delta_phi1 = p4_j1.DeltaPhi(p_Jet[0]);
	  
	  // K+-
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // Kl
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // pi+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // Muon
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // p
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // n
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutB->Fill(delta_theta1,delta_phi1,p_norm1);
	  
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
	  delta_phi2 = p4_j2.DeltaPhi(p_Jet[1]);
	  
	  // K+-
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // Kl
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // pi+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // Muon
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // p
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // n
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutB->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	}

      jet1Const.clear();
      jet2Const.clear();
      

      //cout<<"============================"<<endl;
    }

  file->Close();
  
  histFile->Write();
  histFile->Close();
      
  //delete jetConst;
  //jetConst = NULL;
  
  return -1;
}
