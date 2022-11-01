#include "LHAPDF/PDF.h"
#include <iostream>

using namespace std;


/// Demo of an analytic/custom PDF class
///
/// Returns the same value for all light flavors (inc. gluons)
struct AnalyticPDF : public LHAPDF::PDF {

  AnalyticPDF() {
    info().set_entry("Flavors", "-5,-4,-3,-2,-1,21,1,2,3,4,5");
  }

  double _xfxQ2(int id, double x, double q2) const {
    if (abs(id) > 5 && id != 21) return 0;
    return 0.15 * sin(20.0*x) * sin(20.0*q2);
  }

  bool inRangeX(double x) const { return true; }
  bool inRangeQ2(double q2) const { return true; }

};


int main(int argc, const char* argv[]) {
  AnalyticPDF apdf;
  LHAPDF::PDF& pdf = apdf;
  for (double x = 0; x < 1.0; x += 0.1) {
    for (double logq2 = 1; logq2 < 6; logq2 += 0.5) {
      const double q2 = pow(10, logq2);
      cout << x << " " << q2 << " " << pdf.xfxQ2(21, x, q2) << endl;
    }
  }
  return 0;
}
