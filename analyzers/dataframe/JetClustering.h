
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


/** Jet clustering interface. 
This represents a set functions and utilities to perfom jet clustering from a list of.  
*/

namespace JetClustering{

  /** @name JetClustering
   *  Jet clustering interface. 
   This represents a set functions and utilities to perfom jet clustering from a list of. 
  */
  ///@{
  
  ///Jet Clustering interface
  struct clustering {
    clustering (int arg_jetalgo, float arg_radius, int arg_exclusive, float arg_cut);
    
    int m_jetalgo = 1; ///< jet algorithm to choose. Possible choices are 1=kt_algorithm, 2=antikt_algorithm, 3=cambridge_algorithm
    float m_radius = 0.5; ///< jet cone radius
    int   m_exclusive = 0; ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut 
    float m_cut = 5.; ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
    ROOT::VecOps::RVec<fastjet::PseudoJet>  operator() (ROOT::VecOps::RVec<float> p_x, ROOT::VecOps::RVec<float> p_y, ROOT::VecOps::RVec<float> p_z, ROOT::VecOps::RVec<float> E);
  };
  
  

  ///@}
}


#endif
