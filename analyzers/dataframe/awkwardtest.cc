#include "awkwardtest.h"

#include <iostream>
#include <cstdlib>
#include <vector>

#include "awkward/Content.h"
#include "awkward/io/json.h"
#include "awkward/array/NumpyArray.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

#include "VertexFitterActs.h"


bool awkwardtest(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,  
		 ROOT::VecOps::RVec<edm4hep::TrackState> tracks){


  ROOT::VecOps::RVec<int> rp_ind;
  ROOT::VecOps::RVec<int> tk_ind;

  for (size_t i = 0; i < recop.size(); ++i) {
    auto & p = recop[i];
    if (p.tracks_begin<tracks.size()) {
      rp_ind.push_back(i);
      tk_ind.push_back(p.tracks_begin);
    }
  }
     
  awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));
  for (size_t i = 0; i < rp_ind.size(); ++i) {
    builder.beginlist();
    builder.integer(rp_ind.at(i));
    builder.integer(tk_ind.at(i));
    builder.endlist();
  }

  std::shared_ptr<awkward::Content> array = builder.snapshot();
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(3, false, nullptr, awkward::util::Parameters(), 0, 0);

  int64_t length = comb->length();
  std::cout << "ntracks " << tracks.size()<< "  length 3 comb " << length << std::endl;

  for (int64_t i=0;i<length;i++){
    std::shared_ptr<awkward::Content> sel = comb->getitem_at(i);
    awkward::ContentPtr other  = comb.get()->getitem_at(i);

    awkward::ContentPtr content(nullptr);
    content = comb.get()->getitem_at(i);

    const awkward::NumpyArray* raw = dynamic_cast<const awkward::NumpyArray*>(content.get());
    std::cout << "test data content len " << raw->length() << std::endl;


    //    uint8_t* data_ptr = reinterpret_cast<uint8_t*>(data.data());

    //awkward::NumpyArray *test2 = dynamic_cast<awkward::NumpyArray*>(other);

//awkward::NumpyArray test = sel->data();
    std::cout << "json "<<sel->tojson(false, 1) << std::endl;
    std::cout << "sel len " << sel->length() << std::endl;
    //std::shared_ptr<awkward::NumpyArray> toto = comb->getitem_at(i);
    const awkward::NumpyArray *test = dynamic_cast<const awkward::NumpyArray*>(sel.get());
    std::cout << "is scalar sel  " << sel->isscalar() << std::endl;
    std::cout << "is scalar comb " << comb->isscalar() << std::endl;
    std::cout << "test data len " << test->length() << std::endl;
    
    //std::make_shared<awkward::NumpyArray> test = std::dynamic_cast<awkward::NumpyArray*>(sel.get());
//sel->data()
    //const std::string val = sel.get()->tojson(false, 1);
   
    //std::cout <<"str " << s << std::endl;
    //VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterActs::VertexFitterFullBilloir(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
    //											    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks ){

  } 
  return 0;
}
