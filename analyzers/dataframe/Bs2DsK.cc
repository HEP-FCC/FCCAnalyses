#include "Bs2DsK.h"

#include <random>
#include <chrono>

using namespace MCParticle;
using namespace Vertexing;


// ---------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<int>  getMC_indices_Ds2KKPi ( ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                  ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

 ROOT::VecOps::RVec<int>  result;

 if ( Bs2DsK_indices.size() == 0) return result;
 if ( Bs2DsK_indices.size() != 3) {
        std::cout << "  !!!!  getMC_indices_Bs2DsK: size of Bs2DsK_indices != 3: " << Bs2DsK_indices.size() << std::endl;
        return result;
 }

 //std::cout << " ... in getMC_indices_Ds2KKPi, found a Bs to Ds K " << std::endl;

 int idx_Ds = Bs2DsK_indices[1];  // by construction  ( [0] = index of the mpther Bs )

 // get the indices of the Ds+ daughters :
 std::vector<int> pdg_daughters = { 321, -321, 211 } ;  //  K+, K-, Pi+
 bool stable = true;    // look among the list of *stable* daughters of the Ds+
 ROOT::VecOps::RVec<int> Ds_daughters = get_indices_ExclusiveDecay_MotherByIndex( idx_Ds, pdg_daughters, stable, in, ind);

 // Ds_daughters contains the indices of : the mother Ds, the K+, K-, Pi+
 if ( Ds_daughters.size() != 4 ) return result;   // this is not the decay searched for. Return an empty vector

 //std::cout << " ... Found the Ds daughters " << std::endl;
 //check:
 //std::cout << " end of getMC_indices_Ds2KKPi " << std::endl;
 //for (int i=0; i < Ds_daughters.size(); i++) {
     //std::cout << " index = " << Ds_daughters[i] << " PDG = " << in.at( Ds_daughters[i] ).PDG << std::endl;
 //}

 return Ds_daughters ;
}

// ---------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<int>  getMC_indices_Bs2KKPiK ( ROOT::VecOps::RVec<int> Bs2DsK_indices, 
						  ROOT::VecOps::RVec<int> Ds2KKPi_indices ) {

// returns a vector with the indices of the Bs, (K+ K- Pi+ ) ,  K- , in this order,
// where the first 3 particles are the daughters from the Ds+
// the input lists: Bs2DsK_indices  contains the indices of: the Bs, the Ds+, the K- (in this order)
//                  Ds2KKPi_indices contains the indices of: the Ds+, the K+,K-, Pi+

 ROOT::VecOps::RVec<int>  result;

 if ( Bs2DsK_indices.size() != 3) return result;  
 if ( Ds2KKPi_indices.size() != 4) return result;

 // Now fill in the indices:

 result.push_back(  Bs2DsK_indices[0] );   // the mother Bs

 // the Ds daughters :
 for (int i=1; i< Ds2KKPi_indices.size(); i++) {  // do not include the Ds !
   result.push_back( Ds2KKPi_indices[i] );
 }

 result.push_back(  Bs2DsK_indices[2] );  // the bachelor K-
 //std::cout << " ... in getMC_indices_Bs2DsK, found all daughters " << std::endl;

// check
  //std::cout << " indices of getMC_indices_Bs2KKPiK " << std::endl;
  //for (int i=0;i<  result.size(); i++) {
    //std::cout << "index= " << result[i] << std::endl;
  //}

 return result;

}

