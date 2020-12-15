
TFile* f = new TFile("Z_mumu_hack.root");
TTree* events = (TTree*)f->Get("events");

// D0 :
events->Draw("RP_TRK_D0", "TMath::Abs(RP_TRK_D0) < 0.1") ;  // the RMS should be of a few microns. 
		// the RMS of this histogram is 3e-3
		// Hence the unit of D0 is mm

// Sigma of D0 :
events->Draw("TMath::Sqrt(RP_TRK_D0_var)","TMath::Sqrt(RP_TRK_D0_var) < 1e-5") ;	// the mean should be a few microns
		// the mean of this histogram is 2e-6
		// Hence in the covariance matrix, the units is meters-squared.

// Pull of D0 : should be Gaussian wigh sigma = 1 if units are consistent :
events->Draw("RP_TRK_D0 / TMath::Sqrt(RP_TRK_D0_var)") ;  // sigma = 1000
	// consistent with the above:  the nunmerator is in mm, and the denom is in m


// Z0 :
TH1F* h1 =new TH1F("h1","h1",100,-0.02,0.02) ;
events->Draw("RP_TRK_Z0>>h1") ;		// std dev = 3.6 mum
h1->Fit("gaus") ;   // sigma of 2.4e-3, unit is also in mm

events->Draw("TMath::Sqrt(RP_TRK_Z0_var)") ;  // mean = 4e-6 : the variance is in meter-squared
events->Draw("RP_TRK_Z0 / TMath::Sqrt(RP_TRK_Z0_var)") ;  // std dev = 1000

// matching between the reco'ed particles and the MC-matched :

	// Phi :  OK
events->Draw("RP_TRK_phi:RP_MC_tlv.Phi()") ;
events->Draw("(RP_TRK_phi-RP_MC_tlv.Phi())/TMath::Sqrt(RP_TRK_phi_var)") ;   // OK, sigma = 1

	// Tan Lambda : OK
events->Draw("RP_TRK_tanlambda:1./TMath::Tan(RP_MC_tlv.Theta())") ;  /// tan(lambda) = cotan(theta)
events->Draw("( RP_TRK_tanlambda - 1./TMath::Tan(RP_MC_tlv.Theta()) ) / TMath::Sqrt( RP_TRK_tanlambda_var) ");  // OK

	// compare pT of the MC particle with the curvature of the track :
	// pT (GeV) = 0.3 * B ( Tesla ) / rho (m)
events->Draw("1e-3 * 0.3*2*TMath::Abs(1./RP_TRK_omega):RP_MC_tlv.Pt()") ; // i.e. omega is in in mm-1
		// this plot shows a linear correlation but with slope = 2 :
		// omega is not the curvature, but half of it (cf Franco's C = half curvature)
events->Draw("1e-3 * 0.3*2*TMath::Abs(1./ ( 2.*RP_TRK_omega)):RP_MC_tlv.Pt()") ;  // Now it's fine


	// Pull of the curvature :
events->Draw("TMath::Abs(RP_TRK_omega)*2 :1e-3*0.3*2*(1./RP_MC_tlv.Pt()) "," 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) < 0.0009") ;

events->Draw(" ( TMath::Abs(RP_TRK_omega)*2 - 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) ) / TMath::Sqrt( RP_TRK_omega_var)");   
	// sigma = 2e-3 ...
   	// curvature = 2 * omega, hence the sigma of the curvature is 4* RP_TRK_omega_var in principle
events->Draw(" ( TMath::Abs(RP_TRK_omega)*2 - 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) ) / ( 2.*TMath::Sqrt( RP_TRK_omega_var) ) ");
	// sigma = 1e-3
	// i.e. while omega is in mm-1, the variance RP_TRK_omega_var is in meters-2


