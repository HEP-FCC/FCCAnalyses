import ROOT as r
from math import sqrt
r.gROOT.Reset()
r.gROOT.SetBatch(True)
r.gROOT.ForceStyle()
r.gStyle.SetOptStat(0)


f = r.TFile("/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/events_Bc2TauNuTAUHADNU_truth.root")
tree = f.Get("events")


variables=['Pion1_e','Pion2_e','Pion3_e']
names=['Leading pion energy [GeV]','Sub leading pion energy [GeV]','Sub sub leading pion energy [GeV]']

###################################################
h = r.TH1F("h",";;", 20,0,20)
tree.Draw("MC_Vertex_n>> h_mc")

h_reco = r.TH1F("h_reco",";N vertex;", 20,0,20)
tree.Draw("Vertex_n>> h_reco")

can = r.TCanvas("can","can")
h_reco.SetLineColor(4)
h_reco.Scale(1./h_reco.Integral(0,-1))
h_reco.SetMaximum(0.35)
h_reco.SetMinimum(0.)
h_reco.Draw("HIST,E1")
h_mc.SetLineColor(2)
h_mc.Scale(1./h_mc.Integral(0,-1))
h_mc.Draw("HIST,same,E1")

tt=r.TLatex()
tt.SetTextSize(0.04)
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85,"#color[2]{MC vertex}")
tt.DrawLatexNDC(0.60,0.79,"#color[4]{Reco vertex}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/nVertex.pdf")
can.SaveAs("plots/png/nVertex.png")
###################################################

