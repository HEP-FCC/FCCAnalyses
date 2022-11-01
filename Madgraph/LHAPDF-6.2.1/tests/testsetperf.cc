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
  const double dx = 0.01;
  const double dq = 0.01;

  const clock_t start = clock();

  #if LHAPDF_MAJOR_VERSION > 5
  const vector<LHAPDF::PDF*> pdfs = LHAPDF::mkPDFs("CT10nlo");
  #define XFS(I, X, Q) pdfs[I]->xfxQ(X, Q, xfs)
  #else
  LHAPDF::initPDFSetByName("CT10nlo.LHgrid");
  LHAPDF::initPDF(0);
  #define XFS(I, X, Q) { LHAPDF::initPDF(I+1); LHAPDF::xfx(X, Q, &xfs[0]); }
  #endif

  const clock_t init = clock();

  /// Tests of switching between members of a PDF set
  vector<double> xfs; xfs.resize(13);
  for (double log10x = MINLOGX; log10x <= 0.0; log10x += dx) {
    for (double log10q = MINLOGQ; log10q <= MAXLOGQ; log10q += dq) {
      for (int i = 1; i < 52; ++i) {
        XFS(i, pow(10, log10x), pow(10, log10q));
      }
    }
  }

  const clock_t end = clock();

  std::cout << "Init  = " << (init - start) << std::endl;
  std::cout << "Query = " << (end - init) << std::endl;
  std::cout << "Total = " << (end - start) << std::endl;

  #if LHAPDF_MAJOR_VERSION > 5
  for (const LHAPDF::PDF* pdf : pdfs) delete pdf;
  #endif

  return 0;
}
