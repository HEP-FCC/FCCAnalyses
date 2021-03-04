#include "awkwardtest.h"

#include <iostream>
#include <cstdlib>

#include "awkward/Content.h"
#include "awkward/io/json.h"

#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"
#include <vector>


bool awkwardtest(){


  //This works
  int at = std::atoi("-2");
  
  std::shared_ptr<awkward::Content> input = awkward::FromJsonString("[[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6]]", awkward::ArrayBuilderOptions(1024, 2.0));
  std::shared_ptr<awkward::Content> selection = input.get()->getitem_at(at);
  
  std::cout << selection.get()->tojson(false, 1) << std::endl;


  //This not yet fully clear
  std::vector<std::vector<std::vector<double>>> vector ={{{0.0, 1.1, 2.2}, {}, {3.3, 4.4}}, {{5.5}}, {},{{6.6, 7.7, 8.8, 9.9}}};

  awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));

  builder.real(2.);
  
  // for(auto x : vector)
  //  builder.extend(x);
  std::shared_ptr<awkward::Content> array = builder.snapshot();

  awkward::Slice slice;
  slice.append(awkward::SliceRange(awkward::Slice::none(), awkward::Slice::none(), -1));
  // ::-1
  slice.append(awkward::SliceRange(awkward::Slice::none(), awkward::Slice::none(), 2));// ::2
  slice.append(awkward::SliceRange(1, awkward::Slice::none(), awkward::Slice::none()));
  
  std::cout << "-" <<array.get()->getitem(slice).get()->tojson(false, 1) << std::endl;
  
  //std::shared_ptr<awkward::Content> input = awkward::FromJsonString("[[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6]]", awkward::ArrayBuilderOptions(1024, 2.0));
  //std::shared_ptr<awkward::ArrayBuilderOptions> options;
  //options.resize(2);
  //awkward::ArrayBuilderOptions options2(1024, 2.0);
  
  //std::shared_ptr<awkward::Content> input = awkward::ArrayBuilder(options2);
  
  //std::shared_ptr<awkward::Content> options = std::shared_ptr<awkward::ArrayBuilderOptions(1024, 2.0)>;
  //std::shared_ptr<awkward::Content> input = awkward::ArrayBuilder(options);
  //input.extend([1.1, 2.2, 3.3]);
  //input.extend([1.1554, 2.232, 3.343, 9.039]);
  //input.extend([]);
  //input.extend([8.0]);


  //std::cout <<  input << std::endl;

  //std::shared_ptr<awkward::Content> selection = input.get()->getitem_at(at);


  
  
  //std::cout << selection.get()->tojson(false, 1) << std::endl;

  return 0;
}
