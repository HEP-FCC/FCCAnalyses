#include "FCCAnalyses/VertexFitterActs.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/ReconstructedParticle2MC.h"

// ACTS
#include "Acts/EventData/TrackParameters.hpp"
#include "Acts/MagneticField/ConstantBField.hpp"
#include "Acts/Propagator/EigenStepper.hpp"
#include "Acts/Propagator/Propagator.hpp"
#include "Acts/Surfaces/PerigeeSurface.hpp"
#include "Acts/Vertexing/FullBilloirVertexFitter.hpp"
#include "Acts/Vertexing/HelicalTrackLinearizer.hpp"
#include "Acts/Vertexing/Vertex.hpp"

//V5.0
#include "Acts/Definitions/Algebra.hpp"
#include "Acts/Definitions/Units.hpp"


#include "TMath.h"

using namespace Acts::UnitLiterals;

namespace FCCAnalyses{

namespace VertexFitterActs{


VertexingUtils::FCCAnalysesVertex VertexFitterFullBilloir(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
									    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks ){


  using Propagator = Acts::Propagator<Acts::EigenStepper<>>;

  // retrieve the tracks associated to the recoparticles
  ROOT::VecOps::RVec<edm4hep::TrackState> tracks = ReconstructedParticle2Track::getRP2TRK( recoparticles, thetracks );


  // Create a test context
  //Acts::GeometryContext geoContext = Acts::GeometryContext();
  //Acts::MagneticFieldContext magFieldContext = Acts::MagneticFieldContext();
  const auto& geoContext = Acts::GeometryContext();
  const auto& magFieldContext = Acts::MagneticFieldContext();

  // Set up EigenStepper
  //Acts::ConstantBField bField(Acts::Vector3(0., 0., 2_T));
  //Acts::EigenStepper<Acts::ConstantBField> stepper(bField);
  auto bField = std::make_shared<Acts::ConstantBField>(Acts::Vector3(0., 0., 2_T));
  Acts::EigenStepper<> stepper(bField);

  // Set up the propagator
  //using Propagator = Acts::Propagator<Acts::EigenStepper<Acts::ConstantBField>>;
  auto propagator = std::make_shared<Propagator>(stepper);


  using Linearizer = Acts::HelicalTrackLinearizer;
  Linearizer::Config ltConfig(bField, propagator);
  Linearizer linearizer(ltConfig);

  // Set up Billoir Vertex Fitter
  using VertexFitter = Acts::FullBilloirVertexFitter;
  VertexFitter::Config vertexFitterCfg;
  VertexFitter billoirFitter(vertexFitterCfg);
  //VertexFitter::State state(magFieldContext);
  // TODO:
  //VertexFitter::State state(bField->makeCache(magFieldContext));

#if ACTS_VERSION_MAJOR < 29
  using CovMatrix4D = Acts::SymMatrix4;
#else
  using CovMatrix4D = Acts::SquareMatrix4;
#endif
  // Constraint for vertex fit
  Acts::Vertex myConstraint;
  // Some abitrary values
  CovMatrix4D myCovMat = CovMatrix4D::Zero();
  myCovMat(0, 0) = 30.;
  myCovMat(1, 1) = 30.;
  myCovMat(2, 2) = 30.;
  myCovMat(3, 3) = 30.;
  myConstraint.setFullCovariance(std::move(myCovMat));
  myConstraint.setFullPosition(Acts::Vector4(0, 0, 0, 0));


  Acts::VertexingOptions vfOptions(geoContext, magFieldContext);
  Acts::VertexingOptions vfOptionsConstr(geoContext, magFieldContext, myConstraint);


  int Ntr = tracks.size();
  //std::cout <<"ntr  : " << Ntr << std::endl;

  std::vector<Acts::BoundTrackParameters> allTracks;
  allTracks.reserve(Ntr);

  for (Int_t i = 0; i < Ntr; i++){

    //get the edm4hep track
    edm4hep::TrackState ti = tracks[i] ;

    //convert edm4hep track to FB track
    TVectorD trackFB  = VertexingUtils::get_trackParam(ti);
    TMatrixDSym covFB = VertexingUtils::get_trackCov(ti);

    //use FB tool to convert to ACTS track
    TVectorD trackACTS = VertexingUtils::ParToACTS(trackFB);
    TMatrixDSym covACTS = VertexingUtils::CovToACTS(covFB,trackFB);

    //Acts::BoundTrackParameters::ParametersVector newTrackParams;
    Acts::BoundVector newTrackParams;
    newTrackParams << trackACTS[0], trackACTS[1], trackACTS[2], trackACTS[3], trackACTS[4] ,trackACTS[5];

    for (int ii=0; ii<6; ii++){
      for (int jj=0; jj<6; jj++){
	covACTS(jj,ii) = double(covACTS(jj,ii));
      }
    }

    // Get track covariance vector
#if ACTS_VERSION_MAJOR < 29
    using Covariance = Acts::BoundSymMatrix;
#else
    using Covariance = Acts::BoundSquareMatrix;
#endif
    Covariance covMat;
    covMat <<
      covACTS(0,0), covACTS(1,0), covACTS(2,0), covACTS(3,0), covACTS(4,0), covACTS(5,0),
      covACTS(0,1), covACTS(1,1), covACTS(2,1), covACTS(3,1), covACTS(4,1), covACTS(5,1),
      covACTS(0,2), covACTS(1,2), covACTS(2,2), covACTS(3,2), covACTS(4,2), covACTS(5,2),
      covACTS(0,3), covACTS(1,3), covACTS(2,3), covACTS(3,3), covACTS(4,3), covACTS(5,3),
      covACTS(0,4), covACTS(1,4), covACTS(2,4), covACTS(3,4), covACTS(4,4), covACTS(5,4),
      covACTS(0,5), covACTS(1,5), covACTS(2,5), covACTS(3,5), covACTS(4,5), covACTS(5,5);

    // Create track parameters and add to track list
    Acts::Vector3 beamspotPos;
    beamspotPos << 0.0, 0.0, 0.0;
    auto perigeeSurface = Acts::Surface::makeShared<Acts::PerigeeSurface>(beamspotPos);

#if ACTS_VERSION_MAJOR < 30
    allTracks.emplace_back(perigeeSurface, newTrackParams, std::move(covMat));
#else
    allTracks.emplace_back(perigeeSurface, newTrackParams, std::move(covMat), Acts::ParticleHypothesis::pion());
#endif
  }


  //std::cout << "Number of tracks in event: " << tracks.size() << std::endl;
  //int count = 0;
  //for (const auto& trk : allTracks) {
  //  std::cout << count << ". track: " << std::endl;
  //  std::cout << "params: " << trk << std::endl;
  //  count++;
  // }

  std::vector<const Acts::BoundTrackParameters*> tracksPtr;
  for (const auto& trk : allTracks) {
    tracksPtr.push_back(&trk);
  }

  VertexingUtils::FCCAnalysesVertex TheVertex;
  edm4hep::VertexData edm4hep_vertex;
  ROOT::VecOps::RVec<float> reco_chi2;
  ROOT::VecOps::RVec< TVectorD >  updated_track_parameters;
  ROOT::VecOps::RVec<int> reco_ind;
  ROOT::VecOps::RVec<float> final_track_phases;
  ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex;

  TheVertex.vertex = edm4hep_vertex;
  TheVertex.reco_chi2 = reco_chi2;
  TheVertex.updated_track_parameters = updated_track_parameters;
  TheVertex.reco_ind = reco_ind;
  TheVertex.final_track_phases = final_track_phases;
  TheVertex.updated_track_momentum_at_vertex = updated_track_momentum_at_vertex;


  TheVertex.ntracks = Ntr;
  if ( Ntr <= 1) {
    return TheVertex;   // can not reconstruct a vertex with only one track...
  }

  // TODO:
  std::vector<Acts::InputTrack> newTracks;

  // TODO:
  auto ctx = Acts::MagneticFieldContext();
  auto cache = Acts::MagneticFieldProvider::Cache();

  Acts::Vertex fittedVertex =
    billoirFitter.fit(newTracks, vfOptions, cache).value();
  //Acts::Vertex<Acts::BoundTrackParameters> fittedVertexConstraint =
  //  billoirFitter.fit(tracksPtr, linearizer, vfOptionsConstr, state).value();


  //std::cout << "Fitting nTracks: " << Ntr << std::endl;
  //  std::cout << "Fitted Vertex: " << fittedVertex.position() << std::endl;
  //  std::cout << "Fitted constraint Vertex: "
  //             << fittedVertexConstraint.position() << std::endl;



  TheVertex.ntracks = Ntr;
  edm4hep_vertex.chi2 = fittedVertex.fitQuality().first/ fittedVertex.fitQuality().second ;
  //std::cout << "Fitted chi2: " << edm4hep_vertex.chi2 << std::endl;

  edm4hep_vertex.position = edm4hep::Vector3f( fittedVertex.position()[0],
					       fittedVertex.position()[1],
					       fittedVertex.position()[2]) ;  // store the  vertex in mm
    auto vtxCov = fittedVertex.covariance();
    std::array< float, 6 > edm4hep_vtxcov;

    edm4hep_vtxcov[0] = vtxCov(0,0);
    edm4hep_vtxcov[1] = vtxCov(1,0);
    edm4hep_vtxcov[2] = vtxCov(1,1);
    edm4hep_vtxcov[3] = vtxCov(2,0);
    edm4hep_vtxcov[4] = vtxCov(2,1);
    edm4hep_vtxcov[5] = vtxCov(2,2);

  edm4hep_vertex.algorithmType = 3;
  edm4hep_vertex.covMatrix = edm4hep_vtxcov;

  TheVertex.vertex = edm4hep_vertex;

  return TheVertex;
}

}//end NS VertexFitterActs

}//end NS FCCAnalyses
