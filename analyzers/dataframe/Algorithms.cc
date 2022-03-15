#include "Algorithms.h"

#include <algorithm>
#include <iostream>
#include <numeric>

#include "Math/IFunction.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "Math/LorentzVector.h"

using namespace Algorithms;

sphericityFit::sphericityFit(const ROOT::VecOps::RVec<float> & arg_px,
	                           const ROOT::VecOps::RVec<float> & arg_py,
														 const ROOT::VecOps::RVec<float> & arg_pz){
  m_px=arg_px;
	m_py=arg_py;
	m_pz=arg_pz;
}
float Algorithms::sphericityFit::operator()(const double *pars){

  double num = 0.;
  double den = 0.;
  double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

  for (unsigned int i =0; i<m_px.size(); i++){
    double part = m_px[i]*m_px[i] + m_py[i]*m_py[i] + m_pz[i]*m_pz[i];
    double pl = m_px[i]*(pars[0]/mag) + m_py[i]*(pars[1]/mag) + m_pz[i]*(pars[2]/mag);
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
  m_minname=arg_minname.c_str();
  m_algoname=arg_algoname.c_str();
  m_maxcalls=arg_maxcalls;
	m_tolerance=arg_tolerance;

  m_min = ROOT::Math::Factory::CreateMinimizer(m_minname, m_algoname);
  m_min->SetMaxFunctionCalls(m_maxcalls); // for Minuit/Minuit2
  m_min->SetMaxIterations(10000);  // for GSL
  m_min->SetTolerance(m_tolerance);
  m_min->SetPrintLevel(0);

  // create functon wrapper for minmizer
  // a IMultiGenFunction type
  double step[3] = {0.001,0.001,0.001};

  // starting point
  double variable[3] = { 1.0,1.0,1.0};

  m_min->SetVariable(0,"x",variable[0], step[0]);
  m_min->SetVariable(1,"y",variable[1], step[1]);
  m_min->SetVariable(2,"z",variable[2], step[2]);
}
ROOT::VecOps::RVec<float> Algorithms::minimize_sphericity::operator()(const ROOT::VecOps::RVec<float> & px,
	                                                                    const ROOT::VecOps::RVec<float> & py,
																																			const ROOT::VecOps::RVec<float> & pz){

  ROOT::Math::Functor f(sphericityFit(px,py,pz),3);
  m_min->SetFunction(f);
  m_min->Minimize();

  const double *xs     = m_min->X();
  const double *xs_err = m_min->Errors();

  ROOT::VecOps::RVec<float> result;
  result.push_back(m_min->MinValue());
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
  m_px=arg_px;
	m_py=arg_py;
	m_pz=arg_pz;
}
float Algorithms::thrustFit::operator()(const double *pars){

  double num = 0.;
  double den = 0.;
  double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

  for (unsigned int i =0; i<m_px.size(); i++){
    num += abs(m_px[i]*(pars[0]/mag) + m_py[i]*(pars[1]/mag) + m_pz[i]*(pars[2]/mag));
    den += sqrt(m_px[i]*m_px[i] + m_py[i]*m_py[i] + m_pz[i]*m_pz[i]);
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
  m_minname=arg_minname.c_str();
  m_algoname=arg_algoname.c_str();
	m_maxcalls=arg_maxcalls;
	m_tolerance=arg_tolerance;

  m_min = ROOT::Math::Factory::CreateMinimizer(m_minname, m_algoname);
  m_min->SetMaxFunctionCalls(m_maxcalls); // for Minuit/Minuit2
  m_min->SetMaxIterations(10000);  // for GSL
  m_min->SetTolerance(m_tolerance);
  m_min->SetPrintLevel(0);

  double step[3] = {0.001,0.001,0.001};
  // starting point
  double variable[3] = { 1.,1.,1.};

  m_min->SetVariable(0,"x",variable[0], step[0]);
  m_min->SetVariable(1,"y",variable[1], step[1]);
  m_min->SetVariable(2,"z",variable[2], step[2]);
}
ROOT::VecOps::RVec<float> Algorithms::minimize_thrust::operator()(const ROOT::VecOps::RVec<float> & px,
	                                                                const ROOT::VecOps::RVec<float> & py,
																																	const ROOT::VecOps::RVec<float> & pz){

  // create functon wrapper for minmizer
  // a IMultiGenFunction type
  ROOT::Math::Functor f(thrustFit(px,py,pz),3);
  m_min->SetFunction(f);

  //min->SetValidError(true);
  //min->ProvidesError();
  m_min->Minimize();
  //std::cout << "is valid error before hesse " << min->IsValidError() <<std::endl;
  //min->Hesse();
  //std::cout << "is valid error after hesse  " << min->IsValidError() <<std::endl;
  //std::cout << "Ncalls  " << min->NCalls() << "  Niter " << min->NIterations() <<std::endl;
  //min->PrintResults();
  const double *xs = m_min->X();
  const double *xs_err = m_min->Errors();

  //std::cout << "Minimum: f(" << xs[0] << "," << xs[1] << "," << xs[2] << "): " << min->MinValue()  << std::endl;

  ROOT::VecOps::RVec<float> result;
  result.push_back(-1.*m_min->MinValue());
  result.push_back(xs[0]);
  result.push_back(xs_err[0]);
  result.push_back(xs[1]);
  result.push_back(xs_err[1]);
  result.push_back(xs[2]);
  result.push_back(xs_err[2]);

  //delete min;
  return result;
}


getAxisCharge::getAxisCharge(bool arg_pos,
	                           float arg_power){
  m_pos = arg_pos;
	m_power = arg_power;
}
float  Algorithms::getAxisCharge::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                            const ROOT::VecOps::RVec<float> & charge,
																							const ROOT::VecOps::RVec<float> & px,
																							const ROOT::VecOps::RVec<float> & py,
																							const ROOT::VecOps::RVec<float> & pz){
  float result=0.;
  float norm = 0.;
  for (size_t i = 0; i < angle.size(); ++i) {
    norm+=px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i];

    if (m_pos==1 && angle[i]>0.) result+=charge[i]*std::pow(sqrt(px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i]),m_power);
    if (m_pos==0 && angle[i]<0.) result+=charge[i]*std::pow(sqrt(px[i]*px[i]+py[i]*py[i]+pz[i]*pz[i]),m_power);
  }
  return result/std::pow(norm,m_power);
}



