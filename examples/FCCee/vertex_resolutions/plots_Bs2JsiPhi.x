{

TChain* events = new TChain("events","events");
events -> Add("Bs2JpsiPhi_evtgen.root");
events -> Add("Bs2JpsiPhi_evtgen_2.root");
events -> Add("Bs2JpsiPhi_evtgen_3.root");
events -> Add("Bs2JpsiPhi_evtgen_4.root");


TString cut0 = "BsMCDecayVertex.position.z < 1e10" ;   // a Bs -> mumuKK has been found in MCParticle

// Number of tracks
TH1F* hntr = new TH1F("hntr",";N( Bs tracks ); a.u.",5,-0.5,4.5);
events->Draw("n_BsTracks >>hntr", cut0);
TCanvas* cnt = new TCanvas("cnt","cnt");
gStyle->SetOptStat(10);   // Entries only
hntr->Draw();
gStyle->SetOptStat(10);
TLatex tt;
tt.SetTextSize(0.04);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
gPad -> SetLogy(1);
//cnt->SaveAs("plots/Bs2JPsiPhi_nTracks.pdf");

// Chi2 of the vertex fit
TCanvas* c1 = new TCanvas("c1","c1");
TH1F* hchi2 = new TH1F("hchi2",";#chi^{2}/n.d.f.; a.u.",100,0.,10.);
gStyle->SetOptStat(1110);
events->Draw("BsVertex.chi2 >>hchi2",cut0+"&& BsVertex.chi2>0");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
gPad -> SetLogy(1);
//c1->SaveAs("plots/Bs2JPsiPhi_chi2.pdf");

TString cut = cut0+" && BsVertex.chi2 < 10";

// Pulls of the vertex in x, y, z
TH1F* px = new TH1F("px",";Pull x_{vtx}; a.u.",100,-5,5) ;
events->Draw("(BsVertex.position.x-BsMCDecayVertex.x[0])/TMath::Sqrt(BsVertex.covMatrix[0])>>px",cut);

TH1F* py = new TH1F("py",";Pull y_{vtx}; a.u.",100,-5,5);
events->Draw("(BsVertex.position.y-BsMCDecayVertex.y[0])/TMath::Sqrt(BsVertex.covMatrix[3])>>py",cut);

TH1F* pz = new TH1F("pz",";Pull z_{vtx}; a.u.",100,-5,5);
events->Draw("(BsVertex.position.z-BsMCDecayVertex.z[0])/TMath::Sqrt(BsVertex.covMatrix[5])>>pz",cut);

TCanvas* c1 = new TCanvas("pulls","pulls");
px->Draw(); px->Fit("gaus");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");


// resolutions on the Bs decay vertex :
TH1F* hx = new TH1F("hx",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-40,40);
events->Draw("1e3*(BsVertex.position.x-BsMCDecayVertex.x[0]) >>hx",cut);

TF1* ff =new TF1("ff","gaus(0)+gaus(3)",-40,40);
ff->SetParameter(1,-5e-2) ;
ff->SetParameter(2,6);
ff->SetParameter(3,500) ;
ff->SetParameter(4,1e-2) ;
ff->SetParameter(5,15) ;
hx->Fit("ff","l") ;

TH1F* hy = new TH1F("hy",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-40,40);
events->Draw("1e3*(BsVertex.position.y-BsMCDecayVertex.y[0]) >>hy",cut);
hy->Fit("ff","l");

TH1F* hz = new TH1F("hz",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-40,40);
events->Draw("1e3*(BsVertex.position.z-BsMCDecayVertex.z[0]) >>hz",cut);
hz->Fit("ff","l");


// ----------------------------------------------------------------------------

// resolution on flight  distance :


TString fld = "TMath::Sqrt( pow( 1e3*BsVertex.position.x, 2) + pow( 1e3*BsVertex.position.y,2) + pow( 1e3*BsVertex.position.z,2))";
TString fld_gen = "TMath::Sqrt( pow( 1e3*BsMCDecayVertex.x[0], 2) + pow( 1e3*BsMCDecayVertex.y[0],2) + pow( 1e3*BsMCDecayVertex.z[0],2)   )";
TString fld_res =  fld + " - " + fld_gen;

TH1F* hfld = new TH1F("hfld","; flight distance (rec-true) (#mum); Events",100,-70,70);
events->Draw(fld_res+ " >> hfld", cut);
hfld->Fit("gaus");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");


// Pull of the flight distance :

TString fld_mm = "TMath::Sqrt( pow( BsVertex.position.x, 2) + pow( BsVertex.position.y,2) + pow( BsVertex.position.z,2))";
TString fld_gen_mm = "TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) + pow( BsMCDecayVertex.z[0],2)   )";
TString fld_res_mm =  fld_mm + " - " + fld_gen_mm;
TString term1 = " BsVertex.position.x * ( BsVertex.covMatrix[0] * BsVertex.position.x + BsVertex.covMatrix[1] * BsVertex.position.y + BsVertex.covMatrix[2] * BsVertex.position.z ) " ;
TString term2 = " BsVertex.position.y * ( BsVertex.covMatrix[1] * BsVertex.position.x + BsVertex.covMatrix[3] * BsVertex.position.y + BsVertex.covMatrix[4] * BsVertex.position.z ) " ;
TString term3 = " BsVertex.position.z * ( BsVertex.covMatrix[2] * BsVertex.position.x + BsVertex.covMatrix[4] * BsVertex.position.y + BsVertex.covMatrix[5] * BsVertex.position.z ) ";
TString tsum = term1 + " + " + term2 + " + " + term3;
TString fld_unc = " ( TMath::Sqrt( " + tsum + ") / " + fld_mm +" ) ";
TString fld_pull = "( " + fld_res_mm + " ) / " + fld_unc;
TH1F* h_fld_pull = new TH1F("h_fld_pull","; Pull flight distance; a.u.",100,-5,5);
events->Draw(fld_pull+" >> h_fld_pull" , cut);


TString cut4 = cut + " && n_BsTracks == 4";

// Profile of the flight distance resolution versus the uncertainty on the FD, nTracks = 4
TProfile* pro_unc = new TProfile("pro_unc",";uncertainty on the FD (#mum); flight distance (rec-true) (#mum)", 4,10.,50.,-70,70,"s");
events->Draw(fld_res+":"+fld_unc_mum+" >>pro_unc",cut4);
pro_unc->Draw();
gStyle->SetOptStat(0);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
tt.DrawLatexNDC(0.2,0.9,"N( B_{s} tracks ) = 4");
//c1->SaveAs("plots/profile_FD_uncertainty_on_FD_Ntra4.pdf");

// Profile of the flight distance resolution versus the theta of the Bs
TProfile* ptheta = new TProfile("ptheta",";#theta of B_{s} (rad); flight distance (rec-true) (#mum)",10,0.,TMath::Pi(),-70.,70.,"s");
events->Draw(fld_res+":Bs_theta >>ptheta",cut4);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
tt.DrawLatexNDC(0.2,0.9,"N( B_{s} tracks ) = 4");
gPad -> SetGridx(1);
gPad->SetGridy(1);
//c1->SaveAs("plots/profile_FD_theta_Bs.pdf");

// Profile of the flight distance resolution versus the flight distance
TProfile* pfld = new TProfile("pfld",";flight distance (mm); flight distance (rec-true) (#mum)", 4,0.,12.,-70,70,"s");
events->Draw(fld_res+":"+fld_mm+" >>pfld",cut4);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
tt.DrawLatexNDC(0.7,0.9,"N( B_{s} tracks ) = 4");
//c1->SaveAs("plots/profile_FDreso_FD.pdf");


// angular separations
TH1F* dmax = new TH1F("dmax",";#Delta#alpha max (rad); a.u.",100,0.,1.);
events->Draw("deltaAlpha_max >>dmax",cut)
TH1F* dmin = new TH1F("dmin",";#Delta#alpha min (rad); a.u.",100,0.,0.2);
events->Draw("deltaAlpha_min >>dmin",cut)
TH1F* dave = new TH1F("dave",";#Delta#alpha average (rad); a.u.",100,0.,1);
events->Draw("deltaAlpha_ave>>dave",cut);




}

