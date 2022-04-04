#ifndef analyzers_dataframe_JetConstituentsUtils_h
#define analyzers_dataframe_JetConstituentsUtils_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace JetConstituentsUtils {
  using FCCAnalysesJetConstituents = ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>;
  //using FCCAnalysesJetConstituentsData = ROOT::VecOps::RVec<float>;
  using FCCAnalysesJetConstituentsData = std::vector<float>;

  ROOT::VecOps::RVec<FCCAnalysesJetConstituents> build_constituents(
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>);

  FCCAnalysesJetConstituents get_jet_constituents(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>, int);
  ROOT::VecOps::RVec<FCCAnalysesJetConstituents> get_constituents(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>,
                                                                  ROOT::VecOps::RVec<int>);

  /*ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_pt(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_e(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_theta(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_phi(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_type(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  ROOT::VecOps::RVec<FCCAnalysesJetConstituentsData> get_charge(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);*/
  std::vector<FCCAnalysesJetConstituentsData> get_pt(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  std::vector<FCCAnalysesJetConstituentsData> get_e(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  std::vector<FCCAnalysesJetConstituentsData> get_theta(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  std::vector<FCCAnalysesJetConstituentsData> get_phi(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  std::vector<FCCAnalysesJetConstituentsData> get_type(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
  std::vector<FCCAnalysesJetConstituentsData> get_charge(ROOT::VecOps::RVec<FCCAnalysesJetConstituents>);
}  // namespace JetConstituentsUtils

#endif
