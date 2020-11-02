
#ifndef  FCCANALYSES_ANALYZERS_H
#define  FCCANALYSES_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/ClusterData.h"
#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"
#include "edm4hep/MCRecoParticleAssociationData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/TrackState.h"
#include "edm4hep/TrackCollection.h"
#include "edm4hep/TrackState.h"


/// compute transverse momentum of a MCParticle
ROOT::VecOps::RVec<float> pt (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// compute pseudorapidity of a MCPparticle
ROOT::VecOps::RVec<float> eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);



/// select ReconstructedParticles with transverse momentum greater than a minimum value [GeV]
struct selectParticlesPt {
  selectParticlesPt(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

/// Return the D0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float> get_D0 (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
std::vector<float> get_D0_std (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the Z0 of a track to a reconstructed particle
ROOT::VecOps::RVec<float> get_Z0 (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);
std::vector<float> get_Z0_std (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the Phi of a track to a reconstructed particle
ROOT::VecOps::RVec<float> get_phi (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the omega of a track to a reconstructed particle
ROOT::VecOps::RVec<float> get_omega (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// Return the tanLambda of a track to a reconstructed particle
ROOT::VecOps::RVec<float> get_tanLambda (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<edm4hep::TrackState> tracks);

/// return the transverse momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
std::vector<float> get_px_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);



/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
std::vector<float> get_py_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the momenta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
std::vector<float> get_pz_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the pseudo-rapidity of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the rapidity of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the theta of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the phi of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the energy of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

/// return the masses of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in); 
std::vector<float> get_mass_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in); 

/// return the charges of the input ReconstructedParticles
ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in); 
std::vector<float> get_charge_std(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in); 

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y);

/// return the size of the input collection
int get_nparticles(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

#endif
