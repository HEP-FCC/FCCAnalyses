#ifndef  ALGORITHM_ANALYZERS_H
#define  ALGORITHM_ANALYZERS_H

#include <cmath>
#include <vector>

#include "edm4hep/ReconstructedParticleData.h"

//#include "TFitter.h"
#include "Math/Minimizer.h"
#include "ROOT/RVec.hxx"

namespace Algorithms{

  /** @name Algorithms
   * Algorithms class .
   This represents a set functions and utilities to perfom algorithmics in FCCAnalyses.
  */
  ///@{

  /// Function that runs the fit for the sphericity axis determination
  struct sphericityFit {
  public:
    sphericityFit(const ROOT::VecOps::RVec<float> & arg_px,
                  const ROOT::VecOps::RVec<float> & arg_py,
                  const ROOT::VecOps::RVec<float> & arg_pz);
    float operator()(const double *par);

  private:
    ROOT::VecOps::RVec<float> m_px; ///vector of px
    ROOT::VecOps::RVec<float> m_py; ///vector of py
    ROOT::VecOps::RVec<float> m_pz; ///vector of pz
  };


  /// Calculates the sphericity axis based on a list of px, py, pz
  struct minimize_sphericity {
  public:
    minimize_sphericity(std::string arg_minname="Minuit2",
                        std::string arg_algoname="Migrad",
                        int arg_maxcalls=100000,
                        float arg_tolerance=0.001);
    ROOT::VecOps::RVec<float> operator()(const ROOT::VecOps::RVec<float> & px,
                                         const ROOT::VecOps::RVec<float> & py,
                                         const ROOT::VecOps::RVec<float> & pz);

  private:
    char const *m_minname; ///Minimizer to use, Minuit2 default
    char const *m_algoname; ///Optimisation algorithm, Migrad default
    int m_maxcalls; ///Maximum call to minimization function, default=100000
    float m_tolerance; ///Tolerance for minimization, default=0.001
    ROOT::Math::Minimizer *m_min; ///internal ROOT minimizer
  };


  /// Function that runs the fit for the thrust axis determination
  struct thrustFit {
  public:
    thrustFit(const ROOT::VecOps::RVec<float> & arg_px,
	      const ROOT::VecOps::RVec<float> & arg_py,
	      const ROOT::VecOps::RVec<float> & arg_pz);
    float operator()(const double *par);

  private:
    ROOT::VecOps::RVec<float> m_px; ///vector of px
    ROOT::VecOps::RVec<float> m_py; ///vector of py
    ROOT::VecOps::RVec<float> m_pz; ///vector of pz
  };


  /// Calculates the thrust axis based on a list of px, py, pz
  struct minimize_thrust {
    minimize_thrust(std::string arg_minname="Minuit2",
                    std::string arg_algoname="Migrad",
                    int arg_maxcalls=100000,
                    float arg_tolerance=0.001);
    ROOT::VecOps::RVec<float> operator()(const ROOT::VecOps::RVec<float> & px,
                                         const ROOT::VecOps::RVec<float> & py,
                                         const ROOT::VecOps::RVec<float> & pz);

  private:
    char const *m_minname; ///Minimizer to use, Minuit2 default
    char const *m_algoname; ///Optimisation algorithm, Migrad default
    int m_maxcalls;///Maximum call to minimization function, default=100000
    float m_tolerance;///Tolerance for minimization, default=0.001
    ROOT::Math::Minimizer *m_min; ///internal ROOT minimizer
  };


  /// Get the weighted charge in a given hemisphere (defined by it's angle wrt to axis). For definition see eq1 https://arxiv.org/pdf/1209.2421.pdf
  struct getAxisCharge {
  public:
    getAxisCharge(bool arg_pos=0,
                  float arg_power=1);
    float operator() (const ROOT::VecOps::RVec<float> & angle,
                      const ROOT::VecOps::RVec<float> & charge,
                      const ROOT::VecOps::RVec<float> & px,
                      const ROOT::VecOps::RVec<float> & py,
                      const ROOT::VecOps::RVec<float> & pz);
  private:
    bool m_pos; /// Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0. Default=0
    float m_power; /// kappa parameter for the weighting. Default=1
  };


  /// Get the invariant mass in a given hemisphere (defined by it's angle wrt to axis).
  struct getAxisMass {
  public:
    getAxisMass(bool arg_pos=0);
    float operator() (const ROOT::VecOps::RVec<float> & angle,
                      const ROOT::VecOps::RVec<float> & energy,
                      const ROOT::VecOps::RVec<float> & px,
                      const ROOT::VecOps::RVec<float> & py,
                      const ROOT::VecOps::RVec<float> & pz);
  private:
    bool m_pos; /// Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0. Default=0
  };


  /// Get the energy in a given hemisphere (defined by it's angle wrt to axis). Returns 3 values: total, charged, neutral energies
  struct getAxisEnergy {
  public:
    getAxisEnergy(bool arg_pos=0);
    ROOT::VecOps::RVec<float> operator() (const ROOT::VecOps::RVec<float> & angle,
                                          const ROOT::VecOps::RVec<float> & charge,
                                          const ROOT::VecOps::RVec<float> & energy);
    private:
      bool m_pos; /// Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0. Default=0
  };


  /// Get the number of particles in a given hemisphere (defined by it's angle wrt to axis). Returns 3 values: total, charged, neutral multiplicity
  struct getAxisN {
  public:
    getAxisN(bool arg_pos=0);
    ROOT::VecOps::RVec<int> operator() (const ROOT::VecOps::RVec<float> & angle,
                                        const ROOT::VecOps::RVec<float> & charge);
  private:
    bool m_pos; /// Which hemisphere to select, false/0=cosTheta<0 true/1=cosTheta>0. Default=0
  };


  ///Make the thrust axis points to hemisphere with maximum or minimum energy
  struct getThrustPointing {
  public:
    getThrustPointing(float arg_dir=1.);
    ROOT::VecOps::RVec<float> operator() (const ROOT::VecOps::RVec<float> & in,
                                          const ROOT::VecOps::RVec<float> & rp_e,
                                          const ROOT::VecOps::RVec<float> & thrust);
  private:
    float m_dir;///if dir > 0. points to minimum hemis if dir < 0, points to maximum energy. Default is 1. (minimum energy)
  };


  /// Get the angle cosTheta between particles and an axis
  ROOT::VecOps::RVec<float> getAxisCosTheta(const ROOT::VecOps::RVec<float> & axis,
                                            const ROOT::VecOps::RVec<float> & px,
                                            const ROOT::VecOps::RVec<float> & py,
                                            const ROOT::VecOps::RVec<float> & pz);

  /// Get the angle cosTheta between one particle and an axis
  float getAxisCosTheta(const ROOT::VecOps::RVec<float> & axis,
                        float px,
                        float py,
                        float pz);

  /// Get the invariant mass from a list of reconstructed particles
  float getMass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> & in);

  ///@}

}
#endif
