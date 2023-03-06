#Optional test file
testFile="/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bs2DsK/events_017659734.root"



##########################################################################################################

#
#   	Code dedicated to the Bs to Ds K analysis, not in central FCCAnalysis library
#

##########################################################################################################


ReconstructedDs_code='''

//
//	-- This method reconstructs the Ds pseudo-track using Franco's VertexMore.
//      -- It returns a vector by convenience - but the vector only contains at most one TrackState.
//      -- tracks in input = the DsTracks
//

#include "FCCAnalyses/VertexFitterSimple.h"
#include "FCCAnalyses/VertexingUtils.h"


ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs( ROOT::VecOps::RVec<edm4hep::TrackState>  tracks,
				                          bool AddMassConstraints = false) {


  ROOT::VecOps::RVec<edm4hep::TrackState > result;

  int Ntr = tracks.size();
  if ( Ntr != 3 ) return result;

  TVectorD** trkPar = new TVectorD*[Ntr];
  TMatrixDSym** trkCov = new TMatrixDSym*[Ntr];

  bool Units_mm = true;

  for (Int_t i = 0; i < Ntr; i++) {
    edm4hep::TrackState t = tracks[i] ;
    TVectorD par = FCCAnalyses::VertexingUtils::get_trackParam( t, Units_mm ) ;
    trkPar[i] = new TVectorD( par );
    TMatrixDSym Cov = FCCAnalyses::VertexingUtils::get_trackCov( t, Units_mm );
    trkCov[i] = new TMatrixDSym ( Cov );
  }

  VertexFit theVertexFit( Ntr, trkPar, trkCov );
  TVectorD  x = theVertexFit.GetVtx() ;   // this actually runs the fit

  VertexFit* vertexfit = &theVertexFit;
  VertexMore vertexmore( vertexfit, Units_mm );

  if ( AddMassConstraints ) {
     
      const double kaon_mass = 4.9367700e-01 ;
      const double pion_mass = 0.140;
      const double Ds_mass = 1.9683000e+00 ;
      const double Phi_mass = 1.0194610e+00 ;

      double Ds_masses[3] = { kaon_mass, kaon_mass, pion_mass };
      int Ds_list[3] = { 0, 1, 2 };
      vertexmore.AddMassConstraint(Ds_mass, 3, Ds_masses, Ds_list);   // Ds mass constraint

      /*
      // Phi mass constraint: does not crash, but pulls of the resulting Bs vertex are bad.
      double Phi_masses[2] = { kaon_mass, kaon_mass };
      int Phi_list[2] = { 0, 1 };
      vertexmore.AddMassConstraint(Phi_mass, 2, Phi_masses, Phi_list);   // Phi mass constraint
      */

      vertexmore.MassConstrFit();
  }

  TVectorD  Ds_track_param  = vertexmore.GetVpar();
  TMatrixDSym cov = vertexmore.GetVcov();

  TVectorD  Ds_track_param_edm4hep = FCCAnalyses::VertexingUtils::Delphes2Edm4hep_TrackParam( Ds_track_param, Units_mm );
  edm4hep::TrackState track;
  track.D0  = Ds_track_param_edm4hep[0] ;
  track.phi = Ds_track_param_edm4hep[1];
  track.omega  = Ds_track_param_edm4hep[2];
  track.Z0  = Ds_track_param_edm4hep[3] ;
  track.tanLambda = Ds_track_param_edm4hep[4] ;

  // now the covariance matrix - lower-triangle :

  TMatrixDSym covM(5);
  std::array<float, 21> covMatrix = FCCAnalyses::VertexingUtils::Delphes2Edm4hep_TrackCovMatrix( cov, Units_mm )  ;

  track.covMatrix = covMatrix ;

  result.push_back(  track );

 return result;
}
'''


##########################################################################################################

Momentum_ReconstructedDs_code='''

#include "FCCAnalyses/VertexFitterSimple.h"
#include "FCCAnalyses/VertexingUtils.h"

TVector3 Momentum_ReconstructedDs( edm4hep::TrackState Ds_pseudoTrack ) {

  TVectorD Param = FCCAnalyses::VertexingUtils::get_trackParam( Ds_pseudoTrack );  // track parameters, Franco's convention
  TVector3 result = FCCAnalyses::VertexingUtils::ParToP( Param );

 return result;

}

'''


##########################################################################################################


Tracks_for_the_Bs_vertex_code='''
#include "FCCAnalyses/VertexingUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"

ROOT::VecOps::RVec<edm4hep::TrackState>  tracks_for_fitting_the_Bs_vertex(
                                ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs,
                                ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack) {

 ROOT::VecOps::RVec<edm4hep::TrackState>  result;
 if ( ReconstructedDs.size() != 1 ) return result;
 if ( BachelorKTrack.size() != 1 )  return result;

 result.push_back( ReconstructedDs[0])  ;  // the pseudo-Ds track
 result.push_back( BachelorKTrack[0] );        // the bachelor K

 return result;
}
'''


