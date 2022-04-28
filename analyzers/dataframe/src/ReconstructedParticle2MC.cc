#include "ReconstructedParticle2MC.h"
#include <iostream>


using namespace ReconstructedParticle2MC;


ROOT::VecOps::RVec<float>
ReconstructedParticle2MC::getRP2MC_p(ROOT::VecOps::RVec<int> recind, 
				     ROOT::VecOps::RVec<int> mcind, 
				     ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
				     ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv.P();
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector>
ReconstructedParticle2MC::getRP2MC_tlv(ROOT::VecOps::RVec<int> recind, 
				       ROOT::VecOps::RVec<int> mcind, 
				       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
				       ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  
  ROOT::VecOps::RVec<TLorentzVector> result;
  result.resize(reco.size(),TLorentzVector());

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv;
  }
  return result;
}

ROOT::VecOps::RVec<float>
ReconstructedParticle2MC::getRP2MC_px(ROOT::VecOps::RVec<int> recind, 
				      ROOT::VecOps::RVec<int> mcind, 
				      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
				      ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).momentum.x;
  }
  return result;
}

ROOT::VecOps::RVec<float>
ReconstructedParticle2MC::getRP2MC_py(ROOT::VecOps::RVec<int> recind, 
				      ROOT::VecOps::RVec<int> mcind, 
				      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
				      ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).momentum.y;
  }
  return result;
}

ROOT::VecOps::RVec<float>
ReconstructedParticle2MC::getRP2MC_pz(ROOT::VecOps::RVec<int> recind,
				      ROOT::VecOps::RVec<int> mcind, 
				      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
				      ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).momentum.z;
  }
  return result;
}

ROOT::VecOps::RVec<float> 
ReconstructedParticle2MC::getRP2MC_pdg(ROOT::VecOps::RVec<int> recind,
				       ROOT::VecOps::RVec<int> mcind, 
				       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
				       ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).PDG;
  }
  return result;
}

ROOT::VecOps::RVec<float>
ReconstructedParticle2MC::getRP2MC_charge(ROOT::VecOps::RVec<int> recind, 
					  ROOT::VecOps::RVec<int> mcind, 
					  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
					  ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).charge;
  }
  return result;
}

ROOT::VecOps::RVec<float> 
ReconstructedParticle2MC::getRP2MC_mass(ROOT::VecOps::RVec<int> recind, 
					ROOT::VecOps::RVec<int> mcind, 
					ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
					ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    result[recind.at(i)]=mc.at(mcind.at(i)).mass;
  }
  return result;
}

ROOT::VecOps::RVec<int>
ReconstructedParticle2MC::getRP2MC_index(ROOT::VecOps::RVec<int> recind, 
					 ROOT::VecOps::RVec<int> mcind, 
					 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco) {
  ROOT::VecOps::RVec<int> result;
  result.resize(reco.size(),-1.);
  for (size_t i=0; i<recind.size();i++) {
    result[recind.at(i)]=mcind.at(i);
  }
  return result;
}


ROOT::VecOps::RVec< ROOT::VecOps::RVec<int> >
ReconstructedParticle2MC::getRP2MC_indexVec(ROOT::VecOps::RVec<int> recind, 
					    ROOT::VecOps::RVec<int> mcind, 
					    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco) {
  
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result;
  for (size_t i=0; i<reco.size();i++) {
    ROOT::VecOps::RVec<int> tmp;
    result.push_back(tmp);
  }

  for (size_t i=0; i<recind.size();i++) {
    result[recind.at(i)].push_back(mcind.at(i));
  }
  return result;
}

