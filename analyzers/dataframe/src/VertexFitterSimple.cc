#include "VertexFitterSimple.h"
#include <iostream>

#include "TFile.h"
#include "TString.h"

#include  "MCParticle.h"

using namespace VertexFitterSimple;




TVector3 VertexFitterSimple::ParToP(TVectorD Par){
  double fB = 2;  // 2 Tesla
  
  Double_t C    = Par(2);
  Double_t phi0 = Par(1);
  Double_t ct   = Par(4);
  //
  TVector3 Pval;
  Double_t pt = fB*0.2998 / TMath::Abs(2 * C);
  Pval(0) = pt*TMath::Cos(phi0);
  Pval(1) = pt*TMath::Sin(phi0);
  Pval(2) = pt*ct;
  //
  return Pval;
}


TVectorD VertexFitterSimple::XPtoPar(TVector3 x, TVector3 p, Double_t Q){

  double fB = 2;  // 2 Tesla
  
  //
  TVectorD Par(5);
  // Transverse parameters
  Double_t a = -Q*fB*0.2998;                      // Units are Tesla, GeV and meters
  Double_t pt = p.Pt();
  Double_t C = a / (2 * pt);                      // Half curvature
  //cout << "ObsTrk::XPtoPar: fB = " << fB << ", a = " << a << ", pt = " << pt << ", C = " << C << endl;
  Double_t r2 = x.Perp2();
  Double_t cross = x(0)*p(1) - x(1)*p(0);
  Double_t T = TMath::Sqrt(pt*pt - 2 * a*cross + a*a*r2);
  Double_t phi0 = TMath::ATan2((p(1) - a*x(0)) / T, (p(0) + a*x(1)) / T); // Phi0
  Double_t D;                                                     // Impact parameter D
  if (pt < 10.0) D = (T - pt) / a;
  else D = (-2 * cross + a*r2) / (T + pt);
  //
  Par(0) = D;             // Store D
  Par(1) = phi0;  // Store phi0
  Par(2) = C;             // Store C
  //Longitudinal parameters
  Double_t B = C*TMath::Sqrt(TMath::Max(r2 - D*D,0.0) / (1 + 2 * C*D));
  Double_t st = TMath::ASin(B) / C;
  Double_t ct = p(2) / pt;
  Double_t z0 = x(2) - ct*st;
  //
  Par(3) = z0;            // Store z0
  Par(4) = ct;            // Store cot(theta)
  //
  return Par;
}


