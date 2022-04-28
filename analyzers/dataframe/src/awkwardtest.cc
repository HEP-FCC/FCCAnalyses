#include "awkwardtest.h"

#include <iostream>
#include <cstdlib>
#include <vector>

#include "awkward/Content.h"
#include "awkward/io/json.h"
#include "awkward/array/NumpyArray.h"
#include "awkward/array/RecordArray.h"
#include "awkward/array/Record.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

#include "VertexFitterActs.h"
#include "VertexFitterSimple.h"
#include "ReconstructedParticle.h"


ROOT::VecOps::RVec<float> awkwardtest(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,  
				      ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
				      ROOT::VecOps::RVec<int> recind, 
				      ROOT::VecOps::RVec<int> mcind, 
				      ROOT::VecOps::RVec<edm4hep::MCParticleData> mc){

  ROOT::VecOps::RVec<float> result;
  ROOT::VecOps::RVec<int> rp_ind;
  ROOT::VecOps::RVec<int> tk_ind;

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> seltracks = VertexingUtils::selTracks(0.,3.,0.,3.)( recop, tracks);
  VertexingUtils::FCCAnalysesVertex ThePVertex = VertexFitterSimple::VertexFitter(0,seltracks, tracks );

  int PV_ntrk   = ThePVertex.ntracks;
  float PV_chi2 = ThePVertex.vertex.chi2;
  ROOT::VecOps::RVec<int> reco_ind = ThePVertex.reco_ind;

  std::cout << "ntracks PV " << PV_ntrk << " nreco ind " <<reco_ind.size() << std::endl;

  for (size_t i = 0; i < recop.size(); ++i) {
    auto & p = recop[i];
    if (p.tracks_begin<tracks.size()) {
      if(std::find(reco_ind.begin(), reco_ind.end(), p.tracks_begin) != reco_ind.end()) continue;
      rp_ind.push_back(i);
      tk_ind.push_back(p.tracks_begin);
    }
  }

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco;
  for (size_t i = 0; i < rp_ind.size(); ++i) {
    reco.push_back(recop[rp_ind.at(i)]);
  }
  std::cout <<"beofre"<<std::endl;
  ROOT::VecOps::RVec<int> pions = ReconstructedParticle2MC::selRP_PDG_index(211,true)(recind, mcind, recop, mc) ;
  ROOT::VecOps::RVec<int> kaons = ReconstructedParticle2MC::selRP_PDG_index(321,true)(recind, mcind, recop, mc) ;
  
  std::cout << "n pions " << pions.size() << std::endl;
  std::cout << "n kaons " << kaons.size() << std::endl;

  awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));
  for (size_t i = 0; i < rp_ind.size(); ++i) {
    builder.beginlist();
    builder.integer(rp_ind.at(i));
    builder.integer(tk_ind.at(i));
    builder.endlist();
  }

  std::shared_ptr<awkward::Content> array = builder.snapshot();  
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(2, false, nullptr, awkward::util::Parameters(), 0, 0);
  int64_t length = comb->length();
 
  std::cout << "recarray ntracks     : " << tracks.size()<< "  length 2 comb " << length << std::endl;

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> vec_rp;
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> vec_tk;
  
  //loop over combinations
  for (int64_t i=0;i<length;i++){
    awkward::ContentPtr item = comb.get()->getitem_at(i);
    awkward::Record* recitem = dynamic_cast<awkward::Record*>(item.get());
    std::vector<std::shared_ptr<awkward::Content>> contentvec = recitem->contents();
    //loop over items of the comb
    ROOT::VecOps::RVec<int> tmpvec_rp;
    ROOT::VecOps::RVec<int> tmpvec_tk;

    for (size_t j=0;j<contentvec.size();j++){
      awkward::NumpyArray* numpyraw = dynamic_cast<awkward::NumpyArray*>(contentvec.at(j).get());
      int64_t lengthnp = numpyraw->length();

      //loop over the items of the items and get the data (if nested array)
      for (int64_t k=0;k<lengthnp;k++){
	awkward::ContentPtr item2 = numpyraw->getitem_at(k);
	awkward::NumpyArray* npitem = dynamic_cast<awkward::NumpyArray*>(item2.get());	
	int32_t value = *reinterpret_cast<int32_t*>(npitem->data());
	if (k==0)tmpvec_rp.push_back(value);
	else tmpvec_tk.push_back(value);
      }
      //in case the data structure is a simple array (and not an array with a nested array)
      if (lengthnp<0){
	int32_t value = *reinterpret_cast<int32_t*>(numpyraw->data());
      }
    }

    int charge=0;
    bool pcut=false;
    for (size_t k=0;k<tmpvec_rp.size();k++){
      charge+=recop[tmpvec_rp.at(k)].charge;
      if (ReconstructedParticle::get_p(recop[tmpvec_rp.at(k)])<2.)pcut=true;
    }
    if (charge!=0)continue;
    if (pcut==true)continue;
    
    //PID
    //if( (std::find(pions.begin(), pions.end(), tmpvec_rp.at(0)) != pions.end()) && (std::find(pions.begin(), pions.end(), tmpvec_rp.at(1)) != pions.end())) continue;
    //if( (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(0)) != kaons.end()) && (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(1)) != kaons.end())) continue;

    float mass=0;
    if ( (std::find(pions.begin(), pions.end(), tmpvec_rp.at(0)) != pions.end()) && (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(1)) != kaons.end())){
      TLorentzVector tlvpion;
      tlvpion.SetXYZM(recop.at(tmpvec_rp.at(0)).momentum.x, recop.at(tmpvec_rp.at(0)).momentum.y, recop.at(tmpvec_rp.at(0)).momentum.z, 0.13957039000000002);
      TLorentzVector tlvkaon;
      tlvkaon.SetXYZM(recop.at(tmpvec_rp.at(1)).momentum.x, recop.at(tmpvec_rp.at(1)).momentum.y, recop.at(tmpvec_rp.at(1)).momentum.z, 0.49367700000000003);
      tlvpion+=tlvkaon;
      mass=tlvpion.M();
    }
    else if ( (std::find(pions.begin(), pions.end(), tmpvec_rp.at(1)) != pions.end()) && (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(0)) != kaons.end())){
      TLorentzVector tlvpion;
      tlvpion.SetXYZM(recop.at(tmpvec_rp.at(1)).momentum.x, recop.at(tmpvec_rp.at(1)).momentum.y, recop.at(tmpvec_rp.at(1)).momentum.z, 0.13957039000000002);
      TLorentzVector tlvkaon;
      tlvkaon.SetXYZM(recop.at(tmpvec_rp.at(0)).momentum.x, recop.at(tmpvec_rp.at(0)).momentum.y, recop.at(tmpvec_rp.at(0)).momentum.z, 0.49367700000000003);
      tlvpion+=tlvkaon;
      mass=tlvpion.M();
    }
    else mass=-9999;
    //float mass=build_invmass(recop,tmpvec_rp);
    


    if (fabs(mass-1.86483)>0.05)continue;



    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles;
    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks;
    for (size_t k=0;k<tmpvec_rp.size();k++){
      recoparticles.push_back(recop.at(tmpvec_rp.at(k)));
      thetracks.push_back(tracks.at(tmpvec_tk.at(k)));
    }
 
    //VertexingUtils::FCCAnalysesVertex TheVertexActs = VertexFitterActs::VertexFitterFullBilloir(recoparticles, tracks );
    VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterSimple::VertexFitter(0,recoparticles, tracks );
    float chi2 = TheVertex.vertex.chi2;
  
    if (chi2<0.01)continue;
    if (chi2>10.)continue;

    std::cout << "SELECTED----------------"<<std::endl;
    std::cout << "charge " << charge << std::endl;
    std::cout << "mass   " << mass << std::endl;
    std::cout << "chi2   " << chi2 << std::endl;
    std::cout << "ntrk   " << TheVertex.ntracks << std::endl;
    vec_rp.push_back(tmpvec_rp);
    vec_tk.push_back(tmpvec_tk);
    result.push_back(mass);
  }

  std::cout << "nresults " << result.size()<<std::endl;
  return result;
}


float build_invmass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, ROOT::VecOps::RVec<int> index){
  float result=0;
  TLorentzVector tlv;
  for (size_t i=0;i<index.size();i++){
    TLorentzVector tmp_tlv = ReconstructedParticle::get_tlv(recop[index.at(i)]);
    tlv+=tmp_tlv;
  }
  return tlv.M();
}
