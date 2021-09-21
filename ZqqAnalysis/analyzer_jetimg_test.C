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
#include <TH1.h>
#include <TH2.h>
#include <TH2D.h>
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
 
  TFile *file = TFile::Open("p8_ee_Zbb_ecm91.root");
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
  
  cout<<"Before defining histograms"<<endl;
  
  TString histfname;
  histfname = "histZbb_jetImages.root";
  TFile histFile(histfname,"RECREATE");
  
  vector<TH2D*> h_JetCKaonB;
  
  for(int nH=0; nH<nEvents; nH++) {
    stringstream ss;
    ss<<"hist_jetCKaon_"<<nH;
    string s = ss.str();
    
    h_JetCKaonB.push_back(new TH2D(s.c_str(),"K^{+/-} in b jets",29,-0.5,0.5,29,-0.5,0.5));
  }

  
  cout<<"After defining histograms"<<endl;
  
  // event counter
  int evt = 0;
  
  while(tree.Next()) {

    if(evt%1000==0) cout<<evt<<" done"<<endl;
    
    // jets
    double jPx=0., jPy=0., jPz=0., jE=0., invMjet=0.;
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
    double px_j1=0, py_j1=0, pz_j1=0, e_j1=0;
    TLorentzVector p4_j1;
    
    double p_norm1 = 0.;
    double delta_theta1 = 0., delta_phi1 = 0.;
    
    //double delta_ang1=0.;
    for(int ele : jet1Const) {
      px_j1 = MCpxF->at(ele);
      py_j1 = MCpyF->at(ele);
      pz_j1 = MCpzF->at(ele);
      e_j1 = MCeF->at(ele);
      
      p4_j1.SetPxPyPzE(px_j1, py_j1, pz_j1, e_j1);
      
      p_norm1 = p4_j1.P()/p_Jet[0].P();
      delta_theta1 = p4_j1.Theta() - p_Jet[0].Theta();
      delta_phi1 = p4_j1.Phi() - p_Jet[0].Phi();
      
      // K+-
      if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB[evt]->Fill(delta_theta1,delta_phi1,p_norm1);
    }

    // JET 2
    double px_j2=0, py_j2=0, pz_j2=0, e_j2=0;
    TLorentzVector p4_j2;
    
    double p_norm2 = 0.;
    double delta_theta2 = 0., delta_phi2 = 0.;
    
    //double delta_ang2=0.;
    for(int ele : jet2Const) {
      px_j2 = MCpxF->at(ele);
      py_j2 = MCpyF->at(ele);
      pz_j2 = MCpzF->at(ele);
      e_j2 = MCeF->at(ele);
      
      p4_j2.SetPxPyPzE(px_j2, py_j2, pz_j2, e_j2);
      
      p_norm2 = p4_j2.P()/p_Jet[1].P();
      delta_theta2 = p4_j2.Theta() - p_Jet[1].Theta();
      delta_phi2 = p4_j2.Phi() - p_Jet[1].Phi();
      
      // K+-
      if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB[evt]->Fill(delta_theta2,delta_phi2,p_norm2);
    }

    //cout<<"End of Jet 2"<<endl;

    jet1Const.clear();
    jet2Const.clear();
    
    evt++;
  }
  
  cout<<"Event loop ends"<<endl;
  
  file->Close();
  
  //TList *hist_list = new TList();
  
  for(int iH=0; iH<nEvents; iH++) {
    //hist_list->Add(h_JetCKaonB[iH]);
    h_JetCKaonB[iH]->Write();
  }
  
  cout<<"defining hist file"<<endl;
  
  //hist_list->Write("histZbb_jemages");
  //histFile.Write();
  
  //cout<<"Hist file written"<<endl;
  
  //histFile->Write();
  histFile.Close();
  
  cout<<"Hist file closed"<<endl;
  
  //delete jetConst;
  //jetConst = NULL;
    
  return -1;
}

