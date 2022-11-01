// Example program to test LHAPDF index lookup and loading

#include "LHAPDF/PDFIndex.h"
#include <iostream>
using namespace LHAPDF;
using namespace std;

void lookup(int id) {
  pair<string, int> set_id = lookupPDF(id);
  cout << "ID=" << id << " -> set=" << set_id.first << ", mem=" << set_id.second << endl;
}


int main() {
  lookup(10800);
  lookup(10801);
  lookup(10042);
  lookup(10041);
  lookup(10799);
  lookup(12346);
  return 0;
}
