import ROOT
hist_file = ROOT.TFile.Open("../HNL_Majorana_20GeV_1e-3Ve_analysis/output_finalSel_HNL_Majorana_20GeV_1e-3Ve/HNL_Majorana_20GeV_1e-3Ve_selNone_histo.root")
histSelect = ROOT.TFile.Open("histMajoranaSelect.root", "RECREATE")
histSelect.WriteObject(hist_file.Get("FSGenElectron_phi"), "FSGenElectron_phi")
histSelect.WriteObject(hist_file.Get("FSGenElectron_theta"), "FSGenElectron_theta")
histSelect.WriteObject(hist_file.Get("RecoElectron_pt"), "RecoElectron_pt")
histSelect.WriteObject(hist_file.Get("RecoElectron_phi"), "RecoElectron_phi")
histSelect.WriteObject(hist_file.Get("RecoElectron_theta"), "RecoElectron_theta")
histSelect.WriteObject(hist_file.Get("RecoElectron_e"), "RecoElectron_e")
histSelect.WriteObject(hist_file.Get("RecoMissingEnergy_e"), "RecoMissingEnergy_e")