getAxisMass::getAxisMass(bool arg_pos){
  m_pos=arg_pos;
}
float  Algorithms::getAxisMass::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                          const ROOT::VecOps::RVec<float> & energy,
																						const ROOT::VecOps::RVec<float> & px,
																						const ROOT::VecOps::RVec<float> & py,
																						const ROOT::VecOps::RVec<float> & pz){

  ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> result;
  for (size_t i = 0; i < angle.size(); ++i) {
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> tmp;
    tmp.SetPxPyPzE(px[i], py[i], pz[i], energy[i]);
    if (m_pos==1 && angle[i]>0.) result+=tmp;
    if (m_pos==0 && angle[i]<0.) result+=tmp;
  }
  return result.M();
}

getAxisEnergy::getAxisEnergy(bool arg_pos){
	m_pos=arg_pos;
}
ROOT::VecOps::RVec<float>  Algorithms::getAxisEnergy::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                                                const ROOT::VecOps::RVec<float> & charge,
																																	const ROOT::VecOps::RVec<float> & energy){
  ROOT::VecOps::RVec<float> result={0.,0.,0.};
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle[i]>0.){
      result[0]+=energy[i];
      if (abs(charge[i])>0) result[1]+=energy[i];
      else result[2]+=energy[i];
    }
    if (m_pos==0 && angle[i]<0.){
      result[0]+=energy[i];
      if (abs(charge[i])>0) result[1]+=energy[i];
      else result[2]+=energy[i];
    }
  }
  return result;
}


getAxisN::getAxisN(bool arg_pos){
	m_pos=arg_pos;
}
ROOT::VecOps::RVec<int>  Algorithms::getAxisN::operator() (const ROOT::VecOps::RVec<float> & angle,
	                                                         const ROOT::VecOps::RVec<float> & charge){
  ROOT::VecOps::RVec<int> result={0,0,0};
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle[i]>0.){
      result[0]+=1;
      if (abs(charge[i])>0) result[1]+=1;
      else result[2]+=1;
    }
    if (m_pos==0 && angle[i]<0.){
      result[0]+=1;
      if (abs(charge[i])>0) result[1]+=1;
      else result[2]+=1;
    }
  }
  return result;
}

getThrustPointing::getThrustPointing(float arg_dir){
  m_dir=arg_dir;
}
ROOT::VecOps::RVec<float> Algorithms::getThrustPointing::operator()(const ROOT::VecOps::RVec<float> & in,
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

  result[1]=thrust[1]*direction*m_dir;
  result[3]=thrust[3]*direction*m_dir;
  result[5]=thrust[5]*direction*m_dir;
  return thrust;
}


float Algorithms::getMass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> & in){
  ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> result;
  for (auto & p: in) {
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> tmp;
    tmp.SetPxPyPzE(p.momentum.x, p.momentum.y, p.momentum.z, p.energy);
    result+=tmp;
  }
  return result.M();
}


ROOT::VecOps::RVec<float> Algorithms::getAxisCosTheta(const ROOT::VecOps::RVec<float> & axis,
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


float Algorithms::getAxisCosTheta(const ROOT::VecOps::RVec<float> & axis,
	                                float px,
																	float py,
																	float pz){

  float thrust_mag = sqrt(axis[1]*axis[1] + axis[3]*axis[3] + axis[5]*axis[5]);
  float result = (px*axis[1] + py*axis[3] + pz*axis[5])/(sqrt(px*px+py*py+pz*pz)*thrust_mag);

  return result;
}