##########################################################################################################


import ROOT
ROOT.gInterpreter.Declare(ReconstructedDs_code)
ROOT.gInterpreter.Declare(Momentum_ReconstructedDs_code)
ROOT.gInterpreter.Declare(Tracks_for_the_Bs_vertex_code)



#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               # ---------------------------------------------------------------------------------------
	       #
               # -----  Retrieve the indices of the MC Particles of interest

               # MC indices of the decay Bs_bar (PDG = -531) -> Ds+ (PDG = 431) K- (PDG = -321) 
               # Retrieves a vector of int's which correspond to indices in the Particle block
               # vector[0] = the mother, and then the daughters in the order specified, i.e. here
               #       [1] = the Ds+, [2] = the K-
               # Boolean arguments :
               #	1st: stableDaughters. when set to true, the daughters specified in the list are looked
               #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
               #             explored recursively if needed.
               #        2nd: chargeConjugateMother
               #        3rd: chargeConjugateDaughters
               #        4th: inclusiveDecay: when set to false, if a mother is found, that decays
               #             into the particles specified in the list plus other particle(s), this decay is not selected.
               # If the event contains more than one such decays,only the first one is kept.
               .Define("Bs2DsK_indices", "MCParticle::get_indices( -531, {431, -321}, false, true, true, false) ( Particle, Particle1)" )

               # select events for which the requested decay chain has been found:
               .Filter("Bs2DsK_indices.size() > 0")

               .Define("Bs_MCindex",  "return Bs2DsK_indices[0] ;" )
               .Define("Ds_MCindex",  "return Bs2DsK_indices[1] ;" )
               .Define("BachelorK_MCindex",  "return Bs2DsK_indices[2] ;" )


               # MC indices of (this) Ds+ -> K+ K- Pi+
               # Boolean arguments :
               #        1st: stableDaughters. when set to true, the daughters specified in the list are looked
               #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
               #             explored recursively if needed.
               #        2nd: chargeConjugateDaughters
               #        3rd: inclusiveDecay
               .Define("Ds2KKPi_indices",  "MCParticle::get_indices_MotherByIndex( Ds_MCindex, { 321, -321, 211 }, true, true, false, Particle, Particle1 )")

               .Define("Kplus_MCindex",  "return Ds2KKPi_indices[1] ; ")
               .Define("Kminus_MCindex",  "return Ds2KKPi_indices[2] ; ")
               .Define("Piplus_MCindex",  "return Ds2KKPi_indices[3] ; ")

               # ---------------------------------------------------------------------------------------


               # ---------------------------------------------------------------------------------------
               # -----    The MC Particles :

               # the MC Bs :
               .Define("Bs",  "return Particle[ Bs_MCindex ]; ")
               # the MC Ds :
               .Define("Ds",  "return Particle[ Ds_MCindex ]; ")
               # the MC bachelor K- from the Bs decay :
               .Define("BachelorK",  "return Particle[ BachelorK_MCindex  ]; " )
               # The MC legs from the Ds decay
               .Define("Kplus", "return Particle[ Kplus_MCindex ] ; ")
               .Define("Kminus", "return Particle[ Kminus_MCindex ] ; ")
               .Define("Piplus", "return Particle[ Piplus_MCindex ] ; ")

               # some MC-truth kinematic quantities:
               .Define("BachelorK_px", "return BachelorK.momentum.x ;")
               .Define("BachelorK_py", "return BachelorK.momentum.y ;")
               .Define("BachelorK_pz", "return BachelorK.momentum.z ;")

               .Define("Ds_px",  "return Ds.momentum.x ;")
               .Define("Ds_py",  "return Ds.momentum.y ;")
               .Define("Ds_pz",  "return Ds.momentum.z ;")
               .Define("Ds_pt", "ROOT::VecOps::RVec<edm4hep::MCParticleData> v; v.push_back( Ds ); return MCParticle::get_pt(v ) ;")


               # ---------------------------------------------------------------------------------------


               # ---------------------------------------------------------------------------------------
               # -----	The MC-truth decay vertices of the Bs and of the Ds

               # Note: in case the Bs or Bsbar has oscillated  before it decays, the vertex returned
               # below is the decay vertex of the Bs after oscillation.

               # MC Decay vertex of the Bs = the production vertex of the Bachelor K
               .Define("BsMCDecayVertex",  "return BachelorK.vertex; " )
               # MC Decay vertex of the Ds = the production vertex of the Kplus
               .Define("DsMCDecayVertex",  "return Kplus.vertex ; " )

               # ---------------------------------------------------------------------------------------


               # ---------------------------------------------------------------------------------------
               # -----    The RecoParticles that are MC-matched with the particles of the Ds decay

               # RecoParticles associated with the Ds decay
               # Note: the size of DsRecoParticles below is always 3 provided that Ds2KKPi_indices is not empty.
               # possibly including "dummy" particles in case one of the legs did not make a RecoParticle
               # (e.g. because it is outside the tracker acceptance).
               # This is done on purpose, in order to maintain the mapping with the indices - i.e. the 1st particle in
               # the list BsRecoParticles is the Kminus, then the Kplus, then the Piplus.
               # (selRP_matched_to_list ignores the unstable MC particles that are in the input list of indices
               # hence the mother particle, which is the [0] element of the Ds2KKPi_indices vector).
               #
               # The matching between RecoParticles and MCParticles requires 4 collections. For more
               # detail, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics

               .Define("DsRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Ds2KKPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("DsTracks",  "ReconstructedParticle2Track::getRP2TRK( DsRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Ds vertex
               .Define("n_DsTracks", "ReconstructedParticle2Track::getTK_n( DsTracks )")

               # ---------------------------------------------------------------------------------------
               # ------      Reco'ed vertex of the Ds

               # The index "3" below is just to indicate that this is a "tertiary" vertex, it has no influence
               # on the vertex fitting.
               # Note: no mass constraint is applied here. See the code of "ReconstructedDs" for an example
               # of how mass constraints can be applied.
               .Define("DsVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 3, DsTracks)" )
               .Define("DsVertex",  "VertexingUtils::get_VertexData( DsVertexObject )")

               # -------------------------------------------------------------------------------------------------------


               # -------------------------------------------------------------------------------------------------------
               # ----------  Reconstruction of the Bs vertex 

               # The Ds pseudoTrack (TrackState) - returned as a vector of TrackState, with one single element :
               # boolean = true: add Ds mass constraint in the Ds vertex fit. 
               # Default = false (no mass constraint applied)
               .Define("v_Ds_PseudoTrack",  "ReconstructedDs( DsTracks, true )")

               # Number of Ds pseudoTracks. In principle it should always be equal to one at this stage.
               .Define("n_pdt", "ReconstructedParticle2Track::getTK_n( v_Ds_PseudoTrack )")
               # but it is explicitely required to be non zero, otherwise the code that comes next would crash:
               .Filter("n_pdt > 0")

               # The momentum vector (TVector3) of the Ds :
               .Define("Ds_momentum",   "Momentum_ReconstructedDs( v_Ds_PseudoTrack[0] ) ")
               .Define("RecoDs_px",  "return Ds_momentum.x() ")
               .Define("RecoDs_py",  "return Ds_momentum.y() ")
               .Define("RecoDs_pz",  "return Ds_momentum.z() ")


               # the  RecoParticle associated with  the bachelor K
               .Define("BsRecoParticles", "ReconstructedParticle2MC::selRP_matched_to_list( Bs2DsK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define("RecoBachelorK",  " return BsRecoParticles[0] ; ")   # only the bachelor K is stable, among the indices of Bs2DsK_indices

	       .Define("RecoBachelorK_px", "return RecoBachelorK.momentum.x; ")
               .Define("RecoBachelorK_py", "return RecoBachelorK.momentum.y; ")
               .Define("RecoBachelorK_pz", "return RecoBachelorK.momentum.z; ")


               # and the corresponding track
               .Define("v_RecoBachelorK", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> v; v.push_back( RecoBachelorK ); return v; ")
               .Define("v_BachelorKTrack",  "ReconstructedParticle2Track::getRP2TRK(  v_RecoBachelorK, EFlowTrack_1)" )

               # Now we have the two tracks that we need for the Bs vertex :
               .Define("BsTracks",  "tracks_for_fitting_the_Bs_vertex( v_Ds_PseudoTrack, v_BachelorKTrack) ")


               # ---------------------------------------------------------------------------------------
               # ------      Reco'ed vertex of the Bs

               .Define("BsVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 2, BsTracks )" )
               .Define("n_BsTracks", "ReconstructedParticle2Track::getTK_n( BsTracks )")

               # This is the final Bs vertex
               .Define("BsVertex",  "VertexingUtils::get_VertexData( BsVertexObject )")

               
        )
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "DsMCDecayVertex",
                "BsMCDecayVertex",
                "n_DsTracks",
                "DsVertex",
                "Ds_momentum",
                "n_BsTracks",
                "BsVertex",
	        "BachelorK_px", "BachelorK_py", "BachelorK_pz",
		"RecoBachelorK_px","RecoBachelorK_py","RecoBachelorK_pz",
		"Ds_px", "Ds_py", "Ds_pz","Ds_pt",
		"RecoDs_px", "RecoDs_py", "RecoDs_pz",

        ]
        return branchList
