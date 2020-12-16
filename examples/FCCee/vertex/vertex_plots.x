{

gROOT->Reset();

// processed :
// /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_Zuds_ecm91/events_199980034.root

TFile* f = new TFile("events_199980034.root");
TTree* events = (TTree*)f->Get("events");

// plot the normalised chi2 / ndf :
TH1F* hchi2 = new TH1F("hchi2",";chi2; Events",100,0,10);
events->Draw("Vertex.chi2>>hchi2","Vertex.chi2<10") ;
	// OK-ish. For 98% of the events, the chi2//ndf is < 10.


TString cut = "Vertex.chi2 <10";

// ---------------------------------------------------------------
//
// Vertex resolutions - these  GEN events have no vertex smearing
//
// ---------------------------------------------------------------


TH1F*  hx = new TH1F("hx",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-40,40);
events -> Draw( "Vertex.position.x * 1e6 >> hx", cut);    // the vertex positions 
							  // im the tree  are in m.
hx -> Fit("gaus");

TH1F*  hy = new TH1F("hy",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-40,40);
events -> Draw( "Vertex.position.y * 1e6 >> hy", cut);    
hy -> Fit("gaus");

TH1F*  hz = new TH1F("hz",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-40,40);
events -> Draw( "Vertex.position.z * 1e6 >> hz", cut);
hz -> Fit("gaus");

	// OKish, the resolutions are of a few microns.


// ---------------------------------------------------------------
//
// Pulls of the reconstructed vertex
//
// ---------------------------------------------------------------

// covMatrix[0] = cov(0,0) = variance of the x position
// covMatrix[3] = cov(1,1) = variance of the y position
// covMatrix[5] = cov(2,2) = variance of the z position

TH1F*  px = new TH1F("px","; Pull x_{vtx}; Events",100,-5,5);
events -> Draw( "Vertex.position.x / TMath::Sqrt( Vertex.covMatrix[0] ) >> px",cut);

TH1F*  py = new TH1F("py","; Pull y_{vtx}; Events",100,-5,5);
events -> Draw( "Vertex.position.y / TMath::Sqrt( Vertex.covMatrix[3] ) >> py",cut);

TH1F*  pz = new TH1F("pz","; Pull z_{vtx}; Events",100,-5,5);
events -> Draw( "Vertex.position.z / TMath::Sqrt( Vertex.covMatrix[5] ) >> pz",cut);

	// not so great, the pulls are large especially for (x,y).
	// Suspiscion that it is due to the fact that the events are
	// generated at vtx = (0, 0, 0).
	// See the same with Framco's test code, under the same condition.


// ---------------------------------------------------------------
//
// Plots :

TCanvas* c1 = new TCanvas("c1","c1");
c1 -> Divide(2,2);
c1 ->cd(1); hchi2 -> Draw();
c1->cd(2); hx->Draw();
c1->cd(3); hy -> Draw();
c1->cd(4); hz->Draw();

TCanvas* c2 = new TCanvas("c2","c2");
c2->Divide(2,2);
c2->cd(1); px->Draw();
c2->cd(2); py->Draw();
c2->cd(3); pz->Draw();

}

