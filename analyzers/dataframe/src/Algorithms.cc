#include "FCCAnalyses/Algorithms.h"
#include "FCCAnalyses/Utils.h"
#include "Math/Minimizer.h"
#include "Math/IFunction.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include <algorithm>
#include <iostream>
#include <numeric>

#include "Math/IFunction.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "Math/LorentzVector.h"

namespace FCCAnalyses{

namespace Algorithms{

sphericityFit::sphericityFit(const ROOT::VecOps::RVec<float> & arg_px,
	                           const ROOT::VecOps::RVec<float> & arg_py,
														 const ROOT::VecOps::RVec<float> & arg_pz){
  _px=arg_px;
	_py=arg_py;
	_pz=arg_pz;
}
float sphericityFit::operator()(const double *pars){

  double num = 0.;
  double den = 0.;
  double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

  for (unsigned int i =0; i<_px.size(); i++){
    double part = _px[i]*_px[i] + _py[i]*_py[i] + _pz[i]*_pz[i];
    double pl = _px[i]*(pars[0]/mag) + _py[i]*(pars[1]/mag) + _pz[i]*(pars[2]/mag);
    num += part - pl*pl;
    den += part;
  }
  if (den>0.){
    double val = 3.*num / (2.*den);
    return val;
  }
  return 0.;
};

minimize_sphericity::minimize_sphericity(std::string arg_minname,
	                                       std::string arg_algoname,
																				 int arg_maxcalls,
																				 float arg_tolerance){
  _minname=arg_minname.c_str();
  _algoname=arg_algoname.c_str();
  _maxcalls=arg_maxcalls;
	_tolerance=arg_tolerance;

  _min = ROOT::Math::Factory::CreateMinimizer(_minname, _algoname);
  _min->SetMaxFunctionCalls(_maxcalls); // for Minuit/Minuit2
  _min->SetMaxIterations(10000);  // for GSL
  _min->SetTolerance(_tolerance);
  _min->SetPrintLevel(0);
}
ROOT::VecOps::RVec<float> minimize_sphericity::operator()(const ROOT::VecOps::RVec<float> & px,
	                                                                    const ROOT::VecOps::RVec<float> & py,
																																			const ROOT::VecOps::RVec<float> & pz){
  _min->SetVariable(0,"x",_variable[0], _step[0]);
	_min->SetVariable(0,"y",_variable[1], _step[1]);
	_min->SetVariable(2,"z",_variable[2], _step[2]);

	// create functon wrapper for minmizer
  // a IMultiGenFunction type
  ROOT::Math::Functor f(sphericityFit(px,py,pz),3);
  _min->SetFunction(f);
  _min->Minimize();

  const double *xs     = _min->X();
  const double *xs_err = _min->Errors();

  ROOT::VecOps::RVec<float> result;
  result.push_back(_min->MinValue());
  result.push_back(xs[0]);
  result.push_back(xs_err[0]);
  result.push_back(xs[1]);
  result.push_back(xs_err[1]);
  result.push_back(xs[2]);
  result.push_back(xs_err[2]);
  //delete min;
  return result;
}


thrustFit::thrustFit(const ROOT::VecOps::RVec<float> & arg_px,
	                   const ROOT::VecOps::RVec<float> & arg_py,
										 const ROOT::VecOps::RVec<float> & arg_pz){
  _px=arg_px;
	_py=arg_py;
	_pz=arg_pz;
}
float thrustFit::operator()(const double *pars){

  double num = 0.;
  double den = 0.;
  double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

  for (unsigned int i =0; i<_px.size(); i++){
    num += abs(_px[i]*(pars[0]/mag) + _py[i]*(pars[1]/mag) + _pz[i]*(pars[2]/mag));
    den += sqrt(_px[i]*_px[i] + _py[i]*_py[i] + _pz[i]*_pz[i]);
  }
  if (den>0.){
    double val = num / den;
    return -val;
  }
  return 0.;
};


minimize_thrust::minimize_thrust(std::string arg_minname,
	                               std::string arg_algoname,
																 int arg_maxcalls,
																 float arg_tolerance){
  _minname=arg_minname.c_str();
  _algoname=arg_algoname.c_str();
	_maxcalls=arg_maxcalls;
	_tolerance=arg_tolerance;

  _min = ROOT::Math::Factory::CreateMinimizer(_minname, _algoname);
  _min->SetMaxFunctionCalls(_maxcalls); // for Minuit/Minuit2
  _min->SetMaxIterations(10000);  // for GSL
  _min->SetTolerance(_tolerance);
  _min->SetPrintLevel(0);
}
ROOT::VecOps::RVec<float> minimize_thrust::operator()(const ROOT::VecOps::RVec<float> & px,
	                                                                const ROOT::VecOps::RVec<float> & py,
																																	const ROOT::VecOps::RVec<float> & pz){
  _min->SetVariable(0,"x",_variable[0], _step[0]);
	_min->SetVariable(1,"y",_variable[1], _step[1]);
	_min->SetVariable(2,"z",_variable[2], _step[2]);
  // create functon wrapper for minmizer
  // a IMultiGenFunction type
  ROOT::Math::Functor f(thrustFit(px,py,pz),3);
  _min->SetFunction(f);

  //min->SetValidError(true);
  //min->ProvidesError();
  _min->Minimize();
  //std::cout << "is valid error before hesse " << min->IsValidError() <<std::endl;
  //min->Hesse();
  //std::cout << "is valid error after hesse  " << min->IsValidError() <<std::endl;
  //std::cout << "Ncalls  " << min->NCalls() << "  Niter " << min->NIterations() <<std::endl;
  //min->PrintResults();
  const double *xs = _min->X();
  const double *xs_err = _min->Errors();

  //std::cout << "Minimum: f(" << xs[0] << "," << xs[1] << "," << xs[2] << "): " << min->MinValue()  << std::endl;

  ROOT::VecOps::RVec<float> result;
  result.push_back(-1.*_min->MinValue());
  result.push_back(xs[0]);
  result.push_back(xs_err[0]);
  result.push_back(xs[1]);
  result.push_back(xs_err[1]);
  result.push_back(xs[2]);
  result.push_back(xs_err[2]);

  return result;
}


ROOT::VecOps::RVec<float> Algorithms::calculate_thrust::operator()(
    const ROOT::VecOps::RVec<float>& px,
    const ROOT::VecOps::RVec<float>& py,
    const ROOT::VecOps::RVec<float>& pz) {

  if (px.size() != py.size()) {
    throw std::domain_error("calculate_thrust: Input vector sizes are not equal.");
  }
  if (px.size() != pz.size()) {
    throw std::domain_error("calculate_thrust: Input vector sizes are not equal.");
  }

  ROOT::VecOps::RVec<float> result;

  size_t nParticles = px.size();
  if (nParticles < 2) {
    // std::cout << "calculate_thrust: Number of input particles too small."
    //           << std::endl;

    result.push_back(-1);
    result.push_back(-1);
    result.push_back(-1);
    result.push_back(-1);

    return result;
  }

  // std::cout << "calculate_thrust: Calculating sum of all particles in event"
  //           << std::endl;

  // Array to store x, y, z and magnitude squared of the particles.
  // 0 -- magnitude squared, 1 -- x, 2 -- y, 3 -- z
  float pArr[nParticles][4];
  float pSum = 0.;
  for (size_t i = 0; i < nParticles; ++i) {
    pArr[i][1] = px[i];
    pArr[i][2] = py[i];
    pArr[i][3] = pz[i];
    mag2(pArr[i]);
    pSum += std::sqrt(pArr[i][0]);
  }

  // Trying all combinations of reference vector orthogonal to two selected
  // particles.
  // std::cout << "Trying all combinations..." << std::endl;
  float pMax[4] = {0., 0., 0., 0.};
  for (size_t i = 0; i < nParticles - 1; ++i) {
    for (size_t j = i + 1; j < nParticles; ++j) {
      float nRef[4];
      cross(nRef, pArr[i], pArr[j]);
      mag2(nRef);
      unit(nRef);

      float pPart[4] = {0., 0., 0., 0.};
      for (size_t k = 0; k < nParticles; ++k) {
        if (k == i || k == j) {
          continue;
        }

        if (dot(nRef, pArr[k]) > 0.) {
          plus(pPart, pPart, pArr[k]);
        } else {
          minus(pPart, pPart, pArr[k]);
        }
      }

      float pFullArr[4][4];
      // pPart + pArr[i] + pArr[j]
      plus(pFullArr[0], pPart, pArr[i]);
      plus(pFullArr[0], pFullArr[0], pArr[j]);

      // pPart + pArr[i] - pArr[j]
      plus(pFullArr[1], pPart, pArr[i]);
      minus(pFullArr[1], pFullArr[1], pArr[j]);

      // pPart - pArr[i] + pArr[j]
      minus(pFullArr[2], pPart, pArr[i]);
      plus(pFullArr[2], pFullArr[2], pArr[j]);

      // pPart - pArr[i] - pArr[j]
      minus(pFullArr[3], pPart, pArr[i]);
      minus(pFullArr[3], pFullArr[3], pArr[j]);

      for (size_t k = 0; k < 4; ++k) {
        mag2(pFullArr[k]);
        if (pFullArr[k][0] > pMax[0]) {
          copy(pMax, pFullArr[k]);
        }
      }
    }
  }

  float pMaxMag = std::sqrt(pMax[0]);
  // std::cout << "Thrust value arr: " << pMaxMag / pSum << std::endl;
  result.push_back(pMaxMag / pSum);
  // Normalizing the thrust vector
  result.push_back(pMax[1]/pMaxMag);
  result.push_back(pMax[2]/pMaxMag);
  result.push_back(pMax[3]/pMaxMag);

  return result;
}

inline void Algorithms::calculate_thrust::mag2(float (&vec)[4]) {
  vec[0] = vec[1]*vec[1] + vec[2]*vec[2] + vec[3]*vec[3];
}

inline float Algorithms::calculate_thrust::dot(float vec1[4], float vec2[4]) {
  return vec1[1]*vec2[1] + vec1[2]*vec2[2] + vec1[3]*vec2[3];
}

inline void Algorithms::calculate_thrust::cross(float (&vec)[4], float vec1[4], float vec2[4]) {
  vec[1] = vec1[2]*vec2[3] - vec1[3]*vec2[2];
  vec[2] = vec1[3]*vec2[1] - vec1[1]*vec2[3];
  vec[3] = vec1[1]*vec2[2] - vec1[2]*vec2[1];
}

inline void Algorithms::calculate_thrust::unit(float (&vec)[4]) {
  float mag = std::sqrt(vec[0]);
  vec[1] = vec[1]/mag;
  vec[2] = vec[2]/mag;
  vec[3] = vec[3]/mag;
}

inline void Algorithms::calculate_thrust::plus(float (&vec)[4], float vecIn1[4], float vecIn2[4]) {
  vec[1] = vecIn1[1] + vecIn2[1];
  vec[2] = vecIn1[2] + vecIn2[2];
  vec[3] = vecIn1[3] + vecIn2[3];
}

inline void Algorithms::calculate_thrust::minus(float (&vecOut)[4], float vecIn1[4], float vecIn2[4]) {
  vecOut[1] = vecIn1[1] - vecIn2[1];
  vecOut[2] = vecIn1[2] - vecIn2[2];
  vecOut[3] = vecIn1[3] - vecIn2[3];
}

inline void Algorithms::calculate_thrust::copy(float (&vecOut)[4], float vecIn[4]) {
  vecOut[0] = vecIn[0];
  vecOut[1] = vecIn[1];
  vecOut[2] = vecIn[2];
  vecOut[3] = vecIn[3];
}


getAxisCharge::getAxisCharge(bool arg_pos,
	                           float arg_power){
  _pos = arg_pos;
	_power = arg_power;
}
float  getAxisCharge::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                            const ROOT::VecOps::RVec<float> & charge,
																							const ROOT::VecOps::RVec<float> & px,
																							const ROOT::VecOps::RVec<float> & py,
																							const ROOT::VecOps::RVec<float> & pz){
  float result=0.;
  float norm = 0.;
  for (size_t i = 0; i < angle.size(); ++i) {
    norm+=px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i];

    if (_pos==1 && angle[i]>0.) result+=charge[i]*std::pow(sqrt(px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i]),_power);
    if (_pos==0 && angle[i]<0.) result+=charge[i]*std::pow(sqrt(px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i]),_power);
  }
  return result/std::pow(norm,_power);
}


