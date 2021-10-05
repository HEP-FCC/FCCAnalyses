// Trial to implement THnSparse to reduce the file size for the jet-image file (uses Zbb, change file name to get Zuds)
// File size is reduced but still stores everything until histograms are written, therefore fails when not enough RAM; tried writing histograms inside the event loop, didn't work. NEED A FIX (run in batches? How?)
// Note: Give each jet image a different name, event if of same type. e.g. h_JetCKaon[i] needs to have a unique name for each i                             
// No cuts

#include <iostream>
#include <cmath>
#include <vector>

#include <TObject.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TH2F.h>
#include <THnSparse.h>
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
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPx(tree, "jets_ee_kt_p\
x");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPy(tree, "jets_ee_kt_p\
y");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetPz(tree, "jets_ee_kt_p\
z");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> jetE(tree, "jets_ee_kt_e"\
										    );

  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  TString histfname;
  histfname = "histZbb_jets_sparse.root";
  TFile histFile(histfname,"RECREATE");

  cout<<"Before defining histograms"<<endl;

  // Using THnSparse for hists
  int ndim = 2;
  int nbin[2] = {29, 29};
  double xmin[2] = {-0.5, -0.5};
  double xmax[2] = {0.5, 0.5};
  //int nchunk = 1024*2;

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

      h_JetCKaonB.push_back(new THnSparseD(sck.c_str(),"K^{+/-} in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetNKaonB.push_back(new THnSparseD(snk.c_str(),"K_{L} in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetCPionB.push_back(new THnSparseD(scp.c_str(),"#pi^{+/-} in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetElecB.push_back(new THnSparseD(se.c_str(),"e^{+/-} in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetMuonB.push_back(new THnSparseD(smu.c_str(),"#mu^{+/-} in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetPhotB.push_back(new THnSparseD(sph.c_str(),"#gamma in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetProtB.push_back(new THnSparseD(sp.c_str(),"p in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
      h_JetNeutB.push_back(new THnSparseD(sn.c_str(),"n in b jets",ndim,nbin,xmin,xmax/*,nchunk*/));
    }
  
  cout<<"After defining histograms"<<endl;

  // event counter
  int evt = 0;

  while(tree.Next())
    {
      if(evt%10000==0) cout<<evt<<" done"<<endl;

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
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB[evt]->Fill(delta1,p_norm1);
	  
	  // Kl
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonB[evt]->Fill(delta1,p_norm1);
	  
	  // pi+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionB[evt]->Fill(delta1,p_norm1);

	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecB[evt]->Fill(delta1,p_norm1);
	  
	  // mu+-
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonB[evt]->Fill(delta1,p_norm1);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotB[evt]->Fill(delta1,p_norm1);
	  
	  // proton
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtB[evt]->Fill(delta1,p_norm1);
	  
	  // neutron
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutB[evt]->Fill(delta1,p_norm1);
	  
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
	  if(MCpdgF->at(ele)==321 || MCpdgF->at(ele)==-321) h_JetCKaonB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // K0
	  if(MCpdgF->at(ele)==130 || MCpdgF->at(ele)==-130) h_JetNKaonB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // pi+-
	  if(MCpdgF->at(ele)==211 || MCpdgF->at(ele)==-211) h_JetCPionB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // e+-
	  if(MCpdgF->at(ele)==11 || MCpdgF->at(ele)==-11) h_JetElecB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // mu+-
	  if(MCpdgF->at(ele)==13 || MCpdgF->at(ele)==-13) h_JetMuonB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // photon
	  if(MCpdgF->at(ele)==22 || MCpdgF->at(ele)==-22) h_JetPhotB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // proton
	  if(MCpdgF->at(ele)==2212 || MCpdgF->at(ele)==-2212) h_JetProtB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	  // Neutron
	  if(MCpdgF->at(ele)==2112 || MCpdgF->at(ele)==-2112) h_JetNeutB[nEvents+evt]->Fill(delta2,p_norm2);
	  
	}

      jet1Const.clear();
      jet2Const.clear();

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

      evt++;
    }
      
  cout<<"Event loop ends"<<endl;

  file->Close();
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
  cout<<"hists written to file"<<endl;

  histFile.Close();

  cout<<"hist file closed"<<endl;
      
  //delete jetConst;
  //jetConst = NULL;
  
  return -1;
}
