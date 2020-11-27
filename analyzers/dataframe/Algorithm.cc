#include "Algorithm.h"
#include "Math/Minimizer.h"
#include "Math/IFunction.h"
#include "Math/Factory.h"
#include "Math/Functor.h"

sphericityFit::sphericityFit(ROOT::VecOps::RVec<float> arg_px, ROOT::VecOps::RVec<float> arg_py, ROOT::VecOps::RVec<float> arg_pz) {m_px=arg_px;m_py=arg_py;m_pz=arg_pz; }
float sphericityFit::operator()(const double *pars){
  
  double num = 0.;
  double den = 0.;
  double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

  for (unsigned int i =0; i<m_px.size(); i++){
    double part = m_px.at(i)*m_px.at(i) + m_py.at(i)*m_py.at(i) + m_pz.at(i)*m_pz.at(i);
    double pl = m_px.at(i)*(pars[0]/mag) + m_py.at(i)*(pars[1]/mag) + m_pz.at(i)*(pars[2]/mag);
    num += part - pl*pl;                 
    den += part;
  }           
  if (den>0.){
    double val = 3.*num / (2.*den);
    return val;
  }
  return 0.;
};

minimize_sphericity::minimize_sphericity(std::string arg_minname, std::string arg_algoname){m_minname=arg_minname.c_str(); m_algoname=arg_algoname.c_str();}
ROOT::VecOps::RVec<float> minimize_sphericity::operator()(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz){

  ROOT::Math::Minimizer *min = ROOT::Math::Factory::CreateMinimizer(m_minname, m_algoname);
  min->SetMaxFunctionCalls(1000000); // for Minuit/Minuit2 
  min->SetMaxIterations(10000);  // for GSL 
  min->SetTolerance(0.001);
  min->SetPrintLevel(0);

  // create functon wrapper for minmizer
  // a IMultiGenFunction type 
  ROOT::Math::Functor f(sphericityFit(px,py,pz),3); 
  double step[3] = {0.001,0.001,0.001};
  
  // starting point
  
  double variable[3] = { 1.0,1.0,1.0};
  min->SetFunction(f);
  
  min->SetVariable(0,"x",variable[0], step[0]);
  min->SetVariable(1,"y",variable[1], step[1]);
  min->SetVariable(2,"z",variable[2], step[2]);
  
  min->Minimize();
  
  
  const double *xs = min->X();
  //std::cout << "Minimum: f(" << xs[0] << "," << xs[1] << "," << xs[2] << "): " << min->MinValue()  << std::endl;

  ROOT::VecOps::RVec<float> result;
  result.push_back(xs[0]);
  result.push_back(xs[1]);
  result.push_back(xs[2]);
  result.push_back(min->MinValue());
  delete min;
  return result;
}


thrustFit::thrustFit(ROOT::VecOps::RVec<float> arg_px, ROOT::VecOps::RVec<float> arg_py, ROOT::VecOps::RVec<float> arg_pz) {m_px=arg_px;m_py=arg_py;m_pz=arg_pz; }
float thrustFit::operator()(const double *pars){
  
  double num = 0.;
  double den = 0.;
  double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

  for (unsigned int i =0; i<m_px.size(); i++){
    num += abs(m_px.at(i)*(pars[0]/mag) + m_py.at(i)*(pars[1]/mag) + m_pz.at(i)*(pars[2]/mag));                 
    den += sqrt(m_px.at(i)*m_px.at(i) + m_py.at(i)*m_py.at(i) + m_pz.at(i)*m_pz.at(i));
  }           
  if (den>0.){
    double val = num / den;
    return -val;
  }
  return 0.;
};


minimize_thrust::minimize_thrust(std::string arg_minname, std::string arg_algoname){m_minname=arg_minname.c_str(); m_algoname=arg_algoname.c_str();}
ROOT::VecOps::RVec<float> minimize_thrust::operator()(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz){

  
  
  ROOT::Math::Minimizer *min = ROOT::Math::Factory::CreateMinimizer(m_minname, m_algoname);
  min->SetMaxFunctionCalls(1000000); // for Minuit/Minuit2 
  min->SetMaxIterations(10000);  // for GSL 
  min->SetTolerance(0.001);
  min->SetPrintLevel(0);

  // create functon wrapper for minmizer
  // a IMultiGenFunction type 
  ROOT::Math::Functor f(thrustFit(px,py,pz),3); 
  double step[3] = {0.001,0.001,0.001};
  
  // starting point
  
  double variable[3] = { 1.,1.,1.};
  min->SetFunction(f);
  
  min->SetVariable(0,"x",variable[0], step[0]);
  min->SetVariable(1,"y",variable[1], step[1]);
  min->SetVariable(2,"z",variable[2], step[2]);
  
  min->Minimize();
  
  
  const double *xs = min->X();
  //std::cout << "Minimum: f(" << xs[0] << "," << xs[1] << "," << xs[2] << "): " << min->MinValue()  << std::endl;

  ROOT::VecOps::RVec<float> result;
  result.push_back(xs[0]);
  result.push_back(xs[1]);
  result.push_back(xs[2]);
  result.push_back(-1.*min->MinValue());
  delete min;
  return result;
}


ROOT::VecOps::RVec<float> thrust_angle(ROOT::VecOps::RVec<float> thrust, ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz){

  float thrust_mag = sqrt(thrust[0]*thrust[0] + thrust[1]*thrust[1] + thrust[2]*thrust[2]);
  ROOT::VecOps::RVec<float> result;
  for (unsigned int i =0; i<px.size(); i++){
    float value = (px.at(i)*thrust[0] + py.at(i)*thrust[1] + pz.at(i)*thrust[2])/(sqrt(px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i))*thrust_mag);
    result.push_back(value);
  }
  return result;
}

getThrustCharge::getThrustCharge(bool arg_pos) : m_pos(arg_pos) {};

float  getThrustCharge::operator() (ROOT::VecOps::RVec<float> thrust_angle, ROOT::VecOps::RVec<float> charge, ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz) {
  float result=0.;
  float norm = 0.;
  for (size_t i = 0; i < thrust_angle.size(); ++i) {
    norm+=px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i);

    if (m_pos==1 && thrust_angle.at(i)>0.) result+=charge.at(i)*sqrt(px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i));
    if (m_pos==0 && thrust_angle.at(i)<0.) result+=charge.at(i)*sqrt(px.at(i)*px.at(i)+py.at(i)*py.at(i)+pz.at(i)*pz.at(i));
  }
  return result/norm;
}
