// Program to convert LHAPDF6 grid files from Hessian to replicas.
// Written in March 2014 by G. Watt <Graeme.Watt(at)durham.ac.uk>.
// Extended version of http://mstwpdf.hepforge.org/random/conversion.C.

#include "LHAPDF/LHAPDF.h"
#include <random>
using namespace std;

// Function to convert Hessian "set" to replica set with name "randsetname"
// in directory "randdir" (default: current directory) using "seed" for
// random number generator with "nrep" replica PDF members and an option
// to "symmetrise" the Hessian predictions if they are asymmetric.
void convertHessianToReplicas(const LHAPDF::PDFSet& set, const string& randsetname,
                              const unsigned& seed, const unsigned& nrep,
                              const string& randdir=".", const bool& symmetrise=true);


int main(int argc, char* argv[]) {

  if (argc < 4) {
    cerr << "You must specify a PDF set, random seed and number of replicas (1-9999):" << endl;
    cerr << "  ./hessian2replicas setname seed nrep" << endl;
    cerr << "  e.g. ./hessian2replicas MSTW2008nnlo68cl 1234 100" << endl;
    return 1;
  }

  const string setname = argv[1];
  const string strseed = argv[2];
  const unsigned seed = LHAPDF::lexical_cast<unsigned>(strseed);
  const unsigned nrep = LHAPDF::lexical_cast<unsigned>(argv[3]);

  const LHAPDF::PDFSet set(setname);

  // Allocate a name for the new randomly sampled PDF set.
  const string randsetname = setname + "_rand" + strseed;

  // Convert Hessian "set" to replica set with name "randsetname" in current
  // directory using "seed" for random number generator with "nrep" replica
  // PDF members and symmetrised Hessian predictions (so average = best-fit).
  convertHessianToReplicas(set, randsetname, seed, nrep);

  // Same thing but non-default values for "randdir" or "symmetrise".
  //const string randdir = "/tmp"; // directory to write new replica set
  const string randdir = "."; // default: current directory
  //convertHessianToReplicas(set, randsetname, seed, nrep, randdir);
  //const bool symmetrise = false; // average differs from best-fit
  //const bool symmetrise = true; // default: average tends to best-fit
  //convertHessianToReplicas(set, randsetname, seed, nrep, randdir, symmetrise);

  // Code below provides a simple test comparing the Hessian and replica sets.

  //const bool testrandset = false; // uncomment to skip test below
  const bool testrandset = true; // uncomment to activate test below

  if (testrandset) {

    // Add the directory containing the new replica set to the path (if not already there).
    vector<string> paths = LHAPDF::paths();
    bool pathfound = false;
    for (size_t ipath = 0; ipath < paths.size(); ipath++) {
      if (paths[ipath] == randdir) pathfound = true;
    }
    if (!pathfound) LHAPDF::pathsAppend(randdir);

    const LHAPDF::PDFSet randset(randsetname);
    const unsigned nmem = set.size()-1;
    const unsigned nmemRand = randset.size()-1;
    const vector<LHAPDF::PDF*> pdfs = set.mkPDFs();
    const vector<LHAPDF::PDF*> randpdfs = randset.mkPDFs();
    double x = 0.1; // momentum fraction
    double Q = 100.0; // factorisation scale in GeV
    // Fill vectors xgAll and xuAll using all PDF members.
    vector<double> xgAll, xuAll;
    for (unsigned imem = 0; imem <= nmem; imem++) {
      xgAll.push_back(pdfs[imem]->xfxQ(21,x,Q)); // gluon distribution
      xuAll.push_back(pdfs[imem]->xfxQ(2,x,Q)); // up-quark distribution
    }
    vector<double> xgAllRand, xuAllRand;
    for (unsigned imem = 0; imem <= nmemRand; imem++) {
      xgAllRand.push_back(randpdfs[imem]->xfxQ(21,x,Q)); // gluon distribution
      xuAllRand.push_back(randpdfs[imem]->xfxQ(2,x,Q)); // up-quark distribution
    }

    // Define formats for printing labels and numbers in output.
    string labformat = "%2s%10s%12s%12s%12s%12s\n";
    string numformat = "%12.4e%12.4e%12.4e%12.4e%12.4e\n";

    // Calculate 1-sigma PDF uncertainty on gluon and up-quark.

    const LHAPDF::PDFUncertainty xgErr = set.uncertainty(xgAll); // scale to 1-sigma (default)
    cout << "Gluon distribution at Q = " << Q << " GeV (original Hessian)" << endl;
    printf(labformat.c_str()," #","x","xg","error+","error-","error");
    printf(numformat.c_str(), x, xgErr.central, xgErr.errplus, xgErr.errminus, xgErr.errsymm);
    cout << "Scaled PDF uncertainties to 1-sigma using scale = " << xgErr.scale << endl;
    cout << endl;

    const LHAPDF::PDFUncertainty xgErrRand = randset.uncertainty(xgAllRand);
    cout << "Gluon distribution at Q = " << Q << " GeV (new replicas)" << endl;
    printf(labformat.c_str()," #","x","xg","error+","error-","error");
    printf(numformat.c_str(), x, xgErrRand.central, xgErrRand.errplus, xgErrRand.errminus, xgErrRand.errsymm);
    cout << endl;

    const LHAPDF::PDFUncertainty xuErr = set.uncertainty(xuAll); // scale to 1-sigma (default)
    cout << "Up-quark distribution at Q = " << Q << " GeV (original Hessian)" << endl;
    printf(labformat.c_str()," #","x","xu","error+","error-","error");
    printf(numformat.c_str(), x, xuErr.central, xuErr.errplus, xuErr.errminus, xuErr.errsymm);
    cout << "Scaled PDF uncertainties to 1-sigma using scale = " << xgErr.scale << endl;
    cout << endl;

    const LHAPDF::PDFUncertainty xuErrRand = randset.uncertainty(xuAllRand);
    cout << "Up-quark distribution at Q = " << Q << " GeV (new replicas)" << endl;
    printf(labformat.c_str()," #","x","xu","error+","error-","error");
    printf(numformat.c_str(), x, xuErrRand.central, xuErrRand.errplus, xuErrRand.errminus, xuErrRand.errsymm);
    cout << endl;

    // Calculate PDF correlation between gluon and up-quark.
    const double corr = set.correlation(xgAll, xuAll);
    cout << "Correlation between xg and xu (original Hessian) = " << corr << endl;
    const double randcorr = randset.correlation(xgAllRand, xuAllRand);
    cout << "Correlation between xg and xu (new replicas) = " << randcorr << endl;
    cout << endl;

  }

  return 0;

}


