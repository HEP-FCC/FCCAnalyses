// Trial to implement THnSparse to reduce the file size for the jet-image file (uses Zbb, change file name to get Zuds)
// File size is reduced but still stores everything until histograms are written, therefore fails when not enough RAM; tried writing histograms inside the event loop, didn't work
// NEED A FIX (run in batches? How?)
// Note: Give each jet image a different name, event if of same type. e.g. h_JetCKaon[i] needs to have a unique name for each i                             
// No cuts
// Trying to introduce TTree to put Lorentz vectors, labels, and jet number in the same root file along with jet-images
// currently jet images with TH2F, somehow file size smaller with TH2F than THnSparse


#include <iostream>
#include <cmath>
#include <vector>

#include <TObject.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <THnSparse.h>
#include <TH2F.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include "ROOT/RVec.hxx"
#include <TSystem.h>
#include <TInterpreter.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>

using namespace std;

int main()
{
  gInterpreter->GenerateDictionary("vector<vector<int> >","vector");

  TFile *file = TFile::Open("p8_ee_Zuds_ecm91.root");
  TTreeReader tree("events", file);

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

  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  TString histfname;
  histfname = "histZuds_jetimages_600k.root";
  TFile histFile(histfname,"RECREATE");

  // define a tree
  TTree* jets_uds = new TTree("jets_uds","Jet Images and Corresponding Attributes");

  cout<<"Defined the tree, initialising sparse histograms"<<endl;

  // Using THnSparse for hists
  int ndim = 2;
  int nbin[2] = {29, 29};
  double xmin[2] = {-0.5, -0.5};
  double xmax[2] = {0.5, 0.5};
  //int nchunk = 1024*2;
  /*
  THnSparse* h_JetCKaonL1 = new THnSparseD("h_JetCKaonL1","K^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetNKaonL1 = new THnSparseD("h_JetNKaonL1","K_{L} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetCPionL1 = new THnSparseD("h_JetCPionL1","#pi^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetElecL1 = new THnSparseD("h_JetElecL1","e^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetMuonL1 = new THnSparseD("h_JetMuonL1","#mu^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetPhotL1 = new THnSparseD("h_JetPhotL1","#gamma in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetProtL1 = new THnSparseD("h_JetProtL1","p in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetNeutL1 = new THnSparseD("h_JetNeutL1","n in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetCKaonL2 = new THnSparseD("h_JetCKaonL2","K^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetNKaonL2 = new THnSparseD("h_JetNKaonL2","K_{L} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetCPionL2 = new THnSparseD("h_JetCPionL2","#pi^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetElecL2 = new THnSparseD("h_JetElecL2","e^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetMuonL2 = new THnSparseD("h_JetMuonL2","#mu^{#pm} in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetPhotL2 = new THnSparseD("h_JetPhotL2","#gamma in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetProtL2 = new THnSparseD("h_JetProtL2","p in uds jet",ndim,nbin,xmin,xmax);
  THnSparse* h_JetNeutL2 = new THnSparseD("h_JetNeutL2","n in uds jet",ndim,nbin,xmin,xmax);
  */
  TH2F* h_JetCKaonL1 = new TH2F("h_JetCKaonL1","K^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetNKaonL1 = new TH2F("h_JetNKaonL1","K_{L} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetCPionL1 = new TH2F("h_JetCPionL1","#pi^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetElecL1 = new TH2F("h_JetElecL1","e^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetMuonL1 = new TH2F("h_JetMuonL1","#mu^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetPhotL1 = new TH2F("h_JetPhotL1","#gamma in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetProtL1 = new TH2F("h_JetProtL1","p in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetNeutL1 = new TH2F("h_JetNeutL1","n in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetCKaonL2 = new TH2F("h_JetCKaonL2","K^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetNKaonL2 = new TH2F("h_JetNKaonL2","K_{L} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetCPionL2 = new TH2F("h_JetCPionL2","#pi^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetElecL2 = new TH2F("h_JetElecL2","e^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetMuonL2 = new TH2F("h_JetMuonL2","#mu^{#pm} in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetPhotL2 = new TH2F("h_JetPhotL2","#gamma in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetProtL2 = new TH2F("h_JetProtL2","p in uds jet",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetNeutL2 = new TH2F("h_JetNeutL2","n in uds jet",29,-0.5,0.5,29,-0.5,0.5);

  // define the histogram branches
  jets_uds->Branch("cKaon1", &h_JetCKaonL1);
  jets_uds->Branch("nKaon1", &h_JetNKaonL1);
  jets_uds->Branch("cPion1", &h_JetCPionL1);
  jets_uds->Branch("elec1", &h_JetElecL1);
  jets_uds->Branch("muon1", &h_JetMuonL1);
  jets_uds->Branch("phot1", &h_JetPhotL1);
  jets_uds->Branch("prot1", &h_JetProtL1);
  jets_uds->Branch("neut1", &h_JetNeutL1);
  jets_uds->Branch("cKaon2", &h_JetCKaonL2);
  jets_uds->Branch("nKaon2", &h_JetNKaonL2);
  jets_uds->Branch("cPion2", &h_JetCPionL2);
  jets_uds->Branch("elec2", &h_JetElecL2);
  jets_uds->Branch("muon2", &h_JetMuonL2);
  jets_uds->Branch("phot2", &h_JetPhotL2);
  jets_uds->Branch("prot2", &h_JetProtL2);
  jets_uds->Branch("neut2", &h_JetNeutL2);

  cout<<"histograms defined as branches"<<endl;

  /*
  vector<THnSparse*> h_JetCKaonB;
  vector<THnSparse*> h_JetNKaonB;
  vector<THnSparse*> h_JetCPionB;
  vector<THnSparse*> h_JetElecB;
  vector<THnSparse*> h_JetMuonB;
  vector<THnSparse*> h_JetPhotB;
  vector<THnSparse*> h_JetProtB;
  vector<THnSparse*> h_JetNeutB;

  for(int nH=0; nH<2*nEvents; nH++)
    {
      stringstream ssck, ssnk, sscp, sse, ssmu, ssph, ssp, ssn;
      ssck<<"hist_jetCKaon_"<<nH;
      ssnk<<"hist_jetNKaon_"<<nH;
      sscp<<"hist_jetCPion_"<<nH;
      sse<<"hist_jetElec_"<<nH;
      ssmu<<"hist_jetMuon_"<<nH;
      ssph<<"hist_jetPhot_"<<nH;
      ssp<<"hist_jetProt_"<<nH;
      ssn<<"hist_jetNeut_"<<nH;
      string sck = ssck.str();
      string snk = ssnk.str();
      string scp = sscp.str();
      string se = sse.str();
      string smu = ssmu.str();
      string sph = ssph.str();
      string sp = ssp.str();
      string sn = ssn.str();

      h_JetCKaonB.push_back(new THnSparseD(sck.c_str(),"K^{+/-} in b jets",ndim,nbin,xmin,xmax));
      h_JetNKaonB.push_back(new THnSparseD(snk.c_str(),"K_{L} in b jets",ndim,nbin,xmin,xmax));
      h_JetCPionB.push_back(new THnSparseD(scp.c_str(),"#pi^{+/-} in b jets",ndim,nbin,xmin,xmax));
      h_JetElecB.push_back(new THnSparseD(se.c_str(),"e^{+/-} in b jets",ndim,nbin,xmin,xmax));
      h_JetMuonB.push_back(new THnSparseD(smu.c_str(),"#mu^{+/-} in b jets",ndim,nbin,xmin,xmax));
      h_JetPhotB.push_back(new THnSparseD(sph.c_str(),"#gamma in b jets",ndim,nbin,xmin,xmax));
      h_JetProtB.push_back(new THnSparseD(sp.c_str(),"p in b jets",ndim,nbin,xmin,xmax));
      h_JetNeutB.push_back(new THnSparseD(sn.c_str(),"n in b jets",ndim,nbin,xmin,xmax));
    }
  */

  // event counter
  int evt = 0;

  while(tree.Next())
    {
      if(evt%5000==0) cout<<evt<<" done"<<endl;

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
      double delta1[2];

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
	  delta1[0] = delta_theta1;
	  delta1[1] = delta_phi1;

	  /*
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130)
	    {
	      delta_ang1 = p4_j1.Angle(p_Jet[0].Vect());
	      h_deltaAngKl->Fill(delta_ang1);
	    }
	  */

	  // K+-
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	  // Kl
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	  // pi+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionL1->Fill(delta1[0],delta1[1],p_norm1);

	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	  // mu+-
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	  // proton
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	  // neutron
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutL1->Fill(delta1[0],delta1[1],p_norm1);
	  
	}
            
      // JET 2
      double px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      double p_norm2 = 0.;
      double delta_theta2 = 0., delta_phi2 = 0.;
      double delta2[2];

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
	  delta2[0] = delta_theta2;
	  delta2[1] = delta_phi2;

	  /*
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130)
	    {
	      delta_ang2 = p4_j2.Angle(p_Jet[1].Vect());
	      h_deltaAngKl->Fill(delta_ang2);
	    }
	  */

	  // K+-
	  //if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB->Fill(delta_theta2,delta_phi2,p_norm2);
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // K0
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // pi+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // mu+-
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // proton
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	  // Neutron
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutL2->Fill(delta2[0],delta2[1],p_norm2);
	  
	}

      jet1Const.clear();
      jet2Const.clear();
      /*
      h_JetCKaonB[evt]->Write();
      h_JetNKaonB[evt]->Write();
      h_JetCPionB[evt]->Write();
      h_JetElecB[evt]->Write();
      h_JetMuonB[evt]->Write();
      h_JetPhotB[evt]->Write();
      h_JetProtB[evt]->Write();
      h_JetNeutB[evt]->Write();

      h_JetCKaonB[nEvents+evt]->Write();
      h_JetNKaonB[nEvents+evt]->Write();
      h_JetCPionB[nEvents+evt]->Write();
      h_JetElecB[nEvents+evt]->Write();
      h_JetMuonB[nEvents+evt]->Write();
      h_JetPhotB[nEvents+evt]->Write();
      h_JetProtB[nEvents+evt]->Write();
      h_JetNeutB[nEvents+evt]->Write();
      */

      // how to write histograms from both jets in the same branch without overwriting?
      jets_uds->Fill();

      evt++;
    }
      
  cout<<"Event loop ends"<<endl;

  file->Close();
  cout<<"event file closed"<<endl;

  /*
  for(int iH=0; iH<2*nEvents; iH++) {
    //hist_list->Add(h_JetCKaonB[iH]);                                                                   
    h_JetCKaonB[iH]->Write();
    h_JetNKaonB[iH]->Write();
    h_JetCPionB[iH]->Write();
    h_JetElecB[iH]->Write();
    h_JetMuonB[iH]->Write();
    h_JetPhotB[iH]->Write();
    h_JetProtB[iH]->Write();
    h_JetNeutB[iH]->Write();
  }
  */

  jets_uds->Write();
  histFile.Close();
  cout<<"tree written to the file and file closed"<<endl;

  //delete jetConst;
  //jetConst = NULL;
  
  return -1;
}
