//#include "ReconstructedParticle2Track.h"
#include "Vertex.h"

#include "TFile.h"
#include "TString.h"

int get_nTracks( ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
   int nt = tracks.size();
   return nt;
}


// 
// Selection of particles based on the d0 / z0 significances of the associated track
//

selTracks::selTracks( float arg_d0sig_min, float arg_d0sig_max, float arg_z0sig_min, float arg_z0sig_max) : m_d0sig_min(arg_d0sig_min), 
		m_d0sig_max  ( arg_d0sig_max ), m_z0sig_min( arg_z0sig_min ), m_z0sig_max (arg_z0sig_max) { };

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  selTracks::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
  										ROOT::VecOps::RVec<edm4hep::TrackState> tracks  ) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  result;
  result.reserve(recop.size());

    for (size_t i = 0; i < recop.size(); ++i) {
    auto & p = recop[i];
      if (p.tracks_begin<tracks.size()) {
	  auto & tr = tracks.at( p.tracks_begin );
          double d0sig = fabs( tr.D0 / sqrt( tr.covMatrix[0]) ) ;
          if ( fabs( d0sig ) > m_d0sig_max || fabs( d0sig ) < m_d0sig_min  ) continue;
          double z0sig = fabs( tr.Z0 / sqrt( tr.covMatrix[12]) );
          if ( fabs( z0sig ) > m_z0sig_max || fabs( z0sig ) < m_z0sig_min  ) continue;
          result.emplace_back(p);
      }
    }
  return result;
}


//
// Selection of primary particles based on the matching of RecoParticles
// to MC particles
//

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> SelPrimaryTracks ( ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, 
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(reco.size());

  for (unsigned int i=0; i<recind.size();i++) {
    double xvtx = mc.at(mcind.at(i)).vertex.x ;
    double yvtx = mc.at(mcind.at(i)).vertex.y ;
    double zvtx = mc.at(mcind.at(i)).vertex.z ;
    // primary particle ?
       	// to be refined by using the genuine MC primary vertex, in the general case  !
    double zero = 1e-12;
    //if ( xvtx == 0 && yvtx == 0 && zvtx == 0 ) {
    if ( fabs( xvtx) < zero && fabs( yvtx) < zero && fabs( zvtx) < zero ) {
	int reco_idx = recind.at(i); 
        result.push_back( reco.at( reco_idx )  );
    }

  }
  return result;
}



// ---------------------------------------------------------------
//
// Interface of  the vertexing code of Franco Bedeschi
// see https://www.pi.infn.it/~bedeschi/RD_FA/Software/
// VertexNew.c,  dated 18 Sep 2020
//
// ---------------------------------------------------------------



TMatrixDSym SymRegInv(TMatrixDSym &Smat)
{
	//
 	Int_t N = Smat.GetNrows();
	TMatrixDSym D(N); D.Zero();
	for (Int_t i = 0; i < N; i++) D(i, i) = 1.0/TMath::Sqrt(Smat(i, i));
	TMatrixDSym RegMat = Smat.Similarity(D); 
	TDecompChol rChl(RegMat);
	Bool_t OK = rChl.Decompose();
	if (!OK)
	{
		std::cout << "RegMat: input matrix not positive definite"; RegMat.Print();
	}
	RegMat = rChl.Invert(OK);
	TMatrixDSym RegOut = RegMat.Similarity(D);
	//
	return RegOut;
}

TVectorD get_trackParam( edm4hep::TrackState & atrack) {
    double d0 =atrack.D0 ;
    double phi0 = atrack.phi ;
    double omega = atrack.omega ;
    double z0 = atrack.Z0 ;
    double tanlambda = atrack.tanLambda ;
    TVectorD res(5);

    double scale0 = 1e-3;   //convert mm to m
    double scale1 = 1;
    double scale2 = 0.5*1e3;  // C = rho/2, convert from mm-1 to m-1
    double scale3 = 1e-3 ;  //convert mm to m
    double scale4 = 1.;

    // Same units and definitions as Franco :
    //scale0= 1.;
    //scale2 = 1.;
    //scale3 = 1.;

    res[0] = d0 * scale0;   
    res[1] = phi0 * scale1 ;
    res[2] = omega * scale2 ;   
    res[3] = z0 * scale3 ;  
    res[4] = tanlambda * scale4 ;
    return res;
}