// ---------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedDs( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoKplus,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoKminus,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoPiplus) {

 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  result;

 if ( RecoKplus.size() != 1 || RecoKminus.size()!= 1 || RecoPiplus.size() != 1 ) return result;
 // require that esch particle be reconstructed,i.e. remove the dummies
 if ( RecoKplus[0].energy < 0 || RecoKminus[0].energy < 0 || RecoPiplus[0].energy <0) return result;

 std::vector< edm4hep::ReconstructedParticleData> legs = { RecoKplus[0], RecoKminus[0], RecoPiplus[0] };
 float mK = 4.9367700e-01;
 float mPi = 1.3957018e-01;
 std::vector< float> masses={ mK, mK, mPi };
 
 edm4hep::ReconstructedParticleData theDs;
 TLorentzVector theDs4v;
 float Ds_charge = 0;

 for (int ileg = 0; ileg < 3; ileg++) {
   
	TLorentzVector leg;
        leg.SetXYZM( legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, masses[ileg] );
        theDs4v +=  leg;
        Ds_charge += legs[ileg].charge;

 }
 theDs.charge =  Ds_charge;
 theDs.momentum.x = theDs4v.Px();
 theDs.momentum.y = theDs4v.Py();
 theDs.momentum.z = theDs4v.Pz();
 theDs.mass = theDs4v.M();
 theDs.referencePoint = legs[0].referencePoint;

 result.push_back( theDs );
 return result;
}


// ----------------------------------------------------------------------------------------------------------------------------


ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> theDss,
	ROOT::VecOps::RVec<edm4hep::MCParticleData> theMCDs, edm4hep::Vector3d  theMDsMCDecayVertex ) {

// return a TrackState corresponding to the reco'ed Ds

// The MC information, theMCDs and theMDsMCDecayVertex, is passed here only for debugging / check purposes


  ROOT::VecOps::RVec<edm4hep::TrackState > result;
  if ( theDss.size() != 1 ) return result;

  edm4hep::MCParticleData MCDs = theMCDs[0];

  float norm = 1e-3;   // to convert from mm to meters 

        edm4hep::ReconstructedParticleData theDs = theDss[0];

        // use the  reco'ed Ds :
        TVector3 vertex( theDs.referencePoint.x * norm, theDs.referencePoint.y * norm, theDs.referencePoint.z * norm );
        TVector3 momentum ( theDs.momentum.x, theDs.momentum.y, theDs.momentum.z)  ;

        // use the MC Ds and its vertex
        TVector3 MCvertex( theMDsMCDecayVertex.x * norm, theMDsMCDecayVertex.y * norm, theMDsMCDecayVertex.z * norm );
        TVector3 MCmomentum ( MCDs.momentum.x, MCDs.momentum.y, MCDs.momentum.z );

 //std::cout << " Reco'ed Ds momentum " <<  theDs.momentum.x << " " << theDs.momentum.y << " " << theDs.momentum.z << std::endl;
 //std::cout << "      MC Ds momentum " << MCDs.momentum.x << " " << MCDs.momentum.y << " " << MCDs.momentum.z << std::endl;
 //std::cout << " Reco'ed Ds vertex   " << theDs.referencePoint.x << " " << theDs.referencePoint.y << " " << theDs.referencePoint.z << std::endl;
 //std::cout << "      MC Ds vertex   " << theMDsMCDecayVertex.x << " " << theMDsMCDecayVertex.y  << " " << theMDsMCDecayVertex.z  << std::endl;
 //std::cout << " Reco'ed Ds charge   " << theDs.charge << std::endl;

 // To use the MC Ds instead of the reco'ed one :
 //vertex = MCvertex;
 //momentum = MCmomentum;

        // get the corresponding track parameters using Franco's code 
        TVectorD track_param = XPtoPar( vertex, momentum, theDs.charge );

        edm4hep::TrackState track;
        track.D0        = track_param[0] * 1e3 ; // from meters to mm
        track.phi       = track_param[1];
        track.omega     = track_param[2] / ( 0.5*1e3 ) ; // C from Franco = rho/2, and convert from m-1 to mm-1

  // need to change here, because the TracSTate of edm4heo currently use
  // the wrong sign !
        track.omega = -track.omega ;

        track.Z0        = track_param[3] * 1e3  ;   // from meters to mm
        track.tanLambda = track_param[4];

        track.referencePoint.x = vertex[0];
        track.referencePoint.y = vertex[1];
        track.referencePoint.z = vertex[2];

        // assume here that the parameters are perfectly measured
        std::array<float, 15> covMatrix;
        for (int icov=0; icov < 15; icov++) {
           covMatrix[icov] = 0;
        }
        // diagonal terms: take error = 5% of the parameter
        float arbitrary_value = 0.05 ;
	//float arbitrary_value = 2.;   // 200% !!
        covMatrix[0] = pow( arbitrary_value * track_param[0] ,2);
        covMatrix[5] = pow( arbitrary_value * track_param[1] , 2);
        covMatrix[9] = pow( arbitrary_value * track_param[2] , 2) ;
        covMatrix[12] = pow( arbitrary_value * track_param[3] , 2);
        covMatrix[14] = pow( arbitrary_value* track_param[4] , 2);
        track.covMatrix = covMatrix;

        result.push_back( track );

  return ROOT::VecOps::RVec<edm4hep::TrackState>( result );
}

