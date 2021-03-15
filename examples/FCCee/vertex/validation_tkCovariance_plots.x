{

gROOT->Reset();

//
// Validation of  the off-diagonal terms of the covariance matrix
//
// Run over a file that contains the same gen-level dimuon
// event, that has been processed N times by Delphes.
//

TFile* f = new TFile("same_dimuonEvent_fullCovmat_v2.root");
TTree* evts = (TTree*)f->Get("events");

TString cut = "RP_TRK_omega >0";   // to select just one muon leg

// First retrieve the nominal values of the parameters of the track
// we are looking at :

evts->Draw("RP_TRK_D0", cut + "&& TMath::Abs(RP_TRK_D0) < 0.1") ;  // the RMS should be of a few microns. 
float d0_mean = htemp->GetMean();

TH1F* h1 =new TH1F("h1","h1",100,-0.02,0.02) ;
evts->Draw("RP_TRK_Z0>>h1",cut) 
h1->Fit("gaus") ;
float z0_mean = h1->GetMean();

evts->Draw("RP_TRK_phi",cut);
float phi0_mean = htemp->GetMean();

evts->Draw("RP_TRK_omega",cut);
float omega_mean = htemp->GetMean();

evts->Draw("RP_TRK_tanlambda",cut);
float tanlambda_mean = htemp->GetMean();

// The strings below correspond to:  variable - < variable >, where
// < variable > is the average that has been calculated above.

char bu[100];
sprintf(bu,"( RP_TRK_D0 - %g )",d0_mean) ;
TString s_d0_mean = TString( bu);
sprintf(bu,"( RP_TRK_Z0 - %g )",z0_mean) ;
TString s_z0_mean = TString( bu);
sprintf(bu,"( RP_TRK_omega - %g )", omega_mean);
TString s_omega_mean = TString( bu);
sprintf(bu,"( RP_TRK_phi - %g )", phi0_mean);
TString s_phi0_mean = TString( bu);
sprintf(bu,"( RP_TRK_tanlambda - %g )", tanlambda_mean);
TString s_tanlambda_mean = TString( bu);


// Now look at the covariances between the parameters. For example, for
// (d0, phi0) : look at the distribution of ( d0 - <d0> ) x ( phi0 - <phi0> ).
// The mean value of this distribution should be equal to the value of
// the corresponding off-diagonal term in the covariance matrix, RP_TRK_d0_phi0_cov.
// 
// And the covariances are normalised to sigma(Var 1) x sigma(Var 2), since such
// correlation terms (dimensionless) are easier to interpret than the covariamnce terms
// themselves.

// correlation between d0 and phi0 :

gStyle->SetOptStat(200);

TCanvas* c1 =new TCanvas("c1","c1");

TString var = " ( " + s_d0_mean + " * " + s_phi0_mean + " ) / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_phi_cov) )";
c1->Divide(1,2);
c1->cd(1);
evts->Draw( var ,cut) ;  // the mean value should be equal to RP_TRK_d0_phi0_cov
htemp->SetTitle("; ( d_{0} - < d_{0} > ) x ( #phi_{0} -< #phi_{0} > ) / ( #sigma_{d0} x #sigma_{#phi0} ); a.u");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_d0_phi0_cov / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_phi_cov))", cut);
htemp->SetTitle(";Cov( d_{0}, #phi_{0} );a.u.");
c1->SaveAs("validation_Cov_d0_phi0.pdf");

// correlation between d0 and omega

c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_d0_mean + " * " + s_omega_mean + " ) / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_omega_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( d_{0} - < d_{0} > ) x ( #omega -< #omega > ) / ( #sigma_{d0} x #sigma_{#omega} );a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_d0_omega_cov / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_omega_cov))",cut);
c1->SaveAs("validation_Cov_d0_omega.pdf");

// correlation between d0 and z0
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_d0_mean + " * " + s_z0_mean + " ) / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_Z0_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( d_{0} - < d_{0} > ) x ( z_{0} - < z_{0}> ) / ( #sigma_{d0} x #sigma_{z0} ); a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_d0_z0_cov / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_Z0_cov))",cut);
c1->SaveAs("validation_Cov_d0_z0.pdf");