//


// Function to convert Hessian "set" to replica set with name "randsetname"
// in directory "randdir" (default: current directory) using "seed" for
// random number generator with "nrep" replica PDF members and an option
// to "symmetrise" the Hessian predictions if they are asymmetric.
void convertHessianToReplicas(const LHAPDF::PDFSet& set, const string& randsetname, const unsigned& seed, const unsigned& nrep, const string& randdir, const bool& symmetrise) {

  if (set.errorType() != "hessian" && set.errorType() != "symmhessian") {
    throw LHAPDF::MetadataError("This PDF set is not in the Hessian format.");
  }

  if (nrep < 1 || nrep > 9999) {
    throw LHAPDF::NotImplementedError("Number of replicas must be between 1 and 9999.");
  }

  // Make directory to store new random PDF set (if it doesn't already exist).
  if (!LHAPDF::dir_exists(randdir + "/" + randsetname)) {
    string mkdir = "mkdir -p " + randdir + "/" +randsetname;
    if (system(mkdir.c_str()) == -1) {
      throw LHAPDF::Exception("Error creating directory " + randdir + "/" + randsetname);
    } else {
      cout << "Creating directory " << randdir + "/" + randsetname << endl;
    }
  } else {
    cout << "Directory " << randdir + "/" + randsetname << " already exists" << endl;
  }

  // Copy information from original .info file to new .info file.
  /// @todo Wouldn't it be nicer to use the PDFSet metadata system for this rather than re-parse the .info?
  const string setinfopath = LHAPDF::findpdfsetinfopath(set.name());
  ifstream infile (setinfopath.c_str());
  if (infile.good()) {
    cout << "Reading info file from " << setinfopath << endl;
  } else {
    throw LHAPDF::ReadError("Error reading " + setinfopath);
  }
  const string randsetinfopath = randdir+"/"+randsetname+"/"+randsetname+".info";
  ofstream outfile (randsetinfopath.c_str());
  if (outfile.good()) {
    cout << "Writing info file to " << randsetinfopath << endl;
  } else {
    throw LHAPDF::Exception("Error writing to " + randsetinfopath);
  }
  string line;
  while (getline(infile, line)) {
    LHAPDF::trim(line);
    if (LHAPDF::contains(line, "SetDesc")) {
      outfile << "SetDesc: \"Based on original " << set.name() << ".  This set has " << nrep+1 << " member PDFs.  mem=0 => average over " << nrep << " random PDFs; mem=1-" << nrep << " => " << nrep << " random PDFs generated using ";
      if (symmetrise) {
        outfile << "corrected Eq. (6.5) of arXiv:1205.4024v2\"" << endl;
      } else {
        outfile << "Eq. (6.4) of arXiv:1205.4024v2\"" << endl;
      }
    } else if (LHAPDF::contains(line, "SetIndex")) {
      // Miss out SetIndex.
    } else if (LHAPDF::contains(line, "NumMembers")) {
      outfile << "NumMembers: " << nrep+1 << endl;
    } else if (LHAPDF::contains(line, "ErrorType")) {
      outfile << "ErrorType: replicas" << endl;
    } else if (LHAPDF::contains(line, "ErrorConfLevel")) {
      // Miss out ErrorConfLevel.
    } else {
      // outfile << line << endl;
      istringstream tokens(line);
      string word;
      tokens >> word;
      if (LHAPDF::endswith(word, ":")) outfile << line << endl;
    }
  }
  infile.close();
  outfile.close();

  // Loop over number of members, storing metadata and (x,Q,flavor) values.
  // Check that (x,Q,flavor) values are equal for all members.
  // Need to allow for different Q subgrids used in MSTW case,
  // and different AlphaS values for each member in ABM case.
  vector<string> meta; // assume same for each imem
  vector<double> alphasMZ; // assume different for each imem
  vector<double> alphasQs; // assume same for each imem
  vector<vector<double> > alphasVals; // assume different for each imem
  vector<vector<double> > xs, qs; // store x and Q values for each Q subgrid
  vector<vector<int> > flavors; // store flavours for each Q subgrid
  const int nmem = set.size()-1; // number of members in original set
  for (int imem = 0; imem <= nmem; imem++) {
    const string mempath = LHAPDF::findpdfmempath(set.name(), imem);
    ifstream infile (mempath.c_str());
    if (infile.good()) {
      cout << "Reading dat file from " << mempath << endl;
    } else {
      throw LHAPDF::ReadError("Error reading " + mempath);
    }
    int iblock(0), iblockline(0), iline(0);
    double token;
    while (getline(infile, line)) {
      LHAPDF::trim(line);
      iline += 1;
      // If the line is commented out, increment the line number but not the block line.
      if (line.find("#") == 0) continue;
      iblockline += 1;
      if (line != "---") { // if we are not on a block separator line...
        if (iblock == 0) { // metadata
          if (imem == 0) meta.push_back(line); // store to be written later
          if (LHAPDF::contains(line, "AlphaS_MZ")) {
            istringstream tokens(line);
            string dummy;
            tokens >> dummy >> token;
            alphasMZ.push_back(token); // store for each member
          }
          if (LHAPDF::contains(line, "AlphaS_Qs")) {
            while (line.find(",") != string::npos) {
              line.replace(line.find(","), 1, " "); // replace commas by spaces
            }
            // Consider only the substring inside the square brackets.
            istringstream tokens(line.substr(line.find("[")+1, line.find("]")-1));
            int iq = 0;
            while (tokens >> token) {
              if (imem > 0 && token != alphasQs[iq]) {
                throw LHAPDF::NotImplementedError("Error: AlphaS_Qs not same for all PDF members");
              } else if (imem == 0) {
                alphasQs.push_back(token); // store for zeroth member
              }
              iq++;
            }
          }
          if (LHAPDF::contains(line, "AlphaS_Vals")) {
            while (line.find(",") != string::npos) {
              line.replace(line.find(","), 1, " "); // replace commas by spaces
            }
            // Consider only the substring inside the square brackets.
            istringstream tokens(line.substr(line.find("[")+1, line.find("]")-1));
            vector<double> alphasValstemp;
            while (tokens >> token) alphasValstemp.push_back(token);
            alphasVals.push_back(alphasValstemp); // store for all members
          }
          continue;
        }
        // Parse the data lines.
        istringstream tokens(line);
        if (iblockline == 1) { // x knots line
          vector<double> xstemp;
          int ix = 0;
          while (tokens >> token) {
            if (imem > 0 && token != xs[iblock-1][ix]) {
              throw LHAPDF::NotImplementedError("Error: x knots not same for all PDF members");
            } else if (imem == 0) {
              xstemp.push_back(token); // store for zeroth member
            }
            ix++;
          }
          if (imem == 0) xs.push_back(xstemp); // store for zeroth member
        } else if (iblockline == 2) { // Q knots line
          vector<double> qstemp;
          int iq = 0;
          while (tokens >> token) {
            if (imem > 0 && token != qs[iblock-1][iq]) {
              throw LHAPDF::NotImplementedError("Error: Q knots not same for all PDF members");
            } else if (imem == 0) {
              qstemp.push_back(token); // store for zeroth member
            }
            iq++;
          }
          if (imem == 0) qs.push_back(qstemp); // store for zeroth member
        } else if (iblockline == 3) { // internal flavor IDs line
          vector<int> flavorstemp;
          int iflavor = 0;
          while (tokens >> token) {
            if (imem > 0 && token != flavors[iblock-1][iflavor]) {
              throw LHAPDF::NotImplementedError("Error: flavor knots not same for all PDF members");
            } else if (imem == 0) {
              flavorstemp.push_back(token); // store for zeroth member
            }
            iflavor++;
          }
          if (imem == 0) flavors.push_back(flavorstemp); // store for zeroth member
        } else { // xf block: ignore
          continue;
        }
      } else { // block separator line: "---"
        // Increment/reset the block and line counters.
        iblock += 1;
        iblockline = 0;
      }
    }
    infile.close();
  } // end loop over members

  // Allocate number of eigenvectors based on ErrorType.
  int neigen = 0;
  if (set.errorType() == "hessian") {
    neigen = nmem/2;
  } else if (set.errorType() == "symmhessian") {
    neigen = nmem;
  }
  // Vector containing all original PDF members.
  const vector<LHAPDF::PDF*> pdfs = set.mkPDFs();

  // Initialise Gaussian random number generator.
  default_random_engine generator(seed); // seed passed as argument
  normal_distribution<double> distribution; // mean 0.0, s.d. = 1.0

  // Calculate the mean over all replicas.  First initialise everything to zero.
  double alphasMZmean = 0.0;
  vector<double> alphasValsMean (alphasQs.size(), 0.0);
  vector<vector<vector<vector<double> > > > xfmean; // mean xf[isub][ix][iq][iflavor]
  for (size_t isub=0; isub < qs.size(); isub++) { // loop over Q subgrids
    vector<vector<vector<double> > > xfmean_xs;
    for (size_t ix = 0; ix < xs[isub].size(); ix++) { // loop over x values
      vector<vector<double> > xfmean_qs;
      for (size_t iq = 0; iq < qs[isub].size(); iq++) { // loop over Q values
        vector<double> xfmean_flavors;
        for (size_t iflavor = 0; iflavor < flavors[isub].size(); iflavor++) { // loop over flavours
          xfmean_flavors.push_back(0.0);
        }
        xfmean_qs.push_back(xfmean_flavors);
      }
      xfmean_xs.push_back(xfmean_qs);
    }
    xfmean.push_back(xfmean_xs);
  }

  // Loop over number of requested replica members, plus zeroth member containing mean.
  for (unsigned ireplica = 1; ireplica <= nrep+1; ireplica++) {

    unsigned irep = ireplica;
    if (irep == nrep+1) irep = 0; // do central member last since need average

    // Fill vector "randoms" with neigen Gaussian random numbers.
    vector<double> randoms;
    if (irep > 0) {
      for (int ieigen=1; ieigen <= neigen; ieigen++) {
        const double r = distribution(generator);
        randoms.push_back(r);
        //randoms.push_back(0.0); // for testing purposes (all replicas equal best-fit)
      }
    }

    // Open new .dat file for this replica member.
    const string randsetmempath = randdir + "/" + randsetname + "/" + randsetname + "_" + LHAPDF::to_str_zeropad(irep) + ".dat";
    ofstream outfile (randsetmempath.c_str());
    char buffer[256];
    if (outfile.good()) {
      cout << "Writing dat file to " << randsetmempath << endl;
    } else {
      throw LHAPDF::Exception("Error writing to " + randsetmempath);
    }

    // Write metadata for this replica member.
    for (size_t i = 0; i < meta.size(); i++) {
      if (LHAPDF::contains(meta[i], "PdfType")) {
        if (irep == 0) outfile << "PdfType: central" << endl;
        else outfile << "PdfType: replica" << endl;
      } else if (LHAPDF::contains(meta[i], "AlphaS_MZ")) {
        // Write randomly sampled value of AlphaS_MZ.
        if (irep > 0) {
          double alphasMZrand = set.randomValueFromHessian(alphasMZ, randoms, symmetrise);
          alphasMZmean += alphasMZrand;
          sprintf(buffer, "AlphaS_MZ: %g", alphasMZrand);
        } else {
          alphasMZmean /= nrep;
          sprintf(buffer, "AlphaS_MZ: %g", alphasMZmean);
        }
        outfile << buffer << endl;
      } else if (LHAPDF::contains(meta[i], "AlphaS_Vals")) {
        // Write randomly sampled values of AlphaS_Vals.
        vector<double> alphasValsRand;
        if (irep > 0) {
          for (size_t iq = 0; iq < alphasQs.size(); iq++) {
            vector<double> alphasAll;
            for (int imem=0; imem <= nmem; imem++) {
              alphasAll.push_back(alphasVals[imem][iq]);
            }
            double alphasValRand = set.randomValueFromHessian(alphasAll, randoms, symmetrise);
            alphasValsRand.push_back(alphasValRand);
            // Check that alphasValsMean is initialised to zero.
            if (irep == 1 && alphasValsMean[iq] != 0.0) {
              throw LHAPDF::LogicError("Error: alphasValsMean[" + LHAPDF::to_str(iq) + "] = " + LHAPDF::to_str(alphasValsMean[iq]));
            }
            alphasValsMean[iq] += alphasValRand;
          }
        }
        outfile << "AlphaS_Vals: [";
        for (size_t iq = 0; iq < alphasQs.size(); iq++) {
          if (irep > 0) {
            sprintf(buffer, "%2.6e", alphasValsRand[iq]);
          } else {
            alphasValsMean[iq] /= nrep;
            sprintf(buffer, "%2.6e", alphasValsMean[iq]);
          }
          outfile << buffer;
          if (iq < alphasQs.size()-1) outfile << ", ";
        }
        outfile << "]" << endl;
      } else {
        outfile << meta[i] << endl;
      }
    }
    outfile << "---" << endl;

    // Loop over same Q subgrids as in original grid file.
    for (size_t isub=0; isub < xs.size(); isub++) {

      // Write x points for this Q subgrid.
      for (size_t ix = 0; ix < xs[isub].size(); ix++) {
        sprintf(buffer, "%2.6e", xs[isub][ix]);
        outfile << buffer;
        if (ix < xs[isub].size()-1) outfile << " ";
      }
      outfile << endl;
      // Write Q points for this Q subgrid.
      for (size_t iq = 0; iq < qs[isub].size(); iq++) {
        sprintf(buffer, "%2.6e", qs[isub][iq]);
        outfile << buffer;
        if (iq < xs[isub].size()-1) outfile << " ";
      }
      outfile << endl;
      // Write internal flavour list for this Q subgrid.
      for (size_t iflavor = 0; iflavor < flavors[isub].size(); iflavor++) {
        outfile << flavors[isub][iflavor];
        if (iflavor < flavors[isub].size()-1) outfile << " ";
      }
      outfile << endl;

      // Loop over x and Q points for this Q subgrid.
      for (size_t ix = 0; ix < xs[isub].size(); ix++) {
        double x = xs[isub][ix];
        for (size_t iq = 0; iq < qs[isub].size(); iq++) {
          double Q = qs[isub][iq];
          // At subgrid boundaries, shift Q by tiny amount (but within numerical
          // precision) to call PDFs on correct side of appropriate boundary.
          if (isub > 0 && iq == 0) {
            Q += 1e-15; // first Q value in a subgrid
          } else if (isub < qs.size()-1 && iq == qs[isub].size()-1) {
            Q -= 1e-15; // last Q value in a subgrid
          }
          for (size_t iflavor = 0; iflavor < flavors[isub].size(); iflavor++) {
            if (irep > 0) {
              vector<double> xfAll;
              for (int imem = 0; imem <= nmem; imem++) {
                int flavor = flavors[isub][iflavor];
                xfAll.push_back(pdfs[imem]->xfxQ(flavor,x,Q));
              }
              // Get random value for PDF (scaling to 1-sigma is automatic).
              double xfrand = set.randomValueFromHessian(xfAll, randoms, symmetrise);
              sprintf(buffer, "%2.8e", xfrand);
              // Check that xfmean is initialised to zero.
              if (irep == 1 && xfmean[isub][ix][iq][iflavor] != 0.0) {
                throw LHAPDF::LogicError("Error: xfmean[" + LHAPDF::to_str(isub) + "][" + LHAPDF::to_str(ix) + "][" + LHAPDF::to_str(iq) + "][" + LHAPDF::to_str(iflavor) + "] = " + LHAPDF::to_str(xfmean[isub][ix][iq][iflavor]));
              }
              xfmean[isub][ix][iq][iflavor] += xfrand;
            } else {
              xfmean[isub][ix][iq][iflavor] /= nrep;
              sprintf(buffer,"%2.8e",xfmean[isub][ix][iq][iflavor]);
            }
            outfile << buffer;
            if (iflavor < flavors[isub].size()-1) outfile << " ";
          } // iflavor
          outfile << endl;
        } // iq
      } // ix
      outfile << "---" << endl;
    } // isub
    outfile.close();
  } // ireplica

}