//
//TH1F* hTry;
//
Double_t VertexFitterSimple::FastRv(TVectorD p1, TVectorD p2){
  //
  // Find radius of intersection between two tracks in the transverse plane
  //
  // p = (D,phi, C)
  //
  // Solving matrix
  TMatrixDSym H(2);
  H(0, 0) = -TMath::Cos(p2(1));
  H(0, 1) =  TMath::Cos(p1(1));
  H(1, 0) = -TMath::Sin(p2(1));
  H(1, 1) =  TMath::Sin(p1(1));
  Double_t Det = TMath::Sin(p2(1) - p1(1));
  H *= 1.0 / Det;
  //
  // Convergence parameters
  Int_t Ntry = 0;
  Int_t NtryMax = 100;
  Double_t eps = 1000.;
  Double_t epsMin = 1.0e-6;
  //
  // Vertex finding loop
  //
  TVectorD cterm(2);
  cterm(0) = p1(0);
  cterm(1) = p2(0);
  TVectorD xv(2);
  Double_t R = 1000.;
  while (eps > epsMin)
    {
      xv = H * cterm;
      Ntry++;
      if (Ntry > NtryMax)
	{
	  std::cout << "FastRv: maximum number of iteration reached" << std::endl;
	  break;
	}
      Double_t Rnew = TMath::Sqrt(xv(0) * xv(0) + xv(1) * xv(1));
      eps = Rnew - R;
      R = Rnew;
      cterm(0) = p1(2) * R * R;
      cterm(1) = p2(2) * R * R;
    }
  //
  return R;
}
TMatrixDSym VertexFitterSimple::RegInv3(TMatrixDSym &Smat0){
  //
  // Regularized inversion of symmetric 3x3 matrix with positive diagonal elements
  //
  TMatrixDSym Smat = Smat0;
  Int_t N = Smat.GetNrows();
  if (N != 3){
    std::cout << "RegInv3 called with  matrix size != 3. Abort & return standard inversion." << std::endl;
    return Smat.Invert();
  }
  TMatrixDSym D(N); D.Zero();
  Bool_t dZero = kTRUE;	// No elements less or equal 0 on the diagonal
  for (Int_t i = 0; i < N; i++) if (Smat(i, i) <= 0.0)dZero = kFALSE;
  if (dZero){
    for (Int_t i = 0; i < N; i++) D(i, i) = 1.0 / TMath::Sqrt(Smat(i, i));
    TMatrixDSym RegMat = Smat.Similarity(D);
    TMatrixDSym Q(2);
    for (Int_t i = 0; i < 2; i++){
      for (Int_t j = 0; j < 2; j++)Q(i, j) = RegMat(i, j);
    }
    Double_t Det = 1 - Q(0, 1)*Q(1, 0);
    TMatrixDSym H(2);
    H = Q;
    H(0, 1) = -Q(0, 1);
    H(1, 0) = -Q(1, 0);
    TVectorD p(2);
    p(0) = RegMat(0, 2);
    p(1) = RegMat(1, 2);
    Double_t pHp = H.Similarity(p);
    Double_t h = pHp-Det;
    //
    TMatrixDSym pp(2); pp.Rank1Update(p);
    TMatrixDSym F = (h*H) - pp.Similarity(H);
    F *= 1.0 / Det;
    TVectorD b = H*p;
    TMatrixDSym InvReg(3);
    for (Int_t i = 0; i < 2; i++)
      {
	InvReg(i, 2) = b(i);
	InvReg(2, i) = b(i);
	for (Int_t j = 0; j < 2; j++) InvReg(i, j) = F(i, j);
      }
    InvReg(2, 2) = -Det;
    //
    InvReg *= 1.0 / h;
    //
    //
    return InvReg.Similarity(D);
  }
  else
    {
      //std::cout << "RegInv3: found negative elements in diagonal. Return standard inversion." << std::endl;
      return Smat.Invert();
    }
}
//
//
//
TMatrixD VertexFitterSimple::Fill_A(TVectorD par, Double_t phi){
  //
  // Derivative of track 3D position vector with respect to track parameters at constant phase 
  //
  // par = vector of track parameters
  // phi = phase
  //
  TMatrixD A(3, 5);
  //
  // Decode input arrays
  //
  Double_t D = par(0);
  Double_t p0 = par(1);
  Double_t C = par(2);
  Double_t z0 = par(3);
  Double_t ct = par(4);
  //
  // Fill derivative matrix dx/d alpha
  // D
  A(0, 0) = -TMath::Sin(p0);
  A(1, 0) = TMath::Cos(p0);
  A(2, 0) = 0.0;
  // phi0
  A(0, 1) = -D*TMath::Cos(p0) + (TMath::Cos(phi + p0) - TMath::Cos(p0)) / (2 * C);
  A(1, 1) = -D*TMath::Sin(p0) + (TMath::Sin(phi + p0) - TMath::Sin(p0)) / (2 * C);
  A(2, 1) = 0.0;
  // C
  A(0, 2) = -(TMath::Sin(phi + p0) - TMath::Sin(p0)) / (2 * C*C);
  A(1, 2) = (TMath::Cos(phi + p0) - TMath::Cos(p0)) / (2 * C*C);
  A(2, 2) = -ct*phi / (2 * C*C);
  // z0
  A(0, 3) = 0.0;
  A(1, 3) = 0.0;
  A(2, 3) = 1.0;
  // ct = lambda
  A(0, 4) = 0.0;
  A(1, 4) = 0.0;
  A(2, 4) = phi / (2 * C);
  //
  return A;
}