ROOT::VecOps::RVec<int>
ReconstructedParticle2MC::getRP2MC_index_test(ROOT::VecOps::RVec<int> recind, 
					      ROOT::VecOps::RVec<int> mcind, 
					      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
					      ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, 
					      ROOT::VecOps::RVec<int> parents) {
  std::cout <<"=========NEW EVENT========="<<std::endl;
  ROOT::VecOps::RVec<int> result;
  result.resize(reco.size(),-1.);
  for (size_t i=0; i<recind.size();i++) {
    if (result[recind.at(i)]>-1){
      auto & p_prev = mc.at(result[recind.at(i)]);
      auto & p_now  = mc.at(mcind.at(i));
      auto & p_reco = reco.at(recind.at(i));
      TLorentzVector tlv_prev;
      TLorentzVector tlv_now;
      TLorentzVector tlv_reco;
      tlv_prev.SetXYZM(p_prev.momentum.x, p_prev.momentum.y, p_prev.momentum.z, p_prev.mass);
      tlv_now.SetXYZM(p_now.momentum.x, p_now.momentum.y, p_now.momentum.z, p_now.mass);
      tlv_reco.SetXYZM(p_reco.momentum.x, p_reco.momentum.y, p_reco.momentum.z, p_reco.mass);

      std::cout << "reco energy " << tlv_reco.E() << " eta " << tlv_reco.Eta() << " phi " << tlv_reco.Phi() << " previous PDG " << p_prev.PDG << " energy " << tlv_prev.E() << " eta " << tlv_prev.Eta() << " phi " << tlv_prev.Phi() << " dR reco " << tlv_reco.DeltaR(tlv_prev) << "  new PDG  " << p_now.PDG << " energy " << tlv_now.E() << " eta " << tlv_now.Eta() << " phi " << tlv_now.Phi() << " dR reco " << tlv_reco.DeltaR(tlv_now) <<std::endl;
      for (unsigned j = mc.at(result[recind.at(i)]).parents_begin; j != mc.at(result[recind.at(i)]).parents_end; ++j){
	std::cout << "   prev==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << " px " << mc.at(parents.at(j)).momentum.x << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;
	for (unsigned k = mc.at(parents.at(j)).parents_begin; k != mc.at(parents.at(j)).parents_end; ++k)
	  std::cout << "   prev==index " << k <<" grandparents " << parents.at(k) << "  PDGID "<< mc.at(parents.at(k)).PDG << " px " << mc.at(parents.at(k)).momentum.x << "  status  " << mc.at(parents.at(k)).generatorStatus << std::endl;
      }

      for (unsigned j = mc.at(mcind.at(i)).parents_begin; j != mc.at(mcind.at(i)).parents_end; ++j){
	std::cout << "   now==index  " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << " px " << mc.at(parents.at(j)).momentum.x << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;
	for (unsigned k = mc.at(parents.at(j)).parents_begin; k != mc.at(parents.at(j)).parents_end; ++k)
	  std::cout << "   now==index " << k <<" grandparents " << parents.at(k) << "  PDGID "<< mc.at(parents.at(k)).PDG << " px " << mc.at(parents.at(k)).momentum.x << "  status  " << mc.at(parents.at(k)).generatorStatus << std::endl;
      }
    }
    result[recind.at(i)]=mcind.at(i);
  }
  return result;
}



ROOT::VecOps::RVec<int>
ReconstructedParticle2MC::getRP2MC_parentid (ROOT::VecOps::RVec<int> recind, 
					     ROOT::VecOps::RVec<int> mcind, 
					     ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
					     ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, 
					     ROOT::VecOps::RVec<int> parents){
  ROOT::VecOps::RVec<int> result;
  result.resize(reco.size(),-1.);
  for (unsigned int i=0; i<recind.size();i++) {
    if (mc.at(mcind.at(i)).parents_begin!=mc.at(mcind.at(i)).parents_end){
      result[recind.at(i)]=parents.at(mc.at(mcind.at(i)).parents_begin);
    }
  }

  /*  if (recind.size()>reco.size()){ 
    std::cout << recind.size() <<"========="<<reco.size()<<std::endl;
    for (unsigned int i=0; i<recind.size();i++) {
      if (i<recind.size()-1 && recind[i]==recind[i+1]){
	
	TLorentzVector tlv;
	tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
	TLorentzVector tlv2;
	tlv2.SetXYZM(reco.at(recind.at(i)).momentum.x,reco.at(recind.at(i)).momentum.y,reco.at(recind.at(i)).momentum.z,reco.at(recind.at(i)).mass);
	std::cout << "n mc " << mc.size() << " rec ind " << recind.at(i) << " reco P "<< tlv2.P()<< "  mc ind " << mcind.at(i) << " truth P " << tlv.P() << " pdg_id " << mc.at(mcind.at(i)).PDG  << "  parent id " << parents.at(mc.at(mcind.at(i)).parents_begin) << " parent pdg id " << mc.at(parents.at(mc.at(mcind.at(i)).parents_begin)).PDG << std::endl;

	tlv.SetXYZM(mc.at(mcind.at(i+1)).momentum.x,mc.at(mcind.at(i+1)).momentum.y,mc.at(mcind.at(i+1)).momentum.z,mc.at(mcind.at(i+1)).mass);
	tlv2.SetXYZM(reco.at(recind.at(i+1)).momentum.x,reco.at(recind.at(i+1)).momentum.y,reco.at(recind.at(i+1)).momentum.z,reco.at(recind.at(i+1)).mass);
	std::cout << "n mc " << mc.size() << " rec ind " << recind.at(i+1) << " reco P "<< tlv2.P()<< "  mc ind " << mcind.at(i+1) << " truth P " << tlv.P() << " pdg_id " << mc.at(mcind.at(i+1)).PDG  << "  parent id " << parents.at(mc.at(mcind.at(i+1)).parents_begin) << " parent pdg id " << mc.at(parents.at(mc.at(mcind.at(i+1)).parents_begin)).PDG << std::endl;
	}
    }
    }*/
  return result;
}


