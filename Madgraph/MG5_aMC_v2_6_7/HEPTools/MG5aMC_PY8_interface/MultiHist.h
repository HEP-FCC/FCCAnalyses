
//==========================================================================

using namespace std;

// MultiHist class.

class MultiHist{

public:

  // Constructors, including copy constructors.
  MultiHist() {;}
  MultiHist(string titleIn, int nBinIn = 100, double xMinIn = 0.,
    double xMaxIn = 1., int nWeightsIn = 1) {
    book(titleIn, nBinIn, xMinIn, xMaxIn, nWeightsIn);}
  MultiHist(const MultiHist& h)
    : title(h.title), nBin(h.nBin), nFill(h.nFill), xMin(h.xMin),
    xMax(h.xMax), dx(h.dx), under(h.under), inside(h.inside),
    over(h.over), res(h.res), nWeights(h.nWeights),
    nfills_under(h.nfills_under), nfills_over(h.nfills_over),
    res_under(h.res_under), res_over(h.res_over),
    ressq_under(h.ressq_under), ressq_over(h.ressq_over),
     nfills(h.nfills),
    multires(h.multires), multiressq(h.multiressq) { }
  MultiHist(string titleIn, const MultiHist& h)
    : title(titleIn), nBin(h.nBin), nFill(h.nFill), xMin(h.xMin),
    xMax(h.xMax), dx(h.dx), under(h.under), inside(h.inside),
    over(h.over), res(h.res), nWeights(h.nWeights),
    nfills_under(h.nfills_under), nfills_over(h.nfills_over),
    res_under(h.res_under), res_over(h.res_over),
    ressq_under(h.ressq_under), ressq_over(h.ressq_over),
    nfills(h.nfills),
    multires(h.multires), multiressq(h.multiressq) { }
  MultiHist& operator=(const MultiHist& h) { if(this != &h) {
    nBin = h.nBin; nFill = h.nFill; xMin = h.xMin; xMax = h.xMax;
    dx = h.dx;  under = h.under; inside = h.inside; over = h.over;
    res = h.res; nWeights = h.nWeights;
    nfills = h.nfills;
    nfills_under = h.nfills_under; nfills_over = h.nfills_over;
    res_under = h.res_under; res_over = h.res_over;
    ressq_under = h.ressq_under; ressq_over = h.ressq_over;
    multires = h.multires; multiressq = h.multiressq; } return *this; }

  // Book a histogram.
  void book(string titleIn = "  ", int nBinIn = 100, double xMinIn = 0.,
    double xMaxIn = 1., int nWeightsIn = 1) ;

  // Set title of a histogram.
  void name(string titleIn = "  ") {title = titleIn; }

  // Reset bin contents.
  void null() ;

  // Fill bin with weight.
  void fill(double x, double w = 1., int iWeight = 0) ;

  // Print histogram contents as a table (e.g. for Gnuplot).
  void table(ostream& os = cout, bool printOverUnder = false,
    bool xMidBin = true) const ;
  void table(string fileName, bool printOverUnder = false,
    bool xMidBin = true) const { ofstream streamName(fileName.c_str());
    table(streamName, printOverUnder, xMidBin);}

  // Return content of specific bin: 0 gives underflow and nBin+1 overflow.
  double getBinContent(int iBin, int iWeight = 0) const;

  // Return number of entries.
  int getEntries() const {return nFill; }

  // Check whether another histogram has same size and limits.
  bool sameSize(const MultiHist& h) const ;

  // Operator overloading with member functions
  MultiHist& operator+=(const MultiHist& h) ;
  MultiHist& operator-=(const MultiHist& h) ;
  MultiHist& operator*=(const MultiHist& h) ;
  MultiHist& operator/=(const MultiHist& h) ;
  MultiHist& operator+=(double f) ;
  MultiHist& operator-=(double f) ;
  MultiHist& operator*=(double f) ;
  MultiHist& operator/=(double f) ;

  // Operator overloading with friends
  friend MultiHist operator+(double f, const MultiHist& h1);
  friend MultiHist operator+(const MultiHist& h1, double f);
  friend MultiHist operator+(const MultiHist& h1, const MultiHist& h2);
  friend MultiHist operator-(double f, const MultiHist& h1);
  friend MultiHist operator-(const MultiHist& h1, double f);
  friend MultiHist operator-(const MultiHist& h1, const MultiHist& h2);
  friend MultiHist operator*(double f, const MultiHist& h1);
  friend MultiHist operator*(const MultiHist& h1, double f);
  friend MultiHist operator*(const MultiHist& h1, const MultiHist& h2);
  friend MultiHist operator/(double f, const MultiHist& h1);
  friend MultiHist operator/(const MultiHist& h1, double f);
  friend MultiHist operator/(const MultiHist& h1, const MultiHist& h2);

private:

  // Constants: could only be changed in the code itself.
  static const int    NBINMAX, NCOLMAX, NLINES;
  static const double TOLERANCE, TINY, LARGE, SMALLFRAC, DYAC[];
  static const char   NUMBER[];

  // Properties and contents of a histogram.
  string title;
  int    nBin, nFill;
  double xMin, xMax, dx, under, inside, over;
  vector<double> res;

  int nWeights;
  vector<double> nfills_under, nfills_over, res_under, res_over,
                 ressq_under, ressq_over;
  vector< vector<double> > nfills;
  vector< vector<double> > multires;
  vector< vector<double> > multiressq;

};

//--------------------------------------------------------------------------

// Namespace function declarations; friends of MultiHist class.

// Print a table out of two histograms with same x axis.
void table(const MultiHist& h1, const MultiHist& h2, ostream& os = cout,
  bool printOverUnder = false, bool xMidBin = true) ;
void table(const MultiHist& h1, const MultiHist& h2, string fileName,
  bool printOverUnder = false, bool xMidBin = true) ;

// Operator overloading with friends
MultiHist operator+(double f, const MultiHist& h1);
MultiHist operator+(const MultiHist& h1, double f);
MultiHist operator+(const MultiHist& h1, const MultiHist& h2);
MultiHist operator-(double f, const MultiHist& h1);
MultiHist operator-(const MultiHist& h1, double f);
MultiHist operator-(const MultiHist& h1, const MultiHist& h2);
MultiHist operator*(double f, const MultiHist& h1);
MultiHist operator*(const MultiHist& h1, double f);
MultiHist operator*(const MultiHist& h1, const MultiHist& h2);
MultiHist operator/(double f, const MultiHist& h1);
MultiHist operator/(const MultiHist& h1, double f);
MultiHist operator/(const MultiHist& h1, const MultiHist& h2);

//==========================================================================

// MultiHist class.
// This class handles a single histogram at a time
// (or a vector of histograms).

//--------------------------------------------------------------------------

// Constants: could be changed here if desired, but normally should not.
// These are of technical nature, as described for each.

// Maximum number of bins in a histogram.
const int    MultiHist::NBINMAX   = 1000;

// Maximum number of columns that can be printed for a histogram.
const int    MultiHist::NCOLMAX   = 100;

// Maximum number of lines a histogram can use at output.
const int    MultiHist::NLINES    = 30;

// Tolerance in deviation of xMin and xMax between two histograms.
const double MultiHist::TOLERANCE = 0.001;

// Small and large numbers to avoid division by zero and overflow.
const double MultiHist::TINY      = 1e-20;
const double MultiHist::LARGE     = 1e20;

// When minbin/maxbin < SMALLFRAC the y scale goes down to zero.
const double MultiHist::SMALLFRAC = 0.1;

// Constants for printout: fixed steps on y scale; filling characters.
const double DYAC[] = {0.04, 0.05, 0.06, 0.08, 0.10,
  0.12, 0.15, 0.20, 0.25, 0.30};
const char NUMBER[] = {'0', '1', '2', '3', '4', '5',
  '6', '7', '8', '9', 'X' };

//--------------------------------------------------------------------------

// Book a histogram.

void MultiHist::book(string titleIn, int nBinIn, double xMinIn,
  double xMaxIn, int nWeightsIn) {

  title = titleIn;
  nBin  = nBinIn;
  if (nBinIn < 1) nBin = 1;
  if (nBinIn > NBINMAX) nBin = NBINMAX;
  xMin  = xMinIn;
  xMax  = xMaxIn;
  dx    = (xMax - xMin)/nBin;
  res.resize(nBin);

  nWeights  = nWeightsIn;

  nfills_under.resize(max(1,nWeights));
  res_under.resize(max(1,nWeights));
  ressq_under.resize(max(1,nWeights));
  nfills_over.resize(max(1,nWeights));
  res_over.resize(max(1,nWeights));
  ressq_over.resize(max(1,nWeights));

  for (int i=0; i < nWeights; ++i){
    nfills.push_back(res);
    multires.push_back(res);
    multiressq.push_back(res);
  }

  null();
}

//--------------------------------------------------------------------------

// Reset bin contents.