//
TVectorD VertexFitterSimple::Fill_a(TVectorD par, Double_t phi){
  //
  // Derivative of track 3D position vector with respect to phase at constant track parameters
  //
  // par = vector of track parameters
  // phi = phase
  //
  TVectorD a(3);
  //
  // Decode input arrays
  //
  Double_t D = par(0);
  Double_t p0 = par(1);
  Double_t C = par(2);
  Double_t z0 = par(3);
  Double_t ct = par(4);
  //
  a(0) = TMath::Cos(phi + p0) / (2 * C);
  a(1) = TMath::Sin(phi + p0) / (2 * C);
  a(2) = ct / (2 * C);
  //
  return a;
}
//

TVectorD VertexFitterSimple::Fill_x0(TVectorD par){
  //
  // Calculate track 3D position at R = |D| (minimum approach to z-axis)
  //
  TVectorD x0(3);
  //
  // Decode input arrays
  //
  Double_t D = par(0);
  Double_t p0 = par(1);
  Double_t C = par(2);
  Double_t z0 = par(3);
  Double_t ct = par(4);
  //
  x0(0) = -D *TMath::Sin(p0);
  x0(1) = D*TMath::Cos(p0);
  x0(2) = z0;
  //
  return x0;
}

//
TVectorD VertexFitterSimple::Fill_x(TVectorD par, Double_t phi){
  //
  // Calculate track 3D position for a given phase, phi
  //
  TVectorD x(3);
  //
  // Decode input arrays
  //
  Double_t D = par(0);
  Double_t p0 = par(1);
  Double_t C = par(2);
  Double_t z0 = par(3);
  Double_t ct = par(4);
  //
  TVectorD x0 = Fill_x0(par);
  x(0) = x0(0) + (TMath::Sin(phi + p0) - TMath::Sin(p0)) / (2 * C);
  x(1) = x0(1) - (TMath::Cos(phi + p0) - TMath::Cos(p0)) / (2 * C);
  x(2) = x0(2) + ct*phi / (2 * C);
  //
  return x;
}



VertexingUtils::FCCAnalysesVertex  VertexFitterSimple::VertexFitter( int Primary, 
								     ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
								     ROOT::VecOps::RVec<edm4hep::TrackState> thetracks,
								     bool BeamSpotConstraint,
								     double bsc_sigmax, double bsc_sigmay, double bsc_sigmaz, 
                                                                     double bsc_x, double bsc_y, double bsc_z )  {



  // input = a collection of recoparticles (in case one want to make associations to RecoParticles ?)
  // and thetracks = the collection of all TrackState in the event
  
  VertexingUtils::FCCAnalysesVertex thevertex;
  
  // retrieve the tracks associated to the recoparticles
  ROOT::VecOps::RVec<edm4hep::TrackState> tracks = ReconstructedParticle2Track::getRP2TRK( recoparticles, thetracks );
  
  // and run the vertex fitter
  
  //FCCAnalysesVertex thevertex = VertexFitter_Tk( Primary, tracks, thetracks) ;
  thevertex = VertexFitter_Tk( Primary, tracks,
			       BeamSpotConstraint, bsc_sigmax, bsc_sigmay, bsc_sigmaz, bsc_x, bsc_y, bsc_z );

  //fill the indices of the tracks
  ROOT::VecOps::RVec<int> reco_ind;
  int Ntr = tracks.size();
  for (auto & p: recoparticles) {
    //std::cout << " in VertexFitter:  a recoparticle with charge = " << p.charge << std::endl;
    if ( p.tracks_begin >=0 && p.tracks_begin<thetracks.size()) {
      reco_ind.push_back( p.tracks_begin );
    }
  }
  if ( reco_ind.size() != Ntr ) std::cout << " ... problem in Vertex, size of reco_ind != Ntr " << std::endl;
  
  thevertex.reco_ind = reco_ind;
  
  return thevertex;
}