getAxisMass::getAxisMass(bool arg_pos){
  _pos=arg_pos;
}
float  getAxisMass::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                          const ROOT::VecOps::RVec<float> & energy,
																						const ROOT::VecOps::RVec<float> & px,
																						const ROOT::VecOps::RVec<float> & py,
																						const ROOT::VecOps::RVec<float> & pz){

  ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> result;
  for (size_t i = 0; i < angle.size(); ++i) {
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> tmp;
    tmp.SetPxPyPzE(px[i], py[i], pz[i], energy[i]);
    if (_pos==1 && angle[i]>0.) result+=tmp;
    if (_pos==0 && angle[i]<0.) result+=tmp;
  }
  return result.M();
}

getAxisEnergy::getAxisEnergy(bool arg_pos){
	_pos=arg_pos;
}
ROOT::VecOps::RVec<float>  getAxisEnergy::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                                                const ROOT::VecOps::RVec<float> & charge,
																																	const ROOT::VecOps::RVec<float> & energy){
  ROOT::VecOps::RVec<float> result={0.,0.,0.};
  for (size_t i = 0; i < angle.size(); ++i) {
    if (_pos==1 && angle[i]>0.){
      result[0]+=energy[i];
      if (abs(charge[i])>0) result[1]+=energy[i];
      else result[2]+=energy[i];
    }
    if (_pos==0 && angle[i]<0.){
      result[0]+=energy[i];
      if (abs(charge[i])>0) result[1]+=energy[i];
      else result[2]+=energy[i];
    }
  }
  return result;
}