void MultiHist::null() {

  nFill  = 0;
  under  = 0.;
  inside = 0.;
  over   = 0.;
  for (int ix = 0; ix < nBin; ++ix) {
    res[ix] = 0.;
    for (int jx = 0; jx < nWeights; ++jx) nfills[jx][ix] = 0.;
    for (int jx = 0; jx < nWeights; ++jx) multires[jx][ix] = 0.;
    for (int jx = 0; jx < nWeights; ++jx) multiressq[jx][ix] = 0.;
  }

  for (int jx = 0; jx < nWeights; ++jx) {
    nfills_under[jx] = 0.;
    res_under[jx]    = 0.;
    ressq_under[jx]  = 0.;
    nfills_over[jx]  = 0.;
    res_over[jx]     = 0.;
    ressq_over[jx]   = 0.;
  }

}

//--------------------------------------------------------------------------

// Fill bin with weight.

void MultiHist::fill(double x, double w, int iWeight) {

  ++nFill;
  // underflow
  if (x < xMin) {
    under += w;
    if (iWeight > -1) {
      nfills_under[iWeight] += 1.;
      res_under[iWeight] += w;
      ressq_under[iWeight] += w*w;
    }
    return;
  }
  // overflow
  if (x > xMax) {
    over  += w;
    if (iWeight > -1) {
      nfills_over[iWeight] += 1.;
      res_over[iWeight] += w;
      ressq_over[iWeight] += w*w;
    }
    return;
  }
  // inside
  int iBin = int(floor((x - xMin)/dx));
  if      (iBin < 0)     under += w;
  else if (iBin >= nBin) over  += w;
  else if (iWeight < 0) {inside += w; res[iBin] += w; }
  else {
    inside += w;
    res[iBin] += w;
    nfills[iWeight][iBin] += 1.;
    multires[iWeight][iBin] += w;
    multiressq[iWeight][iBin] += w*w;
  }

}

//--------------------------------------------------------------------------

// Print histogram contents as a table (e.g. for Gnuplot).

void MultiHist::table(ostream& os, bool printOverUnder, bool xMidBin) const {

  // Print histogram vector bin by bin, with mean x as first column.
  os << scientific << setprecision(4);

  double xBeg = (xMidBin) ? xMin + 0.5 * dx : xMin;

  if (printOverUnder)
    os << setw(12) << xBeg - dx << setw(12) << res_under[0] << "\n";
  for (int ix = 0; ix < nBin; ++ix) {
    os << setw(12) << xBeg + ix * dx
       << setw(12) << xBeg + (ix+1) * dx;
    os << setw(12) << multires[0][ix]
       << setw(12) << multires[0][ix]/sqrt(max(1.,nfills[0][ix]));
    for (int jx = 1; jx < nWeights; ++jx) {
      os << setw(12) << multires[jx][ix];
    }
    os << "\n";
  }
  if (printOverUnder)
    os << setw(12) << xBeg + nBin * dx << setw(12) << res_over[0] << "\n";

}

//--------------------------------------------------------------------------

// Get content of specific bin.
// Special values are bin 0 for underflow and bin nBin+1 for overflow.
// All other bins outside proper histogram range return 0.

double MultiHist::getBinContent(int iBin, int iWeight) const {

  if      (iBin > 0 && iBin <= nBin && iWeight >= 0) return multires[iWeight][iBin - 1];
  else if (iBin > 0 && iBin <= nBin && iWeight <  0) return res[iBin - 1];
  else if (iBin == 0)           return under;
  else if (iBin == nBin + 1)    return over;
  else                          return 0.;

}

//--------------------------------------------------------------------------

// Check whether another histogram has same size and limits.

bool MultiHist::sameSize(const MultiHist& h) const {

  if (nBin == h.nBin && abs(xMin - h.xMin) < TOLERANCE * dx &&
    abs(xMax - h.xMax) < TOLERANCE * dx) return true;
  else return false;

}

//--------------------------------------------------------------------------

// Add histogram to existing one.

MultiHist& MultiHist::operator+=(const MultiHist& h) {
  if (!sameSize(h)) return *this;
  nFill  += h.nFill;
  under  += h.under;
  inside += h.inside;
  over += h.over;
  for (int ix = 0; ix < nBin; ++ix) res[ix] += h.res[ix];
  return *this;
}

//--------------------------------------------------------------------------

// Subtract histogram from existing one.

MultiHist& MultiHist::operator-=(const MultiHist& h) {
  if (!sameSize(h)) return *this;
  nFill  += h.nFill;
  under  -= h.under;
  inside -= h.inside;
  over -= h.over;
  for (int ix = 0; ix < nBin; ++ix) res[ix] -= h.res[ix];
  return *this;
}

//--------------------------------------------------------------------------

// Multiply existing histogram by another one.

