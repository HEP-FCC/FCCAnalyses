#include "FCCAnalyses/JetTaggingUtils.h"

namespace FCCAnalyses{

namespace JetTaggingUtils{

ROOT::VecOps::RVec<int> get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in,
                                    ROOT::VecOps::RVec<edm4hep::MCParticleData> MCin)
{
  ROOT::VecOps::RVec<int> result(in.size(),0);

  int loopcount =0;
  for (size_t i = 0; i < MCin.size(); ++i) {
    auto & parton = MCin[i];
    //Select partons only (for pythia8 71-79, for pythia6 2):
    if ((parton.generatorStatus>80 ||
         parton.generatorStatus<70) &&
        parton.generatorStatus != 2 ) continue;
    if (std::abs(parton.PDG) > 5 && parton.PDG!=21) continue;
    ROOT::Math::PxPyPzMVector lv(parton.momentum.x, parton.momentum.y,
                                 parton.momentum.z, parton.mass);

    for (size_t j = 0; j < in.size(); ++j) {
      auto & p = in[j];
      //float dEta = lv.Eta() - p.eta();
      //float dPhi = lv.Phi() - p.phi();
      //float deltaR = sqrt(dEta*dEta+dPhi*dPhi);
      //if (deltaR <= 0.5 && gRandom->Uniform() <= efficiency) result[j] = true;

      Float_t dot = p.px() * parton.momentum.x
                  + p.py() * parton.momentum.y
                  + p.pz() * parton.momentum.z;
      Float_t lenSq1 = p.px() * p.px()
                     + p.py() * p.py()
                     + p.pz() * p.pz();
      Float_t lenSq2 = parton.momentum.x * parton.momentum.x
                     + parton.momentum.y * parton.momentum.y
                     + parton.momentum.z * parton.momentum.z;
      Float_t norm = sqrt(lenSq1*lenSq2);
      Float_t angle = acos(dot/norm);

      if (angle <= 0.3) {
        if (result[j]==21 or result[j]==0) {
          // if no match before, or matched to gluon, match to
          // this particle (favour quarks over gluons)
          result[j] = std::abs ( parton.PDG );
        }
        else if (parton.PDG!=21) {
          // if matched to quark, and this is a quark, favour
          // heavier flavours
          result[j] = std::max(result[j], std::abs ( parton.PDG ));
        } else {
          // if matched to quark, and this is a gluon, keep
          // previous result (favour quark)
           ;
        }
       }


    }
  }

  return result;
}

ROOT::VecOps::RVec<int> find_ghosts(const ROOT::VecOps::RVec<edm4hep::MCParticleData> & Particle,
                                const ROOT::VecOps::RVec<int> & ind) {

  ROOT::VecOps::RVec<int> MCindices;

  std::vector<int> partonStatus = {20, 30};

  int partonFlag;

  // In loop below ghosts are selected from MCParticle collection
  for (size_t i = 0; i < Particle.size(); ++i) {
    bool isGhost = false;


    // Ghost partons as any partons that do not have partons as daughters
    if (std::abs(Particle[i].PDG)<=5||Particle[i].PDG==21) {
      isGhost = true;
      auto daughters = MCParticle::get_list_of_particles_from_decay(i, Particle, ind);
      for(auto& daughter_index : daughters){
        if (std::abs(Particle[daughter_index].PDG)<=5||Particle[daughter_index].PDG==21) {
          isGhost = false;
          break;
        }
      }
    }


    // Ghost hadrons are selected as b/c hadrons that do not have b/c hadrons as daughters
    if ((std::abs(int((Particle[i].PDG/100))%10)==5)||(std::abs(int((Particle[i].PDG/1000))%10)==5)){
      isGhost = true;
      auto daughters = MCParticle::get_list_of_particles_from_decay(i, Particle, ind);
      for(auto& daughter_index : daughters){
        if((std::abs(int((Particle[daughter_index].PDG/100))%10)==5)||(std::abs(int((Particle[daughter_index].PDG/1000))%10)==5)){
          isGhost = false;
          break;
        }
      }
    
    }
    else if ((std::abs(int((Particle[i].PDG/100))%10)==4)||(std::abs(int((Particle[i].PDG/1000))%10)==4)){
      isGhost = true;
      auto daughters = MCParticle::get_list_of_particles_from_decay(i, Particle, ind);
      for(auto& daughter_index : daughters){
        if((std::abs(int((Particle[daughter_index].PDG/100))%10)==4)||(std::abs(int((Particle[daughter_index].PDG/1000))%10)==4)){
          isGhost = false;
          break;
        }
      }
    }
    if (isGhost) MCindices.push_back(i);
  }
  return MCindices;
}

JetClusteringUtils::FCCAnalysesJet set_flavour(const ROOT::VecOps::RVec<edm4hep::MCParticleData> & Particle,
                                const ROOT::VecOps::RVec<int> & MCindices,
                                JetClusteringUtils::FCCAnalysesJet & jets,
                                std::vector<fastjet::PseudoJet> & pseudoJets) {
  unsigned int index = pseudoJets.size();
  ROOT::VecOps::RVec<int> pdg(pseudoJets.size(),0);
  ROOT::VecOps::RVec<int> ghostStatus(pseudoJets.size(),0);
  ROOT::VecOps::RVec<int> MCindex(pseudoJets.size(),-1);

  ROOT::VecOps::RVec<int> partonStatus = {20, 30};
  
  // In loop below ghosts are selected from MCParticle collection
  for (auto & i : MCindices) {
  
    // Ghost partons as any partons that do not have partons as daughters
    if (std::abs(Particle[i].PDG)<=5||Particle[i].PDG==21) {
      ghostStatus.push_back(1);
    }
  
  
    // Ghost hadrons are selected as b/c hadrons that do not have b/c hadrons as daughters
    else if ((std::abs(int((Particle[i].PDG/100))%10)==5)||(std::abs(int((Particle[i].PDG/1000))%10)==5)){
      ghostStatus.push_back(2);
  
    }
  
    else if ((std::abs(int((Particle[i].PDG/100))%10)==4)||(std::abs(int((Particle[i].PDG/1000))%10)==4)){
      ghostStatus.push_back(2);
    }
    else{
      // This should never be executed and would indicate a bug in ghost finding
      return jets;
    }
  
    // Ghosts 4-mom is scaled by 10^-18  
  
    pdg.push_back(Particle[i].PDG);
    MCindex.push_back(i);
    // the double conversion here is verbose but for precision if I recall...
    double px = Particle[i].momentum.x;//*pow(10, -1);
    double py = Particle[i].momentum.y;
    double pz = Particle[i].momentum.z;
    double m = Particle[i].mass;
    double  E = sqrt(px*px + py*py + pz*pz + m*m);
    pseudoJets.emplace_back(px*pow(10, -18), py*pow(10, -18), pz*pow(10, -18), E*pow(10, -18));
    pseudoJets.back().set_user_index(index);
    ++index;
  
  }
  JetClusteringUtils::flav_details flavour_details;

  flavour_details.ghostStatus = ghostStatus;

  flavour_details.MCindex = MCindex;


  // Jet clustering algorithm is run according to user choice m_algo
  JetClusteringUtils::FCCAnalysesJet FCCAnalysesGhostJets;
  std::vector<fastjet::PseudoJet> pseudoJets_(pseudoJets.begin(), pseudoJets.end());
  if (jets.clustering_algo == "ee-kt") {
    FCCAnalysesGhostJets = JetClustering::clustering_ee_kt(jets.clustering_params[0], jets.clustering_params[1], jets.clustering_params[2], jets.clustering_params[3])(pseudoJets_);
  }
  /*
  else if (jets.clustering_algo == "anti-kt") FCCAnalysesGhostJets = JetClustering::clustering_antikt(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3], clustering_params[4])(pseudoJets);
  else if (jets.clustering_algo == "cambridge") FCCAnalysesGhostJets = JetClustering::clustering_cambridge(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3], clustering_params[4])(pseudoJets);
  else if (jets.clustering_algo == "ee-kt") FCCAnalysesGhostJets = JetClustering::clustering_ee_kt(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3])(pseudoJets);
  else if (jets.clustering_algo == "ee-genkt") FCCAnalysesGhostJets = JetClustering::clustering_ee_genkt(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3], clustering_params[4], m_add1)(pseudoJets);
  else if (jets.clustering_algo == "genkt") FCCAnalysesGhostJets = JetClustering::clustering_genkt(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3], clustering_params[4], clustering_params[5])(pseudoJets);
  else if (jets.clustering_algo == "valencia") FCCAnalysesGhostJets = JetClustering::clustering_valencia(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3], clustering_params[4], clustering_params[5], clustering_params[6])(pseudoJets);
  else if (jets.clustering_algo == "jade") FCCAnalysesGhostJets = JetClustering::clustering_jade(clustering_params[0], clustering_params[1], clustering_params[2], clustering_params[3], clustering_params[4])(pseudoJets);
  */
  else return jets;
  
  //result.jets = FCCAnalysesGhostJets;
  flavour_details.ghost_pseudojets = FCCAnalysesGhostJets.jets;
  flavour_details.ghost_jetconstituents = FCCAnalysesGhostJets.constituents;
  
  // Jet constituents and pseudojets are read from resulting jet struct
  
  auto ghostJets_ee_kt = JetClusteringUtils::get_pseudoJets(FCCAnalysesGhostJets);
  
  auto jetconstituents = JetClusteringUtils::get_constituents(FCCAnalysesGhostJets);
  
  
  
  
  // Flav vector is defined before jets are checked for clustered ghosts
  //std::vector<std::vector<int>> flav_vector;
  ROOT::VecOps::RVec<int> flav_vector;
  
  
  ROOT::VecOps::RVec<int> partonFlavs;
  ROOT::VecOps::RVec<int> hadronFlavs;
  for (auto& consti_index : jetconstituents) {
    int partonFlav = 0;
    float partonMom2 = 0;
    float partonMom2_b = 0;
    float partonMom2_c = 0;
  int hadronFlav = 0;
  float hadronMom2_b = 0;
  float hadronMom2_c = 0;
    for (auto& i : consti_index) {

      //Parton-flav loop 
      if (ghostStatus[i]==1) {
        if (std::abs(pdg[i])==5){
          if (pseudoJets[i].modp2()>partonMom2_b){
            partonFlav = pdg[i];
            partonMom2_b = pseudoJets[i].modp2();
          }
        }
        else if ((std::abs(pdg[i])==4) && (std::abs(partonFlav)<5)) {
          if (pseudoJets[i].modp2()>partonMom2_c){
            partonFlav = pdg[i];
            partonMom2_c = pseudoJets[i].modp2();
          }
        }
        else if (((std::abs(pdg[i])==3) || (std::abs(pdg[i])==2) || (std::abs(pdg[i])==1) || (std::abs(pdg[i])==21)) && ((std::abs(partonFlav)<4) || (std::abs(partonFlav)==21))) {
          if (pseudoJets[i].modp2()>partonMom2){
            partonFlav = pdg[i];
            partonMom2 = pseudoJets[i].modp2();
          }
        }
      }
      
      // Hadron-flav loop    
      if (ghostStatus[i]==2) {
        if ((std::abs(int((pdg[i]/100))%10)==5)||(std::abs(int((pdg[i]/1000))%10)==5)){
          if (pseudoJets[i].modp2()>hadronMom2_b){
            hadronFlav = ((pdg[i]<0)-(pdg[i]>0))*5;
            hadronMom2_b = pseudoJets[i].modp2();
          }
        }
        else if (((std::abs(int((pdg[i]/100))%10)==4)||(std::abs(int((pdg[i]/1000))%10)==4)) && (std::abs(hadronFlav)<5)) {
          if (pseudoJets[i].modp2()>hadronMom2_c){
            hadronFlav = ((pdg[i]>0)-(pdg[i]<0))*4;
            hadronMom2_c = pseudoJets[i].modp2();
          }
        }
      }
    }
    partonFlavs.push_back(partonFlav);
    hadronFlavs.push_back(hadronFlav);
    if ((std::abs(hadronFlav)>=4)){
      flav_vector.push_back(hadronFlav);
    }
    else if ((hadronFlav<=3) && ((partonFlav<=3)||(partonFlav==21))){
      flav_vector.push_back(partonFlav);
    }
    else{
      flav_vector.push_back(0);
    }

  }

  flavour_details.parton_flavour = partonFlavs;
  flavour_details.hadron_flavour = hadronFlavs;

  //jets.flavour_details = &flavour_details;
  jets.flavour_details = flavour_details;
  
  auto & pseudojets = jets.jets;
  auto & ghost_pseudojets = jets.flavour_details.ghost_pseudojets;
  
  for(int i=0; i<pseudojets.size(); ++i){
    if((pseudojets[i].px()!=ghost_pseudojets[i].px())||(pseudojets[i].py()!=ghost_pseudojets[i].py())||(pseudojets[i].pz()!=ghost_pseudojets[i].pz())){
      std::cout<<"no match to float precision... "<<std::endl;
      //return jets;
    }
  }
  //int pseudojet_counter[pseudojets.size()];
  //std::iota(pseudojet_counter, pseudojet_counter+pseudojets.size(), 0);
  
  jets.flavour = flav_vector;
  return jets;
}

ROOT::VecOps::RVec<int> get_flavour(const JetClusteringUtils::FCCAnalysesJet & jets){
  return jets.flavour;
}

JetClusteringUtils::flav_details get_flavour_details(const JetClusteringUtils::FCCAnalysesJet & jets){
  return jets.flavour_details;
}

ROOT::VecOps::RVec<int> get_flavour(const ROOT::VecOps::RVec<edm4hep::MCParticleData> & Particle,
                 const ROOT::VecOps::RVec<int> & ind,
                 JetClusteringUtils::FCCAnalysesJet & jets,
                           std::vector<fastjet::PseudoJet> & pseudoJets){
  auto MCindices = JetTaggingUtils::find_ghosts(Particle, ind);
  jets = JetTaggingUtils::set_flavour(Particle, MCindices, jets, pseudoJets);

  return get_flavour(jets);

}


ROOT::VecOps::RVec<int>
get_btag(ROOT::VecOps::RVec<int> in,
                          float efficiency, float mistag_c,
                          float mistag_l, float mistag_g) {

  ROOT::VecOps::RVec<int> result(in.size(),0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) ==  5 && gRandom->Uniform() <= efficiency) result[j] = 1;
    if (in.at(j) ==  4 && gRandom->Uniform() <= mistag_c) result[j] = 1;
    if (in.at(j)  <  4 && gRandom->Uniform() <= mistag_l) result[j] = 1;
    if (in.at(j) == 21 && gRandom->Uniform() <= mistag_g) result[j] = 1;
  }
  return result;
}

