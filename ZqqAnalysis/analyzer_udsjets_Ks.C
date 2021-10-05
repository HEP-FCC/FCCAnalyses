// studying uds jets, gets summed jet-images of all categories, includs Ks not pi0
// also studying the Ks->pipi decays - angluar distributions to decide on jet assignment, momentum distribution to see the effect by cuts, and multiplicity of the decays in the events
// tried the "consecutive pion" strategy instead of index matching: didn't work

#include <iostream>
#include <cmath>
#include <vector>

#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
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

  // All particles                                                                                     
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpx(tree, "MC_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpy(tree, "MC_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpz(tree, "MC_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCe(tree,  "MC_e");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpdg(tree,"MC_pdg");

  // final particles                                                                                     
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpxF(tree, "MC_px_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpyF(tree, "MC_py_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpzF(tree, "MC_pz_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCeF(tree,  "MC_e_f");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpdgF(tree,"MC_pdg_f");

  // jet constituents                                                                                     
  TTreeReaderValue<vector<vector<int>>> jetConst(tree, "jetconstituents_ee_kt");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_ee_kt_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_ee_kt_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_ee_kt_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree,  "jets_ee_kt_e");
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree,"jets_ee_kt_flavour");

  // Ks->pi+pi-
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> Ks2pipi(tree, "K0spipi_indices");

  // pi->gamma gamma
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> pi2gmgm(tree, "pi0gammagamma_indices");
  
  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  TString histfname;
  histfname = "histZuds_jetImages_summed.root";
  TFile histFile(histfname,"RECREATE");
  
  // hists for jet angluar distributions
  TH2F* h_JetCKaonL = new TH2F("h_JetCKaonL","K^{+/-} in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetNKaonL = new TH2F("h_JetNKaonL","K_{L} in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetCPionL = new TH2F("h_JetCPionL","#pi^{+/-} in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetElecL = new TH2F("h_JetElecL","e^{+/-} in light jets",29,-0.5,0.5,29,-0.5,0.5);
  //TH2F* h_JetMuonL = new TH2F("h_JetMuonL","#mu^{+/-} in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetPhotL = new TH2F("h_JetPhotL","#gamma in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetProtL = new TH2F("h_JetProtL","p in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetNeutL = new TH2F("h_JetNeutL","n in light jets",29,-0.5,0.5,29,-0.5,0.5);

  TH2F* h_JetKs2pipiL = new TH2F("h_JetKs2pipiL","K_{S} #rightarrow #pi^{+}#pi^{-} in light jets",29,-0.5,0.5,29,-0.5,0.5);
  TH2F* h_JetKs2pipiPiL = new TH2F("h_JetKs2pipiPiL","#pi's from K_{S} #rightarrow #pi^{+}#pi^{-} in light jets",29,-0.5,0.5,29,-0.5,0.5);

  TH1F* h_Kspipi = new TH1F("h_Kspipi","No. of K_{S} #rightarrow #pi^{+}#pi^{-}",8,0,8);
  TH1F* h_Ks_pipi_consec = new TH1F("h_Ks_pipi_consec","No. of K_{S} #rightarrow #pi^{+}#pi^{-} (Consecutive Pions)",8,0,8);

  TH1F* h_Ks_p = new TH1F("h_Ks_p","K_{S} momentum",100,0,20);

  // event counter
  int evt = 0;

  int nKspipi_max=0; // checking max no of Ks
  
  while(tree.Next())
    {

      if(evt%10000==0) cout<<evt<<" events processed"<<endl;
      
      float jPx=0., jPy=0., jPz=0., jE=0., invMjet=0.;
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
      int nKspipi = Ks2pipi->size()/3; // Ks counter
      h_Kspipi->Fill(nKspipi);
      if(nKspipi > nKspipi_max) nKspipi_max = nKspipi;  // max Ks counter

      float px=0., py=0., pz=0., e=0.;
      TLorentzVector p4;
      float KsAngJ1=0., KsAngJ2=0.;
      float PiAngJ1=0., PiAngJ2=0.;
      float p_normKsJ1=0., KsThetaJ1=0., KsPhiJ1=0.;
      float p_normKsJ2=0., KsThetaJ2=0., KsPhiJ2=0.;
      float p_normPiJ1=0., PiThetaJ1=0., PiPhiJ1=0.;
      float p_normPiJ2=0., PiThetaJ2=0., PiPhiJ2=0.;
      for(int iKP=0; iKP<Ks2pipi->size(); iKP++)
	{
	  px = MCpx->at(Ks2pipi->at(iKP));
	  py = MCpy->at(Ks2pipi->at(iKP));
	  pz = MCpz->at(Ks2pipi->at(iKP));
	  e = MCe->at(Ks2pipi->at(iKP));
	  
	  p4.SetPxPyPzE(px, py, pz, e);

	  // cuts
	  //if(p4.Pt()<0.5) continue;
	  //if(abs(cos(p4.Theta()))>0.97) continue;
	  
	  //cout<<MCpdg->at(Ks2pipi->at(iKP))<<endl;
	  // K-shorts
	  if(iKP%3 == 0)
	    {
	      // angle to assign to a jet, normalise with momentum magnitude, get delta theta and delta phi (NOTE: delta phi is not simply the difference between phi's of the particle and the jet)

	      h_Ks_p->Fill(p4.Pt());
	      
	      KsAngJ1 = p4.Angle(p_Jet[0].Vect());
	      KsAngJ2 = p4.Angle(p_Jet[1].Vect());
	      
	      p_normKsJ1 = p4.P()/p_Jet[0].P();
	      KsThetaJ1 = p4.Theta() - p_Jet[0].Theta();
	      KsPhiJ1 = p4.DeltaPhi(p_Jet[0]);
	      
	      p_normKsJ2 = p4.P()/p_Jet[1].P();
	      KsThetaJ2 = p4.Theta() - p_Jet[1].Theta();
	      KsPhiJ2 = p4.DeltaPhi(p_Jet[1]);

	      // assign to a jet if within 0.5 rad to that jet's axis
	      if(KsAngJ1<0.5) h_JetKs2pipiL->Fill(KsThetaJ1, KsPhiJ1, p_normKsJ1);
	      else if(KsAngJ2<0.5) h_JetKs2pipiL->Fill(KsThetaJ2, KsPhiJ2, p_normKsJ2);
	    }
	  // Pions
	  if(abs(MCpdg->at(Ks2pipi->at(iKP))) == 211)
	    {
	      // same as for Ks but twice for each decay
	      
	      PiAngJ1 = p4.Angle(p_Jet[0].Vect());
	      PiAngJ2 = p4.Angle(p_Jet[1].Vect());
	      
	      p_normPiJ1 = p4.P()/p_Jet[0].P();
	      PiThetaJ1 = p4.Theta() - p_Jet[0].Theta();
	      PiPhiJ1 = p4.DeltaPhi(p_Jet[0]);
	      
	      p_normPiJ2 = p4.P()/p_Jet[1].P();
	      PiThetaJ2 = p4.Theta() - p_Jet[1].Theta();
	      PiPhiJ2 = p4.DeltaPhi(p_Jet[1]);

	      // assign to a jet if within 05 rad to that jet's axis
	      if(abs(PiThetaJ1)<0.5 && abs(PiPhiJ1)<0.5) h_JetKs2pipiPiL->Fill(PiThetaJ1, PiPhiJ1, p_normPiJ1);
	      else if(abs(PiThetaJ2)<0.5 && abs(PiPhiJ2)<0.5) h_JetKs2pipiPiL->Fill(PiThetaJ2, PiPhiJ2, p_normPiJ2);
	    }
	  
	}
      /*
      // consecutive pions: DOESN'T WORK
      int nKs_pipi=0, recount=-1;
      for(int iPi=0; iPi<MCpdgF->size(); iPi++)
	{
	  if(iPi == MCpdgF->size()-1) break;
	  if(abs(MCpdgF->at(iPi))==211 && abs(MCpdgF->at(iPi+1))==211 && iPi!=recount && (MCpdgF->at(iPi)*MCpdgF->at(iPi+1))<0)
	    {
	      nKs_pipi++;
	      recount = iPi+1;
	    }
	}
      h_Ks_pipi_consec->Fill(nKs_pipi);
      */

      // extract jet constituents
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;

      // JET 1
      float px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
      TLorentzVector p4_j1;

      float p_norm1 = 0.;
      float delta_theta1 = 0., delta_phi1 = 0.;

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
	  if(abs(MCpdgF->at(ele))==321) h_JetCKaonL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // Kl
	  if(abs(MCpdgF->at(ele))==130) h_JetNKaonL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // pi+-
	  if(abs(MCpdgF->at(ele))==211) h_JetCPionL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // e+-
	  if(abs(MCpdgF->at(ele))==11) h_JetElecL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // Muon
	  //if(abs(MCpdgF->at(ele))==13) h_JetMuonL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // photon
	  if(abs(MCpdgF->at(ele))==22) h_JetPhotL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // p
	  if(abs(MCpdgF->at(ele))==2212) h_JetProtL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	  // n
	  if(abs(MCpdgF->at(ele))==2112) h_JetNeutL->Fill(delta_theta1,delta_phi1,p_norm1);
	  
	}
            
      // JET 2
      float px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
      TLorentzVector p4_j2;

      float p_norm2 = 0.;
      float delta_theta2 = 0., delta_phi2 = 0.;

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
	  if(abs(MCpdgF->at(ele))==321) h_JetCKaonL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // Kl
	  if(abs(MCpdgF->at(ele))==130) h_JetNKaonL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // pi+-
	  if(abs(MCpdgF->at(ele))==211) h_JetCPionL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // e+-
	  if(abs(MCpdgF->at(ele))==11) h_JetElecL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // Muon
	  //if(abs(MCpdgF->at(ele))==13) h_JetMuonL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // photon
	  if(abs(MCpdgF->at(ele))==22) h_JetPhotL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // p
	  if(abs(MCpdgF->at(ele))==2212) h_JetProtL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	  // n
	  if(abs(MCpdgF->at(ele))==2112) h_JetNeutL->Fill(delta_theta2,delta_phi2,p_norm2);
	  
	}

      // empty the jet constituent vectors
      jet1Const.clear();
      jet2Const.clear();
      
      evt++;
      //cout<<"============================"<<endl;
    }

  cout<<"processed all events"<<endl;
  
  cout<<"Max number of Ks->pipi is "<<nKspipi_max<<endl;
  
  file->Close();
  cout<<"event file closed"<<endl;

  h_JetCKaonL->Write();
  h_JetNKaonL->Write();
  h_JetCPionL->Write();
  h_JetElecL->Write();
  //h_JetMuonL->Write();
  h_JetPhotL->Write();
  h_JetProtL->Write();
  h_JetNeutL->Write();
  h_JetKs2pipiL->Write();
  h_JetKs2pipiPiL->Write();

  h_Kspipi->Write();
  h_Ks_pipi_consec->Write();
  h_Ks_p->Write();

  cout<<"hists written to file"<<endl;

  histFile.Close();
  cout<<"hist file closed"<<endl;
      
  //delete jetConst;
  //jetConst = NULL;
  
  return -1;
}
