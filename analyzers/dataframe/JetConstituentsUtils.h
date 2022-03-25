#ifndef analyzers_dataframe_JetConstituentsUtils_h
#define analyzers_dataframe_JetConstituentsUtils_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace JetConstituentsUtils {
  using FCCAnalysesJetConstituents = ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>;

  ROOT::VecOps::RVec<FCCAnalysesJetConstituents> build_constituents(
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>);

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > get_constituents(
      ROOT::VecOps::RVec<FCCAnalysesJetConstituents>, ROOT::VecOps::RVec<int>);

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_pt(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_e(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_theta(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_phi(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_pid(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > get_charge(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
}  // namespace JetConstituentsUtils

#endif
