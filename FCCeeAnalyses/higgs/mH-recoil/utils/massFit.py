#!/usr/bin/env python3

#####################################################################################
#   Macro to fit the higgs recoil mass out of FlatNtuples produced by FCCAnalysis   #
#   Author: Clement Helsens (clement.helsens@cern.ch)                               #
#   Date: November 2020                                                             #
#####################################################################################

import ROOT as r
import sys

if len(sys.argv)!=4 and len(sys.argv)!=6:
    print ('usage:   python massFit.py BASEDIR HISTONAME SELECTION BINLOW=120 BINHIGH=140')
    print ('example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zee/ leptonic_recoil_m_zoom3 sel1')
    print ('example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zmumu/ leptonic_recoil_m_zoom4 sel0 122 128')
    sys.exit(3)

basedir=sys.argv[1]
hname=sys.argv[2]
selection=sys.argv[3]
binlow=120
binhigh=140

if len(sys.argv)==6:
    binlow=float(sys.argv[4])
    binhigh=float(sys.argv[5])

if basedir[-1]!='/':
    basedir+='/'

infile=basedir+'p8_ee_ZH_ecm240_{}_histo.root'.format(selection)
print (infile)
tfsig=r.TFile(infile)
histosig=tfsig.Get(hname)

infile=basedir+'p8_ee_ZZ_ecm240_{}_histo.root'.format(selection)
tfbg1=r.TFile(infile)
histobg1=tfbg1.Get(hname)
print (infile)

infile=basedir+'p8_ee_WW_ecm240_{}_histo.root'.format(selection)
tfbg2=r.TFile(infile)
histobg2=tfbg2.Get(hname)
print (infile)


histosig.Add(histobg1)
histosig.Add(histobg2)

#Scale to lumi
histosig.Scale(5.0e+06)

#bins for the fit
x = r.RooRealVar("recoil", "M_{recoil} [GeV]", binlow, binhigh)

# data is breit-wigner convoluted with a gaussian, taken from histogram
dhData = r.RooDataHist("dhData", "dhData", r.RooArgList(x), r.RooFit.Import(histosig))

cbmean  = r.RooRealVar("cbmean", "cbmean" , 125.0, 120., 130.0)
cbsigma = r.RooRealVar("cbsigma", "cbsigma" , 0.2, 0.0, 0.6)
n     = r.RooRealVar("n","n", 0.9,0.,100.0)
alpha   = r.RooRealVar("alpha","alpha", -1.2,-5.,-0.0001)
cball   = r.RooCBShape("cball", "crystal ball", x, cbmean, cbsigma, alpha, n)

lam = r.RooRealVar("lam","lam",-1e-3,-1,-1e-10)
bkg = r.RooExponential("bkg","bkg",x,lam)

nsig  = r.RooRealVar("nsig", "number of signal events", 10000, 0., 10000000)
nbkg  = r.RooRealVar("nbkg", "number of background events", 50000, 0, 10000000)
model = r.RooAddPdf("model","(g1+g2)+a",r.RooArgList(bkg,cball),r.RooArgList(nbkg,nsig))

result = model.fitTo(dhData,r.RooFit.Save(),r.RooFit.NumCPU(8,0),r.RooFit.Extended(True),r.RooFit.Optimize(False),r.RooFit.Offset(True),r.RooFit.Minimizer("Minuit2","migrad"),r.RooFit.Strategy(2))

frame = x.frame(r.RooFit.Title("recoil "), )
dhData.plotOn(frame,r.RooFit.Name("data"))
model.plotOn(frame,r.RooFit.Name("model"))

ras_bkg = r.RooArgSet(bkg)
model.plotOn(frame, r.RooFit.Components(ras_bkg), r.RooFit.LineStyle(r.kDashed), r.RooFit.Name("ras_bkg"))

ras_sig = r.RooArgSet(cball)
model.plotOn(frame, r.RooFit.LineColor(r.kRed), r.RooFit.Components(ras_sig), r.RooFit.LineStyle(r.kDashed), r.RooFit.Name("ras_sig"))


c = r.TCanvas()
frame.Draw()

leg = r.TLegend(0.6,0.7,0.89,0.89)
leg.AddEntry(frame.findObject("data"),"FCC IDEA Delphes","ep")
leg.AddEntry(frame.findObject("model"),"S+B fit","l")
leg.AddEntry(frame.findObject("ras_sig"),"Signal","l")
leg.AddEntry(frame.findObject("ras_bkg"),"background","l")

leg.Draw()

r.gPad.SaveAs("fitResult.pdf")
r.gPad.SaveAs("fitResult.png")



fCB  = r.TF1("fCB","crystalball")

fCB.SetParameter(0, 1.)
fCB.SetParameter(1, 125.)
fCB.SetParameter(2, 0.5)
fCB.SetParameter(3, -1.)
fCB.SetParameter(4, 1.)
fCB.SetRange(120.,128.)




c = r.TCanvas()
#c.SetLogy()
histosig.Draw()
histosig.Fit(fCB)
