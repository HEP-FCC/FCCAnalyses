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
  const double dx = 0.005;
  const double dq = 0.005;

  const clock_t start = clock();

  #if LHAPDF_MAJOR_VERSION > 5
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF("CT10nlo", 0);
  #define XFS(X, Q) pdf->xfxQ(X, Q, xfs)
  #else
  LHAPDF::initPDFSetByName("CT10nlo.LHgrid");
  LHAPDF::initPDF(0);
  #define XFS(X, Q) LHAPDF::xfx(X, Q, &xfs[0])
  #endif

  const clock_t init = clock();

  /// Tests of a single PDF member
  vector<double> xfs; xfs.resize(13);
  for (double log10x = MINLOGX; log10x <= 0.0; log10x += dx) {
    for (double log10q = MINLOGQ; log10q <= MAXLOGQ; log10q += dq) {
      XFS(pow(10, log10x), pow(10, log10q));
    }
  }

  const clock_t end = clock();

  std::cout << "Init  = " << (init - start) << std::endl;
  std::cout << "Query = " << (end - init) << std::endl;
  std::cout << "Total = " << (end - start) << std::endl;

  #if LHAPDF_MAJOR_VERSION > 5
  delete pdf;
  #endif

  return 0;
}
