#include "Algorithms.h"

#include "Math/IFunction.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include <algorithm>
#include <iostream>
#include <numeric>

using namespace Algorithms;

getRP_combination::getRP_combination(int arg_n, 
				     int arg_charge, 
				     bool arg_abs){m_n = arg_n; m_charge = arg_charge; m_abs = arg_charge;}
ROOT::VecOps::RVec<int> Algorithms::getRP_combination::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<int> result;

  std::vector<int> d(in.size());
  std::cout<<"==============================NEX EVET====================="<<std::endl;
  std::iota(d.begin(),d.end(),1);
  std::cout << "These are the Possible Permutations: " << std::endl;
  int index=0;
  do
    {
      int charge=0;
      for (int i = 0; i < m_n; i++)
	charge+=in[d[i]].charge;
      if ((abs(charge)==m_charge and m_abs) || charge==m_charge){
	index+=1;
	for (int i = 0; i < m_n; i++)
	  std::cout << d[i] << " ";
        std::cout << "  charge  " << charge << "  index " << index << std::endl;
      }
        std::reverse(d.begin()+m_n,d.end());
    } while (next_permutation(d.begin(),d.end()));

  return result;
}



sphericityFit::sphericityFit(const ROOT::VecOps::RVec<float> & arg_px, 
			     const ROOT::VecOps::RVec<float> & arg_py, 
			     const ROOT::VecOps::RVec<float> & arg_pz) {m_px=arg_px;m_py=arg_py;m_pz=arg_pz; }
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
					 std::string arg_algoname){
  m_minname=arg_minname.c_str(); 
  m_algoname=arg_algoname.c_str();

  m_min = ROOT::Math::Factory::CreateMinimizer(m_minname, m_algoname);
  m_min->SetMaxFunctionCalls(100000); // for Minuit/Minuit2 
  m_min->SetMaxIterations(10000);  // for GSL 
  m_min->SetTolerance(0.001);
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
		     const ROOT::VecOps::RVec<float> & arg_pz) {m_px=arg_px;m_py=arg_py;m_pz=arg_pz; }
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


minimize_thrust::minimize_thrust(std::string arg_minname, std::string arg_algoname){
  m_minname=arg_minname.c_str(); 
  m_algoname=arg_algoname.c_str();

  m_min = ROOT::Math::Factory::CreateMinimizer(m_minname, m_algoname);
  m_min->SetMaxFunctionCalls(100000); // for Minuit/Minuit2 
  m_min->SetMaxIterations(10000);  // for GSL 
  m_min->SetTolerance(0.001);
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
			     float arg_power){m_pos = arg_pos; m_power = arg_power;};
float  Algorithms::getAxisCharge::operator() (ROOT::VecOps::RVec<float> angle, 
					      ROOT::VecOps::RVec<float> charge, 
					      ROOT::VecOps::RVec<float> px, 
					      ROOT::VecOps::RVec<float> py, 
					      ROOT::VecOps::RVec<float> pz) {
  float result=0.;
  float norm = 0.;
  for (size_t i = 0; i < angle.size(); ++i) {
    norm+=px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i);

    if (m_pos==1 && angle.at(i)>0.) result+=charge.at(i)*std::pow(sqrt(px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i)),m_power);
    if (m_pos==0 && angle.at(i)<0.) result+=charge.at(i)*std::pow(sqrt(px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i)),m_power);
  }
  return result/std::pow(norm,m_power);
}



getAxisMass::getAxisMass(bool arg_pos) : m_pos(arg_pos) {};
float  Algorithms::getAxisMass::operator() (ROOT::VecOps::RVec<float> angle, 
					    ROOT::VecOps::RVec<float> energy, 
					    ROOT::VecOps::RVec<float> px, 
					    ROOT::VecOps::RVec<float> py, 
					    ROOT::VecOps::RVec<float> pz) {
  
  TLorentzVector result;
  for (size_t i = 0; i < angle.size(); ++i) {
    TLorentzVector tmp;
    tmp.SetPxPyPzE(px.at(i), py.at(i), pz.at(i), energy.at(i));
    if (m_pos==1 && angle.at(i)>0.) result+=tmp;
    if (m_pos==0 && angle.at(i)<0.) result+=tmp;
  }
  return result.M();
}

