#ifndef FCCAnalyses_JetConstituentsUtils_h
#define FCCAnalyses_JetConstituentsUtils_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace FCCAnalyses {
  namespace JetConstituentsUtils {
    namespace rv = ROOT::VecOps;
    using FCCAnalysesJetConstituents = rv::RVec<edm4hep::ReconstructedParticleData>;
    using FCCAnalysesJetConstituentsData = rv::RVec<float>;

    /// Build the collection of constituents (mapping jet -> reconstructed particles) for all jets in event
    rv::RVec<FCCAnalysesJetConstituents> build_constituents(rv::RVec<edm4hep::ReconstructedParticleData>,
                                                            rv::RVec<edm4hep::ReconstructedParticleData>);

    /// Retrieve the constituents of an indexed jet in event
    FCCAnalysesJetConstituents get_jet_constituents(rv::RVec<FCCAnalysesJetConstituents>, int);
    /// Retrieve the constituents of a collection of indexed jets in event
    rv::RVec<FCCAnalysesJetConstituents> get_constituents(rv::RVec<FCCAnalysesJetConstituents>, rv::RVec<int>);

    rv::RVec<FCCAnalysesJetConstituentsData> get_pt(rv::RVec<FCCAnalysesJetConstituents>);
    rv::RVec<FCCAnalysesJetConstituentsData> get_e(rv::RVec<FCCAnalysesJetConstituents>);
    rv::RVec<FCCAnalysesJetConstituentsData> get_theta(rv::RVec<FCCAnalysesJetConstituents>);
    rv::RVec<FCCAnalysesJetConstituentsData> get_phi(rv::RVec<FCCAnalysesJetConstituents>);
    rv::RVec<FCCAnalysesJetConstituentsData> get_type(rv::RVec<FCCAnalysesJetConstituents>);
    rv::RVec<FCCAnalysesJetConstituentsData> get_charge(rv::RVec<FCCAnalysesJetConstituents>);
  }  // namespace JetConstituentsUtils
}  // namespace FCCAnalyses

#endif
