import ROOT
hist_file = ROOT.TFile.Open("../HNL_Majorana_20GeV_1e-3Ve_analysis/output_finalSel_HNL_Majorana_20GeV_1e-3Ve/HNL_Majorana_20GeV_1e-3Ve_selNone_histo.root")
histSelect = ROOT.TFile.Open("histMajoranaSelect.root", "RECREATE")
histSelect.WriteObject(hist_file.Get("RecoElectron_theta"), "RecoElectron_theta")
h1 = histSelect.Get("RecoElectron_theta")
#h1.Draw()
c1 = TCanvas()
c1.Draw()


