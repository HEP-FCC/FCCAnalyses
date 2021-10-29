// Studying the Spring2021 event files (Zuds files in particular): events, partons, jets - reco level
// Note: Close the event file before writing histograms/jet images
// No cuts
// REMEMBER TO ADD jetFlavour TO THE NTUPLE

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

  TFile *file = TFile::Open("p8_ee_Zuds_ecm91_reco.root");
  TTreeReader tree("events", file);
  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  TString histfname;
  histfname = "histZuds.root";
  TFile *histFile = new TFile(histfname,"RECREATE");
  
  // hists for the particle loop
  TH1F* h_nreco = new TH1F("h_nreco","Multiplicity",60,0,60);
  TH1F* h_pT = new TH1F("h_pT","p_{T} [GeV]",100,0,10);
  TH1F* h_p = new TH1F("h_p","|p| [GeV]",100,0,20);
  TH1F* h_e = new TH1F("h_e","E [GeV]",100,0,20);
  TH1F* h_theta = new TH1F("h_theta","Polar Angle (#theta)",100,0,3.15);
  TH1F* h_phi = new TH1F("h_phi","Azimuthal Angle (#phi)",100,-3.15,3.15);
  TH1F* h_invM = new TH1F("h_invM","Invariant Mass (event) [GeV]",100,75,100);
  TH1F* h_invM_RP = new TH1F("h_invM_RP","Invariant Mass (reco particles) [MeV]",100,0,26);
  
  // hists for the jet loop
  TH1F* h_njet = new TH1F("h_njet","Jet Multiplicity",20,0,20);
  TH1F* h_pjet = new TH1F("h_pjet","|p| - jets [GeV]",100,0,50);
  TH1F* h_pTjet = new TH1F("h_pTjet","p_{T} - jets [GeV]",100,0,50);
  TH1F* h_Ejet = new TH1F("h_Ejet","Energy - jet [GeV]",100,0,50);
  TH1F* h_jetTheta = new TH1F("h_jetTheta","Jet Polar Angle (#theta)",100,0,3.15);
  TH1F* h_jetPhi = new TH1F("h_jetPhi","Jet Azimuthal Angle (#phi)",100,-3.15,3.15);
  TH1F* h_invMjets = new TH1F("h_invMjets","Invariant Mass - sum of jets [GeV]",100,75,100);
  TH1F* h_invMjets_b = new TH1F("h_invMjets_b","b-jets",100,75,100);
  TH1F* h_invMjets_c = new TH1F("h_invMjets_c","c-jets",100,75,100);
  TH1F* h_invMjets_s = new TH1F("h_invMjets_s","s-jets",100,75,100);
  TH1F* h_invMjets_u = new TH1F("h_invMjets_u","u-jets",100,75,100);
  TH1F* h_invMjets_d = new TH1F("h_invMjets_d","d-jets",100,75,100);
  
  // hists for the jet constituents
  TH1F* h_angJP = new TH1F("h_angJP","Angle b/n Jet Constituents and Jet Axis",100,0,3.14);
  TH1F* h_thetaJP = new TH1F("h_thetaJP","#Delta#theta Jet Constituents & Jet Axis",100,-3.14,3.14);
  TH1F* h_phiJP = new TH1F("h_phiJP","#Delta#phi Jet Constituents & Jet Axis",100,-3.14,3.14);

  // reco particles                                                       
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> RPpx(tree, "RP_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> RPpy(tree, "RP_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> RPpz(tree, "RP_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> RPe(tree, "RP_e");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> RPp(tree, "RP_p");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> RPtheta(tree, "RP_theta");
  
  // jets and jet constituents - eekt     
  TTreeReaderValue<vector<vector<int>>> jetConst(tree, "jetconstituents_ee_kt");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_ee_kt_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_ee_kt_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_ee_kt_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree, "jets_ee_kt_e");
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_ee_kt_flavour"); //not in the ntuple yet

  // jets and jet constituents - kt     
  //TTreeReaderValue<vector<vector<int>>> jetConst(tree, "jetconstituents_kt");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_kt_px");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_kt_py");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_kt_pz");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree, "jets_kt_e");
  //TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_kt_flavour");

  // jets and jet constituents - ee-genkt     
  //TTreeReaderValue<vector<vector<int>>> jetConst(tree, "jetconstituents_ee_genkt");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_ee_genkt_px");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_ee_genkt_py");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_ee_genkt_pz");
  //TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree, "jets_ee_genkt_e");
  //TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_ee_genkt_flavour");

  // event counter
  int evt = 0;

  // event loop
  while(tree.Next())
    {
      // particle loop
      float px=0., py=0., pz=0., p=0., e=0.;
      TLorentzVector p4, p4_evt;

      for(unsigned int ctr=0; ctr<RPe->size(); ctr++)
	{	  
	  px = RPpx->at(ctr);
	  py = RPpy->at(ctr);
	  pz = RPpz->at(ctr);
	  p = RPp->at(ctr);
	  e = RPe->at(ctr);

	  p4.SetPxPyPzE(px, py, pz, e);
	  p4_evt += p4;
	  
	  // polar angle
	  h_theta->Fill(RPtheta->at(ctr));
	  
	  // azimuthal angle
	  h_phi->Fill(p4.Phi());

	  // abs momenta
	  h_p->Fill(p);

	  // transverse momenta
	  h_pT->Fill(p4.Pt());

	  // energy
	  h_e->Fill(e);

	  // invariant mass - reco particles
	  h_invM_RP->Fill(1000*p4.M());
	}

      // event multiplicity
      h_nreco->Fill(RPe->size());

      // invariant mass - (particle sum)
      h_invM->Fill(p4_evt.M());

      /*======================*/
      
      // jet loop
      float jPx=0., jPy=0., jPz=0., jE=0.;
      int nJet = jetE->size();
      TLorentzVector p_Jet[nJet], p_Jets;
      
      for(unsigned int j=0; j<jetE->size(); j++)
	{
	  jE = jetE->at(j);
	  jPx = jetPx->at(j);
	  jPy = jetPy->at(j);
	  jPz = jetPz->at(j);

	  p_Jet[j].SetPxPyPzE(jPx, jPy, jPz, jE);

	  // jet theta
	  h_jetTheta->Fill(p_Jet[j].Theta());
	  
	  // jet phi
	  h_jetPhi->Fill(p_Jet[j].Phi());
	  
	  // jet |p|
	  h_pjet->Fill(p_Jet[j].P());

	  // jet pT  
	  h_pTjet->Fill(p_Jet[j].Pt());

	  // jet E
	  h_Ejet->Fill(jE);

	  // sum of all jets' momenta
	  p_Jets += p_Jet[j];
							   
	}

      // jet multiplicity
      h_njet->Fill(nJet);
      	
      // invariant mass - (jet sum)
      h_invMjets->Fill(p_Jets.M());     // entire dataset
      if(jetFlavour->size()>0)
	{
	  if(jetFlavour->at(0)==5 && jetFlavour->at(1)==5) h_invMjets_b->Fill(p_Jets.M()); // b-jets
	  if(jetFlavour->at(0)==4 && jetFlavour->at(1)==4) h_invMjets_c->Fill(p_Jets.M()); // c-jets
	  if(jetFlavour->at(0)==3 && jetFlavour->at(1)==3) h_invMjets_s->Fill(p_Jets.M()); // s-jets
	  if(jetFlavour->at(0)==2 && jetFlavour->at(1)==2) h_invMjets_u->Fill(p_Jets.M()); // u-jets
	  if(jetFlavour->at(0)==1 && jetFlavour->at(1)==1) h_invMjets_d->Fill(p_Jets.M()); // d-jets
	}
      // REMEMBER TO CHANGE WHILE USING INCLUSIVE CLUSTERING

      /*======================*/
      
      // jet constituents
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"**No jet constituents found in event#"<<evt+1<<"**"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"**Second jet constituents not found in event#"<<evt+1<<"**"<<endl;
      
      // JET 1
      float px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
      TLorentzVector p4_j1;

      for(int ele : jet1Const) 
	{
	  px_j1 = RPpx->at(ele);
	  py_j1 = RPpy->at(ele);
	  pz_j1 = RPpz->at(ele);
	  e_j1 = RPe->at(ele);
	  
	  p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);

	  h_angJP->Fill(p4_j1.Angle(p_Jet[0].Vect()));     // angle b/n jet const and jet
	  h_thetaJP->Fill(p4_j1.Theta()-p_Jet[0].Theta()); // delta theta
	  h_phiJP->Fill(p4_j1.DeltaPhi(p_Jet[0]));         // delta phi
	}

      // JET 2
      float px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      for(int ele : jet2Const) 
	{
	  px_j2 = RPpx->at(ele);
	  py_j2 = RPpy->at(ele);
	  pz_j2 = RPpz->at(ele);
	  e_j2 = RPe->at(ele);
	  
	  p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);

	  h_angJP->Fill(p4_j2.Angle(p_Jet[1].Vect()));     // angle b/n jet const and jet
	  h_thetaJP->Fill(p4_j2.Theta()-p_Jet[1].Theta()); // delta theta
	  h_phiJP->Fill(p4_j2.DeltaPhi(p_Jet[1]));         // delta phi
	}
           
      jet1Const.clear();
      jet2Const.clear();

      evt++;

      if(evt%50000==0)
	{
	  //cout<<evt<<" events processed"<<endl;
	  cout<<"Event #"<<evt<<":"<<endl;
	  cout<<"This event has "<<RPe->size()<<" particles and "<<nJet<<" jets."<<endl;
	  cout<<"====================="<<endl<<endl;
	}
    }

  file->Close();
  cout<<"Event file closed"<<endl;

  h_nreco->Write();
  h_pT->Write();
  h_p->Write();
  h_e->Write();
  h_theta->Write();
  h_phi->Write();
  h_invM->Write();
  h_invM_RP->Write();
  h_njet->Write();
  h_pjet->Write();
  h_pTjet->Write();
  h_Ejet->Write();
  h_jetTheta->Write();
  h_jetPhi->Write();
  h_invMjets->Write();
  h_invMjets_b->Write();
  h_invMjets_c->Write();
  h_invMjets_s->Write();
  h_invMjets_u->Write();
  h_invMjets_d->Write();
  h_angJP->Write();
  h_thetaJP->Write();
  h_phiJP->Write();
  histFile->Close();
  cout<<"Histograms written to file and file closed"<<endl;

  //delete jetConst;
  //jetConst = NULL;

  cout<<endl;
  return -1;
}
