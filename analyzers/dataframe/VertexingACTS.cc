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
#include "Acts/Utilities/Logger.hpp"

#include "TMath.h"

#include "Vertexing.h"

using namespace VertexingACTS;
using namespace Acts::UnitLiterals;

TVectorD VertexingACTS::ParToACTS(TVectorD Par){

  TVectorD pACTS(6);	// Return vector
  //
  double fB=2.;
  Double_t b = -0.29988*fB / 2.;
  pACTS(0) = 1000*Par(0);		// D from m to mm
  pACTS(1) = 1000 * Par(3);	// z0 from m to mm
  pACTS(2) = Par(1);			// Phi0 is unchanged
  pACTS(3) = TMath::ATan2(1.0,Par(4));		// Theta in [0, pi] range
  pACTS(4) = Par(2) / (b*TMath::Sqrt(1 + Par(4)*Par(4)));		// q/p in GeV
  pACTS(5) = 0.0;				// Time: currently undefined
  //
  return pACTS;
}


// Covariance conversion to ACTS format
TMatrixDSym VertexingACTS::CovToACTS(TMatrixDSym Cov, TVectorD Par){
  
  double fB=2.;
  TMatrixDSym cACTS(6); cACTS.Zero();
  Double_t b = -0.29988*fB / 2.;
  //
  // Fill derivative matrix
  TMatrixD A(5, 5);	A.Zero();
  Double_t ct = Par(4);	// cot(theta)
  Double_t C = Par(2);		// half curvature
  A(0, 0) = 1000.;		// D-D	conversion to mm
  A(1, 2) = 1.0;		// phi0-phi0
  A(2, 4) = 1.0/(TMath::Sqrt(1.0 + ct*ct) * b);	// q/p-C
  A(3, 1) = 1000.;		// z0-z0 conversion to mm
  A(4, 3) = -1.0 / (1.0 + ct*ct); // theta - cot(theta)
  A(4, 4) = -C*ct / (b*pow(1.0 + ct*ct,3.0/2.0)); // q/p-cot(theta)
  //
  TMatrixDSym Cv = Cov;
  TMatrixD At(5, 5);
  At.Transpose(A);
  Cv.Similarity(At);
  TMatrixDSub(cACTS, 0, 4, 0, 4) = Cv;
  cACTS(5, 5) = 0.1;	// Currently undefined: set to arbitrary value to avoid crashes
  //
  return cACTS;
}

bool VertexingACTS::VertexFinder(ROOT::VecOps::RVec<edm4hep::TrackState> tracks ){
  
  using Covariance = Acts::BoundSymMatrix;
  Acts::Logging::Level loggingLevel = Acts::Logging::Level::DEBUG;
  std::any myContext;

  // Create a test context
  Acts::GeometryContext geoContext = Acts::GeometryContext();
  Acts::MagneticFieldContext magFieldContext = Acts::MagneticFieldContext();

  // Set up EigenStepper
  Acts::ConstantBField bField(Acts::Vector3D(0., 0., 2_T));
  Acts::EigenStepper<Acts::ConstantBField> stepper(bField);

  // Set up the propagator
  using Propagator = Acts::Propagator<Acts::EigenStepper<Acts::ConstantBField>>;
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
  Acts::AnnealingUtility::Config annealingConfig(temperatures);
  Acts::AnnealingUtility annealingUtility(annealingConfig);


  // Set up the vertex fitter with user-defined annealing
  using Fitter = Acts::AdaptiveMultiVertexFitter<Acts::BoundTrackParameters, Linearizer>;
  Fitter::Config fitterCfg(ipEstimator);
  fitterCfg.annealingTool = annealingUtility;
  Fitter fitter(fitterCfg);

  // Set up the vertex seed finder
  using SeedFinder = Acts::TrackDensityVertexFinder<Fitter, Acts::GaussianTrackDensity<Acts::BoundTrackParameters>>;
  SeedFinder seedFinder;

  // The vertex finder type
  using Finder = Acts::AdaptiveMultiVertexFinder<Fitter, SeedFinder>;

  Finder::Config finderConfig(std::move(fitter), seedFinder, ipEstimator, linearizer);
  // We do not want to use a beamspot constraint here
  finderConfig.useBeamSpotConstraint = false;

  // Instantiate the finder
  Finder finder(finderConfig);
  // The vertex finder state
  Finder::State state;

  // Default vertexing options, this is where e.g. a constraint could be set
  using VertexingOptions = Acts::VertexingOptions<Acts::BoundTrackParameters>;
  VertexingOptions finderOpts(geoContext, magFieldContext);
  //  vertexingOptions.vertexConstraint = std::get<BeamSpotData>(csvData);


  //std::vector<const Acts::BoundTrackParameters*> Mytracks;
  std::vector<Acts::BoundTrackParameters> allTracks;
  int Ntr = tracks.size();
  std::cout <<"ntr  : " << Ntr << std::endl;

  for (Int_t i = 0; i < Ntr; i++)
    {
      edm4hep::TrackState ti = tracks[i] ;

      TVectorD trackFB  = Vertexing::get_trackParam(ti);
      TMatrixDSym covFB = Vertexing::get_trackCov(ti);

      TVectorD trackACTS = ParToACTS(trackFB);
      TMatrixDSym covACTS = CovToACTS(covFB,trackFB);

      Acts::BoundTrackParameters::ParametersVector newTrackParams;
      //newTrackParams << d0, z0, phi0, theta, qOverP ,0.0;
      newTrackParams << trackACTS[0], trackACTS[1], trackACTS[2], trackACTS[3], trackACTS[4] ,trackACTS[5];

      std::cout << "track " << i << "  d0  " << trackACTS[0] << "  z0  " << trackACTS[1] << "  phi0  " << trackACTS[2] << "  theta  " << trackACTS[3] << "  qOverP  " << trackACTS[4] << "  P  " << 1./trackACTS[4] << std::endl;


      // Get track covariance vector
      Covariance covMat;
      covMat << 
	covACTS(0,0), covACTS(1,0), covACTS(2,0), covACTS(3,0), covACTS(4,0), covACTS(5,0), 
	covACTS(0,1), covACTS(1,1), covACTS(2,1), covACTS(3,1), covACTS(4,1), covACTS(5,1), 
	covACTS(0,2), covACTS(1,2), covACTS(2,2), covACTS(3,2), covACTS(4,2), covACTS(5,2), 
	covACTS(0,3), covACTS(1,3), covACTS(2,3), covACTS(3,3), covACTS(4,3), covACTS(5,3), 
	covACTS(0,4), covACTS(1,4), covACTS(2,4), covACTS(3,4), covACTS(4,4), covACTS(5,4), 
	covACTS(0,5), covACTS(1,5), covACTS(2,5), covACTS(3,5), covACTS(4,5), covACTS(5,5);

      std::shared_ptr<Acts::PerigeeSurface> perigeeSurface;
      // Create track parameters and add to track list
      Acts::Vector3D beamspotPos;
      beamspotPos << 0.0, 0.0, 0.0;
      perigeeSurface = Acts::Surface::makeShared<Acts::PerigeeSurface>(beamspotPos);
      allTracks.emplace_back(perigeeSurface, newTrackParams, std::move(covMat));
    }
  

  std::vector<const Acts::BoundTrackParameters*> tracksPtr;
  for (const auto& trk : allTracks) {
    tracksPtr.push_back(&trk);
  }

  std::cout << " --- n trk " << tracksPtr.size() << std::endl;
 
  // find vertices
  auto result = finder.find(tracksPtr, finderOpts, state);

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