getAxisN::getAxisN(bool arg_pos){
	_pos=arg_pos;
}
ROOT::VecOps::RVec<int>  getAxisN::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                                         const ROOT::VecOps::RVec<float> & charge){
  ROOT::VecOps::RVec<int> result={0,0,0};
  for (size_t i = 0; i < angle.size(); ++i) {
    if (_pos==1 && angle[i]>0.){
      result[0]+=1;
      if (abs(charge[i])>0) result[1]+=1;
      else result[2]+=1;
    }
    if (_pos==0 && angle[i]<0.){
      result[0]+=1;
      if (abs(charge[i])>0) result[1]+=1;
      else result[2]+=1;
    }
  }
  return result;
}

getThrustPointing::getThrustPointing(float arg_dir){
  _dir=arg_dir;
}
ROOT::VecOps::RVec<float> getThrustPointing::operator()(const ROOT::VecOps::RVec<float> & in,
	                                                                  const ROOT::VecOps::RVec<float> & rp_e,
																																		const ROOT::VecOps::RVec<float> & thrust){

  ROOT::VecOps::RVec<float> result;
  for (unsigned int i =0; i<thrust.size(); i++)result.push_back(thrust[i]);
  float direction = 1.;
  float pos_angle=0.;
  float neg_angle=0.;
  for (unsigned int i =0; i<rp_e.size(); i++){
    if (in[i]>0.)pos_angle+=rp_e[i];
    else neg_angle+=rp_e[i];
  }

  if (pos_angle>neg_angle)direction=-1.;

  result[1]=thrust[1]*direction*_dir;
  result[3]=thrust[3]*direction*_dir;
  result[5]=thrust[5]*direction*_dir;
  return result;
}


