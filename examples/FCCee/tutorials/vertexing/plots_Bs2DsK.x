{

// ------------------------------------------------------------------

// Ds vertex fit

TString cut = "n_DsTracks==3";

// normalised chi2 of the fit :  (Ndf = 2 x Ntracks - 3 )
events->Draw("DsVertex.chi2", cut);

// resolutions in x :
events->Draw("(DsVertex.position.x-DsMCDecayVertex.x)",cut) ;

// pulls of the fitted vertex position :
events->Draw("(DsVertex.position.x-DsMCDecayVertex.x)/TMath::Sqrt( DsVertex.covMatrix[0] )",cut);
events->Draw("(DsVertex.position.y-DsMCDecayVertex.y)/TMath::Sqrt( DsVertex.covMatrix[2] )",cut) ;
events->Draw("(DsVertex.position.z-DsMCDecayVertex.z)/TMath::Sqrt( DsVertex.covMatrix[5] )",cut) ;


// ------------------------------------------------------------------


// Bs vertex fit 

cut = "n_DsTracks==3 && n_BsTracks ==2" ;


// normalised chi2 :
events->Draw("BsVertex.chi2", cut);

// resolutions:
events->Draw("(BsVertex.position.x-BsMCDecayVertex.x)",cut) ;

// pulls in x :
events->Draw("(BsVertex.position.x-BsMCDecayVertex.x)/TMath::Sqrt( BsVertex.covMatrix[0] )",cut);

// pulls of the flight distance :

TString fld_mm = "TMath::Sqrt( pow( BsVertex.position.x, 2) + pow( BsVertex.position.y,2) + pow( BsVertex.position.z,2))";
TString fld_gen_mm = "TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) + pow( BsMCDecayVertex.z[0],2)   )";
TString fld_res_mm =  fld_mm + " - " + fld_gen_mm;
TString term1 = " BsVertex.position.x * ( BsVertex.covMatrix[0] * BsVertex.position.x + BsVertex.covMatrix[1] * BsVertex.position.y + BsVertex.covMatrix[3] * BsVertex.position.z ) " ;
TString term2 = " BsVertex.position.y * ( BsVertex.covMatrix[1] * BsVertex.position.x + BsVertex.covMatrix[2] * BsVertex.position.y + BsVertex.covMatrix[4] * BsVertex.position.z ) " ;
TString term3 = " BsVertex.position.z * ( BsVertex.covMatrix[3] * BsVertex.position.x + BsVertex.covMatrix[4] * BsVertex.position.y + BsVertex.covMatrix[5] * BsVertex.position.z ) ";
TString tsum = term1 + " + " + term2 + " + " + term3;
TString fld_unc = " ( TMath::Sqrt( " + tsum + ") / " + fld_mm +" ) ";
TString fld_pull = "( " + fld_res_mm + " ) / " + fld_unc;
events->Draw(fld_pull , cut);




}