TMatrixDSym get_trackCov( edm4hep::TrackState &  atrack) {
    std::array<float, 15> covMatrix = atrack.covMatrix;
    TMatrixDSym covM(5);

    double scale0 = 1e-3;
    double scale1 = 1;
    double scale2 = 0.5*1e3;
    double scale3 = 1e-3 ;
    double scale4 = 1.;

    // Same units and definitions as Franco :
    //scale0= 1.;
    //scale2 = 1.;
    //scale3 = 1.;

    covM[0][0] = covMatrix[0] *scale0 * scale0;
    covM[0][1] = covMatrix[1] *scale0 * scale1;
    covM[0][2] = covMatrix[2] *scale0 * scale2;
    covM[0][3] = covMatrix[3] *scale0 * scale3;
    covM[0][4] = covMatrix[4] *scale0 * scale4;

    covM[1][0] = covM[0][1];
    covM[2][0] = covM[0][2] ;
    covM[3][0] = covM[0][3] ;
    covM[4][0] = covM[0][4];

    covM[1][1] = covMatrix[5] *scale1 * scale1;
    covM[1][2] = covMatrix[6] *scale1 * scale2;
    covM[1][3] = covMatrix[7] *scale1 * scale3;
    covM[1][4] = covMatrix[8] *scale1 * scale4;;

    covM[2][1] = covM[1][2] ;
    covM[3][1] = covM[1][3];
    covM[4][1] = covM[1][4];

    covM[2][2] = covMatrix[9] *scale2 *scale2;
    covM[2][3] = covMatrix[10] * scale2 * scale3;
    covM[2][4] = covMatrix[11] * scale2 * scale4;

    covM[3][2] = covM[2][3];
    covM[4][2] = covM[2][4];

    covM[3][3] = covMatrix[12] * scale3 * scale3;
    covM[3][4] = covMatrix[13] * scale3 * scale4;

    covM[4][3] = covM[3][4];

    covM[4][4] = covMatrix[14] * scale4*scale4;;

    return covM;
}



//std::vector<float> Vertex0FB( ROOT::VecOps::RVec<edm4hep::TrackState> tracks )
TVector3 Vertex0FB( ROOT::VecOps::RVec<edm4hep::TrackState> tracks )
{
	//
 	// Preliminary estimate of the vertex position
   	// based on transformation of track into points
   	// and vertices into lines
   	// No steering of track parameters
   	// No error calculation
   	//


        int Ntr = tracks.size();
        TVector3 dummy(-1e12,-1e12,-1e12);
        if (Ntr <= 0) return dummy;

  	TVectorD xv(3);		// returned vertex position
	//
  	TMatrixDSym H(2); 
	TVectorD xvt(2);
	TVectorD cxy(2); 
	//
  	// Loop on tracks for transverse fit
   	//
  	TVectorD x0(2); x0.Zero();
	double Rv = 0.0;	    // Radius of first iteration
	int Ntry = 0;
	int TryMax = 10;
	double epsi = 1000.;		// Starting stability
	double eps = 0.0001;		// vertex stability required
	while (epsi > eps && Ntry < TryMax)
	{
		H.Zero(); 
                cxy.Zero();
		for (int i = 0; i < Ntr; i++)
		{
			// Get track helix parameters and their covariance matrix 
   			//ObsTrk *t = tracks[i];
                        edm4hep::TrackState t = tracks[i] ;
			// ROOT::TVectorD par = t->GetObsPar();
			TVectorD par = get_trackParam( t ) ;
			//ROOT::TMatrixDSym C = t->GetCov();
		        TMatrixDSym C = get_trackCov( t) ;
  			// Transverse fit
   			double D0i = par(0);
			double phi = par(1);
			double Ci = par(2);
			double Di = (D0i*(1. + Ci*D0i) + Rv*Rv*Ci) / (1. + 2 * Ci*D0i);
			double sDi2 = C(0, 0);
			//  Debug :
			    /*
			   std::cout << " track # " << i <<std::endl;
			   std::cout << "  params = " << std::endl;
			   par.Print();
			   std::cout << " C(0,0) = " << C(0, 0) << std::endl;
 			   char buffer[100];
			   sprintf(buffer,"_%i",i);
			   TString trackIndex(buffer);
			   par.Write("par"+trackIndex);
			   C.Write("cov"+trackIndex);
			*/
  			TVectorD ni(2);
			ni(0) = -TMath::Sin(phi);
			ni(1) =  TMath::Cos(phi);
			TMatrixDSym Hadd(2);
			Hadd.Rank1Update(ni, 1);		// Tensor product of vector ni with itself
			H += (1.0 / sDi2)*Hadd;
			cxy += (Di / sDi2)*ni;
		}
		//
 		TMatrixDSym Cov = SymRegInv(H);
		xvt = Cov*cxy;
		xv.SetSub(0, xvt);	// Store x,y of vertex
		Rv = TMath::Sqrt(xv(0)*xv(0) + xv(1)*xv(1));
		TVectorD dx = xvt - x0;
		epsi = H.Similarity(dx);
		x0 = xvt;
		Ntry++;
		//cout << "Vtx0: Iteration #" << Ntry << ", eps = " << epsi << ", x = " << xv(0) << ", y = " << xv(1);
  	}
	//
  	// Longitudinal fit
   	double Rv2 = Rv*Rv;
	//
 	// Loop on tracks for longitudinal fit
   	double hz = 0.0;
	double cz = 0.0;
	for (int i = 0; i < Ntr; i++)
	{
		// Get track helix parameters and their covariance matrix 
   		//ObsTrk *t = tracks[i];
                edm4hep::TrackState t = tracks[i];
		//ROOT::TVectorD par = t->GetObsPar();
		//ROOT::TMatrixDSym C = t->GetCov();
                TVectorD par = get_trackParam( t ) ;
                TMatrixDSym C = get_trackCov( t) ;

		//
  		// Longitudinal fit
   		double zi = par(3);
		double cti = par(4);
		double Di = par(0);
		double Ci = par(2);
		double sZi2 = C(3, 3);
		//
 		hz += 1 / sZi2;
		double arg = TMath::Sqrt(TMath::Max(0.0, Rv*Rv - Di*Di)/(1.+2*Ci*Di));
		cz += (cti*arg + zi)/sZi2;
	}
	xv(2) = cz / hz;

        TVector3 result( xv(0), xv(1), xv(2));

  	return result;
}

