// jet-images (wrote for Zbb, practically no changes for Zuds): 8 categories- K+-, Kl, pi+-, e+-, mu+-, photon, p, n (plan to remove muons, maybe also electrons - too few)
// Note: Give each jet image a different name, event if of same type. e.g. h_JetCKaon[i] needs to have a unique name for each i
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
    
  TString histfname;
  histfname = "histZuds_jetImages.root";
  TFile histFile(histfname,"RECREATE");
  
  vector<TH2F*> h_JetCKaonB;
  vector<TH2F*> h_JetNKaonB;
  vector<TH2F*> h_JetCPionB;
  vector<TH2F*> h_JetElecB;
  vector<TH2F*> h_JetMuonB;
  vector<TH2F*> h_JetPhotB;
  vector<TH2F*> h_JetProtB;
  vector<TH2F*> h_JetNeutB;
  
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
      
      h_JetCKaonB.push_back(new TH2F(sck.c_str(),"K^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetNKaonB.push_back(new TH2F(snk.c_str(),"K_{L} in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetCPionB.push_back(new TH2F(scp.c_str(),"#pi^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetElecB.push_back(new TH2F(se.c_str(),"e^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetMuonB.push_back(new TH2F(smu.c_str(),"#mu^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetPhotB.push_back(new TH2F(sph.c_str(),"#gamma in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetProtB.push_back(new TH2F(sp.c_str(),"p in b jets",29,-0.5,0.5,29,-0.5,0.5));
      h_JetNeutB.push_back(new TH2F(sn.c_str(),"n in b jets",29,-0.5,0.5,29,-0.5,0.5));
    }

  cout<<"defined histograms"<<endl;
  
  // event counter
  int evt = 0;
  
  while(tree.Next()) {

    if(evt%10000==0) cout<<evt<<" events processed"<<endl;
    
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
      if(abs(MCpdgF->at(ele))==321) h_JetCKaonB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);

      // Kl
      if(abs(MCpdgF->at(ele))==130) h_JetNKaonB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);

      // pi+-
      if(abs(MCpdgF->at(ele))==211) h_JetCPionB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // e+-
      if(abs(MCpdgF->at(ele))==11) h_JetElecB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // mu+-
      if(abs(MCpdgF->at(ele))==13) h_JetMuonB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // photon
      if(abs(MCpdgF->at(ele))==22) h_JetPhotB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // p
      if(abs(MCpdgF->at(ele))==2212) h_JetProtB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);
      
      // n
      if(abs(MCpdgF->at(ele))==2112) h_JetNeutB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);      
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
      if(abs(MCpdgF->at(ele))==321) h_JetCKaonB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);

      // Kl
      if(abs(MCpdgF->at(ele))==130) h_JetNKaonB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);

      // pi+-
      if(abs(MCpdgF->at(ele))==211) h_JetCPionB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // e+-
      if(abs(MCpdgF->at(ele))==11) h_JetElecB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // mu+-
      if(abs(MCpdgF->at(ele))==13) h_JetMuonB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // photon
      if(abs(MCpdgF->at(ele))==22) h_JetPhotB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // p
      if(abs(MCpdgF->at(ele))==2212) h_JetProtB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);
      
      // n
      if(abs(MCpdgF->at(ele))==2112) h_JetNeutB[nEvents+evt]->Fill(delta_theta2,delta_phi2,p_norm2);
    }

    //cout<<"End of Jet 2"<<endl;

    jet1Const.clear();
    jet2Const.clear();
    
    evt++;
  }
  
  cout<<"processed all events"<<endl;
  
  file->Close();
  
  //TList *hist_list = new TList();
  
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

