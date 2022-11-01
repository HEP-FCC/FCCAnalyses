#include "LHAPDF/LHAPDF.h"
#include <memory>
using namespace std;

int main() {

  // Get a PDF set object and use it to get a vector of heap-allocated PDFs
  LHAPDF::PDFSet set("CT10nlo");
  vector<LHAPDF::PDF*> pdfs = set.mkPDFs();
  for (LHAPDF::PDF* p : pdfs) {
    const double xf_g = p->xfxQ(21, 1e-3, 126.0);
    cout << xf_g << endl;
    delete p; //< Manual deletion required
  }

  // Directly get a PDF vector using smart pointers for memory handling.
  typedef unique_ptr<LHAPDF::PDF> PDFPtr;
  vector<PDFPtr> smartpdfs = set.mkPDFs<PDFPtr>();

  return 0;
}