VertexingUtils::FCCAnalysesVertex  VertexFitterSimple::VertexFitter_Tk( int Primary, 
									ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                                                                        bool BeamSpotConstraint, 
                                                                        double bsc_sigmax, double bsc_sigmay, double bsc_sigmaz,
									double bsc_x, double bsc_y, double bsc_z )  {
  
  // Units for the beam-spot : mum
  // See https://github.com/HEP-FCC/FCCeePhysicsPerformance/tree/master/General#generating-events-under-realistic-fcc-ee-environment-conditions

  // final results :
  VertexingUtils::FCCAnalysesVertex TheVertex;
  
  edm4hep::VertexData result;
  ROOT::VecOps::RVec<float> reco_chi2;
  ROOT::VecOps::RVec< TVectorD >  updated_track_parameters;
  ROOT::VecOps::RVec<int> reco_ind;
  ROOT::VecOps::RVec<float> final_track_phases;
  ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex;
  
  TheVertex.vertex = result;
  TheVertex.reco_chi2 = reco_chi2;
  TheVertex.updated_track_parameters = updated_track_parameters;
  TheVertex.reco_ind = reco_ind;
  TheVertex.final_track_phases = final_track_phases;
  TheVertex.updated_track_momentum_at_vertex = updated_track_momentum_at_vertex;
  
  
  int Ntr = tracks.size();
  TheVertex.ntracks = Ntr; 
  if ( Ntr <= 1) return TheVertex;   // can not reconstruct a vertex with only one track...
  

  bool debug = false;
  if (debug) std::cout << " enter in VertexFitter_Tk for the Bs decay vertex " << std::endl;
  
  // if a beam-spot constraint is required :
  TMatrixDSym BeamSpotCovI(3);
  TVectorD BeamSpotPos(3);
  if (BeamSpotConstraint) {   // fill in the inverse of the covariance matrix. Convert the units into meters
     BeamSpotCovI(0,0) = 1./pow( bsc_sigmax * 1e-6, 2) ;   // mum to m
     BeamSpotCovI(1,1) = 1./pow( bsc_sigmay * 1e-6, 2) ;   
     BeamSpotCovI(2,2) = 1./pow( bsc_sigmaz * 1e-6, 2) ; 
     BeamSpotPos(0) = bsc_x * 1e-6;
     BeamSpotPos(1) = bsc_y * 1e-6 ;
     BeamSpotPos(2) = bsc_z * 1e-6 ;
  }

  Double_t *final_chi2 = new Double_t[Ntr];
  Double_t *final_phases = new Double_t[Ntr];
  std::vector< TVectorD > final_delta_alpha ;
  TVectorD dummy(5);
  for (int i=0; i < Ntr; i++) {
    final_delta_alpha.push_back( dummy );
  }
  
  
  //
  // Vertex fit (units are meters)
  //
  // Initial variable definitions
  TVectorD x0(3); for (Int_t v = 0; v < 3; v++)x0(v) = 100.; // set to large value
  Double_t Chi2 = 0;
  //
  
  TVectorD x(3);
  TMatrixDSym covX(3);
  
  
  // Stored quantities
  Double_t *fi = new Double_t[Ntr];				// Phases 
  TVectorD **x0i = new TVectorD*[Ntr];			// Track expansion point
  TVectorD **ai = new TVectorD*[Ntr];				// dx/dphi
  Double_t *a2i = new Double_t[Ntr];				// a'Wa
  TMatrixDSym **Di = new TMatrixDSym*[Ntr];		// W-WBW
  TMatrixDSym **Wi = new TMatrixDSym*[Ntr];		// (ACA')^-1
  TMatrixDSym **Winvi = new TMatrixDSym*[Ntr];	// ACA'
  TMatrixD  **Ai = new TMatrixD*[Ntr];            // A
  TMatrixDSym **Covi = new TMatrixDSym*[Ntr];     // Cov matrix of the track parameters
  
  //
  // vertex radius approximation
  // Maximum impact parameter
  Double_t Rd = 0;
  for (Int_t i = 0; i < Ntr; i++)
    {
      //ObsTrk* t = tracks[i];
      //TVectorD par = t->GetObsPar();
      edm4hep::TrackState t = tracks[i] ;
      TVectorD par = VertexingUtils::get_trackParam( t ) ;
      Double_t Dabs = TMath::Abs(par(0));
      if (Dabs > Rd)Rd = Dabs;
    }
  //
  // Find track pair with largest phi difference
  Int_t isel; Int_t jsel; // selected track indices
  Double_t dphiMax = -9999.;	// Max phi difference 
  for (Int_t i = 0; i < Ntr-1; i++)
    {
      //ObsTrk* ti = tracks[i];
      //TVectorD pari = ti->GetObsPar();
      edm4hep::TrackState ti = tracks[i] ;
      TVectorD pari = VertexingUtils::get_trackParam( ti );
      Double_t phi1 = pari(1);
      
      for (Int_t j = i+1; j < Ntr; j++)
	{
	  //ObsTrk* tj = tracks[j];
	  //TVectorD parj = tj->GetObsPar();
	  edm4hep::TrackState tj = tracks[j];
	  TVectorD parj = VertexingUtils::get_trackParam( tj );
	  Double_t phi2 = parj(1);
	  Double_t dphi = TMath::Abs(phi2 - phi1);
	  if (dphi > TMath::Pi())dphi = TMath::TwoPi() - dphi;
	  if (dphi > dphiMax)
	    {
	      isel = i; jsel = j;
	      dphiMax = dphi;
	    }
	}
    }
  //
  // 
  //ObsTrk* t1 = tracks[isel];
  //TVectorD p1 = t1->GetObsPar();
  edm4hep::TrackState t1 = tracks[isel];
  TVectorD p1 = VertexingUtils::get_trackParam( t1 );
  //ObsTrk* t2 = tracks[jsel];
  //TVectorD p2 = t2->GetObsPar();
  edm4hep::TrackState t2 = tracks[jsel];
  TVectorD p2 = VertexingUtils::get_trackParam( t2 );
  Double_t R = FastRv(p1, p2);
  if (R > 1.0) R = Rd;
  R = 0.5 * (R + Rd);
  //
  // Iteration properties
  //
  Int_t Ntry = 0;
  Int_t TryMax = 100;
  if (BeamSpotConstraint) TryMax = TryMax * 5;
  Double_t eps = 1.0e-9; // vertex stability
  Double_t epsi = 1000.;
  //
  while (epsi > eps && Ntry < TryMax)		// Iterate until found vertex is stable
    {
      x.Zero();
      TVectorD cterm(3); TMatrixDSym H(3); TMatrixDSym DW1D(3);
      covX.Zero();	// Reset vertex covariance
      cterm.Zero();	// Reset constant term
      H.Zero();		// Reset H matrix
      DW1D.Zero();
      // 
      for (Int_t i = 0; i < Ntr; i++)
	{
	  // Get track helix parameters and their covariance matrix 
	  //ObsTrk *t = tracks[i];
	  //TVectorD par = t->GetObsPar();
	  //TMatrixDSym Cov = t->GetCov(); 
	  edm4hep::TrackState t = tracks[i] ;
	  TVectorD par = VertexingUtils::get_trackParam( t ) ;
	  TMatrixDSym Cov = VertexingUtils::get_trackCov( t );
	  Covi[i] = new TMatrixDSym(Cov);         // Store matrix
	  Double_t fs;
	  if (Ntry <= 0)	// Initialize all phases on first pass
	    {
	      Double_t D = par(0);
	      Double_t C = par(2);
	      Double_t arg = TMath::Max(1.0e-6, (R*R - D*D) / (1 + 2 * C*D));
	      fs = 2 * TMath::ASin(C*TMath::Sqrt(arg));
	      fi[i] = fs;
	    }
	  //
	  // Starting values
	  //
	  fs = fi[i];								// Get phase
	  TVectorD xs = Fill_x(par, fs);
	  x0i[i] = new TVectorD(xs);				// Start helix position
	  // W matrix = (A*C*A')^-1; W^-1 = A*C*A'
	  TMatrixD A = Fill_A(par, fs);			// A = dx/da = derivatives wrt track parameters
	  Ai[i]  = new TMatrixD(A);       // Store matrix
	  TMatrixDSym Winv = Cov.Similarity(A);	// W^-1 = A*C*A'
	  Winvi[i] = new TMatrixDSym(Winv);		// Store W^-1 matrix
	  TMatrixDSym W = RegInv3(Winv);			// W = (A*C*A')^-1
	  Wi[i] = new TMatrixDSym(W);				// Store W matrix
	  TVectorD a = Fill_a(par, fs);			// a = dx/ds = derivatives wrt phase
	  ai[i] = new TVectorD(a);				// Store a
	  Double_t a2 = W.Similarity(a);
	  a2i[i] = a2;							// Store a2
	  // Build D matrix
	  TMatrixDSym B(3); 
	  B.Rank1Update(a, 1.0);
	  B *= -1. / a2;
	  B.Similarity(W);
	  TMatrixDSym Ds = W+B;					// D matrix
	  Di[i] = new TMatrixDSym(Ds);			// Store D matrix
	  TMatrixDSym DsW1Ds = Winv.Similarity(Ds);	// Service matrix to calculate covX
	  DW1D += DsW1Ds;								
	  // Update hessian
	  H += Ds;
	  // update constant term
	  cterm += Ds * xs;
	}				// End loop on tracks
      //

      TMatrixDSym H0 = H;

      if (BeamSpotConstraint) {
	H += BeamSpotCovI ;
        cterm += BeamSpotCovI * BeamSpotPos ;
        DW1D  += BeamSpotCovI ;
      }

      // update vertex position
      TMatrixDSym H1 = RegInv3(H);
      x = H1*cterm;
      
      // Update vertex covariance
      covX = DW1D.Similarity(H1);

      // Update phases and chi^2
      Chi2 = 0.0;
      for (Int_t i = 0; i < Ntr; i++)
	{
	  TVectorD lambda = (*Di[i])*(*x0i[i] - x);
	  TMatrixDSym Wm1 = *Winvi[i];
	  Double_t addChi2 = Wm1.Similarity(lambda);;
	  //Chi2 += Wm1.Similarity(lambda);
	  Chi2 += addChi2;
	  final_chi2[i] = addChi2;
	  TVectorD a = *ai[i];
	  TVectorD b = (*Wi[i])*(x - *x0i[i]);
	  for (Int_t j = 0; j < 3; j++)fi[i] += a(j)*b(j) / a2i[i];
	  final_phases[i] = fi[i];
	  
	  TMatrixD ta(TMatrixD::kTransposed, *Ai[i]);
	  TMatrixDSym kk(5);
	  kk = *Covi[i];
	  final_delta_alpha[i] =  kk * ta * lambda;  // that's minus delta_alpha
	}
      //

      TVectorD dx = x - x0;
      x0 = x;
      // update vertex stability
      TMatrixDSym Hess = RegInv3(covX);

      epsi = Hess.Similarity(dx);
      Ntry++;
      //if ( Ntry >= TryMax) std::cout << " ... in VertexFitterSimple, Ntry >= TryMax " << std::endl;

      if (BeamSpotConstraint) {
        
        // add the following term to the chi2 :
        TVectorD dx_beamspot = x - BeamSpotPos ;
        Double_t chi2_bsc = BeamSpotCovI.Similarity( dx_beamspot );
        //Chi2 += chi2_bsc -3;
        Chi2 += chi2_bsc ;

      }



      //
      // Cleanup
      //
      for (Int_t i = 0; i < Ntr; i++)
	{
	  x0i[i]->Clear();
	  Winvi[i]->Clear();
	  Wi[i]->Clear();
	  ai[i]->Clear();
	  Di[i]->Clear();
	  Ai[i]->Clear();
	  Covi[i]->Clear();
	  
	  delete x0i[i];
	  delete Winvi[i];
	  delete Wi[i];
	  delete ai[i];
	  delete Di[i];
	  delete Ai[i];
	  delete Covi[i];
	}
    }
  //
  delete[] fi;		// Phases 
  delete[] x0i;		// Track expansion point
  delete[] ai;		// dx/dphi
  delete[] a2i;		// a'Wa
  delete[] Di;		// W-WBW
  delete[] Wi;		// (ACA')^-1
  delete[] Winvi;	// ACA'
  delete[] Ai ;           // A
  delete[] Covi;          // Cov
  
  //
  //return Chi2;
  
  // store the results in an edm4hep::VertexData object
  // go back from meters to millimeters for the units 
  float conv = 1e3;
  std::array<float,6> covMatrix;	// covMat in edm4hep is a LOWER-triangle matrix.
  covMatrix[0] = covX(0,0) * pow(conv,2);
  covMatrix[1] = covX(1,0) * pow(conv,2);
  covMatrix[2] = covX(1,1) * pow(conv,2);
  covMatrix[3] = covX(2,0) * pow(conv,2);
  covMatrix[4] = covX(2,1) * pow(conv,2);
  covMatrix[5] = covX(2,2) * pow(conv,2);
  
  float Ndof = 2.0 * Ntr - 3.0; ;
  
  result.primary = Primary;
  result.chi2 = Chi2 /Ndof ;      // I store the normalised chi2 here
  result.position = edm4hep::Vector3f( x(0)*conv, x(1)*conv, x(2)*conv ) ;  // store the  vertex in mm
  result.covMatrix = covMatrix;
  result.algorithmType = 1;
  
  // Need to fill the associations ...
  
  double scale0 = 1e-3;   //convert mm to m
  double scale1 = 1;
  double scale2 = 0.5*1e3;  // C = rho/2, convert from mm-1 to m-1
  double scale3 = 1e-3 ;  //convert mm to m
  double scale4 = 1.;
  
  scale2 = -scale2 ;   // sign of omega (sign convention)
  
  for (Int_t i = 0; i < Ntr; i++) {
    
    edm4hep::TrackState t = tracks[i] ;
    TVectorD par = VertexingUtils::get_trackParam( t ) ;
    
    // initial momentum :
    //TVector3 ptrack_ini = ParToP( par );
    //std::cout << "----- Track # " << i << " initial track momentum : " << std::endl;
    //ptrack_ini.Print();
    
    // uncomment below to get the post-fit track parameters :
    par -= final_delta_alpha[i] ;
    
    //std::cout << " Track i = " << i << " --- delta_alpha : " << std::endl;
    //final_delta_alpha[i].Print();
    
    // ( px, py, pz) of the track
    TVector3 ptrack = ParToP( par );
    //std::cout << "         updates track param :" << std::endl;
    //ptrack.Print();
    
    // and (px, py) at the vertex instead of the dca :
    double phi0 = par(1);
    double phi = final_phases[i]  ;
    double px_at_vertex = ptrack.Pt() * TMath::Cos( phi0 + phi );
    double py_at_vertex = ptrack.Pt() * TMath::Sin( phi0 + phi );
    TVector3 ptrack_at_vertex( px_at_vertex, py_at_vertex, ptrack.Pz() );
    //std::cout << "         momentum at the vertex : " << std::endl;
    //std::cout << " phi0 at dca = " << phi0 << " phi at vertex = " << phi0+phi << " C = " << par(2) << " phase " << phi << std::endl;
    //ptrack_at_vertex.Print();
    
    updated_track_momentum_at_vertex.push_back( ptrack_at_vertex );
    
    // back to EDM4HEP units...
    par[0] = par[0] / scale0 ;
    par[1] = par[1] / scale1 ;
    par[2] = par[2] / scale2 ;
    par[3] = par[3] / scale3 ;
    par[4] = par[4] / scale4 ;
    updated_track_parameters.push_back( par );
    
    reco_chi2.push_back( final_chi2[i] );
    final_track_phases.push_back( final_phases[i] );
    
  }
  
  TheVertex.vertex = result;
  TheVertex.reco_chi2 = reco_chi2;
  TheVertex.reco_ind = reco_ind;
  TheVertex.updated_track_parameters = updated_track_parameters ;
  TheVertex.updated_track_momentum_at_vertex = updated_track_momentum_at_vertex;
  TheVertex.final_track_phases = final_track_phases;
  
  //std::cout << " end of VertexFitter " << std::endl;
  /*
    for ( Int_t i = 0; i < Ntr; i++) {
    std::cout << " Track #" << i << " chi2 = " << reco_chi2[i] << std::endl;
    std::cout << "        Initial parameters: " << std::endl;
    VertexingUtils::get_trackParam( tracks[i] ).Print();
    std::cout << "        Updated parameters : " << std::endl;
    updated_track_parameters[i].Print();
    }
  */
  
  delete final_chi2;
  delete final_phases;
 
  return TheVertex;
}


