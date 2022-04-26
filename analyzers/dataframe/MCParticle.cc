#include <iostream>
#include "MCParticle.h"


namespace FCCAnalyses{

namespace MCParticle{

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

sel_pdgID::sel_pdgID(int arg_pdg, bool arg_chargeconjugate) : m_pdg(arg_pdg), m_chargeconjugate( arg_chargeconjugate )  {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_pdgID::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ( m_chargeconjugate ) {
        if ( std::abs( p.PDG ) == std::abs( m_pdg)  ) result.emplace_back(p);
    }
    else {
        if ( p.PDG == m_pdg ) result.emplace_back(p);
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
    //if (ndaughters>1){
    if (ndaughters>=1){
      result=true;
      return result;
    }
  }
  return result;
}

sel_pt::sel_pt(float arg_min_pt) : m_min_pt(arg_min_pt) {};
ROOT::VecOps::RVec<edm4hep::MCParticleData>  sel_pt::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
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





ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::MCParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y) {
  //to be keept as std::vector
  std::vector<edm4hep::MCParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}


ROOT::VecOps::RVec<float> get_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.time);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.PDG);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.generatorStatus);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.simulatorStatus);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::Vector3d> get_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.vertex);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.vertex.z);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::Vector3d> get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    result.push_back(p.endpoint);
  }
  return result;
}

// E.P : "endpoint" is currenly not filled in the Particle block :-(
// hence retrieve the decay vertices differently :
ROOT::VecOps::RVec<edm4hep::Vector3d> get_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind )  {
        // ( carefull : if a Bs has oscillated into a Bsbar, this returns the production vertex of the Bsbar )
  ROOT::VecOps::RVec<edm4hep::Vector3d> result;
  for (auto & p: in) {
    edm4hep::Vector3d vertex(1e12, 1e12, 1e12);  // a default value for stable particles
    int db = p.daughters_begin ;
    int de = p.daughters_end;
    if (db != de) { // particle unstable
        int d1 = ind[db] ;   // first daughter
        if ( d1 >= 0 && d1 < in.size() ) {
            vertex = in.at(d1).vertex ;
        }
    }
    result.push_back(vertex);
  }
  return result;
}



ROOT::VecOps::RVec<float> get_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.endpoint.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.E());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}

int get_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> x) {
  int result =  x.size();
  return result;
}





ROOT::VecOps::RVec<int> get_parentid(ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents){
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


// ----------------------------------------------------------------------------------------------------------------------------------

// returns one MCParticle selected by its index in the particle block
edm4hep::MCParticleData sel_byIndex( int idx, ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
    edm4hep::MCParticleData dummy;
    if ( idx >= 0 && idx < in.size() ) {
           return in.at(idx) ;
    }
    else {
           std::cout << " !!!! in sel_byIndex : index = " << idx << " is larger than the size of the MCParticle block " << in.size() << std::endl;
    }
    return dummy;
}


// ----------------------------------------------------------------------------------------------------------------------------------

std::vector<int> get_list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

  std::vector<int> res;
  // i = index of a MC particle in the Particle block
  // in = the Particle collection
  // ind = the block with the indices for the daughters, Particle#1.index

  // returns a vector with the indices (in the Particle block) of the stable daughters of the particle i,
  // from the complete decay chain.

  if ( i < 0 || i >= in.size() ) return res;

  int db = in.at(i).daughters_begin ;
  int de = in.at(i).daughters_end;

  if ( db != de ) {// particle is unstable
    //int d1 = ind[db] ;
    //int d2 = ind[de-1];
    //for (int idaughter = d1; idaughter <= d2; idaughter++) {
    for (int id = db; id < de; id++) {
      int idaughter = ind[ id ];
      std::vector<int> rr = get_list_of_stable_particles_from_decay( idaughter, in, ind) ;
      res.insert( res.end(), rr.begin(), rr.end() );
    }
  }
  else {    // particle is stable
     res.push_back( i ) ;
     return res ;
  }
  return res;
}

// ----------------------------------------------------------------------------------------------------------------------------------

std::vector<int> get_list_of_particles_from_decay(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

  std::vector<int> res;

  // i = index of a MC particle in the Particle block
  // in = the Particle collection
  // ind = the block with the indices for the daughters, Particle#1.index

  // returns a vector with the indices (in the Particle block) of the daughters of the particle i

  if ( i < 0 || i >= in.size() ) return res;

  int db = in.at(i).daughters_begin ;
  int de = in.at(i).daughters_end;
  if  ( db == de ) return res;   // particle is stable
  //int d1 = ind[db] ;
  //int d2 = ind[de-1];
  //for (int idaughter = d1; idaughter <= d2; idaughter++) {
     //res.push_back( idaughter);
  for (int id = db; id < de; id++) {
     res.push_back( ind[id] ) ;
  }
  return res;
}


// ----------------------------------------------------------------------------------------------------------------------------------

// obsolete: keep for the while, for backward compatibility

std::vector<int> list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {
   std::cout << " -------- OBSOLETE -----   call to get_list_of_stable_particles_from_decay , please update your code ----- " << std::endl;
   return get_list_of_stable_particles_from_decay( i, in, ind );
}

