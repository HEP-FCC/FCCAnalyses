#include "LHAPDF/LHAPDF.h"
#include "LHAPDF/Reweighting.h"
#include <iostream>
using namespace std;

/// Demonstration of PDF reweighting functions, reweighting
/// a selection of x, Q and parton IDs between two PDF members.
///
/// Run with "from" and "to" PDFs given on the command line as follows:
///  ./reweight CT10nlo/0 MSTW2008lo68cl/0

int main(int argc, char** argv) {

  // Define the sets of parton IDs and xs and Qs to be tested
  const int IDS[3] = { 21, 1, -2 };
  const double QS[3] = { 10, 100, 1000 };
  const double XS[3] = { 3e-5, 3e-2, 3e-1 };

  // Take the PDF identities from the command line
  if (argc != 3) {
    cerr << "Usage: ./reweight <pdfdold> <pdfnew>" << endl;
    exit(1);
  }

  // Load "from" and "to" PDFs, relying on LHAPDF verbosity to write out their details
  cout << "PDF reweighting demo" << endl << endl;
  cout << "From:" << endl;
  LHAPDF::PDF* pold = LHAPDF::mkPDF(argv[1]);
  cout << "\nTo:" << endl;
  LHAPDF::PDF* pnew = LHAPDF::mkPDF(argv[2]);
  cout << endl;

  // Loop over combinations of id,x,Q and print out the reweighting factors
  for (size_t iid = 0; iid < 5; ++iid) {
    for (size_t iq = 0; iq < 3; ++iq) {
      for (size_t ix = 0; ix < 5; ++ix) {
        const int id1 = IDS[iid % 3];
        const int id2 = IDS[(2-iid) % 3];
        const double x1 = XS[ix % 3];
        const double x2 = XS[(2-ix) % 3];
        const double Q = QS[iq];
        const double w = LHAPDF::weightxxQ(id1, id2, x1, x2, Q, pold, pnew);
        cout << "("
             << setw(3) << id1 << " with x = " << setw(5) << x1 << ", "
             << setw(3) << id2 << " with x = " << setw(5) << x2 << ")  "
             << "@  Q = " << setw(4) << Q << " GeV "
             << "=> weight = " << setw(5) << w << endl;
      }
    }
  }

  // Clean up PDF memory
  delete pold;
  delete pnew;

  return 0;
}
