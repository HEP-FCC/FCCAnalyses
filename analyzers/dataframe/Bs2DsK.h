
#ifndef BS2DSK_ANALYZERS_H
#define BS2DSK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "podio/ObjectID.h"
#include "TLorentzVector.h"


#include "MCParticle.h"
#include "ReconstructedParticle2MC.h"
#include "Vertexing.h"

#include <random>


ROOT::VecOps::RVec<int>  getMC_indices_Ds2KKPi ( ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                  ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) ;

ROOT::VecOps::RVec<int>  getMC_indices_Bs2KKPiK ( ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                  ROOT::VecOps::RVec<int> Ds2KKPi_indices ) ;


ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedDs( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoKplus,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoKminus,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoPiplus) ;

/// Returns a "pseudo-track" corresponding to the Ds. The covariance matrix is not determined,
/// an ad-hoc uncertainty of 5% is set on the parameters.
/// see below to determine the covariance matrix more properly.
/// the MC information is passed only for checks (to use the truth Ds instead of the reco'ed one)
ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> theDss,
				        ROOT::VecOps::RVec<edm4hep::MCParticleData> theMCDs,
					edm4hep::Vector3d  theMDsMCDecayVertex ) ;

/// the MC information is passed only for checks (to use the truth Ds instead of the reco'ed one)
ROOT::VecOps::RVec<edm4hep::TrackState>  tracks_for_fitting_the_Bs_vertex(
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> RecoDs_atVertex,
                                ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> theMCDs,
				edm4hep::Vector3d  theMDsMCDecayVertex  ) ;


/// Returns a "pseudo-track" corresponding to the Ds, with the covariance matrix determined.
ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState_withCovariance (
                        ROOT::VecOps::RVec<edm4hep::TrackState> DsTracks,
                        ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState,
			Vertexing::FCCAnalysesVertex centralVertex ) ;

ROOT::VecOps::RVec<edm4hep::TrackState>  tracks_for_fitting_the_Bs_vertex(
                                ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState_withCovariance,
                                ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack);

#endif