ROOT::VecOps::RVec<float> 
ReconstructedParticle2MC::getRP2MC_p_func::operator() (ROOT::VecOps::RVec<int> recind, 
						       ROOT::VecOps::RVec<int> mcind, 
						       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
						       ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  ROOT::VecOps::RVec<float> result;
  result.resize(reco.size(),-1.);

  for (unsigned int i=0; i<recind.size();i++) {
    TLorentzVector tlv;
    tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
    result[recind.at(i)]=tlv.P();
  }

  if (recind.size()>reco.size()){ 
    std::cout << recind.size() <<"========="<<reco.size()<<std::endl;
     for (unsigned int i=0; i<recind.size();i++) {
       TLorentzVector tlv;
       tlv.SetXYZM(mc.at(mcind.at(i)).momentum.x,mc.at(mcind.at(i)).momentum.y,mc.at(mcind.at(i)).momentum.z,mc.at(mcind.at(i)).mass);
       TLorentzVector tlv2;
       tlv2.SetXYZM(reco.at(recind.at(i)).momentum.x,reco.at(recind.at(i)).momentum.y,reco.at(recind.at(i)).momentum.z,reco.at(recind.at(i)).mass);
       std::cout << "n mc " << mc.size() << " rec ind " << recind.at(i) << " reco P "<< tlv2.P()<< "  mc ind " << mcind.at(i) << " truth P " << tlv.P() << " pdg_id " << mc.at(mcind.at(i)).PDG << " parent_begin " <<  mc.at(mcind.at(i)).parents_begin << " parent_end " <<  mc.at(mcind.at(i)).parents_end << " daut_begin " <<  mc.at(mcind.at(i)).daughters_begin << " daut_end " <<  mc.at(mcind.at(i)).daughters_end <<std::endl;
     }
  }
  return result;
}


// -------------------------------------------------------------------------------------------------

// -- select RecoParticles associated with MC particles of a given PDG_id
//    Example use case: muons from JPsi, can not use the Muon collection because it oontains only the isolated muons

selRP_PDG::selRP_PDG( int arg_pdg, 
		      bool arg_chargedOnly ): m_PDG(arg_pdg), m_chargedOnly(arg_chargedOnly)  {} ;
std::vector<edm4hep::ReconstructedParticleData>  
ReconstructedParticle2MC::selRP_PDG::operator() (ROOT::VecOps::RVec<int> recind, 
						 ROOT::VecOps::RVec<int> mcind, 
						 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
						 ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  
  std::vector<edm4hep::ReconstructedParticleData> result;

  for (int i=0; i<recind.size();i++) {
      int reco_idx = recind.at(i);
      int mc_idx = mcind.at(i);
      int pdg = mc.at(mc_idx).PDG ;
      if ( m_chargedOnly ) {
        if ( reco.at( reco_idx ).charge ==0 ) continue;
      }
      if ( std::abs( pdg ) == std::abs( m_PDG)  ) {
         result.push_back( reco.at( reco_idx ) ) ;
      }
  }
  return result;
}

