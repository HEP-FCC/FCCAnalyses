// Example program to test PDF grid format reading and interpolation

#include "LHAPDF/GridPDF.h"
#include <iostream>
#include <fstream>
using namespace std;


void safeprint(const LHAPDF::PDF& pdf, const string& key) {
  if (pdf.info().has_key(key))
    cout << key << " = " << pdf.info().get_entry(key) << endl;
}


int main(int argc, char* argv[]) {

  if (argc < 2) {
    cout << "Usage: testgrid <PDFNAME=CT10nlo>" << endl;
    //exit(1);
  }
  const string setname = (argc < 2) ? "CT10nlo" : argv[1];

  const LHAPDF::PDF* basepdf = LHAPDF::mkPDF(setname);
  const LHAPDF::GridPDF& pdf = * dynamic_cast<const LHAPDF::GridPDF*>(basepdf);

  for (const string& p : LHAPDF::paths()) cout << p << " : ";
  cout << endl;

  safeprint(pdf, "Verbosity");
  safeprint(pdf, "PdfDesc");
  safeprint(pdf, "SetDesc");
  cout << "Flavors (str) = " << pdf.info().get_entry("Flavors") << endl;
  vector<int> pids = pdf.info().get_entry_as< vector<int> >("Flavors");
  cout << "Flavors (ints) = ";
  for (int f : pids) cout << f << " ";
  cout << endl;
  cout << "Flavors (vec<int>) = " << LHAPDF::to_str(pids) << endl;

  cout << "x0, Q0 = " << pdf.subgrid(21, 100).xf(0, 0) << endl;
  cout << "x1, Q0 = " << pdf.subgrid(21, 100).xf(1, 0) << endl;
  cout << "x0, Q1 = " << pdf.subgrid(21, 100).xf(0, 1) << endl;
  cout << "x1, Q1 = " << pdf.subgrid(21, 100).xf(1, 1) << endl;

  cout << pdf.xfxQ(21, 0.7, 10.0) << endl;
  cout << pdf.xfxQ(21, 0.2, 126) << endl;
  for (int pid : pdf.flavors()) {
    cout << pid << " = " << pdf.xfxQ(pid, 0.2, 124) << endl;
  }

  ofstream f("pdf.dat");
  for (double x = 0; x <= 1; x += 0.02) {
    for (double log10q2 = 1; log10q2 < 5; log10q2 += 0.05) {
      f << x << " " << log10q2 << " " << pdf.xfxQ2(21, x, pow(10, log10q2)) << endl;
    }
  }
  f.close();
  cout << endl;

  return 0;
}
