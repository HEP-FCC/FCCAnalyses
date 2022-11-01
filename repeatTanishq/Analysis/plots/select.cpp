void select(){
TFile *file = new TFile("../HNL_Majorana_20GeV_1e-3Ve_analysis/output_finalSel_HNL_Majorana_20GeV_1e-3Ve/HNL_Majorana_20GeV_1e-3Ve_selNone_histo.root", "READ");
TH1D *h1 = (TH1D *)file->Get("RecoElectron_theta");
TCanvas *c1 = new TCanvas();
c1-> Draw();
h1->Draw();

int nbin = h1->GetNbinsX();
double x[nbin - 1];

for (int i{0}; i< nbin; ++i){
	x[i] = cos(h1->GetXaxis()-> GetBinCenter(nbin - i));
}

int n = sizeof(x)/sizeof(x[0]);
std::sort(x,x+n);

TH1D *h2 = new TH1D("nom", "titre", nbin-2, x);
h2->Draw();

}