float getMass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> & in){
  ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> result;
  for (auto & p: in) {
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> tmp;
    tmp.SetPxPyPzE(p.momentum.x, p.momentum.y, p.momentum.z, p.energy);
    result+=tmp;
  }
  return result.M();
}


ROOT::VecOps::RVec<float> getAxisCosTheta(const ROOT::VecOps::RVec<float> & axis,
	                                                    const ROOT::VecOps::RVec<float> & px,
																											const ROOT::VecOps::RVec<float> & py,
																											const ROOT::VecOps::RVec<float> & pz){

  float thrust_mag = sqrt(axis[1]*axis[1] + axis[3]*axis[3] + axis[5]*axis[5]);
  ROOT::VecOps::RVec<float> result;
  for (unsigned int i =0; i<px.size(); i++){
    float value = (px[i]*axis[1] + py[i]*axis[3] + pz[i]*axis[5])/(sqrt(px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i])*thrust_mag);
    result.push_back(value);
  }
  return result;
}


float getAxisCosTheta(const ROOT::VecOps::RVec<float> & axis,
	                                float px,
																	float py,
																	float pz){

  float thrust_mag = sqrt(axis[1]*axis[1] + axis[3]*axis[3] + axis[5]*axis[5]);
  float result = (px*axis[1] + py*axis[3] + pz*axis[5])/(sqrt(px*px+py*py+pz*pz)*thrust_mag);

  return result;
}

}//end NS Algorithms

}//end NS FCCAnalyses
