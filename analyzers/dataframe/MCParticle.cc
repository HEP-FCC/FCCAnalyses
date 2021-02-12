#include "MCParticle.h"

using namespace MCParticle;


sel_genStatus::sel_genStatus(int arg_status) : m_status(arg_status) {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_genStatus::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (p.generatorStatus == m_status) {
      result.emplace_back(p);
    }
  }
  return result;
}


get_decay::get_decay(int arg_mother, int arg_daughters, bool arg_inf){m_mother=arg_mother; m_daughters=arg_daughters; m_inf=arg_inf;};
bool get_decay::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in,  ROOT::VecOps::RVec<int> ind){

  bool result=false;
  for (size_t i = 0; i < in.size(); ++i) {
    if (in[i].PDG!=m_mother)continue;
    int ndaughters=0;
    for (unsigned j = in.at(i).daughters_begin; j != in.at(i).daughters_end; ++j) {
      if (std::abs(in[ind.at(j)].PDG)==m_daughters && m_inf==false)ndaughters+=1;
      else if (std::abs(in[ind.at(j)].PDG)<=m_daughters && m_inf==true)ndaughters+=1;
    }
    if (ndaughters>1){
      result=true;
      return result;
    }
  }
  return result;
}

sel_pT::sel_pT(float arg_min_pt) : m_min_pt(arg_min_pt) {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_pT::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}


filter_pdgID::filter_pdgID(int arg_pdgid, bool arg_abs){m_pdgid = arg_pdgid; m_abs = arg_abs;};
bool  filter_pdgID::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ((m_abs && abs(p.PDG) == m_pdgid) || (p.PDG == m_pdgid)) return true;
  }
  return false;
}


get_EventPrimaryVertex::get_EventPrimaryVertex( int arg_genstatus) { m_genstatus = arg_genstatus; };
TVector3 get_EventPrimaryVertex::operator() ( ROOT::VecOps::RVec<edm4hep::MCParticleData> in )  {
  TVector3 result(-1e12,-1e12,-1e12);
  for (auto & p: in) {
     if ( p.generatorStatus == m_genstatus ) {   // generator status code for the incoming particles of the hardest subprocess
       TVector3 res( p.vertex.x, p.vertex.y, p.vertex.z );
       result = res;
       break;
     }
   }

  return result;
}


get_tree::get_tree(int arg_index) : m_index(arg_index) {};
ROOT::VecOps::RVec<int> get_tree::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind){
  ROOT::VecOps::RVec<int> result;
  auto & particle = in[m_index];
  
  //for (unsigned j = in.at(i).parents_begin; j != in.at(i).parents_end; ++j){
  //  if 
  //  result.push_back(ind.at(j));
  
  
  std::cout << "Thomas logic"<<std::endl;
  
  for (size_t i = 0; i < in.size(); ++i) {
    // all the other cout
    std::cout << i  << " status " << in[i].generatorStatus << " pdg " << in[i].PDG << " p beg "<< in.at(i).parents_begin << " p end " <<in.at(i).parents_end << "  mc size " << in.size() << "  ind size "<<ind.size() << std::endl;
    for (unsigned j = in.at(i).parents_begin; j != in.at(i).parents_end; ++j) {
      std::cout << "   ==index " << j <<" parents " << ind.at(j) << std::endl;
    }
  }
  //std::cout << "END Thomas logic"<<std::endl;

  /*  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    std::cout <<  "here" << std::endl;
    
    if (p.generatorStatus != m_index) continue;
    ROOT::VecOps::RVec<int> tree;
    tree.push_back(in.at(ind.at(i)).parents_begin);
    while(true){
      std::cout <<  "tree back " << tree.back() << std::endl;
      //      std::cout << 
      tree.push_back(in.at(ind.at(tree.back())).parents_begin);
    }
    result.push_back(tree);
  }
  return result;*/
  return result;
}





ROOT::VecOps::RVec<float> MCParticle::get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::MCParticleData> MCParticle::mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y) {
  //to be keept as std::vector
  std::vector<edm4hep::MCParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}


ROOT::VecOps::RVec<float> MCParticle::get_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.time);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.PDG);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.generatorStatus);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.simulatorStatus);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::Vector3d> MCParticle::get_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.vertex);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.z);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::Vector3d> MCParticle::get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.endpoint);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

ROOT::VecOps::RVec<float> MCParticle::get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector> MCParticle::get_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}

int MCParticle::get_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> x) {
  int result =  x.size();
  return result;
}





ROOT::VecOps::RVec<int> MCParticle::get_parentid(ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents){
  ROOT::VecOps::RVec<int> result;
  /*std::cout <<"================== Full Truth=================" <<std::endl;
  for (size_t i = 0; i < mc.size(); ++i) {
    std::cout << "i= " << i << "  PDGID "<< mc.at(i).PDG  <<  "  status  " << mc.at(i).generatorStatus << std::endl;
    for (unsigned j = mc.at(i).parents_begin; j != mc.at(i).parents_end; ++j) 
      std::cout << "   ==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;

  }*/
    
  //std::cout <<"================== NEW EVENT=================" <<std::endl;
  for (size_t i = 0; i < mcind.size(); ++i) {

    if (mcind.at(i)<0){
      result.push_back(-999);
      continue;
    }
    //std::cout << "mc ind " << mcind.at(i) << "  PDGID "<< mc.at(mcind.at(i)).PDG  << "  status  " << mc.at(mcind.at(i)).generatorStatus << std::endl;
    for (unsigned j = mc.at(mcind.at(i)).parents_begin; j != mc.at(mcind.at(i)).parents_end; ++j) {
      //std::cout << "   ==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;
      // result.push_back(parents.at(j));
    }
    //std::cout << mc.at(mcind.at(i)).parents_begin <<"---"<< mc.at(mcind.at(i)).parents_end<< std::endl;	
    if (mc.at(mcind.at(i)).parents_end - mc.at(mcind.at(i)).parents_begin>1) {
      //std::cout << "-999" << std::endl;
      result.push_back(-999);
    }
    else {
      //std::cout << "not -999 "<< parents.at(mc.at(mcind.at(i)).parents_begin) << std::endl;		    
      result.push_back(parents.at(mc.at(mcind.at(i)).parents_begin));
    }
  }
  return result;
}


bool dummyloader(){return false;}



