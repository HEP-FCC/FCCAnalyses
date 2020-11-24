
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

///Jet Clustering
struct clustering {
  clustering (int arg_jetalgo, float arg_radius);
  int m_jetalgo = 1;
  float m_radius = 0.5;
  ROOT::VecOps::RVec<fastjet::PseudoJet>  operator() (ROOT::VecOps::RVec<float> p_x, ROOT::VecOps::RVec<float> p_y, ROOT::VecOps::RVec<float> p_z, ROOT::VecOps::RVec<float> E);
};


/// Get jet px
ROOT::VecOps::RVec<float> getJet_px(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet py
ROOT::VecOps::RVec<float> getJet_py(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet pz
ROOT::VecOps::RVec<float> getJet_pz(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet e
ROOT::VecOps::RVec<float> getJet_e(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet pt
ROOT::VecOps::RVec<float> getJet_pt(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet p
ROOT::VecOps::RVec<float> getJet_p(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet mass
ROOT::VecOps::RVec<float> getJet_m(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet eta
ROOT::VecOps::RVec<float> getJet_eta(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet phi
ROOT::VecOps::RVec<float> getJet_phi(ROOT::VecOps::RVec<fastjet::PseudoJet> in);

/// Get jet theta
ROOT::VecOps::RVec<float> getJet_theta(ROOT::VecOps::RVec<fastjet::PseudoJet> in);



#endif
