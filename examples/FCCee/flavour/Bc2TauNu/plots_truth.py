import ROOT as r
from math import sqrt
r.gROOT.Reset()
r.gROOT.SetBatch(True)
r.gROOT.ForceStyle()
r.gStyle.SetOptStat(0)


f = r.TFile("/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/events_Bc2TauNuTAUHADNU_truth.root")
tree = f.Get("events")



                
                #"B_theta","B_phi","B_e","B_charge",
                
                #"Nu1_theta","Nu1_phi","Nu1_e","Nu1_charge",
                
                #"Nu2_theta","Nu2_phi","Nu2_e","Nu2_charge",



variables=['minPionE','deltaAlpha_max','deltaAlpha_min','deltaAlpha_ave','n_BTracks','Pion1_e','Pion2_e','Pion3_e','Pion1_theta','Pion2_theta','Pion3_theta','Pion1_phi','Pion2_phi','Pion3_phi','Nu1_e','Nu2_e','Nu1_theta','Nu2_theta','Nu1_phi','Nu2_phi']
bins=[100,100,100,100,5,200,200,200,100,100,100,100,100,100,100,100,100,100,100,100]
binsl=[0,0,0,0,0,0,0,0,0,0,0,-4,-4,-4,0,0,0,0,-4,-4]
binsh=[20,3,3,3,5,40,40,40,4,4,4,4,4,4,40,40,4,4,4,4]
names=['min #pi energy [GeV]','#Delta #alpha max 3#pi','#Delta #alpha min 3#pi','#Delta #alpha average 3#pi','n Tracks','Leading pion energy [GeV]','Sub leading pion energy [GeV]','Sub sub leading pion energy [GeV]','Leading pion energy #theta','Sub leading pion energy #theta','Sub sub leading pion energy #theta','Leading pion energy #phi','Sub leading pion energy #phi','Sub sub leading pion energy #phi','Leading neutrino energy [GeV]','Sub leading neutrino energy [GeV]','Leading neutrino energy #theta','Sub leading neutrino energy #theta','Leading neutrino energy #phi','Sub leading neutrino energy #phi']


for i in range(len(variables)):
    ###################################################
    h = r.TH1F("h",";{};".format(names[i]), bins[i],binsl[i],binsh[i])
    tree.Draw("{}>> h".format(variables[i]))

    can = r.TCanvas("can","can")
    h.SetLineColor(4)
    h.Scale(1./h.Integral(0,-1))
    #h.SetMaximum(0.35)
    h.SetMinimum(0.)
    h.Draw("HIST,E1")

    tt=r.TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}, Bc #rightarrow #tau#nu, #tau #rightarrow 3#pi")
    #tt.DrawLatexNDC(0.60,0.85,"#color[2]{MC vertex}")
    #tt.DrawLatexNDC(0.60,0.79,"#color[4]{Reco vertex}")
    #r.gPad.SetLogy(1)
    can.SaveAs("plots_truth/pdf/{}.pdf".format(variables[i]))
    can.SaveAs("plots_truth/png/{}.png".format(variables[i]))
###################################################