ROOT::VecOps::RVec<int>
get_ctag(ROOT::VecOps::RVec<int> in,
                          float efficiency, float mistag_b,
                          float mistag_l, float mistag_g) {

  ROOT::VecOps::RVec<int> result(in.size(),0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) ==  4 && gRandom->Uniform() <= efficiency) result[j] = 1;
    if (in.at(j) ==  5 && gRandom->Uniform() <= mistag_b) result[j] = 1;
    if (in.at(j)  <  4 && gRandom->Uniform() <= mistag_l) result[j] = 1;
    if (in.at(j) == 21 && gRandom->Uniform() <= mistag_g) result[j] = 1;
  }
  return result;
}

ROOT::VecOps::RVec<int>
get_ltag(ROOT::VecOps::RVec<int> in,
                          float efficiency, float mistag_b,
                          float mistag_c, float mistag_g) {

  ROOT::VecOps::RVec<int> result(in.size(),0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) <  4  && gRandom->Uniform() <= efficiency) result[j] = 1;
    if (in.at(j) ==  5 && gRandom->Uniform() <= mistag_b) result[j] = 1;
    if (in.at(j) ==  4 && gRandom->Uniform() <= mistag_c) result[j] = 1;
    if (in.at(j) == 21 && gRandom->Uniform() <= mistag_g) result[j] = 1;
  }
  return result;
}

