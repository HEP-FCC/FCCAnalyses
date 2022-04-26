
#ifndef  ALGORITHM_ANALYZERS_H
#define  ALGORITHM_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/ReconstructedParticleData.h"

#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"
#include "TFitter.h"


namespace Algorithms{

  struct getRP_combination{
    getRP_combination(int arg_n, int arg_charge, bool arg_abs);
    int  m_n;
    int  m_charge;
    bool m_abs;
    ROOT::VecOps::RVec<int> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };


  struct sphericityFit {
    sphericityFit(ROOT::VecOps::RVec<float> arg_px, 
		  ROOT::VecOps::RVec<float> arg_py, 
		  ROOT::VecOps::RVec<float> arg_pz);
    ROOT::VecOps::RVec<float> m_px;
    ROOT::VecOps::RVec<float> m_py;
    ROOT::VecOps::RVec<float> m_pz;
    float operator()(const double *par);
  };
  
  
  struct minimize_sphericity {
    minimize_sphericity(std::string arg_minname, std::string arg_algoname);
    char const *m_minname  = "Minuit2";
    char const *m_algoname = "";
    ROOT::VecOps::RVec<float> operator()(ROOT::VecOps::RVec<float> px, 
					 ROOT::VecOps::RVec<float> py, 
					 ROOT::VecOps::RVec<float> pz);
  };
  
  
  
  struct thrustFit {
    thrustFit(ROOT::VecOps::RVec<float> arg_px, 
	      ROOT::VecOps::RVec<float> arg_py, 
	      ROOT::VecOps::RVec<float> arg_pz);
    ROOT::VecOps::RVec<float> m_px;
    ROOT::VecOps::RVec<float> m_py;
    ROOT::VecOps::RVec<float> m_pz;
    float operator()(const double *par);
  };
  
  
  struct minimize_thrust {
    minimize_thrust(std::string arg_minname, std::string arg_algoname);
    char const *m_minname  = "Minuit2";
    char const *m_algoname = "";
    ROOT::VecOps::RVec<float> operator()(ROOT::VecOps::RVec<float> px, 
					 ROOT::VecOps::RVec<float> py, 
					 ROOT::VecOps::RVec<float> pz);
  };
  
  /// Get the weighted charge in a given hemisphere (defined by it's angle wrt to axis). For definition see eq1 https://arxiv.org/pdf/1209.2421.pdf
  struct getAxisCharge {
    getAxisCharge(bool arg_pos, float arg_power);
    bool m_pos = 0; //> Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0
    float m_power = 1; //> kappa parameter for the weighting
    float operator() (ROOT::VecOps::RVec<float> angle, 
		      ROOT::VecOps::RVec<float> charge, 
		      ROOT::VecOps::RVec<float> px, 
		      ROOT::VecOps::RVec<float> py, 
		      ROOT::VecOps::RVec<float> pz);
  };
  
  /// Get the invariant mass in a given hemisphere (defined by it's angle wrt to axis).
  struct getAxisMass {
    getAxisMass(bool arg_pos);
    bool m_pos = 0; //> Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0
    float operator() (ROOT::VecOps::RVec<float> angle, 
		      ROOT::VecOps::RVec<float> energy, 
		      ROOT::VecOps::RVec<float> px, 
		      ROOT::VecOps::RVec<float> py, 
		      ROOT::VecOps::RVec<float> pz);
  };
  
    
  /// Get the energy in a given hemisphere (defined by it's angle wrt to axis). Returns 3 values: total, charged, neutral energies
  struct getAxisEnergy {
    getAxisEnergy(bool arg_pos);
    bool m_pos = 0; //> Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0
    ROOT::VecOps::RVec<float> operator() (ROOT::VecOps::RVec<float> angle, 
					  ROOT::VecOps::RVec<float> charge, 
					  ROOT::VecOps::RVec<float> energy);
  };
  
  /// Get the number of particles in a given hemisphere (defined by it's angle wrt to axis). Returns 3 values: total, charged, neutral multiplicity
  struct getAxisN {
    getAxisN(bool arg_pos);
    bool m_pos = 0; //> Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0
    ROOT::VecOps::RVec<int> operator() (ROOT::VecOps::RVec<float> angle,  
					ROOT::VecOps::RVec<float> charge);
  };

  /// Get the angle cosTheta between particles and an axis
  ROOT::VecOps::RVec<float> getAxisCosTheta(ROOT::VecOps::RVec<float> axis, 
					    ROOT::VecOps::RVec<float> px, 
					    ROOT::VecOps::RVec<float> py, 
					    ROOT::VecOps::RVec<float> pz);

  /// Get the angle cosTheta between one particle and an axis
  float getAxisCosTheta(ROOT::VecOps::RVec<float> axis, 
			float px, 
			float py, 
			float pz);

  /// Get the invariant mass from a list of reconstructed particles
  float getMass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

  /// if dir == 1. points to minimum hemis if dir == -1, points to maximum energy
  ROOT::VecOps::RVec<float> getThrustPointing(ROOT::VecOps::RVec<float> in,
					      ROOT::VecOps::RVec<float> rp_e,
					      ROOT::VecOps::RVec<float> thrust,
					      float dir);

}
#endif
