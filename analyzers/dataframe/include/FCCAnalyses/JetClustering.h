
#ifndef  JETCLUSTERING_ANALYZERS_H
#define  JETCLUSTERING_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"


#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/JetDefinition.hh"

#include "JetClusteringUtils.h"

/** Jet clustering interface. 
This represents a set functions and utilities to perfom jet clustering from a list of.  
*/

namespace JetClustering{

  /** @name JetClustering
   *  Jet clustering interface. 
   This represents a set functions and utilities to perfom jet clustering from a list of. 
  */
  ///@{
  
  ///Jet Clustering interface for kt
  struct clustering_kt {
    clustering_kt (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };
  

  ///Jet Clustering interface for antikt
  struct clustering_antikt {
    clustering_antikt (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };
  

  ///Jet Clustering interface for Cambridge
  struct clustering_cambridge {
    clustering_cambridge (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11, 
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };

  ///Jet Clustering interface for ee_kt
  struct clustering_ee_kt {
    clustering_ee_kt (int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination);
    
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };


  ///Jet Clustering interface for ee_genkt
  struct clustering_ee_genkt {
    clustering_ee_genkt (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float m_exponent = 0; /// anti-kT algorithm=-1, cambridge algorithm=0, kT algorithm=1
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };


  ///Jet Clustering interface for genkt
  struct clustering_genkt {
    clustering_genkt (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float m_exponent = 0; /// anti-kT algorithm=-1, cambridge algorithm=0, kT algorithm=1
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };


  ///Jet Clustering interface for valencia
  struct clustering_valencia {
    clustering_valencia (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_beta, float arg_gamma);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    float m_beta = 1.; /// beta parameter
    float m_gamma = 1.; /// gamma parameter
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };
  
  ///Jet Clustering interface for jade
  struct clustering_jade {
    clustering_jade (float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination);
    
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    int m_sorted = 0; ///< pT ordering=0, E ordering=1
    int m_recombination = 0; ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
    JetClusteringUtils::FCCAnalysesJet  operator() (std::vector<fastjet::PseudoJet>);
  };
  ///@}
}


#endif