////////////////////////////////////////////////////



ROOT::VecOps::RVec<edm4hep::TrackState>   VertexFitterSimple::get_PrimaryTracks( VertexingUtils::FCCAnalysesVertex  initialVertex,
                                                                        ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                                                                        bool BeamSpotConstraint,
                                                                        double bsc_sigmax, double bsc_sigmay, double bsc_sigmaz,
                                                                        double bsc_x, double bsc_y, double bsc_z,
                                                                        int ipass  )  {


// iterative procedure to determine the primary vertex - and the primary tracks
// Start from a vertex reconstructed from all tracks, remove the one with the highest chi2, fit again etc

// tracks = the collection of tracks that was used in the first step

//bool debug  = true ;
  bool debug = false;
float CHI2MAX = 25  ;

if (debug) {
        if (ipass == 0) std::cout << " \n --------------------------------------------------------\n" << std::endl;
        std::cout << " ... enter in VertexFitterSimple::get_PrimaryTracks   ipass = " << ipass <<  std::endl;
        if (ipass == 0) std::cout  << "    initial number of tracks =  " << tracks.size() <<  std::endl;
}

ROOT::VecOps::RVec<edm4hep::TrackState> seltracks = tracks;
ROOT::VecOps::RVec<float> reco_chi2 = initialVertex.reco_chi2;

if ( seltracks.size() <= 1 ) return seltracks;

int isPrimaryVertex = initialVertex.vertex.primary  ;

int maxElementIndex = std::max_element(reco_chi2.begin(),reco_chi2.end()) - reco_chi2.begin();
auto minmax = std::minmax_element(reco_chi2.begin(), reco_chi2.end());
float chi2max = *minmax.second ;

if ( chi2max < CHI2MAX ) {
        if (debug) {
            std::cout << " --- DONE, all tracks have chi2 < CHI2MAX " << std::endl;
            std::cout  << "     number of primary tracks selected = " << seltracks.size() << std::endl;

        }
        return seltracks ;
}

        if (debug) {
                std::cout << " remove a track that has chi2 = " << chi2max << std::endl;
        }

seltracks.erase( seltracks.begin() + maxElementIndex );
ipass ++;

 VertexingUtils::FCCAnalysesVertex vtx = VertexFitterSimple::VertexFitter_Tk(  isPrimaryVertex,
                                                                                seltracks,
                                                                         BeamSpotConstraint,
                                                                         bsc_sigmax, bsc_sigmay, bsc_sigmaz,
                                                                         bsc_x, bsc_y, bsc_z )  ;

 return VertexFitterSimple::get_PrimaryTracks( vtx, seltracks, BeamSpotConstraint, bsc_sigmax, bsc_sigmay, bsc_sigmaz,
                                                bsc_x,  bsc_y, bsc_z, ipass ) ;



}


