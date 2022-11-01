// Program to test LHAPDF6 PDF behaviour by writing out their values at lots of x and Q points
// Note: the OpenMP directives are there as an example. In fact, in this case OpenMP slows things
// down because of the need to make the stream operations critical!

#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
using namespace LHAPDF;
using namespace std;

int main(int argc, char* argv[]) {

  if (argc < 3) {
    cerr << "You must specify a PDF set and member number" << endl;
    return 1;
  }

  const string setname = argv[1];
  const string smem = argv[2];
  const int imem = lexical_cast<int>(smem);

  const PDF* pdf = mkPDF(setname, imem);
  vector<int> pids = pdf->flavors();

  const double MINLOGX = -10;
  const double MAXLOGX =   0;
  const double DX = 0.01;
  const int NX = (int) floor((MAXLOGX - MINLOGX)/DX) + 1;

  const double MINLOGQ2 = 1;
  const double MAXLOGQ2 = 8;
  const double DQ2 = 0.01;
  const int NQ2 = (int) floor((MAXLOGQ2 - MINLOGQ2)/DQ2) + 1;

  for (int pid : pids) {
    const string spid = lexical_cast<string>(pid);
    const string filename = setname + "_" + smem + "_" + spid + ".dat";
    ofstream f(filename.c_str());
    for (int ix = 0; ix < NX; ++ix) {
      const double log10x = (MINLOGX + ix*DX < -1e-3) ? MINLOGX + ix*DX : 0;
      const double x = pow(10, log10x);
      for (int iq2 = 0; iq2 < NQ2; ++iq2) {
        const double log10q2 = MINLOGQ2 + iq2*DQ2;
        const double q2 = pow(10, log10q2);
        const double xf = pdf->xfxQ2(pid, x, q2);
        f << x << " " << q2 << " " << xf << endl;
      }
    }
    f.close();
  }

  for (double log10q2 = MINLOGQ2; log10q2 <= MAXLOGQ2; log10q2 += 0.2) {
    const double q2 = pow(10, log10q2);
    cout << "alpha_s(" << setprecision(1) << fixed << sqrt(q2) << " GeV) = "
         << setprecision(5) << pdf->alphasQ2(q2) << endl;
  }

  delete pdf;
  return 0;
}