// correlation between d0 and tanlambnda
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_d0_mean + " * " + s_tanlambda_mean + " ) / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_tanlambda_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( d_{0} - < d_{0} > ) x ( t#lambda - < t#lambda > ) / ( #sigma_{d0} x #sigma_{t#lambda} ) ; a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_d0_tanlambda_cov / ( TMath::Sqrt(RP_TRK_D0_cov) * TMath::Sqrt(RP_TRK_tanlambda_cov) )",cut);
c1->SaveAs("validation_Cov_d0_tanlambda.pdf");

// correlation between phi0 and omega
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_phi0_mean + " * " + s_omega_mean + " ) / ( TMath::Sqrt(RP_TRK_phi_cov) * TMath::Sqrt(RP_TRK_omega_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( #phi_{0} -< #phi_{0} > ) x ( #omega -< #omega > ) / ( #sigma_{#phi0} x #sigma_{#omega} );a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_phi0_omega_cov  / ( TMath::Sqrt(RP_TRK_phi_cov) * TMath::Sqrt(RP_TRK_omega_cov) )", cut);
c1->SaveAs("validation_Cov_phi0_omega.pdf");

// correlation between phi0 and  z0
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_phi0_mean + " * " + s_z0_mean + " ) / ( TMath::Sqrt(RP_TRK_phi_cov) * TMath::Sqrt(RP_TRK_Z0_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( #phi_{0} -< #phi_{0} > ) x ( z_{0} - < z_{0}> ) / ( #sigma_{#phi0} x #sigma_{z0} ); a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_phi0_z0_cov / ( TMath::Sqrt(RP_TRK_phi_cov) * TMath::Sqrt(RP_TRK_Z0_cov) )", cut);
c1->SaveAs("validation_Cov_phi0_z0.pdf");

// correlation between phi0 and tanlambd
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_phi0_mean + " * " + s_tanlambda_mean + " ) / ( TMath::Sqrt(RP_TRK_phi_cov) * TMath::Sqrt(RP_TRK_tanlambda_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( #phi_{0} -< #phi_{0} > ) x ( t#lambda - < t#lambda > ) / ( #sigma_{#phi0} x #sigma_{t#lambda} ) ; a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_phi0_tanlambda_cov / ( TMath::Sqrt(RP_TRK_phi_cov) * TMath::Sqrt(RP_TRK_tanlambda_cov) )", cut);
c1->SaveAs("validation_Cov_phi0_tanlambda.pdf");

// correlation between omega and z0
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_omega_mean + " * " + s_z0_mean + " ) / ( TMath::Sqrt(RP_TRK_omega_cov) * TMath::Sqrt(RP_TRK_Z0_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( #omega -< #omega > ) x ( z_{0} - < z_{0}> ) / ( #sigma_{#omega} x #sigma_{z0} ); a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_omega_z0_cov / ( TMath::Sqrt(RP_TRK_omega_cov) * TMath::Sqrt(RP_TRK_Z0_cov) )", cut);
c1->SaveAs("validation_Cov_omega_z0.pdf");

// correlation between omega and tsnlsmbds
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_omega_mean + " * " + s_tanlambda_mean + " ) / ( TMath::Sqrt(RP_TRK_omega_cov) *  TMath::Sqrt(RP_TRK_tanlambda_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( #omega -< #omega > ) x  ( t#lambda - < t#lambda > ) / ( #sigma_{#omega} x #sigma_{t#lambda} ) ; a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_omega_tanlambda_cov / ( TMath::Sqrt(RP_TRK_omega_cov) *  TMath::Sqrt(RP_TRK_tanlambda_cov) )", cut);
c1 -> SaveAs("validation_Cov_omega_tanlambda.pdf");

// correlation between z0 and tanlambda
c1->cd(1);
gStyle->SetOptStat(200);
var = " ( " + s_z0_mean + " * " + s_tanlambda_mean + " ) / ( TMath::Sqrt(RP_TRK_Z0_cov) *  TMath::Sqrt(RP_TRK_tanlambda_cov) )";
evts->Draw( var ,cut) ;
htemp->SetTitle("; ( z_{0} - < z_{0}> ) x  ( t#lambda - < t#lambda > ) / ( #sigma_{z0} x #sigma_{t#lambda} ) ; a.u.");
c1->cd(2);
gStyle->SetOptStat(100);
evts->Draw("RP_TRK_z0_tanlambda_cov / ( TMath::Sqrt(RP_TRK_Z0_cov) *  TMath::Sqrt(RP_TRK_tanlambda_cov) )", cut);
c1->SaveAs("validation_Cov_z0_tanlambda.pdf");


}