ROOT::VecOps::RVec<edm4hep::TrackState>   VertexFitterSimple::get_NonPrimaryTracks( ROOT::VecOps::RVec<edm4hep::TrackState> allTracks,
                                                                                    ROOT::VecOps::RVec<edm4hep::TrackState> primaryTracks ) {

  ROOT::VecOps::RVec<edm4hep::TrackState> result;
  for (auto & track: allTracks) {
     bool isInPrimary = false;
     for ( auto &  primary:  primaryTracks) {
        if ( track.D0 == primary.D0 && track.Z0 == primary.Z0 &&  track.phi == primary.phi &&  track.omega == primary.omega && track.tanLambda == primary.tanLambda ) {
                isInPrimary = true;
                break;
        }
     }
     if ( !isInPrimary) result.push_back( track );
  }

 return result;
}


ROOT::VecOps::RVec<bool> VertexFitterSimple::IsPrimary_forTracks( ROOT::VecOps::RVec<edm4hep::TrackState> allTracks,
                                                                  ROOT::VecOps::RVec<edm4hep::TrackState> primaryTracks ) {

  ROOT::VecOps::RVec<bool> result;
  for (auto & track: allTracks) {
     bool isInPrimary = false;
     for ( auto &  primary:  primaryTracks) {
        if ( track.D0 == primary.D0 && track.Z0 == primary.Z0 &&  track.phi == primary.phi &&  track.omega == primary.omega && track.tanLambda == primary.tanLambda ) {
                isInPrimary = true;
                break;
        }
     }
     result.push_back( isInPrimary );
  }
 return result;
}