MultiHist& MultiHist::operator*=(const MultiHist& h) {
  if (!sameSize(h)) return *this;
  nFill   += h.nFill;
  under  *= h.under;
  inside *= h.inside;
  over *= h.over;
  for (int ix = 0; ix < nBin; ++ix) res[ix] *= h.res[ix];
  return *this;
}

//--------------------------------------------------------------------------

// Divide existing histogram by another one.

MultiHist& MultiHist::operator/=(const MultiHist& h) {
  if (!sameSize(h)) return *this;
  nFill += h.nFill;
  under  = (abs(h.under) < MultiHist::TINY) ? 0. : under/h.under;
  inside = (abs(h.inside) < MultiHist::TINY) ? 0. : inside/h.inside;
  over  = (abs(h.over) < MultiHist::TINY) ? 0. : over/h.over;
  for (int ix = 0; ix < nBin; ++ix)
    res[ix] = (abs(h.res[ix]) < MultiHist::TINY) ? 0. : res[ix]/h.res[ix];
  return *this;
}

//--------------------------------------------------------------------------

// Add constant offset to histogram.

MultiHist& MultiHist::operator+=(double f) {
  under  += f;
  inside += nBin * f;
  over   += f;
  for (int ix = 0; ix < nBin; ++ix) res[ix] += f;
  return *this;
}

//--------------------------------------------------------------------------

// Subtract constant offset from histogram.

MultiHist& MultiHist::operator-=(double f) {
  under  -= f;
  inside -= nBin * f;
  over   -= f;
  for (int ix = 0; ix < nBin; ++ix) res[ix] -= f;
  return *this;
}

//--------------------------------------------------------------------------

// Multiply histogram by constant.

MultiHist& MultiHist::operator*=(double f) {
  under  *= f;
  inside *= f;
  over   *= f;
  for (int ix = 0; ix < nBin; ++ix) res[ix] *= f;
  return *this;
}

//--------------------------------------------------------------------------

// Divide histogram by constant.

MultiHist& MultiHist::operator/=(double f) {
  if (abs(f) > MultiHist::TINY) {
    under  /= f;
    inside /= f;
    over   /= f;
    for (int ix = 0; ix < nBin; ++ix) res[ix] /= f;
  // Set empty contents when division by zero.
  } else {
    under  = 0.;
    inside = 0.;
    over   = 0.;
    for (int ix = 0; ix < nBin; ++ix) res[ix] = 0.;
  }
  return *this;
}

//--------------------------------------------------------------------------

// Implementation of operator overloading with friends.

MultiHist operator+(double f, const MultiHist& h1) {
  MultiHist h = h1; return h += f;}

MultiHist operator+(const MultiHist& h1, double f) {
  MultiHist h = h1; return h += f;}

MultiHist operator+(const MultiHist& h1, const MultiHist& h2) {
  MultiHist h = h1; return h += h2;}

MultiHist operator-(double f, const MultiHist& h1) {
  MultiHist h   = h1;
  h.under  = f - h1.under;
  h.inside = h1.nBin * f - h1.inside;
  h.over   = f - h1.over;
  for (int ix = 0; ix < h1.nBin; ++ix) h.res[ix] = f - h1.res[ix];
  return h;}

MultiHist operator-(const MultiHist& h1, double f) {
  MultiHist h = h1; return h -= f;}

MultiHist operator-(const MultiHist& h1, const MultiHist& h2) {
  MultiHist h = h1; return h -= h2;}

MultiHist operator*(double f, const MultiHist& h1) {
  MultiHist h = h1; return h *= f;}

MultiHist operator*(const MultiHist& h1, double f) {
  MultiHist h = h1; return h *= f;}

MultiHist operator*(const MultiHist& h1, const MultiHist& h2) {
  MultiHist h = h1; return h *= h2;}

MultiHist operator/(double f, const MultiHist& h1) {
  MultiHist h = h1;
  h.under  = (abs(h1.under)  < MultiHist::TINY) ? 0. :  f/h1.under;
  h.inside = (abs(h1.inside) < MultiHist::TINY) ? 0. :  f/h1.inside;
  h.over   = (abs(h1.over)   < MultiHist::TINY) ? 0. :  f/h1.over;
  for (int ix = 0; ix < h1.nBin; ++ix)
    h.res[ix] = (abs(h1.res[ix]) < MultiHist::TINY) ? 0. : f/h1.res[ix];
  return h;
}

MultiHist operator/(const MultiHist& h1, double f) {
  MultiHist h = h1; return h /= f;}

MultiHist operator/(const MultiHist& h1, const MultiHist& h2) {
  MultiHist h = h1; return h /= h2;}