TVectorD Fillf(TVectorD par, TVectorD xin)
{
	//
 	// Decode input arrays
   	//
  	double D = par(0);
	double p0 = par(1);
	double C = par(2);
	double z0 = par(3);
	double ct = par(4);
	//
  	double x = xin(0);
	double y = xin(1);
	double z = xin(2);
	double R2 = x * x + y * y;
	double D2 = D*D;
	double UpCD = 1.0 + C*D;
	double Up2CD = 1.0 + 2 * C*D;
	double Az = C*(z - z0) / ct;
	//
  	// Calculate constraints
   	//
  	TVectorD f(2);
	f(0) = (R2 * C + UpCD*D)/Up2CD - y * TMath::Cos(p0) + x * TMath::Sin(p0);
	f(1) = TMath::Sin(Az)*TMath::Sin(Az) - C*C*(R2 - D2) / Up2CD;
	//
	return f;
}
//


TMatrixD FillD(TVectorD par, TVectorD xin)
{
	//
 	// Decode input arrays
   	//
  	double D = par(0);
	double p0 = par(1);
	double C = par(2);
	double z0 = par(3);
	double ct = par(4);
	//
  	double x = xin(0);
	double y = xin(1);
	double z = xin(2);
	double R2 = x * x + y * y;
	double D2 = D*D;
	double UpCD = 1.0 + C*D;
	double Up2CD = 1.0 + 2 * C*D;
	double Az = C*(z - z0) / ct;
	//
  	// Calculate matrix elements
   	//
  	TMatrixD Do(2, 5); Do.Zero();
	Do(0, 0) = 1.0 - 2 * C*(D + C*(R2 - D2)) / (Up2CD*Up2CD);	// df(0)/dD
	Do(0, 1) = x * TMath::Cos(p0) + y * TMath::Sin(p0);			// df(0)/dphi0
	Do(0, 2) = (R2 - D2) / (Up2CD*Up2CD);						// df(0)/dC
	Do(0, 3) = 0.0;												// df(0)/dz0
	Do(0, 4) = 0.0;												// df(0)/dct
	Do(1, 0) = 2 * C*C*(C*R2 + D*UpCD) / (Up2CD*Up2CD);			// df(1)/dD
	Do(1, 1) = 0.0;												// df(1)/dphi0
	Do(1, 2) = TMath::Sin(2 * Az)*Az / C - 2 * C*(R2 - D2)*UpCD / (Up2CD*Up2CD); // df(1)/dC
	Do(1, 3) = -TMath::Sin(2 * Az)*C / ct;						// df(1)/dz0
	Do(1, 4) = -TMath::Sin(2 * Az)*Az / ct;						// df(1)/dct
	//
  	return Do;
}
//

