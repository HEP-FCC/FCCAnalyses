{

gROOT->Reset();

TFile* f = new TFile("p8_Zmumu.root");
TTree* events = (TTree*)f->Get("events");

// D0 :
events->Draw("RP_TRK_D0", "TMath::Abs(RP_TRK_D0) < 0.1") ;  // the RMS should be of a few microns. 
		// the RMS of this histogram is 3e-3
		// Hence the unit of D0 is mm

// Sigma of D0 :
events->Draw("TMath::Sqrt(RP_TRK_D0_cov)","TMath::Sqrt(RP_TRK_D0_cov) < 1e-2") ;	// the mean should be a few microns
		// the mean of this histogram is 2e-3
		// Hence in the covariance matrix, the units is mm-squared,
		/// consistent indeed with the unit of the track parameter.

// Pull of D0 : should be Gaussian wigh sigma = 1 if units are consistent :
events->Draw("RP_TRK_D0 / TMath::Sqrt(RP_TRK_D0_cov)") ;  // sigma = 1 as it should


// Z0 :
TH1F* h1 =new TH1F("h1","h1",100,-0.02,0.02) ;
events->Draw("RP_TRK_Z0>>h1") ;		// std dev = 3.6 mum
h1->Fit("gaus") ;   // sigma of 2.4e-3, so the unit of  Z0 is also mm

events->Draw("TMath::Sqrt(RP_TRK_Z0_cov)") ;  // mean = 4e-3 : the variance is in mm-squared
events->Draw("RP_TRK_Z0 / TMath::Sqrt(RP_TRK_Z0_cov)") ;  // std dev = 1

// matching between the reco'ed particles and the MC-matched :

	// Phi :  OK
events->Draw("RP_TRK_phi:RP_MC_tlv.Phi()") ;
events->Draw("(RP_TRK_phi-RP_MC_tlv.Phi())/TMath::Sqrt(RP_TRK_phi_cov)") ;   // OK, sigma = 1

	// Tan Lambda : OK  ( tan(lambda) = cotan(theta) )
events->Draw("RP_TRK_tanlambda:1./TMath::Tan(RP_MC_tlv.Theta())") ;  /// tan(lambda) = cotan(theta)
events->Draw("( RP_TRK_tanlambda - 1./TMath::Tan(RP_MC_tlv.Theta()) ) / TMath::Sqrt( RP_TRK_tanlambda_cov) ");  // OK

	// compare pT of the MC particle with the curvature of the track :
	// pT (GeV) = 0.3 * B ( Tesla ) / rho (m)
events->Draw("1e-3 * 0.3*2*TMath::Abs(1./RP_TRK_omega):RP_MC_tlv.Pt()") ; // i.e. omega is in in mm-1
		// this plot shows a linear correlation with slope = 1:
		// omega is indeed  the curvature (and not half of it as used internally
		// in the Delphes TrackCovariance module)


	// Pull of the curvature : OK
events->Draw("TMath::Abs(RP_TRK_omega) :1e-3*0.3*2*(1./RP_MC_tlv.Pt()) "," 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) < 0.0009") ;

events->Draw(" ( TMath::Abs(RP_TRK_omega) - 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) ) / TMath::Sqrt( RP_TRK_omega_cov)");   
	// sigma = 1, OK


}
