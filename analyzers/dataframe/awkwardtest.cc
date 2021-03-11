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
  std::cout << "array class name " << array.get()->classname()<<std::endl;
  
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(3, false, nullptr, awkward::util::Parameters(), 0, 0);
  std::cout << "comb class name " << comb.get()->classname() << std::endl;
  
  //std::shared_ptr<awkward::RecordArray> comb2  = array.get()->combinations(3, false, nullptr, awkward::util::Parameters(), 0, 0);
  //std::cout << "comb2 class name " << comb.get()->classname() << std::endl;

  //awkward::RecordArray comb3  = array.get()->combinations(3, false, nullptr, awkward::util::Parameters(), 0, 0);
  //std::cout << "comb3 class name " << comb.classname() << std::endl;

  int64_t length = comb->length();
  std::cout << "ntracks " << tracks.size()<< "  length 3 comb " << length << std::endl;
  awkward::RecordArray* recarray = dynamic_cast<awkward::RecordArray*>(comb.get());
  int64_t length2 = recarray->length();
  std::cout << "ntracks " << tracks.size()<< "  length 3 comb " << length2 << std::endl;

  for (int64_t i=0;i<length;i++){
    awkward::ContentPtr item = recarray->getitem_at(i);
        std::cout << "item  " << item<< std::endl;
        std::cout << "item class name " << item.get()->classname()<< std::endl;

    awkward::NumpyArray* rawcontent666 = dynamic_cast<awkward::NumpyArray*>(item.get());
        std::cout << "rawcontent66  " << rawcontent666 << std::endl;



    awkward::RecordArray* rec = dynamic_cast<awkward::RecordArray*>(item.get());
    awkward::Record* rec1 = dynamic_cast<awkward::Record*>(item.get());
    std::shared_ptr<const awkward::RecordArray> rec2 = rec1->array();    
    const awkward::NumpyArray* rawcontent = dynamic_cast<const awkward::NumpyArray*>(rec2.get());


    //awkward::RecordArray* rec2 = rec1->array();

    //awkward::RecordArray rec2 = item->array();
    std::cout << "item class name " << item.get()->classname() << std::endl;

    std::cout << "rec  " << rec << std::endl;
    std::cout << "rec1  " << rec1 << std::endl;
    std::cout << "rec2  " << rec2.get()->classname() << std::endl;
    std::cout << "rawcontent  " << rawcontent << std::endl;
    std::cout << "rec class name " << rec->classname() << std::endl;







    std::shared_ptr<awkward::Content> test1 = comb->getitem_at(i);
    //const awkward::Record* rec = dynamic_cast<awkward::Record*>(test1.get());
    //std::cout << "rec class name " << rec->classname() << std::endl;

    //const awkward::RecordArray ra = rec->array();
    //std::cout << ra.classname() << std::endl;


    const awkward::ContentPtr         test2 = comb->getitem_at(i);
    const awkward::FormPtr            test3 = test2.get()->form(false);

    //const awkward::RecordArray test4 = comb->getitem_at(i);
    //std::shared_ptr<awkward::RecordArray> test5 = comb->getitem_at(i);

    awkward::RecordArray* rarray1 = dynamic_cast<awkward::RecordArray*>(test1.get());


    std::cout << "test1 " << test1 << std::endl;
    std::cout << "test2 " << test2 << std::endl;
    std::cout << "test3 " << test3 << std::endl;
    std::cout << "test1 class name " << comb->getitem_at(i)->classname() << std::endl;
   std::cout << test1.get()->tostring() << std::endl;

    awkward::NumpyArray* rawcontent1 = dynamic_cast<awkward::NumpyArray*>(test1.get());
    awkward::NumpyArray* rawcontent2 = dynamic_cast<awkward::NumpyArray*>(test2.get());
    awkward::NumpyArray* rawcontent3 = dynamic_cast<awkward::NumpyArray*>(test3.get());
    awkward::NumpyArray* rawcontent4 = dynamic_cast<awkward::NumpyArray*>(rarray1);
    

    std::cout << "rawcontent1 " << rawcontent1 << std::endl;
    std::cout << "rawcontent2 " << rawcontent2 << std::endl;
    std::cout << "rawcontent3 " << rawcontent3 << std::endl;
    std::cout << "rawcontent4 " << rawcontent4 << std::endl;

   
    
    //const awkward::ContentPtr mytest = sel.get();
    //std::cout <<"my test " <<mytest<<std::endl;
    
    //awkward::ContentPtr other  = comb.get()->getitem_at(i);
    //awkward::NumpyArray *test2 = dynamic_cast<awkward::NumpyArray*>(other);

    std::cout << "json test1 " << test1->tojson(false, 1) << std::endl;
    std::cout << "len  test1 " << test1->length() << std::endl;
    const awkward::NumpyArray *test = dynamic_cast<const awkward::NumpyArray*>(test1.get());
    std::cout << "test " << test << std::endl;
    
    std::cout << "is scalar test1  " << test1->isscalar() << std::endl;
    std::cout << "is scalar test2  " << test2->isscalar() << std::endl;
    std::cout << "is scalar comb   " << comb->isscalar() << std::endl;

    //produces a seg fault
    std::cout << "test data len " << test->length() << std::endl;

    
    awkward::ContentPtr content(nullptr);
    content = comb.get()->getitem_at(i);
    const awkward::NumpyArray* raw = dynamic_cast<const awkward::NumpyArray*>(content.get());
    //produces a seg fault as well
    std::cout << "test data content len " << raw->length() << std::endl;

    

    //std::shared_ptr<awkward::NumpyArray> toto = comb->getitem_at(i);

    //awkward::NumpyArray test = sel->data();

    //std::make_shared<awkward::NumpyArray> test = std::dynamic_cast<awkward::NumpyArray*>(sel.get());
//sel->data()
    //const std::string val = sel.get()->tojson(false, 1);
   
    //std::cout <<"str " << s << std::endl;
    //VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterActs::VertexFitterFullBilloir(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
    //											    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks ){

        //    uint8_t* data_ptr = reinterpret_cast<uint8_t*>(data.data());

  } 
  return 0;
}