std::vector<int> list_of_particles_from_decay(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {
   std::cout << " -------- OBSOLETE -----   call to get_list_of_particles_from_decay , please update your code ----- " << std::endl;
  return get_list_of_particles_from_decay( i, in, ind );
}






// ----------------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<int>  get_indices_ExclusiveDecay_MotherByIndex ( int imother,
								      std::vector<int> m_pdg_daughters,
								      bool m_stableDaughters,
                                                	              ROOT::VecOps::RVec<edm4hep::MCParticleData> in,
								      ROOT::VecOps::RVec<int> ind) {

   // Look for a specific decay specified by the mother index in the Particle block,
   // and by the PDG_ids of the daughters
   // Returns a vector with the indicess, in the Particle block, of the mother and of
   // the daughters - in the order defined by std::vector<int> pdg_daughters.


  ROOT::VecOps::RVec<int>  result;

  //bool debug = true;
  bool debug = false;
        // check :
        if (debug) {
        std::cout << " --- in get_indices_ExclusiveDecay_MotherByIndex " << std::endl;
        std::cout << "  PDG daughters : " << std::endl;
        for (int i=0; i < m_pdg_daughters.size(); i++) {
                std::cout << "     a daughter : " << m_pdg_daughters[i] << std::endl;
        }
        }


    if (debug) {
     std::vector<int> unstable_products = get_list_of_particles_from_decay( imother, in, ind ) ;
      for ( auto & k: unstable_products) {
           std::cout << " ......... unstable daughter PDG = " << in[k].PDG << std::endl;
      }
    }

     std::vector<int> products ;
     if ( m_stableDaughters ) {
        products = get_list_of_stable_particles_from_decay( imother, in, ind ) ;
     }
     else {
        products = get_list_of_particles_from_decay( imother, in, ind ) ;
     }

     if (debug) {
           for (auto& idx: products ) {
               std::cout << " ........... decay PDG = " << in[idx].PDG << std::endl;
           }
     }
     std::vector<int> found;
     for (auto & pdg_d: m_pdg_daughters ) {
        if (debug) std::cout << " -- looking for PDG = " << pdg_d << std::endl;
        for (auto & idx_d: products) {
            if ( in[idx_d].PDG == pdg_d ) {
                // careful, there can be several particles with the same PDG !
                if (std::find(found.begin(), found.end(), idx_d) == found.end())  {  // idx_d has NOT already been "used"
                    found.push_back( idx_d );
                    if (debug) std::cout << "       found PDG = " << pdg_d << std::endl;
                }
            }
        }
     }
     if ( found.size() == m_pdg_daughters.size()  && products.size() == m_pdg_daughters.size()) {  // all daughters have been found. That's the decay mode looked for.
        result.push_back( imother );
        for ( auto & idx_d: found) {   // use "found" and not "products", to get the right ordering
           result.push_back( idx_d );
        }

             if (debug) {
                std::cout << " --- found the decay mode requested " << std::endl;
                for ( auto & id: result ) {
                    std::cout << " idx = " << id << " PDG = " << in[id].PDG << std::endl;
                }
             }
     }

return result;

}


// ----------------------------------------------------------------------------------------------------------------------------------

get_indices_ExclusiveDecay::get_indices_ExclusiveDecay( int pdg_mother, std::vector<int> pdg_daughters, bool stableDaughters, bool chargeConjugate) {
  m_pdg_mother = pdg_mother;
  m_pdg_daughters = pdg_daughters;
  m_stableDaughters = stableDaughters;
  m_chargeConjugate = chargeConjugate;
} ;

ROOT::VecOps::RVec<int>  get_indices_ExclusiveDecay::operator() ( ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

   // Look for a specific decay specified by the mother PDG_id and
   // the PDG_ids of the daughters
   // Returns a vector with the indicess, in the Particle block, of the mother and of
   // the daughters - in the order defined by std::vector<int> pdg_daughters.
   //
   // In case there are several such decays in the event, keep only the first one.

   ROOT::VecOps::RVec<int>  result;

   //bool debug = true;
   bool debug = false;
        // check :
        if (debug) {
        std::cout << " --- in get_indices_ExclusiveDecay " << std::endl;
        std::cout << "  PDG mother = " << m_pdg_mother << std::endl;
        std::cout << "  PDG daughters : " << std::endl;
        std::cout << " m_stableDaughters = "  << m_stableDaughters << std::endl;
        for (int i=0; i < m_pdg_daughters.size(); i++) {
                std::cout << "     a daughter : " << m_pdg_daughters[i] << std::endl;
        }
        }

   for ( int imother =0; imother < in.size(); imother ++){
     int pdg = in[imother].PDG ;
     bool found_a_mother = false;
     if ( ! m_chargeConjugate ) found_a_mother = ( pdg == m_pdg_mother );
     if ( m_chargeConjugate )   found_a_mother = ( abs(pdg) == abs(m_pdg_mother) ) ;
     if ( ! found_a_mother ) continue;

     if (debug) std::cout << " --- found a mother " << std::endl;

     //if ( pdg != m_pdg_mother ) continue;

     ROOT::VecOps::RVec<int> a = get_indices_ExclusiveDecay_MotherByIndex( imother, m_pdg_daughters, m_stableDaughters, in, ind );
     if ( a.size() != 0 ) {
        result = a;
        break;    // return the first decay found
     }

   }
 return result;
}


// --------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<float> AngleBetweenTwoMCParticles( ROOT::VecOps::RVec<edm4hep::MCParticleData> p1, ROOT::VecOps::RVec<edm4hep::MCParticleData> p2 ) {

  ROOT::VecOps::RVec<float> result;
  if ( p1.size() != p2.size() ) {
        std::cout << "  !!! in AngleBetweenTwoMCParticles: the arguments p1 and p2 should have the same size " << std::endl;
        return result;
  }

  for (int i=0; i < p1.size(); i++) {
     TVector3 q1( p1[i].momentum.x, p1[i].momentum.y, p1[i].momentum.z );
     TVector3 q2( p2[i].momentum.x, p2[i].momentum.y, p2[i].momentum.z );
     float delta = fabs( q1.Angle( q2 ) ) ;
     result.push_back( delta );
  }

  return result;

}
}//#end NS MCParticle

}//end NS FCCAnalyses
