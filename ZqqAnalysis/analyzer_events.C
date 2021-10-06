// Studying the Spring2021 event files (Zbb files in particular, but trivial to edit for uds): events, partons, jets
// Encountered the segmentation error - fixed
// Note: Close the event file before writing histograms/jet images
// Note: Prefer using "TTreeReader" and "TTreeReaderValue" instead of "SetBranchAddress" - include the library "ROOT/RVec.hxx" while using TTreeReader
// No cuts

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
  histfname = "histZbb.root";
  TFile *histFile = new TFile(histfname,"RECREATE");

  // hists for the particle loop
  TH1D* h_nb =new TH1D("h_nb","b and #bar{b} in the event",10,0,10);
  TH1D* h_pT =new TH1D("h_pT","p_{T} [GeV]",100,0,10);
  TH1D* h_pbT =new TH1D("h_pbT","p_{T} of b [GeV]",47,0,47);
  TH1D* h_pb =new TH1D("h_pb","|p| of b [GeV]",60,40,46);
  TH1D* h_thetab =new TH1D("h_thetab","#theta of b",100,0,3.15);
  TH1D* h_theta_bq =new TH1D("h_theta_bq","#theta of b (only)",100,0,3.15);
  TH1D* h_theta_bqbar =new TH1D("h_theta_bqbar","#theta of #bar{b}",100,0,3.15);
  TH1D* h_invMb =new TH1D("h_invMb","Invariant Mass - b [GeV]",100,4.79,4.81);
  TH1D* h_invM2b =new TH1D("h_invM2b","Invariant Mass - b and #bar{b} [GeV]",100,86.,91.5);
  
  // hists for final particles
  TH1D* h_theta_f =new TH1D("h_theta_f","#theta of final particles",100,0,3.15);
  TH1D* h_theta_fCut =new TH1D("h_theta_fCut","#theta of final particles (cut ~14^{o})",100,0,3.15);

  // hists for the jet loop
  TH1D* h_njet =new TH1D("h_njet","Jet Multiplicity",25,0,25);
  TH1D* h_pjet =new TH1D("h_pjet","|p| - jet [GeV]",47,0,47);
  TH1D* h_pTjet =new TH1D("h_pTjet","p_{T} - jet [GeV]",47,0,47);
  TH1D* h_invMjets =new TH1D("h_invMjets","Invariant Mass - sum of jets [GeV]",100,89,92);
  TH1D* h_jetTheta =new TH1D("h_jetTheta","Jet Polar Angle (#theta)",100,0,3.15);
  TH1D* h_jetPhi =new TH1D("h_jetPhi","Jet Azimuthal Angle (#phi)",100,-3.15,3.15);
  TH1D* h_Ejet =new TH1D("h_Ejet","Energy - jet [GeV]",47,0,47);
  
  // hists for the jet constituents
  TH1D* h_deltaAngKs1 =new TH1D("h_deltaAngKs1","Angle between K_{S} and jet axis",100,0,3.15);
  TH1D* h_deltaAngKs2 =new TH1D("h_deltaAngKs2","Angle between K_{S} and jet axis",100,0,3.15);
  TH1D* h_deltaThetaKs1 =new TH1D("h_deltaThetaKs1","#Delta #theta between K_{S} and jet axis",100,0,3.15);
  TH1D* h_deltaPhiKs1 =new TH1D("h_deltaPhiKs1","#Delta #phi between K_{S} and jet axis",100,0,3.15);
  TH1D* h_deltaThetaKs2 =new TH1D("h_deltaThetaKs2","#Delta #theta between K_{S} and jet axis",100,0,3.15);
  TH1D* h_deltaPhiKs2 =new TH1D("h_deltaPhiKs2","#Delta #phi between K_{S} and jet axis",100,0,3.15);
  
  vector<float> *MCpx=0, *MCpy=0, *MCpz=0, *MCp=0, *MCe=0, *MCpdg=0, *MCstatus=0;
  // Particle branches
  tree->SetBranchAddress("MC_px", &MCpx);
  tree->SetBranchAddress("MC_py", &MCpy);
  tree->SetBranchAddress("MC_pz", &MCpz);
  tree->SetBranchAddress("MC_p", &MCp);
  tree->SetBranchAddress("MC_e", &MCe);
  tree->SetBranchAddress("MC_pdg", &MCpdg);
  tree->SetBranchAddress("MC_status", &MCstatus);

  vector<float> *MCpxF=0, *MCpyF=0, *MCpzF=0, *MCeF=0, *MCpdgF=0;
  // Final particle branches
  tree->SetBranchAddress("MC_px_f", &MCpxF);
  tree->SetBranchAddress("MC_py_f", &MCpyF);
  tree->SetBranchAddress("MC_pz_f", &MCpzF);
  tree->SetBranchAddress("MC_e_f", &MCeF);
  tree->SetBranchAddress("MC_pdg_f", &MCpdgF);
  
  vector<float> *jetE=0, *jetPx=0, *jetPy=0, *jetPz=0;
  vector<vector<int>> *jetConst;
  // Jet branches (ee-genkt)
  //tree->SetBranchAddress("jetconstituents_ee_genkt", &jetConst);
  //tree->SetBranchAddress("jets_ee_genkt_e", &jetE);
  //tree->SetBranchAddress("jets_ee_genkt_px", &jetPx);
  //tree->SetBranchAddress("jets_ee_genkt_py", &jetPy);
  //tree->SetBranchAddress("jets_ee_genkt_pz", &jetPz);

  // Jet branches (kt)
  //tree->SetBranchAddress("jetconstituents_kt", &jetConst);
  //tree->SetBranchAddress("jets_kt_e", &jetE);
  //tree->SetBranchAddress("jets_kt_px", &jetPx);
  //tree->SetBranchAddress("jets_kt_py", &jetPy);
  //tree->SetBranchAddress("jets_kt_pz", &jetPz);

  // Jet branches (eekt)
  tree->SetBranchAddress("jetconstituents_ee_kt", &jetConst);
  tree->SetBranchAddress("jets_ee_kt_e", &jetE);
  tree->SetBranchAddress("jets_ee_kt_px", &jetPx);
  tree->SetBranchAddress("jets_ee_kt_py", &jetPy);
  tree->SetBranchAddress("jets_ee_kt_pz", &jetPz);
  
  // event loop
  for(unsigned int evt=0; evt<nEvents; evt++)
    {
      tree->GetEntry(evt);

      int nb=0, n_final=0;
      double px=0., py=0., pz=0., p=0., e=0.;
      TLorentzVector p4, p_2b, p_b, p_bbar;

      // particle loop
      for(unsigned int ctr=0; ctr<MCpdg->size(); ctr++)
	{
	  px = MCpx->at(ctr);
	  py = MCpy->at(ctr);
	  pz = MCpz->at(ctr);
	  p = MCp->at(ctr);
	  e = MCe->at(ctr);

	  p4.SetPxPyPzE(px, py, pz, e);
    
	  //if(MCstatus->at(ctr)>20 && MCstatus->at(ctr)<30)
	  if(MCstatus->at(ctr)==23)
	    {
	      //if(MCpdg->at(ctr)==5 || MCpdg->at(ctr)==-5)
	      //{
	      nb++;
	      // pT of b or b-bar
	      h_pbT->Fill(p4.Pt());

	      // |p| of b or b-bar
	      h_pb->Fill(p);

	      // invariant mass
	      h_invMb->Fill(p4.M());

	      // polar angle
	      h_thetab->Fill(p4.Theta());
	      //}
	      
	      // b
	      if(MCpdg->at(ctr)==5)
		{
		  p_b = p4;
		  h_theta_bq->Fill(p4.Theta());
	        }

	      // b-bar
	      if(MCpdg->at(ctr)==-5)
		{
		  p_bbar = p4;
		  h_theta_bqbar->Fill(p4.Theta());
		}
	    }

	  if(MCstatus->at(ctr)==1)
	    {
	      h_pT->Fill(p4.Pt());
	      n_final++;

	      // theta of final particles
	      h_theta_f->Fill(p4.Theta());
	      // theta of final particles - after cut (~14 degrees)
	      if(abs(cos(p4.Theta())) < 0.97) h_theta_fCut->Fill(p4.Theta());
	    }	      
	}

      h_nb->Fill(nb);

      p_2b = p_b + p_bbar;
      // invariant mass of b + b-bar
      h_invM2b->Fill(p_2b.M());

      double jPx=0., jPy=0., jPz=0., jE=0., invMjet=0.;
      int nJet = jetE->size();
      h_njet->Fill(nJet);
      TLorentzVector p_Jet[nJet], p_Jets;
      	
      // jet loop
      for(unsigned int j=0; j<nJet; j++)
	{
	  jE = jetE->at(j);
	  jPx = jetPx->at(j);
	  jPy = jetPy->at(j);
	  jPz = jetPz->at(j);

	  // jet E
	  h_Ejet->Fill(jE);

	  p_Jet[j].SetPxPyPzE(jPx, jPy, jPz, jE);

	  // jet theta
	  h_jetTheta->Fill(p_Jet[j].Theta());
	  
	  // jet Phi
	  h_jetPhi->Fill(p_Jet[j].Phi());
	  
	  // jet |p|
	  h_pjet->Fill(p_Jet[j].P());

	  // jet pT  
	  h_pTjet->Fill(p_Jet[j].Pt());

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
	  //cout<<"jet constituent index: "<<ele<<"\t";
	  px_j1 = MCpxF->at(ele);
	  py_j1 = MCpyF->at(ele);
	  pz_j1 = MCpzF->at(ele);
	  e_j1 = MCeF->at(ele);
	  
	  p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);

	  // angle between Ks and jet axis
	  if(MCpdgF->at(ele)==310 || MCpdgF->at(ele)==-310)
	    {
	      delta_ang1 = p4_j1.Angle(p_Jet[0].Vect());
	      h_deltaAngKs1->Fill(delta_ang1);
	      h_deltaThetaKs1->Fill(p4_j1.Theta() - p_Jet[0].Theta());
	      h_deltaPhiKs1->Fill(p4_j1.DeltaPhi(p_Jet[0]));
	    }
	}

      //      cout<<endl<<"jet 1 ends, jet 2 begins"<<endl;

      // JET 2
      double px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      double delta_ang2=0.;

      for(int ele : jet2Const) 
	{
	  //cout<<"jet constituent index: "<<ele<<"\t";
	  px_j2 = MCpxF->at(ele);
	  py_j2 = MCpyF->at(ele);
	  pz_j2 = MCpzF->at(ele);
	  e_j2 = MCeF->at(ele);
	  
	  p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);

	  // angle between Ks and jet axis
	  if(MCpdgF->at(ele)==310 || MCpdgF->at(ele)==-310)
	    {
	      delta_ang2 = p4_j2.Angle(p_Jet[1].Vect());
	      h_deltaAngKs2->Fill(delta_ang2);
	      h_deltaThetaKs2->Fill(p4_j2.Theta() - p_Jet[1].Theta());
	      h_deltaPhiKs2->Fill(p4_j2.DeltaPhi(p_Jet[1]));
	    }
	}

      // invariant mass of the event
      h_invMjets->Fill(p_Jets.M());

      if(evt%10000==0)
	{
	  cout<<"In event #"<<evt+1<<", there are ";
	  cout<<MCpdg->size()<<" entries."<<endl;
	  cout<<"This event has "<<nb<<" b and bbar; "<<nJet<<" jets; and "<<n_final<<" final particles."<<endl;
	  cout<<endl<<"====================="<<endl;
	}

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
