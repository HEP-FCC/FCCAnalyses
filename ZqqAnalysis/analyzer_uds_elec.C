// studying the jet tagging from FCCAnalyses by checking the statistics - too many untagged events
// also studying the e+- multiplicity in u/d/s jets - not as few as muons but still not comparable to other categories
// no cuts

#include <iostream>
#include <cmath>
#include <vector>

#include <TObject.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include "ROOT/RVec.hxx"
#include <TFile.h>
#include <TTree.h>
#include <TH1I.h>
#include <TPie.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <TSystem.h>
#include <TInterpreter.h>

using namespace std;

int main()
{
  gInterpreter->GenerateDictionary("vector<vector<int> >","vector");

  TFile *file = TFile::Open("p8_ee_Zuds_ecm91.root");
  TTreeReader tree("events", file);
  int nEvents = tree.GetEntries();
  cout<<"Number of Events: "<<nEvents<<endl;

  // All particles                                                       
  /*
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpx(tree, "MC_px");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpy(tree, "MC_py");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpz(tree, "MC_pz");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCe(tree, "MC_e");
  TTreeReaderValue<vector<float,ROOT::Detail::VecOps::RAdoptAllocator<float>>> MCpdg(tree, "MC_pdg");
  */
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
  TTreeReaderValue<vector<int,ROOT::Detail::VecOps::RAdoptAllocator<int>>> jetFlavour(tree, "jets_ee_kt_flavour");

  TString histfname;
  histfname = "histZuds.root";
  TFile histFile(histfname,"RECREATE");

  // histograms
  TH1I* h_nEB = new TH1I("h_nEB", "No. of e in b-jets", 8, 0, 8);

  TH1I* h_nES = new TH1I("h_nES", "No. of e in s-jets", 8, 0, 8);
  TH1I* h_nEU = new TH1I("h_nEU", "No. of e in u-jets", 8, 0, 8);
  TH1I* h_nED = new TH1I("h_nED", "No. of e in d-jets", 8, 0, 8);
  
  // event counter
  int evt = 0;
  int untagged = 0;
  int d_tags=0, u_tags=0, s_tags=0, c_tags=0, b_tags=0;

  // event loop
  while(tree.Next())
    {
      if(evt%10000==0) cout<<evt<<" events processed"<<endl<<"jet flavours: "<<jetFlavour->at(0)<<" & "<<jetFlavour->at(1)<<endl;	

      if(jetFlavour->at(0)==0) untagged++;
      if(jetFlavour->at(1)==0) untagged++;

      if(jetFlavour->at(0)==1) d_tags++;
      if(jetFlavour->at(1)==1) d_tags++;

      if(jetFlavour->at(0)==2) u_tags++;
      if(jetFlavour->at(1)==2) u_tags++;

      if(jetFlavour->at(0)==3) s_tags++;
      if(jetFlavour->at(1)==3) s_tags++;

      if(jetFlavour->at(0)==4) c_tags++;
      if(jetFlavour->at(1)==4) c_tags++;

      if(jetFlavour->at(0)==5) b_tags++;
      if(jetFlavour->at(1)==5) b_tags++;


      // extract jet constituents
      //int nJetC = jetConst->size();
      vector<int> jet1Const, jet2Const;
      if(jetConst->size()>=1)      jet1Const = jetConst->at(0);
      else cout<<"No jet constituents found"<<endl;
      if(jetConst->size()>=2)      jet2Const = jetConst->at(1);
      else cout<<"Second jet constituents not found"<<endl;
      
      // without discriminating among uds

      // JET 1
      int nES=0, nEU=0, nED=0, nEB=0;
      
      for(int ele : jet1Const) 
	{
	  if(abs(MCpdgF->at(ele))==11)
	    {
	      nEB++;

	      if(jetFlavour->at(0)==3) nES++;
	      if(jetFlavour->at(0)==2) nEU++;
	      if(jetFlavour->at(0)==1) nED++;
	    }
	}
      
      h_nEB->Fill(nEB);
      if(jetFlavour->at(0)==3) h_nES->Fill(nES);
      if(jetFlavour->at(0)==2) h_nEU->Fill(nEU);
      if(jetFlavour->at(0)==1) h_nED->Fill(nED);
      
      // JET 2
      // need counts for each jet separately so zeroed all counters
      nES=0, nEU=0, nED=0, nEB=0;
      
      for(int ele : jet2Const) 
	{
	  if(abs(MCpdgF->at(ele))==11)
	    {
	      nEB++;

	      if(jetFlavour->at(1)==3) nES++;
	      if(jetFlavour->at(1)==2) nEU++;
	      if(jetFlavour->at(1)==1) nED++;
	    }
	}
      
      h_nEB->Fill(nEB);
      if(jetFlavour->at(1)==3) h_nES->Fill(nES);
      if(jetFlavour->at(1)==2) h_nEU->Fill(nEU);
      if(jetFlavour->at(1)==1) h_nED->Fill(nED);
      
      jet1Const.clear();
      jet2Const.clear();

      evt++;
    }

  cout<<"processed all events"<<endl<<"there are "<<untagged<<" untagged jets, "<<d_tags<<" d-tagged jets, "<<u_tags<<" u-tagged jets, "<<s_tags<<" s-tagged jets, "<<c_tags<<" c-tagged jets, and "<<b_tags<<" b-tagged jets"<<endl;

  file->Close();
  cout<<"closed the event file"<<endl;

  h_nES->Write();
  h_nEU->Write();
  h_nED->Write();
  h_nEB->Write();
  histFile.Close();
  cout<<"hists written and file closed"<<endl;

  //delete jetConst;
  //jetConst = NULL;

  return -1;
}