getAxisEnergy::getAxisEnergy(bool arg_pos) : m_pos(arg_pos) {};
ROOT::VecOps::RVec<float>  Algorithms::getAxisEnergy::operator() (ROOT::VecOps::RVec<float> angle, 
								  ROOT::VecOps::RVec<float> charge, 
								  ROOT::VecOps::RVec<float> energy) {
  ROOT::VecOps::RVec<float> result={0.,0.,0.};
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle.at(i)>0.){
      result.at(0)+=energy.at(i);
      if (abs(charge.at(i))>0) result.at(1)+=energy.at(i);
      else result.at(2)+=energy.at(i);
    }
    if (m_pos==0 && angle.at(i)<0.){
      result.at(0)+=energy.at(i);
      if (abs(charge.at(i))>0) result.at(1)+=energy.at(i);
      else result.at(2)+=energy.at(i);
    }
  }
  return result;
}


getAxisN::getAxisN(bool arg_pos) : m_pos(arg_pos) {};
ROOT::VecOps::RVec<int>  Algorithms::getAxisN::operator() (ROOT::VecOps::RVec<float> angle, 
							   ROOT::VecOps::RVec<float> charge) {
  ROOT::VecOps::RVec<int> result={0,0,0};
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle.at(i)>0.){
      result.at(0)+=1;
      if (abs(charge.at(i))>0) result.at(1)+=1;
      else result.at(2)+=1;
    }
    if (m_pos==0 && angle.at(i)<0.){
      result.at(0)+=1;
      if (abs(charge.at(i))>0) result.at(1)+=1;
      else result.at(2)+=1;
    }
  }
  return result;
}


float Algorithms::getMass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  TLorentzVector result;
  for (auto & p: in) {
    TLorentzVector tmp;
    tmp.SetPxPyPzE(p.momentum.x, p.momentum.y, p.momentum.z, p.energy);
    result+=tmp;
  }
  return result.M();
}


ROOT::VecOps::RVec<float> Algorithms::getAxisCosTheta(ROOT::VecOps::RVec<float> axis, 
						      ROOT::VecOps::RVec<float> px, 
						      ROOT::VecOps::RVec<float> py, 
						      ROOT::VecOps::RVec<float> pz){

  float thrust_mag = sqrt(axis[1]*axis[1] + axis[3]*axis[3] + axis[5]*axis[5]);
  ROOT::VecOps::RVec<float> result;
  for (unsigned int i =0; i<px.size(); i++){
    float value = (px.at(i)*axis[1] + py.at(i)*axis[3] + pz.at(i)*axis[5])/(sqrt(px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i))*thrust_mag);
    result.push_back(value);
  }
  return result;
}


float Algorithms::getAxisCosTheta(ROOT::VecOps::RVec<float> axis, 
				  float px, 
				  float py, 
				  float pz){

  float thrust_mag = sqrt(axis[1]*axis[1] + axis[3]*axis[3] + axis[5]*axis[5]);
  float result = (px*axis[1] + py*axis[3] + pz*axis[5])/(sqrt(px*px+py*py+pz*pz)*thrust_mag);
 
  return result;
}


ROOT::VecOps::RVec<float> Algorithms::getThrustPointing(ROOT::VecOps::RVec<float> in,
							ROOT::VecOps::RVec<float> rp_e,
							ROOT::VecOps::RVec<float> thrust,
							float dir){

  float direction = 1.;
  float pos_angle=0.;
  float neg_angle=0.;
  for (unsigned int i =0; i<rp_e.size(); i++){
    if (in.at(i)>0.)pos_angle+=rp_e.at(i);
    else neg_angle+=rp_e.at(i);
  }

  if (pos_angle>neg_angle)direction=-1.;
  
  thrust.at(1)=thrust.at(1)*direction*dir;
  thrust.at(3)=thrust.at(3)*direction*dir;
  thrust.at(5)=thrust.at(5)*direction*dir;
  return thrust;
}
