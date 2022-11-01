// Example program for testing the info system

#include "LHAPDF/Info.h"
#include "LHAPDF/Config.h"
#include "LHAPDF/PDFInfo.h"
#include "LHAPDF/PDFSet.h"
#include "LHAPDF/Factories.h"
#include <iostream>
using namespace std;

int main() {

  LHAPDF::Info& cfg = LHAPDF::getConfig();
  // cout << "UndefFlavorAction: " << cfg.get_entry("UndefFlavorAction") << endl;
  cout << "Verbosity: " << cfg.get_entry("Verbosity") << endl;
  cfg.set_entry("Verbosity", 5);
  const LHAPDF::Info& cfg2 = LHAPDF::getConfig();
  cout << "New Verbosity from second Config: " << cfg2.get_entry("Verbosity") << endl;

  const LHAPDF::PDFSet set("CT10nlo");
  cout << "SetDesc: " << set.get_entry("SetDesc") << endl;
  cout << "Verbosity from set: " << set.get_entry("Verbosity") << endl;

  const LHAPDF::PDFInfo info("CT10nlo", 2);
  if (info.has_key("PdfDesc")) cout << "PdfDesc: " << info.get_entry("PdfDesc") << endl;
  cout << "PdfType: " << info.get_entry("PdfType") << endl;
  cout << "Verbosity from PDF: " << info.get_entry("Verbosity") << endl;
  vector<int> pids = info.get_entry_as< vector<int> >("Flavors");
  cout << "PIDs (1): "; for (int f : pids) { cout << f << " "; } cout << endl;
  cout << "PIDs (2): " << LHAPDF::to_str(pids) << endl;

  // Now test loading of all central PDFs
  for (const string& name : LHAPDF::availablePDFSets()) {
    cout << "Testing PDFInfo for " << name << endl;
    LHAPDF::PDFInfo* i = LHAPDF::mkPDFInfo(name, 0);
    i->has_key("Foo"); // < Force loading of all info levels
    delete i;
  }

  return 0;
}
