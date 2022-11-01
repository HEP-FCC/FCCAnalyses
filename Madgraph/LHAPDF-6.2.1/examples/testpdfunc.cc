// Program to test LHAPDF6 automatic calculation of PDF uncertainties.
// Written in March 2014 by G. Watt <Graeme.Watt(at)durham.ac.uk>.
// Use formulae for PDF uncertainties and correlations in:
//   G. Watt, JHEP 1109 (2011) 069 [arXiv:1106.5788 [hep-ph]].
// Also see Section 6 of LHAPDF6 paper [arXiv:1412.7420 [hep-ph]].
// Extended in July 2015 for ErrorType values ending in "+as".
// Modified in September 2015 for more general ErrorType values:
// number of parameter variations determined by counting "+" symbols.

#include "LHAPDF/LHAPDF.h"
#include <random>
using namespace std;

// Simple test program to demonstrate the three PDFSet member functions.
//   set.uncertainty(values, cl=68.268949..., alternative=false);
//   set.correlation(valuesA, valuesB);
//   set.randomValueFromHessian(values, randoms, symmetrise=true);

int main(int argc, char* argv[]) {

  if (argc < 2) {
    cerr << "You must specify a PDF set:  ./testpdfunc setname" << endl;
    return 1;
  }

  const string setname = argv[1];
  const LHAPDF::PDFSet set(setname);
  const size_t nmem = set.size()-1;

  double x = 0.1; // momentum fraction
  double Q = 100.0; // factorisation scale in GeV

  // Fill vectors xgAll and xuAll using all PDF members.
  // Could replace xg, xu by cross section, acceptance etc.
  const vector<LHAPDF::PDF*> pdfs = set.mkPDFs();
  vector<double> xgAll, xuAll;
  vector<string> pdftypes;
  for (size_t imem = 0; imem <= nmem; imem++) {
    xgAll.push_back(pdfs[imem]->xfxQ(21,x,Q)); // gluon distribution
    xuAll.push_back(pdfs[imem]->xfxQ(2,x,Q)); // up-quark distribution
    pdftypes.push_back(pdfs[imem]->type()); // PdfType of member
  }

  cout << endl;
  cout << "ErrorType: " << set.errorType() << endl;
  cout << "ErrorConfLevel: " << set.errorConfLevel() << endl;
  // Count number of parameter variations = number of '+' characters.
  const size_t npar = LHAPDF::countchar(set.errorType(), '+');
  if (npar > 0 )
    cout << "Last " << 2*npar << " members are parameter variations" << endl;
  cout << endl;

  // Check that the PdfType of each member matches the ErrorType of the set.
  // NB. "Hidden" expert-only functionality -- API may change
  set._checkPdfType(pdftypes);

  // Define formats for printing labels and numbers in output.
  string labformat = "%2s%10s%12s%12s%12s%12s\n";
  string numformat = "%12.4e%12.4e%12.4e%12.4e%12.4e\n";

  // Calculate PDF uncertainty on gluon distribution.
  cout << "Gluon distribution at Q = " << Q << " GeV (normal uncertainties)" << endl;
  printf(labformat.c_str()," #","x","xg","error+","error-","error");
  const LHAPDF::PDFUncertainty xgErr = set.uncertainty(xgAll, -1); // -1 => same C.L. as set
  printf(numformat.c_str(), x, xgErr.central, xgErr.errplus, xgErr.errminus, xgErr.errsymm);
  if (npar > 0) {
    // The last 2*npar members correspond to parameter variations (such as alphaS, etc.).
    // In this case, the errors above are combined PDF+parameter uncertainties, obtained by
    // adding in quadrature the PDF and parameter uncertainties, shown separately below.
    printf(labformat.c_str()," #","x","error_par","error_pdf+","error_pdf-","error_pdf");
    printf(numformat.c_str(), x, xgErr.err_par, xgErr.errplus_pdf, xgErr.errminus_pdf, xgErr.errsymm_pdf);
  }
  cout << endl;

  // Calculate PDF uncertainty on up-quark distribution.
  cout << "Up-quark distribution at Q = " << Q << " GeV (normal uncertainties)" << endl;
  printf(labformat.c_str()," #","x","xu","error+","error-","error");
  const LHAPDF::PDFUncertainty xuErr = set.uncertainty(xuAll, -1); // -1 => same C.L. as set
  printf(numformat.c_str(), x, xuErr.central, xuErr.errplus, xuErr.errminus, xuErr.errsymm);
  if (npar > 0) {
    printf(labformat.c_str()," #","x","error_par","error_pdf+","error_pdf-","error_pdf");
    printf(numformat.c_str(), x, xuErr.err_par, xuErr.errplus_pdf, xuErr.errminus_pdf, xuErr.errsymm_pdf);
  }
  cout << endl;

  // Calculate PDF correlation between gluon and up-quark.
  // (This is the PDF-only correlation if npar > 0.)
  const double corr = set.correlation(xgAll, xuAll);
  cout << "Correlation between xg and xu = " << corr << endl;
  cout << endl;

  // Calculate gluon PDF uncertainty scaled to 90% C.L.
  cout << "Gluon distribution at Q = " << Q << " GeV (scaled uncertainties)" << endl;
  printf(labformat.c_str()," #","x","xg","error+","error-","error");
  const LHAPDF::PDFUncertainty xgErr90 = set.uncertainty(xgAll, 90); // scale to 90% C.L.
  printf(numformat.c_str(), x, xgErr90.central, xgErr90.errplus, xgErr90.errminus, xgErr90.errsymm);
  cout << "Scaled PDF uncertainties to 90% C.L. using scale = " << xgErr90.scale << endl;
  if (npar > 0) {
    // If npar > 0 the same scale factor is applied to the parameter variation uncertainty.
    printf(labformat.c_str()," #","x","error_par","error_pdf+","error_pdf-","error_pdf");
    printf(numformat.c_str(), x, xgErr90.err_par, xgErr90.errplus_pdf, xgErr90.errminus_pdf, xgErr90.errsymm_pdf);
  }
  cout << endl;

  // Calculate up-quark PDF uncertainty scaled to 1-sigma.
  cout << "Up-quark distribution at Q = " << Q << " GeV (scaled uncertainties)" << endl;
  printf(labformat.c_str()," #","x","xu","error+","error-","error");
  const LHAPDF::PDFUncertainty xuErr1s = set.uncertainty(xuAll); // scale to 1-sigma (default)
  printf(numformat.c_str(), x, xuErr1s.central, xuErr1s.errplus, xuErr1s.errminus, xuErr1s.errsymm);
  cout << "Scaled PDF uncertainties to 1-sigma using scale = " << xuErr1s.scale << endl;
  if (npar > 0) {
    printf(labformat.c_str()," #","x","error_par","error_pdf+","error_pdf-","error_pdf");
    printf(numformat.c_str(), x, xuErr1s.err_par, xuErr1s.errplus_pdf, xuErr1s.errminus_pdf, xuErr1s.errsymm_pdf);
  }
  cout << endl;

  if (LHAPDF::startswith(set.errorType(), "replicas")) {

    // Calculate gluon PDF as median and 90% C.L. of replica probability distribution.
    cout << "Gluon distribution at Q = " << Q << " GeV (median and 90% C.L.)" << endl;
    printf(labformat.c_str()," #","x","xg","error+","error-","error");
    const LHAPDF::PDFUncertainty xgErr = set.uncertainty(xgAll, 90, true);
    printf(numformat.c_str(), x, xgErr.central, xgErr.errplus, xgErr.errminus, xgErr.errsymm);
    if (npar > 0) {
      // If npar > 0 the parameter variation uncertainty is scaled to the requested C.L.
      printf(labformat.c_str()," #","x","error_par","error_pdf+","error_pdf-","error_pdf");
      printf(numformat.c_str(), x, xgErr.err_par, xgErr.errplus_pdf, xgErr.errminus_pdf, xgErr.errsymm_pdf);
    }
    cout << endl;

    // Calculate up-quark PDF as median and 68% C.L. of replica probability distribution.
    cout << "Up-quark distribution at Q = " << Q << " GeV (median and 68% C.L.)" << endl;
    printf(labformat.c_str()," #","x","xu","error+","error-","error");
    const LHAPDF::PDFUncertainty xuErr = set.uncertainty(xuAll, 68, true);
    printf(numformat.c_str(), x, xuErr.central, xuErr.errplus, xuErr.errminus, xuErr.errsymm);
    if (npar > 0) {
      printf(labformat.c_str()," #","x","error_par","error_pdf+","error_pdf-","error_pdf");
      printf(numformat.c_str(), x, xuErr.err_par, xuErr.errplus_pdf, xuErr.errminus_pdf, xuErr.errsymm_pdf);
    }
    cout << endl;

  } else if (LHAPDF::startswith(set.errorType(), "hessian") || LHAPDF::startswith(set.errorType(), "symmhessian")) {

    // Generate random values from Hessian best-fit and eigenvector values.
    // See: G. Watt and R.S. Thorne, JHEP 1208 (2012) 052 [arXiv:1205.4024 [hep-ph]].

    // If npar > 0 exclude the last 2*npar members (parameter variations).
    const int npdfmem = nmem - 2*npar;
    const int neigen = (LHAPDF::startswith(set.errorType(), "hessian")) ? npdfmem/2 : npdfmem;
    const unsigned seed = 1234;
    default_random_engine generator(seed);
    normal_distribution<double> distribution; //< mean 0.0, s.d. = 1.0
    const int nrand = 5; // generate nrand random values
    for (int irand = 1; irand <= nrand; irand++) {
      // Fill vector "randoms" with neigen Gaussian random numbers.
      vector<double> randoms;
      for (int ieigen=1; ieigen <= neigen; ieigen++) {
        double r = distribution(generator);
        randoms.push_back(r);
      }
      // const bool symmetrise = false; // average differs from best-fit
      const bool symmetrise = true; // default: average tends to best-fit
      double xgrand = set.randomValueFromHessian(xgAll, randoms, symmetrise);
      // Pass *same* random numbers to preserve correlations between xg and xu.
      double xurand = set.randomValueFromHessian(xuAll, randoms, symmetrise);
      cout << "Random " << irand << ": xg = " << xgrand << ", xu = " << xurand << endl;
    }
    // Random values generated in this way can subsequently be used for
    // applications such as Bayesian reweighting or combining predictions
    // from different groups (as an alternative to taking the envelope).
    // See, for example, material at http://mstwpdf.hepforge.org/random/.
    // The "randomValueFromHessian" function is the basis of the program
    // "examples/hessian2replicas.cc" to convert a Hessian set to replicas.
    cout << endl;

  }

  return 0;

}
