#include "FCCAnalyses/VertexFinderActs.h"

#include <iostream>

// ACTS
#include "Acts/MagneticField/ConstantBField.hpp"
#include "Acts/Propagator/EigenStepper.hpp"
#include "Acts/Propagator/Propagator.hpp"
#include "Acts/Utilities/AnnealingUtility.hpp"
#include "Acts/Vertexing/ImpactPointEstimator.hpp"
#include "Acts/Vertexing/HelicalTrackLinearizer.hpp"
//V5.0
#include "Acts/Definitions/Algebra.hpp"
#include "Acts/Definitions/Units.hpp"

#include "Acts/Geometry/GeometryContext.hpp"
#include "Acts/Surfaces/PerigeeSurface.hpp"
#include "Acts/Utilities/Helpers.hpp"
#include "Acts/Vertexing/AdaptiveMultiVertexFinder.hpp"
#include "Acts/Vertexing/AdaptiveMultiVertexFitter.hpp"
#include "Acts/Vertexing/LinearizedTrack.hpp"
#include "Acts/Vertexing/TrackDensityVertexFinder.hpp"
#include "Acts/Vertexing/Vertex.hpp"
#include "Acts/Vertexing/VertexingOptions.hpp"
#include "Acts/Vertexing/TrackAtVertex.hpp"

#include "Acts/Surfaces/PerigeeSurface.hpp"
#include "Acts/Utilities/Logger.hpp"

#include "TMath.h"

using namespace Acts::UnitLiterals;