// ----------------------------------------------------------------------------------------------------------------------------


ROOT::VecOps::RVec<edm4hep::TrackState>  tracks_for_fitting_the_Bs_vertex( 
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoDs_atVertex,
				ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> theMCDs,
				edm4hep::Vector3d  theMDsMCDecayVertex   ) {

// ROOT::VecOps::RVec<edm4hep::MCParticleData> theMCDs : passed to debug (use the MC Ds instead of the recoed one)

 ROOT::VecOps::RVec<edm4hep::TrackState>  result;

 if ( RecoDs_atVertex.size() != 1 ) return result;
 if ( BachelorKTrack.size() != 1 )  return result;

 ROOT::VecOps::RVec<edm4hep::TrackState> DsPseudoTrackState = ReconstructedDs_atVertex_TrackState( RecoDs_atVertex, theMCDs, theMDsMCDecayVertex);

        result.push_back( DsPseudoTrackState[0] );    // the pseudo-Ds track
        result.push_back( BachelorKTrack[0] );        // the bachelor K

 return result;
}


// ----------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::TrackState>  tracks_for_fitting_the_Bs_vertex(
                                ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState_withCovariance,
				ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack) {

 ROOT::VecOps::RVec<edm4hep::TrackState>  result;
 if ( ReconstructedDs_atVertex_TrackState_withCovariance.size() != 1 ) return result;
 if ( BachelorKTrack.size() != 1 )  return result;

 result.push_back( ReconstructedDs_atVertex_TrackState_withCovariance[0])  ;  // the pseudo-Ds track
 result.push_back( BachelorKTrack[0] );        // the bachelor K

 return result;
}

