
#ifndef  JETCLUSTERINGUTILS_ANALYZERS_H
#define  JETCLUSTERINGUTILS_ANALYZERS_H

#include <vector>
#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "fastjet/JetDefinition.hh"
#include "TRandom3.h"

/** Jet clustering utilities interface.
This represents a set functions and utilities to perfom jet clustering from a list of.
*/
namespace FCCAnalyses{

namespace JetClusteringUtils{

  /** @name JetClusteringUtils
   *  Jet clustering interface utilities.
  */
  ///@{

  const int Nmax_dmerge = 10;  // maximum number of d_{n, n+1} that are kept in FCCAnalysesJet

  /** Structure to keep useful informations for the jets*/
  struct FCCAnalysesJet{
    ROOT::VecOps::RVec<fastjet::PseudoJet> jets;
    std::vector<std::vector<int>> constituents;
    std::vector<float> exclusive_dmerge;   // vector of Nmax_dmerge  values associated with merging from n + 1 to n jets, for n =1, 2, ... 10
    std::vector<float> exclusive_dmerge_max ;
  };

  /** Set fastjet pseudoJet for later reconstruction*/
  std::vector<fastjet::PseudoJet> set_pseudoJets(const ROOT::VecOps::RVec<float> &px,
                                                 const ROOT::VecOps::RVec<float> &py,
                                                 const ROOT::VecOps::RVec<float> &pz,
                                                 const ROOT::VecOps::RVec<float> &e);

  /** Set fastjet pseudoJet for later reconstruction using px, py, pz and m
   *
   * This version is to be preferred over the px,py,pz,E version when m is known
   * accurately, because it uses double precision to reconstruct the energy,
   * reducing the size of rounding errors on FastJet calculations (e.g. of
   * PseudoJet masses)
   *
  */
  std::vector<fastjet::PseudoJet> set_pseudoJets_xyzm(const ROOT::VecOps::RVec<float> &px,
                                                      const ROOT::VecOps::RVec<float> &py,
                                                      const ROOT::VecOps::RVec<float> &pz,
                                                      const ROOT::VecOps::RVec<float> &m);

  /** Get fastjet pseudoJet after reconstruction from FCCAnalyses jets*/
  ROOT::VecOps::RVec<fastjet::PseudoJet> get_pseudoJets(const FCCAnalysesJet &in);

  /** Get fastjet constituents after reconstruction from FCCAnalyses jets*/
  std::vector<std::vector<int>> get_constituents(const FCCAnalysesJet &in);


  /// return the dmin corresponding to the recombination that went from n+1 to n jets
  float get_exclusive_dmerge(const FCCAnalysesJet &in, int n);

  float get_exclusive_dmerge_max(const FCCAnalysesJet &in, int n);

  /** Get jet px. Details. */
  ROOT::VecOps::RVec<float> get_px(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet py. Details. */
  ROOT::VecOps::RVec<float> get_py(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet pz. Details. */
  ROOT::VecOps::RVec<float> get_pz(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet energy. Details. */
  ROOT::VecOps::RVec<float> get_e(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet pt. Details. */
  ROOT::VecOps::RVec<float> get_pt(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet p. Details. */
  ROOT::VecOps::RVec<float> get_p(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet mass. Details. */
  ROOT::VecOps::RVec<float> get_m(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet eta. Details. */
  ROOT::VecOps::RVec<float> get_eta(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet phi. Details. */
  ROOT::VecOps::RVec<float> get_phi(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);

  /** Get jet theta. Details. */
  ROOT::VecOps::RVec<float> get_theta(const ROOT::VecOps::RVec<fastjet::PseudoJet> &in);


  ///Internal methods
  FCCAnalysesJet initialise_FCCAnalysesJet();

  FCCAnalysesJet build_FCCAnalysesJet(const std::vector<fastjet::PseudoJet> &in,
                                      const std::vector<float> &dmerge,
                                      const std::vector<float> &dmerge_max);

  std::vector<fastjet::PseudoJet> build_jets(fastjet::ClusterSequence & cs,
                                             int exclusive, float cut,
                                             int sorted);

  bool check(unsigned int n,
             int exclusive,
             float cut);

  fastjet::RecombinationScheme recomb_scheme(int recombination);

  std::vector<float> exclusive_dmerge(fastjet::ClusterSequence & cs,
                                      int do_dmarge_max)  ;


  ///@}

}//end NS JetClusteringUtils

}//end NS FCCAnalyses

#endif
