#include "VertexingACTS.h"

// ACTS
#include "Acts/Propagator/EigenStepper.hpp"
#include "Acts/Propagator/Propagator.hpp"
#include "Acts/Utilities/AnnealingUtility.hpp"
#include "Acts/MagneticField/ConstantBField.hpp"
#include "Acts/Vertexing/ImpactPointEstimator.hpp"
#include "Acts/Vertexing/HelicalTrackLinearizer.hpp"


#include "Acts/Geometry/GeometryContext.hpp"
#include "Acts/Surfaces/PerigeeSurface.hpp"
#include "Acts/Utilities/Helpers.hpp"
#include "Acts/Vertexing/AdaptiveMultiVertexFinder.hpp"
#include "Acts/Vertexing/AdaptiveMultiVertexFitter.hpp"
#include "Acts/Vertexing/LinearizedTrack.hpp"
#include "Acts/Vertexing/TrackDensityVertexFinder.hpp"
#include "Acts/Vertexing/Vertex.hpp"
#include "Acts/Vertexing/VertexingOptions.hpp"

#include "Acts/Surfaces/PerigeeSurface.hpp"

#include "TMath.h"
using namespace VertexingACTS;

bool VertexingACTS::initialize(ROOT::VecOps::RVec<edm4hep::TrackState> tracks ){

  // Set up EigenStepper
  Acts::ConstantBField bField(2.);
  Acts::EigenStepper<Acts::ConstantBField> stepper(bField);

  // Set up the propagator
  using Propagator = Acts::Propagator<Acts::EigenStepper<Acts::ConstantBField>>;
  auto propagator = std::make_shared<Propagator>(stepper);

  // Set up ImpactPointEstimator
  using IPEstimator =
    Acts::ImpactPointEstimator<Acts::BoundTrackParameters, Propagator>;
  IPEstimator::Config ipEstimatorCfg(bField, propagator);
  IPEstimator ipEstimator(ipEstimatorCfg);

  // Set up the helical track linearizer
  using Linearizer = Acts::HelicalTrackLinearizer<Propagator>;
  Linearizer::Config ltConfig(bField, propagator);
  Linearizer linearizer(ltConfig);


  // Set up deterministic annealing with user-defined temperatures
  std::vector<double> temperatures{8.0, 4.0, 2.0, 1.4142136, 1.2247449, 1.0};
  Acts::AnnealingUtility::Config annealingConfig(temperatures);
  Acts::AnnealingUtility annealingUtility(annealingConfig);

  // Set up the vertex fitter with user-defined annealing
  using Fitter =
      Acts::AdaptiveMultiVertexFitter<Acts::BoundTrackParameters, Linearizer>;
  Fitter::Config fitterCfg(ipEstimator);
  fitterCfg.annealingTool = annealingUtility;
  Fitter fitter(fitterCfg);

  // Set up the vertex seed finder
  using SeedFinder = Acts::TrackDensityVertexFinder<
      Fitter, Acts::GaussianTrackDensity<Acts::BoundTrackParameters>>;
  SeedFinder seedFinder;

  // The vertex finder type
  using Finder = Acts::AdaptiveMultiVertexFinder<Fitter, SeedFinder>;

  Finder::Config finderConfig(std::move(fitter), seedFinder, ipEstimator,
                              linearizer);
  // We do not want to use a beamspot constraint here
  finderConfig.useBeamSpotConstraint = false;

  // Instantiate the finder
  Finder finder(finderConfig);
  // The vertex finder state
  Finder::State state;

  std::vector<const Acts::BoundTrackParameters*> Mytracks;

  int Ntr = tracks.size();
  Double_t b = -0.29988*2. / 2.;
  for (Int_t i = 0; i < Ntr; i++)
    {
      edm4hep::TrackState ti = tracks[i] ;
      
      double d0 = ti.D0 ;
      double phi0 = ti.phi ;
      double omega = ti.omega ;
      double z0 = ti.Z0 ;
      double theta = TMath::ATan2(1.0,ti.tanLambda) ;
      double qOverP = omega / (b*TMath::Sqrt(1 + ti.tanLambda*ti.tanLambda));	
      Acts::BoundVector newTrackParams;
      newTrackParams << d0, z0, phi0, theta, qOverP ,0.0;

      // Get track covariance vector
      std::vector<double> trkCovVec(36, 0.0); 
	//ti.covMatrix;
	
      trkCovVec.at(0)=0.001;
      trkCovVec.at(7)=0.001;
      trkCovVec.at(14)=0.001;
      trkCovVec.at(21)=0.001;
      trkCovVec.at(28)=0.001;

      // Construct track covariance
      Acts::BoundSymMatrix covMat =
	Eigen::Map<Acts::BoundSymMatrix>(trkCovVec.data());

      // Create track parameters and add to track list
      std::shared_ptr<Acts::PerigeeSurface> perigeeSurface =
	Acts::Surface::makeShared<Acts::PerigeeSurface>(Acts::Vector3D(0., 0., 0.));
      Mytracks.push_back(Acts::BoundTrackParameters(std::any, std::move(covMat),
						    newTrackParams, perigeeSurface));
    }
  
  const auto& inputTrackPointers = Mytracks;

  // Default vertexing options, this is where e.g. a constraint could be set
  using VertexingOptions = Acts::VertexingOptions<Acts::BoundTrackParameters>;
  //VertexingOptions finderOpts(ctx.geoContext, ctx.magFieldContext);
  VertexingOptions finderOpts(std::any, std::any);

  // find vertices
  auto result = finder.find(inputTrackPointers, finderOpts, state);
  if (not result.ok()) {
    std::cout << "Error in vertex finder: " << result.error().message() << std::endl;
    return false;
  }

  auto vertices = *result;

  // show some debug output
  std::cout << "Found " << vertices.size() << " vertices in event" << std::endl;
  for (const auto& vtx : vertices) {
    std::cout << "Found vertex at " << vtx.fullPosition().transpose() << " with "
	      << vtx.tracks().size() << " tracks." << std::endl;
  }


  return true;
}
