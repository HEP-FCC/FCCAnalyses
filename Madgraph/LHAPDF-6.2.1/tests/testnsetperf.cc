// Program to test LHAPDF6 PDF CPU/memory performance by sampling PDFs in several ways

#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <cmath>
#include <ctime>
using namespace std;

int main(int argc, char* argv[]) {

  const double MINLOGX = -7.5;
  const double MINLOGQ = 1;
  const double MAXLOGQ = 3;
  const double dx = 0.1;
  const double dq = 0.1;

  const clock_t start = clock();

  #if LHAPDF_MAJOR_VERSION > 5
  vector<LHAPDF::PDF*> sets[3];
  sets[0] = LHAPDF::mkPDFs("CT10nlo");
  sets[1] = LHAPDF::mkPDFs("MSTW2008nlo68cl");
  sets[2] = LHAPDF::mkPDFs("NNPDF23_nlo_as_0118");
  #define XFS(N, I, X, Q) sets[N][I]->xfxQ(X, Q, xfs)
  #else
  LHAPDF::initPDFSet(1, "CT10nlo.LHgrid");
  LHAPDF::initPDFSet(2, "MSTW2008nlo68cl.LHgrid");
  LHAPDF::initPDFSet(3, "NNPDF23_nlo_as_0118.LHgrid");
  #define XFS(N, I, X, Q) { LHAPDF::usePDFMember(N+1, I); LHAPDF::xfx(X, Q, &xfs[0]); }
  #endif

  const clock_t init = clock();

  /// Tests of switching between members of multiple PDF sets
  vector<double> xfs; xfs.resize(13);
  for (double log10x = MINLOGX; log10x <= 0.0; log10x += dx) {
    for (double log10q = MINLOGQ; log10q <= MAXLOGQ; log10q += dq) {
      // Using stupid loop ordering for demonstration! Putting n outermost is ok
      for (int i = 1; i < 40; ++i) {
        for (int n = 0; n < 30; ++n) {
          int nset = n % 3;
          XFS(nset, i, pow(10, log10x), pow(10, log10q));
        }
      }
    }
  }

  const clock_t end = clock();

  std::cout << "Init  = " << (init - start) << std::endl;
  std::cout << "Query = " << (end - init) << std::endl;
  std::cout << "Total = " << (end - start) << std::endl;

  #if LHAPDF_MAJOR_VERSION > 5
  for (int i = 0; i < 3; ++i) {
    for (const LHAPDF::PDF* pdf : sets[i]) delete pdf;
  }
  #endif

  return 0;
}