// ----------------------------------------------------------------------------------------------------------------------------


ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState_withCovariance ( 
			ROOT::VecOps::RVec<edm4hep::TrackState> DsTracks,
			ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState,
			FCCAnalysesVertex centralVertex ) {

// more complicated: one wants here the TrackState of the Reco'ed Ds at the vertex but now,
// with the covariance matrix determined "properly" (in order to use this TrackState in
// the vertex fitter).
// Done by brute force.

  ROOT::VecOps::RVec<edm4hep::TrackState > result;
  if ( DsTracks.size() != 3 ) return result;

  if ( ReconstructedDs_atVertex_TrackState.size() != 1 ) return result;

  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  std::default_random_engine generator (seed);
  std::normal_distribution<double> gaus_distribution(0., 1. );


 // central values of the parameters of the Ds at the vertex:
 double central_param[5];
 edm4hep::TrackState central_Ds = ReconstructedDs_atVertex_TrackState[0];
 central_param[0] = central_Ds.D0;
 central_param[1] = central_Ds.phi;
 central_param[2] = central_Ds.omega;
 central_param[3] = central_Ds.Z0;
 central_param[4] = central_Ds.tanLambda;

 //std::cout << " Central Ds : " << central_Ds.D0 << " " << central_Ds.phi << " " << central_Ds.omega << " " << central_Ds.Z0 << " " << central_Ds.tanLambda << std::endl;

	// Now determine the covariance matrix of these parameters using a Monte-Carlo method

 int nsamples = 300;	// Each "sample" corresponds to a smearing of the
			// track parameters of the Ds legs, according to their cov matrix.

 // the Ds tracks are in this order: K, K, Pi
 float mK = 4.9367700e-01;
 float mPi = 1.3957018e-01;
 std::vector< float> masses={ mK, mK, mPi };

 double param_base[5];
 int idxCov[5] = { 0, 5, 9, 12, 14 };  // indices of the diagonal terms in the track covariance matrix
 double randomGaus[5] ;
 double param[5];

 double convert[5] = { 1e-3, 1., 0.5*1e3, 1e-3, 1. }; // to convert the edm4hep tracks into Franco's tracks
						      // ( convert mm to m, and his C = rho / 2 )

 double sum[5];   // to determine the average of the Ds track parameters
 double sumsq[5]; // to determine the variance of the parameters
 
 for (int i=0; i < 5; i++) {
   sum[i] = 0;
   sumsq[i] = 0;
 }

 TVectorD param_Franco(5);  // the track parameters using Franco's units & definitions

 for (int isample=0; isample < nsamples; isample++) {

	ROOT::VecOps::RVec<edm4hep::TrackState> modified_trackStates;  // the Ds legs, after smearing

 	for ( auto & track: DsTracks) {

    	    param_base[0] = track.D0 ;
    	    param_base[1] = track.phi ;
    	    param_base[2] = track.omega ;
    	    param_base[3] = track.Z0 ;
    	    param_base[4] = track.tanLambda ;

        //if (isample == 0) {
	//std::cout << "  a Ds leg D0 (mum)  = " << 1e3 * track.D0 << std::endl;
        //std::cout << "  a Ds leg Z0 (mum)  = " << 1e3 * track.Z0 << std::endl;
        //}

	    edm4hep::TrackState modified_track = track;

	    // modify the track parameters according to their covariance matrix
	    for (int i=0; i < 5; i++) {
	        double uncertainty = 0;
	        if ( track.covMatrix[ idxCov[i] ] > 0 ) {
		    uncertainty = sqrt( track.covMatrix[ idxCov[i] ] ) ;
		}
                randomGaus[i] = gaus_distribution(generator) ;
		param[i] = param_base[i] + randomGaus[i] * uncertainty;
	        // and using Franco's definitions & units :
	        //param_Franco[i] = param[i] * convert[i] ;
	    }

	    modified_track.D0 		= param[0] ;
	    modified_track.phi 		= param[1] ;
	    modified_track.omega	= param[2];
	    modified_track.Z0		= param[3];
	    modified_track.tanLambda	= param[4];

	    modified_trackStates.push_back( modified_track );

 	}  // end loop over the DsTracks

	// Run the vertex fitter over the smeared Ds legs
	FCCAnalysesVertex vertexObject = VertexFitter_Tk(3, modified_trackStates );
	  //FCCAnalysesVertex vertexObject = centralVertex ;    // to check mem leak ... 
        //std::cout << " Fitted Ds vertex: " << vertexObject.vertex.position.x << " " << vertexObject.vertex.position.y << " " << vertexObject.vertex.position.z << std::endl;

        // Reconstruct a Ds :
        edm4hep::ReconstructedParticleData theDs;
        TLorentzVector theDs4v;
        float Ds_charge = 0;

	// now retrieve the track momentum, at the Ds decay vertex
	for (int itrack=0; itrack < 3; itrack++) {	// 3 tracks are required at the very beginning
	    TVector3 track_momentum = vertexObject.updated_track_momentum_at_vertex[ itrack ];
	    TLorentzVector leg;
	    leg.SetXYZM( track_momentum[0], track_momentum[1], track_momentum[2], masses[itrack] );
	    theDs4v += leg;
	    float charge = 1;
	    if (  modified_trackStates[itrack].omega < 0) charge = -1;  // careful, this is with the edm4hep convention !!
	    Ds_charge += charge;
	}
        theDs.charge =  Ds_charge;
        theDs.momentum.x = theDs4v.Px();
        theDs.momentum.y = theDs4v.Py();
        theDs.momentum.z = theDs4v.Pz();
        theDs.mass = theDs4v.M();
        theDs.referencePoint = vertexObject.vertex.position ;
        //std::cout << " Ds mass = " << theDs.mass << " charge = " << theDs.charge << std::endl;

	// now the TrackState corresponding to this Ds 
	TVector3 thevtx( 1e-3*theDs.referencePoint.x, 1e-3*theDs.referencePoint.y, 1e-3*theDs.referencePoint.z );  // mm -> m
        TVector3 themomentum( theDs.momentum.x, theDs.momentum.y, theDs.momentum.z );
        //std::cout << " the vertex " << thevtx.x() << " " << thevtx.y() << " " << thevtx.z() << std::endl;
        //std::cout << " the momentum " << themomentum.x() << " " << themomentum.y() << " " << themomentum.z() << std::endl;
	TVectorD Ds_track_param = XPtoPar( thevtx, themomentum, theDs.charge );
        edm4hep::TrackState track;
        track.D0        = Ds_track_param[0] * 1e3 ; // from meters to mm
        track.phi       = Ds_track_param[1];
        track.omega     = Ds_track_param[2] / ( 0.5*1e3 ) ; // C from Franco = rho/2, and convert from m-1 to mm-1
       // need to change here, because the TracSTate of edm4heo currently use
       // the wrong sign !
        track.omega = -track.omega ;
        track.Z0        = Ds_track_param[3] * 1e3  ;   // from meters to mm
        track.tanLambda = Ds_track_param[4];

	param[0] = track.D0;
	param[1] = track.phi;
	param[2] = track.omega;
	param[3] = track.Z0;
        param[4] = track.tanLambda;
        //std::cout << " parameters : " << track.D0 << " " << track.phi << " " << track.omega << " " << track.Z0 << " " << track.tanLambda << std::endl;

	// and do the sums to determine the variances of these track parameters...
	for (int i=0; i < 5; i++) {
	    sum[i] += param[i];
	    sumsq[i] += pow( param[i] - central_param[i], 2 );
   	}

 } // end loop over isample

 // Central values of the parameters, as determined from the samples
 // These should be very close to the central_params determined earlier
 // and stored in ReconstructedDs_atVertex_TrackState (passed in input)

 for (int i=0; i < 5; i++) {
     sum[i] = sum[i] / float(nsamples);
     sumsq[i] = sumsq[i] / ( nsamples - 1. );
  }

  // printouts...
  //std::cout << " ---- end of ReconstructedDs_atVertex_TrackState_withCovariance " << std::endl;
  //std::cout << " D0 : " << central_param[0] << std::endl;
  //std::cout << " D0 from the samples " << sum[0] << std::endl;
  //std::cout << " D0 variance from the samples = " << sumsq[0] << std::endl;
    /*
   for (int i=0; i < 5; i++) {
       float error = sqrt( sumsq[i] ) ;
       float rel_error = error / central_param[i] ;
	std::cout << " relative uncertainty on param " << i << " amounts to " << 100.*rel_error << " % " << std::endl;
   }
   */

  edm4hep::TrackState the_final_Ds = ReconstructedDs_atVertex_TrackState[0];
  // set up its covariance matrix :
   for (int i=0; i < 5; i++) {
     the_final_Ds.covMatrix[ idxCov[i] ] = sumsq[i] ;
   }
   result.push_back( the_final_Ds );

 return result;

}










