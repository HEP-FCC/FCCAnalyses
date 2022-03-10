#include "JetTaggingUtils.h"
using namespace JetTaggingUtils;

ROOT::VecOps::RVec<int>
JetTaggingUtils::get_flavour(ROOT::VecOps::RVec<fastjet::PseudoJet> in,
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


get_ghostFlavour::get_ghostFlavour(int algo, float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_add1, float arg_add2)
{m_algo = algo; m_radius = arg_radius; m_exclusive = arg_exclusive; m_cut = arg_cut; m_sorted = arg_sorted; m_recombination = arg_recombination; m_add1 = arg_add1; m_add2 = arg_add2;}

ghostFlavour JetTaggingUtils::get_ghostFlavour::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> Particle, ROOT::VecOps::RVec<int> ind, std::vector<fastjet::PseudoJet> pseudoJets, int partonFlag) {



  ghostFlavour result;

  unsigned index = pseudoJets.size();
  std::vector<float> pdg(pseudoJets.size(),0);
  std::vector<float> ghostStatus(pseudoJets.size(),0);
  std::vector<int> MCindex(pseudoJets.size(),-1);


  std::vector<int> partonStatus = {20, 30};

  // In below loop ghosts are selected from MCParticle collection
  for (size_t i = 0; i < Particle.size(); ++i) {
    bool isGhost = false;

    if(!partonFlag){
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
        if (isGhost) ghostStatus.push_back(1);
      }
    }
    else{
      // Ghost partons are selected via chosen Pythia8 status codes
      if ((Particle[i].generatorStatus<partonStatus[1]) && (Particle[i].generatorStatus>partonStatus[0])) {
        isGhost = true;
        ghostStatus.push_back(1);
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
      if (isGhost) ghostStatus.push_back(2);

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
      if (isGhost) ghostStatus.push_back(2);
    }

    // Ghosts 4-mom is scaled by 10^-18  
    if (isGhost){
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
  }

  result.ghostStatus = ghostStatus;
  result.MCindex = MCindex;


  // Jet clustering algorithm is run according to user choice m_algo
  JetClusteringUtils::FCCAnalysesJet FCCAnalysesGhostJets;

  if (m_algo == 0) FCCAnalysesGhostJets = JetClustering::clustering_kt(m_radius, m_exclusive, m_cut, m_sorted, m_recombination)(pseudoJets);
  else if (m_algo == 1) FCCAnalysesGhostJets = JetClustering::clustering_antikt(m_radius, m_exclusive, m_cut, m_sorted, m_recombination)(pseudoJets);
  else if (m_algo == 2) FCCAnalysesGhostJets = JetClustering::clustering_cambridge(m_radius, m_exclusive, m_cut, m_sorted, m_recombination)(pseudoJets);
  else if (m_algo == 3) FCCAnalysesGhostJets = JetClustering::clustering_ee_kt(m_exclusive, m_cut, m_sorted, m_recombination)(pseudoJets);
  else if (m_algo == 4) FCCAnalysesGhostJets = JetClustering::clustering_ee_genkt(m_radius, m_exclusive, m_cut, m_sorted, m_recombination, m_add1)(pseudoJets);
  else if (m_algo == 5) FCCAnalysesGhostJets = JetClustering::clustering_genkt(m_radius, m_exclusive, m_cut, m_sorted, m_recombination, m_add1)(pseudoJets);
  else if (m_algo == 6) FCCAnalysesGhostJets = JetClustering::clustering_valencia(m_radius, m_exclusive, m_cut, m_sorted, m_recombination, m_add1, m_add2)(pseudoJets);
  else if (m_algo == 7) FCCAnalysesGhostJets = JetClustering::clustering_jade(m_radius, m_exclusive, m_cut, m_sorted, m_recombination)(pseudoJets);
  else return result;


  result.jets = FCCAnalysesGhostJets;

  // Jet constituents and pseudojets are read from resulting jet struct
  auto ghostJets_ee_kt = JetClusteringUtils::get_pseudoJets(FCCAnalysesGhostJets);

  auto jetconstituents = JetClusteringUtils::get_constituents(FCCAnalysesGhostJets);






  // Flav vector is defined before jets are check for clustered ghosts
  std::vector<std::vector<float>> flav_vector;


  std::vector<float> partonFlavs;
  std::vector<float> hadronFlavs;
  for (auto& consti_index : jetconstituents) {

  float partonFlav = 0;
  float partonMom2 = 0;
  float partonMom2_b = 0;
  float partonMom2_c = 0;
  float hadronFlav = 0;
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
  }


  flav_vector.push_back(partonFlavs);
  flav_vector.push_back(hadronFlavs);

  result.flavour = flav_vector;
  return result;

}

std::vector<std::vector<float>> JetTaggingUtils::get_flavour(ghostFlavour ghostStruct){
  return ghostStruct.flavour;
}

JetClusteringUtils::FCCAnalysesJet JetTaggingUtils::get_jets(ghostFlavour ghostStruct){
  return ghostStruct.jets;
}

std::vector<float> JetTaggingUtils::get_ghostStatus(ghostFlavour ghostStruct){
  return ghostStruct.ghostStatus;
}

std::vector<int> JetTaggingUtils::get_MCindex(ghostFlavour ghostStruct){
  return ghostStruct.MCindex;
}




ROOT::VecOps::RVec<int>
JetTaggingUtils::get_btag(ROOT::VecOps::RVec<int> in,
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
JetTaggingUtils::get_ctag(ROOT::VecOps::RVec<int> in,
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
JetTaggingUtils::get_ltag(ROOT::VecOps::RVec<int> in,
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
JetTaggingUtils::get_gtag(ROOT::VecOps::RVec<int> in,
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

JetTaggingUtils::sel_tag::sel_tag(bool arg_pass): m_pass(arg_pass) {};
ROOT::VecOps::RVec<fastjet::PseudoJet>
JetTaggingUtils::sel_tag::operator()(ROOT::VecOps::RVec<bool> tags,
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
