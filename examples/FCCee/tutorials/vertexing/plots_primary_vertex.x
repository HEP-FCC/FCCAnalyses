{

gROOT->Reset();


TFile* f = new TFile("primary_Zuds.root");
TTree* events = (TTree*)f->Get("events");

//TString vtx = "Vertex_primaryTracks";   // primary tracks selected based on MC-matching
//TString vtx = "Vertex_primaryTracks_BSC";   // primary tracks selected based on MC-matching, fit with beam-spot constraint
TString vtx = "PrimaryVertex";      // primary tracks selected from the reco algorithm,  fit with beam spot constraint




// plot the normalised chi2 / ndf :
TH1F* hchi2 = new TH1F("hchi2",";chi2; Events",100,0,10);
events->Draw("PrimaryVertex.chi2>>hchi2" );


TString cut = "PrimaryVertex.chi2 <10 ";

// ---------------------------------------------------------------------------
//
// Vertex resolutions 
// The MC_PrimaryVertex and the reco'ed vertex in the ntuple are both in mm
//
//	The resolutions  are of a few microns.
// ---------------------------------------------------------------------------


TH1F*  hx = new TH1F("hx",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-40,40);
events -> Draw( "PrimaryVertex.position.x * 1e3  - MC_PrimaryVertex.x()*1e3>> hx", cut);    
hx -> Fit("gaus");

TH1F*  hy = new TH1F("hy",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-40,40);
events -> Draw( "PrimaryVertex.position.y * 1e3 - MC_PrimaryVertex.y()*1e3  >> hy", cut);    
hy -> Fit("gaus");

TH1F*  hz = new TH1F("hz",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-40,40);
events -> Draw( "PrimaryVertex.position.z * 1e3 - MC_PrimaryVertex.z()*1e3 >> hz", cut);
hz -> Fit("gaus");



// ---------------------------------------------------------------
//
// Pulls of the reconstructed vertex
//
// ---------------------------------------------------------------

// covMatrix[0] = cov(0,0) = variance of the x position
// covMatrix[2] = cov(1,1) = variance of the y position
// covMatrix[5] = cov(2,2) = variance of the z position

TH1F*  px = new TH1F("px","; Pull x_{vtx}; Events",100,-5,5);
events -> Draw( " (PrimaryVertex.position.x - MC_PrimaryVertex.x()) / TMath::Sqrt( PrimaryVertex.covMatrix[0] ) >> px",cut);
px->Fit("gaus");

TH1F*  py = new TH1F("py","; Pull y_{vtx}; Events",100,-5,5);
events -> Draw( "(PrimaryVertex.position.y - MC_PrimaryVertex.y()) / TMath::Sqrt( PrimaryVertex.covMatrix[2] ) >> py",cut);
py->Fit("gaus");

TH1F*  pz = new TH1F("pz","; Pull z_{vtx}; Events",100,-5,5);
events -> Draw( "(PrimaryVertex.position.z - MC_PrimaryVertex.z())  / TMath::Sqrt( PrimaryVertex.covMatrix[5] ) >> pz",cut);
pz->Fit("gaus");



// ---------------------------------------------------------------
//
// Plots :

TCanvas* c1 = new TCanvas("c1","c1");
//gStyle->SetOptStat(0);
c1 -> Divide(2,2);
c1 ->cd(1); hchi2 -> Draw();
c1->cd(2); hx->Draw();
c1->cd(3); hy -> Draw();
c1->cd(4); hz->Draw();

TCanvas* c2 = new TCanvas("c2","c2");
gStyle->SetOptStat(1111);
c2->Divide(2,2);
c2->cd(1); px->Draw();
c2->cd(2); py->Draw();
c2->cd(3); pz->Draw();



}