namespace FCCAnalyses{

namespace VertexFinderActs{

ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>
VertexFinderAMVF(ROOT::VecOps::RVec<edm4hep::TrackState> tracks ){

  using Propagator = Acts::Propagator<Acts::EigenStepper<>>;

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

  // Set up ImpactPointEstimator
  using IPEstimator = Acts::ImpactPointEstimator<Acts::BoundTrackParameters, Propagator>;
  IPEstimator::Config ipEstimatorCfg(bField, propagator);
  IPEstimator ipEstimator(ipEstimatorCfg);

  // Set up the helical track linearizer
  using Linearizer = Acts::HelicalTrackLinearizer<Propagator>;
  Linearizer::Config ltConfig(bField, propagator);
  Linearizer linearizer(ltConfig);

  // Set up deterministic annealing with user-defined temperatures
  std::vector<double> temperatures{8.0, 4.0, 2.0, 1.4142136, 1.2247449, 1.0};
  Acts::AnnealingUtility::Config annealingConfig;
  annealingConfig.setOfTemperatures = temperatures;
  Acts::AnnealingUtility annealingUtility(annealingConfig);


  // Set up the vertex fitter with user-defined annealing
  using Fitter = Acts::AdaptiveMultiVertexFitter<Acts::BoundTrackParameters, Linearizer>;
  Fitter::Config fitterCfg(ipEstimator);
  fitterCfg.annealingTool = annealingUtility;
  Fitter fitter(fitterCfg);//, Acts::getDefaultLogger("Fitter", Acts::Logging::VERBOSE));

  // Set up the vertex seed finder
  using SeedFinder = Acts::TrackDensityVertexFinder<Fitter, Acts::GaussianTrackDensity<Acts::BoundTrackParameters>>;
  SeedFinder seedFinder;


  /*
  // Set up Gaussian track density
  Acts::GaussianTrackDensity::Config trackDensityConfig;
  trackDensityConfig.d0MaxSignificance = 10.;
  trackDensityConfig.z0MaxSignificance = 20.;
  Acts::GaussianTrackDensity trackDensity(trackDensityConfig);


  // Vertex seed finder
  Acts::VertexSeedFinder::Config seedFinderConfig;
  seedFinderConfig.trackDensityEstimator = trackDensity;
  VertexSeedFinder seedFinder(seedFinderConfig, Acts::getDefaultLogger("SeedFinder", Acts::Logging::VERBOSE));
  */

  // The vertex finder type
  using Finder = Acts::AdaptiveMultiVertexFinder<Fitter, SeedFinder>;
  //using Finder = Acts::AdaptiveMultiVertexFinder<Fitter, VertexSeedFinder>;
  //Finder::Config finderConfig(std::move(fitter), seedFinder, ipEstimator, linearizer);
  Finder::Config finderConfig = {std::move(fitter), seedFinder, ipEstimator,
                                 std::move(linearizer), bField};

  // We do not want to use a beamspot constraint here
  finderConfig.useBeamSpotConstraint = false;
  //finderConfig.useSeedConstraint = false;
  //finderConfig.tracksMaxSignificance = 100.;//5.;
  //finderConfig.maxVertexChi2 = 500.;//18.42;
  //finderConfig.tracksMaxZinterval = 300.;//3.;
  //finderConfig.maxIterations = 10000;//100;
  // Instantiate the finder

  Finder finder(finderConfig);//, Acts::getDefaultLogger("Finder", Acts::Logging::VERBOSE));
  // The vertex finder state
  Finder::State state;

  // Default vertexing options, this is where e.g. a constraint could be set
  using VertexingOptions = Acts::VertexingOptions<Acts::BoundTrackParameters>;
  //VertexingOptions finderOpts(myContext, myContext);
  VertexingOptions finderOpts(geoContext, magFieldContext);
  //  vertexingOptions.vertexConstraint = std::get<BeamSpotData>(csvData);

  int Ntr = tracks.size();

  //std::vector<const Acts::BoundTrackParameters*> Mytracks;
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
    using Covariance = Acts::BoundSymMatrix;
    Covariance covMat;
    covMat <<
      covACTS(0,0), covACTS(1,0), covACTS(2,0), covACTS(3,0), covACTS(4,0), covACTS(5,0),
      covACTS(0,1), covACTS(1,1), covACTS(2,1), covACTS(3,1), covACTS(4,1), covACTS(5,1),
      covACTS(0,2), covACTS(1,2), covACTS(2,2), covACTS(3,2), covACTS(4,2), covACTS(5,2),
      covACTS(0,3), covACTS(1,3), covACTS(2,3), covACTS(3,3), covACTS(4,3), covACTS(5,3),
      covACTS(0,4), covACTS(1,4), covACTS(2,4), covACTS(3,4), covACTS(4,4), covACTS(5,4),
      covACTS(0,5), covACTS(1,5), covACTS(2,5), covACTS(3,5), covACTS(4,5), covACTS(5,5);

    // Create track parameters and add to track list
    std::shared_ptr<Acts::PerigeeSurface> perigeeSurface;
    Acts::Vector3 beamspotPos;
    beamspotPos << 0.0, 0.0, 0.0;
    perigeeSurface = Acts::Surface::makeShared<Acts::PerigeeSurface>(beamspotPos);

    allTracks.emplace_back(perigeeSurface, newTrackParams, std::move(covMat));

    //std::cout << "params: " << allTracks[i] << std::endl;
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


  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> TheVertexColl;

  if ( Ntr <= 1)
    return TheVertexColl;   // can not reconstruct a vertex with only one track...return an empty collection

  // find vertices
  auto result = finder.find(tracksPtr, finderOpts, state);

  //std::cout << "result  " << result.ok() << std::endl;
  if (not result.ok()) {
    std::cout << "Error in vertex finder: " << result.error().message() << std::endl;
    return TheVertexColl;   // return an empty collection, as results of fitting is not ok
  }

  auto vertices = *result;

  // show some debug output
  //std::cout << "Found " << vertices.size() << " vertices in event" << std::endl;
  //if (vertices.size()==1){
  //const auto& vtx = vertices.at(0);

  for (const auto& vtx : vertices) {

    VertexingUtils::FCCAnalysesVertex TheVertex;
    edm4hep::VertexData edm4hep_vertex;
    ROOT::VecOps::RVec<float> reco_chi2;
    ROOT::VecOps::RVec< TVectorD >  updated_track_parameters;
    ROOT::VecOps::RVec<int> reco_ind;
    ROOT::VecOps::RVec<float> final_track_phases;
    ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex;

    //std::cout << "Found vertex at " << vtx.fullPosition().transpose() << " with "
    //	      << vtx.tracks().size() << " tracks." << std::endl;

    TheVertex.ntracks = vtx.tracks().size();
    edm4hep_vertex.primary = 1;
    edm4hep_vertex.chi2 = vtx.fitQuality().first/ vtx.fitQuality().second ;
    edm4hep_vertex.position = edm4hep::Vector3f( vtx.position()[0],vtx.position()[1], vtx.position()[2]) ;  // store the  vertex in mm
    auto vtxCov = vtx.covariance();
    std::array< float, 6 > edm4hep_vtxcov;

    edm4hep_vtxcov[0] = vtxCov(0,0);
    edm4hep_vtxcov[1] = vtxCov(1,0);
    edm4hep_vtxcov[2] = vtxCov(1,1);
    edm4hep_vtxcov[3] = vtxCov(2,0);
    edm4hep_vtxcov[4] = vtxCov(2,1);
    edm4hep_vtxcov[5] = vtxCov(2,2);

    //edm4hep_vertex.covMatrix = fullCovariance();
    edm4hep_vertex.algorithmType = 2;
    edm4hep_vertex.covMatrix = edm4hep_vtxcov;

    std::vector<Acts::TrackAtVertex<Acts::BoundTrackParameters>> tracksAtVertex = vtx.tracks();

    for (const auto& trk : tracksAtVertex) {

      reco_chi2.push_back(trk.chi2Track);
      double ndf = trk.ndf;

      const Acts::BoundTrackParameters* originalParams = trk.originalParams;
      for (size_t trkind=0;trkind<tracksPtr.size();trkind++)
	if (originalParams == tracksPtr.at(trkind))reco_ind.push_back(trkind);
    }
    TheVertex.vertex = edm4hep_vertex;
    TheVertex.reco_ind = reco_ind;
    TheVertexColl.push_back(TheVertex);
  }

  if (vertices.size()>0){
    std::cout << "Found more than 0 Primary Vertex " << vertices.size() << std::endl;
    for (const auto& vtx : vertices) {
      std::cout << "Found vertex at " << vtx.fullPosition().transpose() << " with "
		<< vtx.tracks().size() << " tracks." << std::endl;
    }
  }


  return TheVertexColl;
}

}//end NS VertexFinderActs

}//end NS FCCAnalyses
