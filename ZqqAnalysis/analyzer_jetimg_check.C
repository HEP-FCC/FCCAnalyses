// Histogram jet images for first 5 events (i.e. first 10 jets) of the Zuds file to compare with Edi's; if they match, use the h5py files, wouldn't need to edit the network code to read root files
// No Ks or pi0
// Cuts: pt>0.5, |cos(theta)|<0.97 (~14deg)

#include <iostream>
#include <cmath>
#include <vector>
#include <sstream>
#include <string>

#include <TObject.h>
#include <TList.h>
#include <TKey.h>
#include <TFile.h>
#include <TTree.h>
#include <TH2.h>
#include <TH2F.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include "ROOT/RVec.hxx"
#include <TSystem.h>
#include <TInterpreter.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>

using namespace std;
int main() {
  
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
  
  int test_events = 5; // testing on 5 events (10 jets)

  TString histfname;
  histfname = "histZuds_jetImages_check.root";
  TFile histFile(histfname,"RECREATE");
  
  vector<TH2F*> h_JetCKaonL;
  vector<TH2F*> h_JetNKaonL;
  vector<TH2F*> h_JetCPionL;
  vector<TH2F*> h_JetElecL;
  vector<TH2F*> h_JetMuonL;
  vector<TH2F*> h_JetPhotL;
  vector<TH2F*> h_JetProtL;
  vector<TH2F*> h_JetNeutL;

  for(int nH=0; nH<2*test_events; nH++)
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
      
      h_JetCKaonL.push_back(new TH2F(sck.c_str(),"K^{+/-} in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetNKaonL.push_back(new TH2F(snk.c_str(),"K_{L} in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetCPionL.push_back(new TH2F(scp.c_str(),"#pi^{+/-} in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetElecL.push_back(new TH2F(se.c_str(),"e^{+/-} in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetMuonL.push_back(new TH2F(smu.c_str(),"#mu^{+/-} in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetPhotL.push_back(new TH2F(sph.c_str(),"#gamma in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetProtL.push_back(new TH2F(sp.c_str(),"p in uds jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetNeutL.push_back(new TH2F(sn.c_str(),"n in uds jets",29,-0.5,0.5,29,-0.5,0.5));
    }

  cout<<"defined histograms"<<endl;
  
  // event counter
  int evt = 0;
  
  while(tree.Next() && evt<test_events) {

    //if(evt%10000==0) cout<<evt<<" events processed"<<endl;
    cout<<"Event No. "<<evt<<endl;
    
    // jets
    float jPx=0., jPy=0., jPz=0., jE=0., invMjet=0.;
    int nJet = jetE->size();
    TLorentzVector p_Jet[nJet], p_Jets;
    
    for(unsigned int j=0; j<nJet; j++) {
      jE = jetE->at(j);
      jPx = jetPx->at(j);
      jPy = jetPy->at(j);
      jPz = jetPz->at(j);
      
      p_Jet[j].SetPxPyPzE(jPx, jPy, jPz, jE);
      
      cout<<"Jet "<<j+1<<" p: ("<<p_Jet[j].Px()<<", "<<p_Jet[j].Py()<<", "<<p_Jet[j].Pz()<<", "<<p_Jet[j].E()<<")"<<endl;

      // sum of all jets' momenta
      p_Jets += p_Jet[j];
    }
    
    //cout<<"Before writing jet constituents"<<endl;
    
    // jet constituents
    vector<int> jet1Const, jet2Const;
    if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
    else cout<<"No jet constituents found"<<endl;
    if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
    else cout<<"Second jet constituents not found"<<endl;
    
    //cout<<"after writing jet consitituents"<<endl;
    
    // JET 1
    float px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
    TLorentzVector p4_j1;
    
    float p_norm1 = 0.;
    float delta_theta1 = 0., delta_phi1 = 0.;
    
    for(int ele : jet1Const) {
      px_j1 = MCpxF->at(ele);
      py_j1 = MCpyF->at(ele);
      pz_j1 = MCpzF->at(ele);
      e_j1 = MCeF->at(ele);
      
      p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);

      // cuts
      if(p4_j1.Pt() < 0.5) continue;
      if(abs(cos(p4_j1.Theta())) > 0.97) continue;
      
      p_norm1 = p4_j1.P()/p_Jet[0].P();
      delta_theta1 = p4_j1.Theta() - p_Jet[0].Theta();
      delta_phi1 = p4_j1.DeltaPhi(p_Jet[0]);
      
      // K+-
      if(abs(MCpdgF->at(ele))==321) h_JetCKaonL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);

      // Kl
      if(abs(MCpdgF->at(ele))==130) h_JetNKaonL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);

      // pi+-
      if(abs(MCpdgF->at(ele))==211) h_JetCPionL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // e+-
      if(abs(MCpdgF->at(ele))==11) h_JetElecL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // mu+-
      if(abs(MCpdgF->at(ele))==13) h_JetMuonL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // photon
      if(abs(MCpdgF->at(ele))==22) h_JetPhotL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // p
      if(abs(MCpdgF->at(ele))==2212) h_JetProtL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // n
      if(abs(MCpdgF->at(ele))==2112) h_JetNeutL[2*evt]->Fill(delta_theta1,delta_phi1,p_norm1);      
    }

    // JET 2
    float px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
    TLorentzVector p4_j2;
    
    float p_norm2 = 0.;
    float delta_theta2 = 0., delta_phi2 = 0.;
    
    for(int ele : jet2Const) {
      px_j2 = MCpxF->at(ele);
      py_j2 = MCpyF->at(ele);
      pz_j2 = MCpzF->at(ele);
      e_j2 = MCeF->at(ele);
      
      p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);
      
      // cuts
      if(p4_j2.Pt() < 0.5) continue;
      if(abs(cos(p4_j2.Theta())) > 0.97) continue;

      p_norm2 = p4_j2.P()/p_Jet[1].P();
      delta_theta2 = p4_j2.Theta() - p_Jet[1].Theta();
      delta_phi2 = p4_j2.DeltaPhi(p_Jet[1]);
      
      // K+-
      if(abs(MCpdgF->at(ele))==321) h_JetCKaonL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);

      // Kl
      if(abs(MCpdgF->at(ele))==130) h_JetNKaonL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);

      // pi+-
      if(abs(MCpdgF->at(ele))==211) h_JetCPionL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // e+-
      if(abs(MCpdgF->at(ele))==11) h_JetElecL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // mu+-
      if(abs(MCpdgF->at(ele))==13) h_JetMuonL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // photon
      if(abs(MCpdgF->at(ele))==22) h_JetPhotL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // p
      if(abs(MCpdgF->at(ele))==2212) h_JetProtL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // n
      if(abs(MCpdgF->at(ele))==2112) h_JetNeutL[2*evt+1]->Fill(delta_theta2,delta_phi2,p_norm2);
    }

    cout<<"==================================================================="<<endl;

    jet1Const.clear();
    jet2Const.clear();
    
    evt++;
  }
  
  cout<<"processed all events"<<endl;
  
  file->Close();
  
  //TList *hist_list = new TList();
  
  for(int iH=0; iH<2*test_events; iH++) {
    //hist_list->Add(h_JetCKaonL[iH]);
    h_JetCKaonL[iH]->Write();
    h_JetNKaonL[iH]->Write();
    h_JetCPionL[iH]->Write();
    h_JetElecL[iH]->Write();
    h_JetMuonL[iH]->Write();
    h_JetPhotL[iH]->Write();
    h_JetProtL[iH]->Write();
    h_JetNeutL[iH]->Write();
  }
  
  cout<<"hists written to file"<<endl;
  
  //hist_list->Write("histZbb_jemages");
  //histFile.Write();
  
  //cout<<"Hist file written"<<endl;
  
  //histFile->Write();
  histFile.Close();
  
  cout<<"hist file closed"<<endl;
  
  //delete jetConst;
  //jetConst = NULL;
    
  return -1;
}