ROOT::VecOps::RVec<int>
get_gtag(ROOT::VecOps::RVec<int> in,
                          float efficiency, float mistag_b,
                          float mistag_c, float mistag_l) {

  ROOT::VecOps::RVec<int> result(in.size(),0);

  for (size_t j = 0; j < in.size(); ++j) {
    if (in.at(j) == 21 && gRandom->Uniform() <= efficiency) result[j] = 1;
    if (in.at(j) ==  5 && gRandom->Uniform() <= mistag_b) result[j] = 1;
    if (in.at(j) ==  4 && gRandom->Uniform() <= mistag_c) result[j] = 1;
    if (in.at(j)  <  4 && gRandom->Uniform() <= mistag_l) result[j] = 1;
  }
  return result;
}

sel_tag::sel_tag(bool arg_pass): m_pass(arg_pass) {};
ROOT::VecOps::RVec<fastjet::PseudoJet>
sel_tag::operator()(ROOT::VecOps::RVec<bool> tags,
                                     ROOT::VecOps::RVec<fastjet::PseudoJet> in){
  ROOT::VecOps::RVec<fastjet::PseudoJet> result;
  for (size_t i = 0; i < in.size(); ++i) {
    if (m_pass) {
      if (tags.at(i)) result.push_back(in.at(i));
    }
    else {
      if (!tags.at(i)) result.push_back(in.at(i));
    }
  }
  return result;
}

}//end NS JetTaggingUtils

}//end NS FCCAnalyses
