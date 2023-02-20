#ifndef FastJet_JetClustering_h
#define FastJet_JetClustering_h

#include <cmath>
#include <vector>

#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/JetDefinition.hh"
#include "fastjet/EECambridgePlugin.hh"
#include "fastjet/JadePlugin.hh"

#include "FastJet/ValenciaPlugin.h"

/** Jet clustering interface.
This represents a set functions and utilities to perfom jet clustering from a list of.
*/

namespace JetClustering {
  /** Structure to keep useful informations for the jets*/
  struct FCCAnalysesJet {
    std::vector<fastjet::PseudoJet> jets;
    std::vector<std::vector<int>> constituents;
    std::vector<float>
        exclusive_dmerge;  // vector of Nmax_dmerge  values associated with merging from n + 1 to n jets, for n =1, 2, ... 10
    std::vector<float> exclusive_dmerge_max;
  };

  /** @name JetClustering
   *  Jet clustering interface.
   This represents a set functions and utilities to perfom jet clustering from a list of.
  */
  ///@{

  ///Jet Clustering interface for kt

  struct clustering_kt {
  public:
    clustering_kt(float arg_radius = 0.5,
                  int arg_exclusive = 0,
                  float arg_cut = 5,
                  int arg_sorted = 0,
                  int arg_recombination = 0);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for _exclusive=0, dcut for _exclusive=1, N jets for _exlusive=2, N jets for _exclusive=3, ycut for _exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6
    fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for antikt
  struct clustering_antikt {
  public:
    clustering_antikt(float arg_radius = 0.5,
                      int arg_exclusive = 0,
                      float arg_cut = 5.,
                      int arg_sorted = 0,
                      int arg_recombination = 0);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6
    fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for Cambridge
  struct clustering_cambridge {
  public:
    clustering_cambridge(float arg_radius = 0.5,
                         int arg_exclusive = 0,
                         float arg_cut = 5.,
                         int arg_sorted = 0,
                         int arg_recombination = 0);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11,
    fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for ee_kt
  struct clustering_ee_kt {
  public:
    clustering_ee_kt(int arg_exclusive = 0, float arg_cut = 5., int arg_sorted = 0, int arg_recombination = 0);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for ee_genkt
  struct clustering_ee_genkt {
  public:
    clustering_ee_genkt(float arg_radius = 0.5,
                        int arg_exclusive = 0,
                        float arg_cut = 5.,
                        int arg_sorted = 0,
                        int arg_recombination = 0,
                        float arg_exponent = 0.);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float _exponent;     /// anti-kT algorithm=-1, cambridge algorithm=0, kT algorithm=1
    fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for genkt
  struct clustering_genkt {
  public:
    clustering_genkt(float arg_radius = 0.5,
                     int arg_exclusive = 0,
                     float arg_cut = 5.,
                     int arg_sorted = 0,
                     int arg_recombination = 0,
                     float arg_exponent = 0.);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float _exponent;     /// anti-kT algorithm=-1, cambridge algorithm=0, kT algorithm=1
    fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for valencia
  struct clustering_valencia {
  public:
    clustering_valencia(float arg_radius = 0.5,
                        int arg_exclusive = 0,
                        float arg_cut = 5.,
                        int arg_sorted = 0,
                        int arg_recombination = 0,
                        float arg_beta = 1.,
                        float arg_gamma = 1.);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float _beta;         /// beta parameter
    float _gamma;        /// gamma parameter
    //fastjet::JetAlgorithm _jetAlgorithm {fastjet::JetAlgorithm::undefined_jet_algorithm};///<internal jet algorithm
    fastjet::contrib::ValenciaPlugin* _jetAlgorithm;
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };

  ///Jet Clustering interface for jade
  struct clustering_jade {
  public:
    clustering_jade(float arg_radius = 0.5,
                    int arg_exclusive = 0,
                    float arg_cut = 5.,
                    int arg_sorted = 0,
                    int arg_recombination = 0);
    FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

  private:
    float _radius;   ///< jet cone radius
    int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
    float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int _sorted;         ///< pT ordering=0, E ordering=1
    int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    //fastjet::JetAlgorithm _jetAlgorithm {fastjet::JetAlgorithm::undefined_jet_algorithm};///<internal jet algorithm
    fastjet::JadePlugin* _jetAlgorithm;
    fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
    fastjet::ClusterSequence _cs;                ///<internal clustering sequence
    fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
  };
  ///@}

}  // namespace JetClustering

#endif