TMatrixD FillB(TVectorD par, TVectorD xin)
{
	//
 	// Decode input arrays
   	//
  	double D = par(0);
	double p0 = par(1);
	double C = par(2);
	double z0 = par(3);
	double ct = par(4);
	//
  	double x = xin(0);
	double y = xin(1);
	double z = xin(2);
	double R2 = x * x + y * y;
	double D2 = D*D;
	double UpCD = 1.0 + C*D;
	double Up2CD = 1.0 + 2 * C*D;
	double Az = C*(z - z0) / ct;
	//
  	// Calculate constraints
   	//
  	TMatrixD B(2, 3); 
        B.Zero();
	B(0, 0) = 2 * C*x/Up2CD + TMath::Sin(p0);
	B(0, 1) = 2 * C*y/Up2CD - TMath::Cos(p0);
	B(0, 2) = 0.0;
	B(1, 0) = -2 * x*C*C / Up2CD;
	B(1, 1) = -2 * y*C*C / Up2CD;
	B(1, 2) = TMath::Sin(2 * Az)*C / ct;
	//
  	return B;
}





edm4hep::VertexData  VertexFB( int Primary, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
					ROOT::VecOps::RVec<edm4hep::TrackState> thetracks )

{

        edm4hep::VertexData result;

        ROOT::VecOps::RVec<edm4hep::TrackState> tracks = getRP2TRK( recoparticles, thetracks );
        int Ntr = tracks.size();
        if ( Ntr <= 0) return result;

        //std::cout <<" Ntr = " << Ntr << std::endl;

	//
 	// Get approximate vertex evaluation
   	//
  	//TVectorD x0 = Vertex0FB(Ntr, tracks);
  	TVector3 ini_vtx = Vertex0FB( tracks) ;
        TVectorD x0(3);
        x0[0] = ini_vtx[0] ;
        x0[1] = ini_vtx[1] ;
        x0[2] = ini_vtx[2] ;

        TVectorD x(3);
        TMatrixDSym covX(3);

	//std::cout << "Preliminary vertex" << std::endl; x0.Print();
  	TVectorD dx(3);		// Solution x variation
	//
  	TVectorD f(2);		// Constraints
	TMatrixD D(2, 5);	// df/d alf (constraint over parameters)
	TMatrixD B(2, 3);	// df/dx    (constraint over x) 
	// Stored quantities
   	TVectorD **fi = new TVectorD*[Ntr];
	TVectorD **pi = new TVectorD*[Ntr];
	TMatrixD **Di = new TMatrixD*[Ntr];
	TMatrixD **Bi = new TMatrixD*[Ntr];
	TMatrixDSym **Wi = new TMatrixDSym*[Ntr];
	TMatrixDSym **Ci = new TMatrixDSym*[Ntr];
	//
  	// Loop on tracks to calculate everything
   	//
  	int Ntry = 0;
	int TryMax = 100;
	double eps = 0.001; // vertex stability
        double epsi = 1000.;
	
	x = x0;
	// Protect for vertices close to 0
//	
 // 	double pvx = 1.0e-8;
 // 	if (x(0)*x(0) + x(1)*x(1) < pvx)
 // 		{
 // 		double rn = gRandom->Rndm();
 // 		double phrn = TMath::TwoPi()*rn;
 // 		x(0) += 2.*pvx*TMath::Cos(phrn);
 // 		x(1) += 2.*pvx*TMath::Sin(phrn);
 // 		}
 // 	
	while (epsi > eps && Ntry < TryMax)		// Iterate until found vertex is stable
	{
                //std::cout << " Ntry  = " << Ntry << "  epsi = " << epsi << std::endl;
		TVectorD BtWf(3); BtWf.Zero();
		covX.Zero();		// Reset vertex covariance
		// 
   		for (int i = 0; i < Ntr; i++)
		{
		//std::cout << " ... track number " << i << std::endl;
			// Get track helix parameters and their covariance matrix 
   			///ObsTrk *t = tracks[i];
   			edm4hep::TrackState t = tracks[i] ;
			// TVectorD par0 = t->GetObsPar();
			TVectorD par0 = get_trackParam( t ) ;
			// TMatrixDSym C = t->GetCov();
			TMatrixDSym C = get_trackCov( t) ; 
 			    //C.Print();
			    //par0.Print();
			Ci[i] = new TMatrixDSym(C);
			TVectorD par(5);
			if (Ntry > 0) par = *pi[i];
			else
			{
				par = par0;
				pi[i] = new TVectorD(par0);
			}
			// Fill D
			//std::cout << " par = " ; par.Print();
                        //std::cout  << " x = " ; x.Print();
   			D = FillD(par, x);
 			//std::cout <<" D : " ; D.Print();
			Di[i] = new TMatrixD(D);
			// Fill B
   			B = FillB(par, x);
    			//std::cout <<" B : "; B.Print();
			Bi[i] = new TMatrixD(B);
			//std::cout << "Bi" << std::endl; Bi[i]->Print();
  			// Fill constraints
   			f = Fillf(par, x);
			fi[i] = new TVectorD(f);
			//std::cout << "fi" << std::endl; fi[i]->Print();
 			//
  			TMatrixDSym W = C.Similarity(D);
			//std::cout << "W: "; W.Print();
			//W.Invert();
			W = SymRegInv(W);
			Wi[i] = new TMatrixDSym(W);
			//std::cout << "Wi" << std::endl; Wi[i]->Print();
			TMatrixD Bt(TMatrixD::kTransposed, B);
			TMatrixDSym W1(W);
			TMatrixDSym BtWB = W1.Similarity(Bt);
			covX += BtWB;
			BtWf += Bt * (W*f);
		}
		// Update vertex covariance
		TMatrixDSym Hess = covX;
		//cout << "Hesse: "; Hess.Print();
		//covX.Invert();
		covX = SymRegInv(Hess);
		//covX.Print();
		// update vertex position
		dx = (-1.0*covX) * BtWf;
		//dx.Print();
		x += dx;
                //std::cout << " dx= "<<dx(0) <<" " << dx(1) << " " << dx(2) << std::endl;
		// Update track parameters
		for (int i = 0; i < Ntr; i++)
		{
			TVectorD lambda = *fi[i] + (*Bi[i]) * dx;
			TMatrixD Dt(TMatrixD::kTransposed, *Di[i]);
			*pi[i] = *pi[i] - ((*Ci[i])*Dt) * lambda;
		}
		// update vertex stability
		epsi = Hess.Similarity(dx);
		Ntry++;
                //std::cout << " end of iter: epsi = " << epsi << std::endl;
		if (epsi >10)
		std::cout << "Vtx:  Iteration #"<<Ntry<<", eps = "<<epsi<<", x = " << x(0) << ", " << x(1) << ", " << x(2) << std::endl;
	}
	//
  	// Calculate Chi2
   	//
  	double Chi2 = 0.0;
	for (int i = 0; i < Ntr; i++)
	{
		TVectorD lambda = *fi[i] + (*Bi[i]) * dx;
		TMatrixDSym Wp = *Wi[i];
		Chi2 += Wp.Similarity(lambda);
	}


        for (int i = 0; i < Ntr; i++) {
          delete fi[i];
          delete pi[i];
          delete Di[i];
          delete Bi[i];
          delete Wi[i];
          delete Ci[i];
        }
        delete fi;
        delete pi;
        delete Di;
        delete Bi;
        delete Wi;
        delete Ci;




        //std::cout << " final vertex " << x(0) << " " << x(1) << " " << x(2) << std::endl;

	// store the results in an edm4hep::VertexData object
        std::array<float,6> covMatrix;
	covMatrix[0] = covX(0,0);
	covMatrix[1] = covX(0,1);
	covMatrix[2] = covX(0,2);
	covMatrix[3] = covX(1,1);
	covMatrix[4] = covX(1,2);
	covMatrix[5] = covX(2,2);
  
        //result.setPrimary( Primary );
        float Ndof = 2.0 * Ntr - 3.0; ;
        //result.setChi2( Chi2 /Ndof );   
        //result.setPosition ( edm4hep::Vector3f( x(0), x(1), x(2) ));
        //result.setCovMatrix ( covMatrix );
        //result.setAlgorithmType (1);

        result.primary = Primary;
	result.chi2 = Chi2 /Ndof ;	// I store the normalised chi2 here
	result.position = edm4hep::Vector3f( x(0), x(1), x(2) ) ;
	result.covMatrix = covMatrix;
	result.algorithmType = 1;

	// Need to fill the associations ...

        return result;

}
