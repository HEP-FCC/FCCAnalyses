#include <iostream>
#include <cmath>
#include <vector>

#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <TInterpreter.h>

using namespace std;

int main()
{
  TFile* file = new TFile("p8_ee_Zbb_ecm91.root","READ");
  TTree* tree = (TTree*) file->Get("events");
  int nEvents = tree->GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  TString histfname;
  histfname = "histZbb.root";
  TFile *histFile = new TFile(histfname,"RECREATE");

  gInterpreter->GenerateDictionary("vector<vector<int> >","vector");

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
  TH1D* h_status =new TH1D("h_status","Gen Status",200,-100,100);
  TH1D* h_Zpdg =new TH1D("h_Zpdg","PDG code for the mother of b and #bar{b}",50,-25,25);
  TH1D* h_parent_indx =new TH1D("h_parent_indx","Parent Indices",250,0,250);

  // hists for the jet loop
  TH1D* h_njet =new TH1D("h_njet","Jet Multiplicity",25,0,25);
  TH1D* h_pjet =new TH1D("h_pjet","|p| - jet [GeV]",47,0,47);
  TH1D* h_pTjet =new TH1D("h_pTjet","p_{T} - jet [GeV]",47,0,47);
  TH1D* h_invMjets =new TH1D("h_invMjets","Invariant Mass - sum of jets [GeV]",100,89,92);
  TH1D* h_jetTheta =new TH1D("h_jetTheta","Jet Polar Angle (#theta)",100,0,3.15);
  TH1D* h_jetPhi =new TH1D("h_jetPhi","Jet Azimuthal Angle (#phi)",100,-3.15,3.15);
  TH1D* h_Ejet =new TH1D("h_Ejet","Energy - jet [GeV]",47,0,47);
  
  // hists for the jet constituents
  TH1D* h_pbT_jets =new TH1D("h_pbT_jets","p_{T} of b [GeV] (jet constituents)",47,0,47);
  TH1D* h_pb_jets =new TH1D("h_pb_jets","|p| of b [GeV] (jet constituents)",60,40,46);
  TH1D* h_thetab_jets =new TH1D("h_thetab_jets","#theta of b (jet constituents)",100,0,3.15);
  
  vector<float> *MCpx=0, *MCpy=0, *MCpz=0, *MCp=0, *MCe=0, *MCpdg=0, *MCstatus=0;
  vector<int> *MCparent_indx=0;
  tree->SetBranchAddress("MC_px", &MCpx);
  tree->SetBranchAddress("MC_py", &MCpy);
  tree->SetBranchAddress("MC_pz", &MCpz);
  tree->SetBranchAddress("MC_p", &MCp);
  tree->SetBranchAddress("MC_e", &MCe);
  tree->SetBranchAddress("MC_pdg", &MCpdg);
  tree->SetBranchAddress("MC_status", &MCstatus);

  tree->SetBranchAddress("MC_parent", &MCparent_indx);
  
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
  for(unsigned int evt=0; evt<1; evt++)
    {
      tree->GetEntry(evt);

      int nb=0, n_final=0;
      double px=0., py=0., pz=0., p=0., e=0.;
      TLorentzVector p4, p_2b, p_b, p_bbar;

      int b_mot_indx=0, bbar_mot_indx=0, b_mot_pdg=0, bbar_mot_pdg=0;
      
      // particle loop
      for(unsigned int ctr=0; ctr<MCpdg->size(); ctr++)
	{
	  px = MCpx->at(ctr);
	  py = MCpy->at(ctr);
	  pz = MCpz->at(ctr);
	  p = MCp->at(ctr);
	  e = MCe->at(ctr);

	  p4.SetPxPyPzE(px, py, pz, e);
    
	  if(MCstatus->at(ctr)>20 && MCstatus->at(ctr)<30)
	    {
	      if(MCpdg->at(ctr)==5 || MCpdg->at(ctr)==-5)
		{
		  nb++;
		  // pT of b or b-bar
		  h_pbT->Fill(p4.Pt());

		  // |p| of b or b-bar
		  h_pb->Fill(p);

		  // invariant mass
		  h_invMb->Fill(p4.M());

		  // polar angle
		  h_thetab->Fill(p4.Theta());
		}
	      
	      // b
	      if(MCpdg->at(ctr)==5)
		{
		  p_b = p4;
		  h_theta_bq->Fill(p4.Theta());
		  //b_mot_indx = MCparent_indx->at(ctr);
		  //b_mot_pdg = MCpdg->at(b_mot_indx);
		  //h_Zpdg->Fill(b_mot_pdg);
		}

	      // b-bar
	      if(MCpdg->at(ctr)==-5)
		{
		  p_bbar = p4;
		  h_theta_bqbar->Fill(p4.Theta());
		  //bbar_mot_indx = MCparent_indx->at(ctr);
		  //bbar_mot_pdg = MCpdg->at(bbar_mot_indx);
		  //h_Zpdg->Fill(bbar_mot_pdg);
		}
	    }

	  if(MCstatus->at(ctr)==1)
	    {
	      h_pT->Fill(p4.Pt());
	      n_final++;
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
	  
	  // jet theta
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
      jet1Const = jetConst->at(0);
      jet2Const = jetConst->at(1);
      cout<<"Jet constituent vector "<<jetConst->size()<<endl;
      cout<<"vector in vector : "<<jet1Const.size()<<endl;
      cout<<"vector in vector : "<<jet2Const.size()<<endl;

      // JET 1
      double px_j1=0, py_j1=0, pz_j1=0, p_j1=0, e_j1=0;
      TLorentzVector p4_j1;

      for(int ele : jet1Const) 
	{
	  cout<<"jet constituent index: "<<ele<<"\t";
	  /*px_j1 = MCpx->at(ele);
	  py_j1 = MCpy->at(ele);
	  pz_j1 = MCpz->at(ele);
	  p_j1 = MCp->at(ele);
	  e_j1 = MCe->at(ele);
	  
	  p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);
    
	  if(MCstatus->at(ele)>20 && MCstatus->at(ele)<30)
	    {
	      if(MCpdg->at(ele)==5 || MCpdg->at(ele)==-5)
		{
		  // pT of b or b-bar
		  h_pbT_jets->Fill(p4_j1.Pt());

		  // |p| of b or b-bar
		  h_pb_jets->Fill(p_j1);

		  // polar angle
		  h_thetab_jets->Fill(p4_j1.Theta());
		}
		}*/
	}

      cout<<endl<<"jet 1 ends, jet 2 begins"<<endl;

      // JET 2
      double px_j2=0, py_j2=0, pz_j2=0, p_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      for(int ele : jet2Const) 
	{
	  cout<<"jet constituent index: "<<ele<<"\t";
	  /*px_j2 = MCpx->at(ele);
	  py_j2 = MCpy->at(ele);
	  pz_j2 = MCpz->at(ele);
	  p_j2 = MCp->at(ele);
	  e_j2 = MCe->at(ele);
	  
	  p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);
    
	  if(MCstatus->at(ele)>20 && MCstatus->at(ele)<30)
	    {
	      if(MCpdg->at(ele)==5 || MCpdg->at(ele)==-5)
		{
		  // pT of b or b-bar
		  h_pbT_jets->Fill(p4_j2.Pt());

		  // |p| of b or b-bar
		  h_pb_jets->Fill(p_j2);

		  // polar angle
		  h_thetab_jets->Fill(p4_j2.Theta());
		}
		}*/
	}


      // invariant mass of the event
      h_invMjets->Fill(p_Jets.M());

      if(evt%10000==0)
	{
	  cout<<"In event #"<<evt+1<<", there are ";
	  cout<<MCpdg->size()<<" entries."<<endl;
	  cout<<"This event has "<<nb<<" b and bbar; "<<nJet<<" jets; and "<<n_final<<" final particles."<<endl;
	  cout<<"MCpx = "<<MCpx->size()<<", MCparent_indx = "<<MCparent_indx->size()<<endl;
	  cout<<endl<<"====================="<<endl;
	}
    }

  histFile->Write();
  histFile->Close();

  file->Close();
  return -1;
}
