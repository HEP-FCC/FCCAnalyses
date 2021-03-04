#include "awkwardtest.h"

#include <iostream>
#include <cstdlib>

#include "awkward/Content.h"
#include "awkward/io/json.h"


bool awkwardtest(){
  
  int at = std::atoi("-2");

  std::shared_ptr<awkward::Content> input = awkward::FromJsonString("[[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6]]", awkward::ArrayBuilderOptions(1024, 2.0));
  std::shared_ptr<awkward::Content> selection = input.get()->getitem_at(at);

  std::cout << selection.get()->tojson(false, 1) << std::endl;

  return 0;
}