selRP_PDG_index::selRP_PDG_index( int arg_pdg, 
			    bool arg_chargedOnly ): m_PDG(arg_pdg), m_chargedOnly(arg_chargedOnly)  {} ;
ROOT::VecOps::RVec<int>
ReconstructedParticle2MC::selRP_PDG_index::operator() (ROOT::VecOps::RVec<int> recind, 
						 ROOT::VecOps::RVec<int> mcind, 
						 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
						 ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  
  ROOT::VecOps::RVec<int> result;

  for (int i=0; i<recind.size();i++) {
      int reco_idx = recind.at(i);
      int mc_idx = mcind.at(i);
      int pdg = mc.at(mc_idx).PDG ;
      if ( m_chargedOnly ) {
        if ( reco.at( reco_idx ).charge ==0 ) continue;
      }
      if ( std::abs( pdg ) == std::abs( m_PDG)  ) {
         result.push_back( reco_idx ) ;
      }
  }
  return result;
}

// -------------------------------------------------------------------------------------------------

// -- select RecoParticles associated with a charged hadron :
// -- take all charged RecoParticles that are not associated with  a MC lepton

std::vector<edm4hep::ReconstructedParticleData> 
ReconstructedParticle2MC::selRP_ChargedHadrons (ROOT::VecOps::RVec<int> recind, 
						ROOT::VecOps::RVec<int> mcind, 
						ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
						ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

  std::vector<edm4hep::ReconstructedParticleData> result;

  for (int i=0; i<recind.size();i++) {
      int reco_idx = recind.at(i);
      int mc_idx = mcind.at(i);
      int pdg = mc.at(mc_idx).PDG ;
      if ( reco.at( reco_idx ).charge == 0 ) continue;
      if ( std::abs( pdg ) == 11 || std::abs( pdg ) == 13 || std::abs( pdg ) == 15 ) continue ;
      result.push_back( reco.at( reco_idx ) ) ;
  }

  return result;
}

// -------------------------------------------------------------------------------------------------

// -- select RecoParticles associated with a list of MC particles (passed by their index in the Particle block)

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
ReconstructedParticle2MC::selRP_matched_to_list( ROOT::VecOps::RVec<int>  mcParticles_indices,
						 ROOT::VecOps::RVec<int> recind, 
						 ROOT::VecOps::RVec<int> mcind,
						 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,  
						 ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
  
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  results;
  
  edm4hep::ReconstructedParticleData dummy;
  dummy.energy = -9999;
  dummy.tracks_begin = -9999 ;

  for ( auto & idx: mcParticles_indices ) {

    // exclude unstable particles - e.g. the list may contain the index of
    // the mother
    if ( mc.at(idx).generatorStatus != 1 ) continue ;

    // is this MC particle associated with a Reco particle :
    bool found = false;
    for (int i=0; i<recind.size();i++) {
      int reco_idx = recind.at(i);
      int mc_idx = mcind.at(i);
      if ( mc_idx == idx ) {
        found = true;
        results.push_back( reco.at( reco_idx ) );
        break;
      }
    }
    // no Reco particle has been found for idx: add a dummy particle such that
    // one preserves the mapping with the input list
    if ( ! found) results.push_back( dummy );


  } // loop over the indices in the list

  return results;

}




// -------------------------------------------------------------------------------------------------

int ReconstructedParticle2MC::getTrack2MC_index (int track_index,
						 ROOT::VecOps::RVec<int> recind,
						 ROOT::VecOps::RVec<int> mcind,
						 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco) {
  int mc_index = -1;

      for (int i=0; i<recind.size();i++) {
          int reco_idx = recind.at(i);
          // keep only charged particles
          if ( reco.at( reco_idx ).charge == 0 ) continue;
          mc_index = mcind.at(i);
          if ( reco.at( reco_idx ).tracks_begin == track_index ) return mc_index;
      }
 return mc_index;
}





