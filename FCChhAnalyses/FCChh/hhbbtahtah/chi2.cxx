#include <TLorentzVector.h>
#include <iostream>
#define GEV 1000.
#define WHM 80.399*GEV
#define TOPMASS 172.5*GEV

//FRA
#define SWMQ 100.*GEV*GEV
#define STMQ 400.*GEV*GEV

//KLF
//#define SWMQ 2.1*2.1*GEV*GEV
//#define STMQ 1.5*1.5*GEV*GEV

std::vector<double> lepnu(TLorentzVector& l, TLorentzVector& nu) {

  std::vector<double> pznu;
  TLorentzVector w;
  const double WMass = 80.399*GEV;

  double MissingPt = sqrt( nu.Px()*nu.Px()+nu.Py()*nu.Py() );
  
  double alpha  = 0.5*(WMass*WMass-l.M()*l.M());
  double beta   = alpha+nu.Px()*l.Px()+nu.Py()*l.Py();
  double gamma  = -(beta*beta-(l.E()*l.E()*MissingPt*MissingPt))/(l.E()*l.E()-l.Pz()*l.Pz());
  double lambda = 2.*beta*l.Pz()/(l.E()*l.E()-l.Pz()*l.Pz());
  
  double delta  = lambda*lambda-4.*gamma;
  
  if(delta < 0) { 
    nu.SetPtEtaPhiM(nu.Pt(),l.Eta(),nu.Phi(), 0.); pznu.push_back(nu.Pz()); return pznu;
  }
    
  double Pz1 = (lambda-sqrt(delta))/2.;
  double Pz2 = (lambda+sqrt(delta))/2.;

  //first neutrino is the one with lowest pz
  if (TMath::Abs(Pz1)<TMath::Abs(Pz2)) {
    pznu.push_back(Pz1);   pznu.push_back(Pz2);
  }
  else {
    pznu.push_back(Pz2);   pznu.push_back(Pz1);
  }
  return pznu;
}

double calcChi2(TLorentzVector& wh, TLorentzVector& th, TLorentzVector& tlep,float wblep,float wbhad) {
  
  double wm   = wh.M();
  double lm   = tlep.M();
  double tm   = th.M();

  double sigW = SWMQ;
  double sigTop = STMQ;
  //std::cout << "wm  "<< wm/GEV  << "  tm  " << tm/GEV <<  "  lm  " <<lm/GEV << "  wterm  " << (wm-WHM)*(wm-WHM)/sigW  << "  top h " << (tm-TOPMASS)*(tm-TOPMASS)/sigTop << "  top lep   " << (lm-TOPMASS)*(lm-TOPMASS)/sigTop  << "  chi2 " << (wm-WHM)*(wm-WHM)/sigW + (tm-TOPMASS)*(tm-TOPMASS)/sigTop + (lm-TOPMASS)*(lm-TOPMASS)/sigTop << std::endl;
  //std::cout << "(wm-WHM)*(wm-WHM)  " << (wm-WHM)*(wm-WHM) << " SWMQ  " << sigW << "  ratio " << (wm-WHM)*(wm-WHM)/sigW << std::endl;
  //return ( (wm-WHM)*(wm-WHM)/sigW + (tm-TOPMASS)*(tm-TOPMASS)/sigTop + (lm-TOPMASS)*(lm-TOPMASS)/sigTop );
  return ( (wm-WHM)*(wm-WHM)/sigW + (tm-TOPMASS)*(tm-TOPMASS)/sigTop + (lm-TOPMASS)*(lm-TOPMASS)/sigTop )*wblep*wbhad;
  //return ( (wm-WHM)*(wm-WHM)/sigW + (tm-TOPMASS)*(tm-TOPMASS)/sigTop + (lm-TOPMASS)*(lm-TOPMASS)/sigTop );
}


double return2() {return 2;}

double DoChi2SemiLep(vector<TLorentzVector> jets,
		     //TLorentzVector& j2,
		     //LorentzVector& j3,
		     //TLorentzVector& j4,
		     //TLorentzVector& j5,
		     TLorentzVector& l,
		     TLorentzVector& nu,
		     TLorentzVector& hadronic_top,
		     TLorentzVector& leptonic_top,
		     TLorentzVector& hadronic_w,
                     vector<float> proba){

  //  vector<TLorentzVector> jets;
  //  jets.push_back(j1);
  //  jets.push_back(j2);
  //  jets.push_back(j3);
  //  jets.push_back(j4);
  //  jets.push_back(j5);

  vector <TLorentzVector>::iterator it = jets.begin();
  std::vector<double> pznu = lepnu(l,nu);
  
  double minchi2=1.e300; //huge number to be sure that there is always 1 solution.
  TLorentzVector mintlep, minwh, minth;
  
  int nus=pznu.size();
  int limit = std::min(nus,1);
  for (int nn=0; nn<limit; nn++) {
    nu.SetPxPyPzE(nu.Px(),nu.Py(),pznu.at(nn),
		  sqrt(nu.Perp2() + pznu.at(nn)*pznu.at(nn)));
    TLorentzVector wl = l+nu;
    
    int jhigh_limit = jets.size();
    
    for (int jj=0; jj<jhigh_limit;jj++) {
      it = jets.begin()+jj;
      TLorentzVector *bjl = &(*it);
      float wblep = proba[jj];
      TLorentzVector tlep = wl + *bjl;
      
      for (int jk=0; jk<jhigh_limit;jk++) {
	if (jk==jj) continue;
	it = jets.begin()+jk;
	TLorentzVector *jh1 = &(*it);	
        float wbhad = proba[jk];

	TLorentzVector wh;
	  
	for (int jl=0; jl<jhigh_limit;jl++) {
	  if ((jl==jj)||(jl==jk)) continue;
	  it = jets.begin()+jl;
	  TLorentzVector *jh2 = &(*it);
	      
	  for (int jm=jl+1; jm<jhigh_limit;jm++) {
	    if ((jm==jj)||(jm==jk)) continue;
	    it = jets.begin()+jm;
	    TLorentzVector *jh3 = &(*it);

// 	    if(n_jets-get_nbtaggedjets()>1)
// 	      if ( get_jet_isTagged(jl) || get_jet_isTagged(jm) ) continue;
	    
	    wh = *jh3+*jh2;

	    TLorentzVector  th = wh+*jh1;
	          
	    double tmp_chi2 = calcChi2(wh,th,tlep,wblep,wbhad);
	    if (tmp_chi2<minchi2) {
	      minchi2=tmp_chi2;
	      minth = th;    
	      mintlep = tlep;     
	      minwh = wh;
	      
	    }
	  }
	}
 	
      } //loop b had jet2
    }//loop b lep jet1
  }//loop over nu solutions
     
  hadronic_top = minth;
  leptonic_top = mintlep;
  hadronic_w = minwh;
  
  return minchi2;

}
