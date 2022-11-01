 // Example program to test alpha_s calculation

#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <limits>

using namespace LHAPDF;
using namespace std;

int main() {

  // Set up three standalone AlphaS solvers:


  AlphaS_Analytic as_ana;

  // Can set order of QCD (up to 4)
  // 0 returns a constant value -- needs to be set by as_ana.setAlphaSMZ(double value);
  as_ana.setOrderQCD(4);

  // Set quark masses for evolution (both transition points and gradients by default)
  as_ana.setQuarkMass(1, 0.0017);
  as_ana.setQuarkMass(2, 0.0041);
  as_ana.setQuarkMass(3, 0.1);
  as_ana.setQuarkMass(4, 1.29);
  as_ana.setQuarkMass(5, 4.1);
  as_ana.setQuarkMass(6, 172.5);
  as_ana.setLambda(3, 0.339);
  as_ana.setLambda(4, 0.296);
  as_ana.setLambda(5, 0.213);

  // Can override quark masses for Nf transitions thresholds by setting them explicitly
  // You can't mix the two: if you set one flavor threshold explicitly you need to set all of them.
  //as_ode.setQuarkThreshold(6, 650);
  //as_ode.setQuarkThreshold(5, 10);
  //as_ode.setQuarkThreshold(4, 2);
  //as_ode.setQuarkThreshold(3, 0.3);
  //as_ode.setQuarkThreshold(2, 0.1);
  //as_ode.setQuarkThreshold(1, 0.08);

  // Uncomment to use fixed flavor scheme for analytic solver
  // as_ana.setFlavorScheme(AlphaS::FIXED, 5);



  AlphaS_ODE as_ode;

  // As above: order = 0 returns
  // constant value set by
  // as_ode.setAlphaSMZ(double value);
  as_ode.setOrderQCD(5);

  as_ode.setMZ(91);
  as_ode.setAlphaSMZ(0.118);
  // as_ode.setMassReference(4.1);
  // as_ode.setAlphaSReference(0.21);
  as_ode.setQuarkMass(1, 0.0017);
  as_ode.setQuarkMass(2, 0.0041);
  as_ode.setQuarkMass(3, 0.1);
  as_ode.setQuarkMass(4, 1.29);
  as_ode.setQuarkMass(5, 4.1);
  as_ode.setQuarkMass(6, 172.5);

  // Can override quark masses for Nf transitions thresholds by setting them explicitly
  // You can't mix the two: if you set one flavor threshold explicitly you need to set all of them.
  //  as_ode.setQuarkThreshold(6, 650);
  //  as_ode.setQuarkThreshold(5, 10);
  //  as_ode.setQuarkThreshold(4, 2);
  //  as_ode.setQuarkThreshold(3, 0.3);
  //  as_ode.setQuarkThreshold(2, 0.1);
  //  as_ode.setQuarkThreshold(1, 0.08);

  // Uncomment to use fixed flavor scheme for ODE solver
  // as_ode.setFlavorScheme(AlphaS::FIXED, 4);



  AlphaS_Ipol as_ipol;
  vector<double> qs = { 1.300000e+00, 1.300000e+00, 1.560453e+00, 1.873087e+00, 2.248357e+00, 2.698811e+00, 3.239513e+00, 3.888544e+00, 4.667607e+00, 5.602754e+00, 6.725257e+00, 8.072650e+00, 9.689992e+00, 1.163137e+01, 1.396169e+01, 1.675889e+01, 2.011651e+01, 2.414681e+01, 2.898459e+01, 3.479160e+01, 4.176203e+01, 5.012899e+01, 6.017224e+01, 7.222765e+01, 8.669834e+01, 1.040682e+02, 1.249181e+02, 1.499452e+02, 1.799865e+02, 2.160465e+02, 2.593310e+02, 3.112875e+02, 3.736534e+02, 4.485143e+02, 5.383733e+02, 6.462355e+02, 7.757077e+02, 9.311194e+02, 1.117668e+03, 1.341590e+03, 1.610376e+03, 1.933012e+03, 2.320287e+03, 2.785153e+03, 3.343154e+03, 4.012949e+03, 4.816936e+03, 4.816936e+03 };
  vector<double> alphas = { 4.189466e-01, 4.189466e-01, 3.803532e-01, 3.482705e-01, 3.211791e-01, 2.979983e-01, 2.779383e-01, 2.604087e-01, 2.451922e-01, 2.324903e-01, 2.210397e-01, 2.106640e-01, 2.012187e-01, 1.925841e-01, 1.846600e-01, 1.773623e-01, 1.706194e-01, 1.643704e-01, 1.585630e-01, 1.531520e-01, 1.480981e-01, 1.433671e-01, 1.389290e-01, 1.347574e-01, 1.308290e-01, 1.271232e-01, 1.236215e-01, 1.203076e-01, 1.171667e-01, 1.141857e-01, 1.113525e-01, 1.086566e-01, 1.060881e-01, 1.036382e-01, 1.012990e-01, 9.906295e-02, 9.692353e-02, 9.487457e-02, 9.291044e-02, 9.102599e-02, 8.921646e-02, 8.747747e-02, 8.580498e-02, 8.419524e-02, 8.264479e-02, 8.115040e-02, 7.970910e-02, 7.970910e-02 };
  as_ipol.setQValues(qs);
  as_ipol.setAlphaSValues(alphas);

  // Can interpolate ODE with given knots in Q
  // as_ode.setQValues(qs);


  ///////////////////////////////
  // Test these solvers and the CT10nlo PDF's default behaviours:


  PDF* pdf = mkPDF("CT10", 0);
  const double inf = numeric_limits<double>::infinity();
  ofstream fa("alphas_ana.dat"), fo("alphas_ode.dat"), fi("alphas_ipol.dat"), fc("alphas_ct10nlo.dat");
  cout << endl;
  for (double log10q = -0.5; log10q < 3; log10q += 0.05) {
    const double q = pow(10, log10q);
    const double as_ana_q = as_ana.alphasQ(q);
    cout << fixed;
    cout << "Q = " << setprecision(3) << q << " GeV" << endl;
    cout << "Analytical solution:           " << setprecision(3) << setw(6)  << ( (as_ana_q > 2) ? inf : as_ana_q )
         << "    num flavs = " << as_ana.numFlavorsQ(q) << endl;
    fa << q << " " << as_ana_q << endl;

    const double as_ode_q = as_ode.alphasQ(q);
    cout << "ODE solution:                  " << setprecision(3) << setw(6)  << ( (as_ode_q > 2) ? inf : as_ode_q )
         << "    num flavs = " << as_ode.numFlavorsQ(q) << endl;
    fo << q << " " << as_ode_q << endl;
    // const double as_ipol_q = as_ipol.alphasQ(q);
    // cout << "Interpolated solution:         " << setprecision(3) << setw(6)  << ( (as_ipol_q > 2) ? inf : as_ipol_q ) << endl;
    // fi << q << " " << as_ipol_q << endl;
    // const double as_ct10_q = pdf->alphasQ(q);
    // cout << "CT10 solution:                 " << setprecision(3) << setw(6) << as_ct10_q << endl;
    // fc << q << " " << as_ct10_q << endl;
    // const double as_ct10_q_2 = pdf->alphaS().alphasQ(q);
    // cout << "CT10 AlphaS solution:          " << setprecision(3) << setw(6)  << as_ct10_q_2
    //      << "    agrees = " << boolalpha << (as_ct10_q == as_ct10_q_2) << endl;
    // cout << endl;
  }
  fa.close(); fo.close(); fi.close(); fc.close();

  delete pdf;
  return 0;
}
