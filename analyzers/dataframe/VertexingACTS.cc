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
using namespace Acts::UnitLiterals;

//bool VertexingACTS::initialize(ROOT::VecOps::RVec<edm4hep::TrackState> tracks ){
bool VertexingACTS::initialize(std::vector<edm4hep::TrackState> tracks ){
  using Covariance = Acts::BoundSymMatrix;

  std::cout << "in initialize" << std::endl;

  std::any myContext;

  // Create a test context
  Acts::GeometryContext geoContext = Acts::GeometryContext();
  Acts::MagneticFieldContext magFieldContext = Acts::MagneticFieldContext();
  std::cout << "in initialize 2" << std::endl;

  // Set up EigenStepper
  Acts::ConstantBField bField(Acts::Vector3D(0., 0., 2_T));
  Acts::EigenStepper<Acts::ConstantBField> stepper(bField);
  std::cout << "in initialize 3" << std::endl;

  // Set up the propagator
  using Propagator = Acts::Propagator<Acts::EigenStepper<Acts::ConstantBField>>;
  auto propagator = std::make_shared<Propagator>(stepper);
  std::cout << "in initialize 4" << std::endl;

  // Set up ImpactPointEstimator
  using IPEstimator = Acts::ImpactPointEstimator<Acts::BoundTrackParameters, Propagator>;
  IPEstimator::Config ipEstimatorCfg(bField, propagator);
  IPEstimator ipEstimator(ipEstimatorCfg);
  std::cout << "in initialize 5" << std::endl;

  // Set up the helical track linearizer
  using Linearizer = Acts::HelicalTrackLinearizer<Propagator>;
  Linearizer::Config ltConfig(bField, propagator);
  Linearizer linearizer(ltConfig);

  std::cout << "in initialize 6" << std::endl;

  // Set up deterministic annealing with user-defined temperatures
  std::vector<double> temperatures{8.0, 4.0, 2.0, 1.4142136, 1.2247449, 1.0};
  Acts::AnnealingUtility::Config annealingConfig(temperatures);
  Acts::AnnealingUtility annealingUtility(annealingConfig);

  std::cout << "in initialize 7" << std::endl;

  // Set up the vertex fitter with user-defined annealing
  using Fitter = Acts::AdaptiveMultiVertexFitter<Acts::BoundTrackParameters, Linearizer>;
  Fitter::Config fitterCfg(ipEstimator);
  fitterCfg.annealingTool = annealingUtility;
  Fitter fitter(fitterCfg);
  std::cout << "in initialize 8" << std::endl;

  // Set up the vertex seed finder
  using SeedFinder = Acts::TrackDensityVertexFinder<Fitter, 
						    Acts::GaussianTrackDensity<Acts::BoundTrackParameters>>;
  SeedFinder seedFinder;
  std::cout << "in initialize 9" << std::endl;

  // The vertex finder type
  using Finder = Acts::AdaptiveMultiVertexFinder<Fitter, SeedFinder>;

  Finder::Config finderConfig(std::move(fitter), seedFinder, ipEstimator,
                              linearizer);
  // We do not want to use a beamspot constraint here
  finderConfig.useBeamSpotConstraint = false;
  std::cout << "in initialize 10" << std::endl;

  // Instantiate the finder
  Finder finder(finderConfig);
  // The vertex finder state
  Finder::State state;
  std::cout << "in initialize 11" << std::endl;

  


  //std::vector<const Acts::BoundTrackParameters*> Mytracks;
  std::vector<Acts::BoundTrackParameters> allTracks;
  int Ntr = tracks.size();
  std::cout <<"ntr  : " << Ntr << std::endl;
  Double_t b = -0.29988*2. / 2.;
  for (Int_t i = 0; i < Ntr; i++)
    {
      edm4hep::TrackState ti = tracks[i] ;
      std::cout << "in initialize 11.0 track : "<<i << std::endl;

      double d0 = ti.D0 ;
      double phi0 = ti.phi ;
      double omega = ti.omega ;
      double z0 = ti.Z0 ;
      double theta = TMath::ATan2(1.0,ti.tanLambda) ;
      double qOverP = omega / (b*TMath::Sqrt(1 + ti.tanLambda*ti.tanLambda));	
      Acts::BoundTrackParameters::ParametersVector newTrackParams;
      newTrackParams << d0, z0, phi0, theta, qOverP ,0.0;
      std::cout << "in initialize 11.2" << std::endl;

      // Get track covariance vector
      Covariance covMat;

      covMat << 0.001, 0., 0., 0., 0., 0., 0., 0.001, 0., 0., 0.,
        0., 0., 0., 0.001, 0., 0., 0., 0., 0., 0., 0.001, 0.,
        0., 0., 0., 0., 0., 0.001, 0., 0., 0., 0., 0., 0., 1.;
      
      std::cout << "in initialize 11.3" << std::endl;

      // Create track parameters and add to track list
      Acts::Vector3D beamspotPos;
      std::cout << "in initialize 11.4" << std::endl;
      beamspotPos << 0.0, 0.0,0.0;
      std::cout << "in initialize 11.5" << std::endl;
      std::shared_ptr<Acts::PerigeeSurface> perigeeSurface;
      std::cout << "in initialize 11.5.1" << std::endl;
      perigeeSurface = Acts::Surface::makeShared<Acts::PerigeeSurface>(beamspotPos);
      std::cout << "in initialize 11.6" << std::endl;
      allTracks.emplace_back(perigeeSurface, newTrackParams, std::move(covMat));
      std::cout << "in initialize 11.7" << std::endl;

      //Mytracks.push_back(Acts::BoundTrackParameters(myContext, std::move(covMat),
      //					    newTrackParams, perigeeSurface));
    }
  
  std::cout << "in initialize 12" << std::endl;

  std::vector<const Acts::BoundTrackParameters*> tracksPtr;
  for (const auto& trk : allTracks) {
    tracksPtr.push_back(&trk);
  }
  std::cout << "in initialize 13" << std::endl;

  // Default vertexing options, this is where e.g. a constraint could be set

  Acts::VertexingOptions<Acts::BoundTrackParameters> vertexingOptions(geoContext,
								      magFieldContext);
  //  vertexingOptions.vertexConstraint = std::get<BeamSpotData>(csvData);
   std::cout << "in initialize 14" << std::endl;

  // find vertices
  auto result = finder.find(tracksPtr, vertexingOptions, state);

  std::cout << "result  " << result.ok() << std::endl;
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
