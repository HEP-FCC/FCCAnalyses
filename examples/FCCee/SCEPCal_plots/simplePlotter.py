#!/usr/bin/env python
### Produce very simple preliminary plots, no cuts applied, no matching of Cherenkov - Scintillation
import sys, os
import ROOT
from array import array
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetLabelSize(0.05,'X')
ROOT.gStyle.SetLabelSize(0.05,'Y')
ROOT.gStyle.SetTitleSize(0.06,'X')
ROOT.gStyle.SetTitleSize(0.06,'Y')
ROOT.gStyle.SetTitleOffset(0.8,'X')
ROOT.gStyle.SetTitleOffset(0.8,'Y')
ROOT.gStyle.SetLegendFont(42)
ROOT.gStyle.SetLegendTextSize(0.038)
ROOT.gStyle.SetPadTopMargin(0.07)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

parser = argparse.ArgumentParser(description='Module characterization summary plots')
parser.add_argument("--inputFile",   required=True, type=str, help="path to inputfile.root [output of ntuplizer]")
parser.add_argument("--outFolder",   required=True, type=str, help="out folder for plots")
args = parser.parse_args()

# input file should be flat ntupla from ntuplizer
outdir = args.outFolder
inputfile = args.inputFile
os.makedirs(outdir, exist_ok=True)
#os.system("cp /eos/user/f/fcetorel/www/index.php %s"%outdir)  



#Open the file - add some branches - create the canvas
d = ROOT.RDataFrame("events", inputfile)
d = d.Define("multiplicityS",  "SimCaloHit_energy.size()")\
     .Define("multiplicityC", "SimCaloHitC_energy.size()")\
     .Define("etaHitsS", "SimCaloHit_eta.size()")\
     .Define("phiHitsS", "SimCaloHit_phi.size()")\
     .Define("enetotF", "Sum(SimCaloHit_energy[SimCaloHit_depth == 1])")\
     .Define("enetotR", "Sum(SimCaloHit_energy[SimCaloHit_depth == 2])")\
     .Define("enetot", "Sum(SimCaloHit_energy)")\
     .Define("HitEnergyMax", "Max(SimCaloHit_energy)")\
     .Define("indexHitEnergyMax", "ArgMax(SimCaloHit_energy)")\
     .Define("etaMaxHit", "SimCaloHit_eta[indexHitEnergyMax]")\
     .Define("phiMaxHit", "SimCaloHit_phi[indexHitEnergyMax]")\
     .Define("rMaxHit", "SimCaloHit_r[indexHitEnergyMax]")\
     .Define("xMaxHit", "SimCaloHit_x[indexHitEnergyMax]")\
     .Define("yMaxHit", "SimCaloHit_y[indexHitEnergyMax]")\
     .Define("indexHitCherMax", "ArgMax(SimCaloHitC_energy)")\
     .Define("etaMaxHitC", "SimCaloHit_eta[indexHitCherMax]")\
     .Define("phiMaxHitC", "SimCaloHit_phi[indexHitCherMax]")\
     .Define("rMaxHitC", "SimCaloHit_r[indexHitCherMax]")\
     .Define("xMaxHitC", "SimCaloHit_x[indexHitCherMax]")\
     .Define("yMaxHitC", "SimCaloHit_y[indexHitCherMax]") 



c = ROOT.TCanvas("c","",800,600)

#Get the En from the file
pGunEnergy = d.Histo1D ( ("pGunEnergy", "pGunEnergy", 50, 0, 50) , "MCparticle_energy" ).GetMean()

#Define the histos 1D


myhistos1D = {}
#myhistos1D.append(d.Histo1D (  , "" ))

myhistos1D["hMultiplicityS"] = d.Histo1D ( ("hMultiplicityS", "hMultiplicityS", 1500, 0, 1500) , "multiplicityS" )
myhistos1D["hMultiplicityC"] = d.Histo1D ( ("hMultiplicityC", "hMultiplicityC", 1500, 0, 1500) , "multiplicityC" )
myhistos1D["hEtaHits"] = d.Histo1D (("hEtaHits", "hEtaHits", 100, -10, 10) , "etaHitsS" )
myhistos1D["hPhiHits"] = d.Histo1D (("hPhiHits", "hPhiHits", 100, -6.28, 6.28), "phiHitsS" )
myhistos1D["hEneHits"] = d.Histo1D (("hEneHits", ";Hit energy [GeV]; Counts", 1000, 0, pGunEnergy*1.25), "SimCaloHit_energy" )  
myhistos1D["hTotEne"]  = d.Histo1D (("hTotEne", " ;Total energy deposited [GeV]; Counts", 1000, 0, pGunEnergy*1.25), "enetot" )
myhistos1D["hTotEneF"] = d.Histo1D (("hTotEneF"," ;Total energy deposited [GeV]; Counts", 1000, 0, pGunEnergy*1.25), "enetotF" )
myhistos1D["hTotEneR"] = d.Histo1D (("hTotEneR"," ;Total energy deposited [GeV]; Counts", 1000, 0, pGunEnergy*1.25), "enetotR" )


#Define the histos 2D
myhistos2D = {}
#myhistos2D.append(d.Histo2D (, "" ))
myhistos2D["hScatterMultiplicity"] = d.Histo2D (("hScatterMultiplicity", ";S hits multiplicity; C hits multiplicity", 300, 0, 1500, 300, 0, 1500), "multiplicityS", "multiplicityC" )
#myhistos2D.append(d.Histo2D (("hScatterCS", "", 1000, 0, 20, 1000, 0, 1000), "" , ""))
myhistos2D["hTotEne_vs_eta"] = d.Histo2D (("hTotEne_vs_eta", ";#eta;Tot energy [GeV]", 100, -3.2, 3.2 , 1000, 0, pGunEnergy*1.25), "etaMaxHit" , "enetot")
myhistos2D["hTotEne_vs_phi"] = d.Histo2D (("hTotEne_vs_phi", ";#Phi;Tot energy [GeV]", 100, -3.2, 3.2 , 1000, 0, pGunEnergy*1.25), "phiMaxHit" , "enetot" )

### Now drawing
ROOT.gStyle.SetOptStat(1)

for key, h in myhistos1D.items():
    c.Clear()
    c.cd()
    
    #h.GetXaxis().SetRangeUser(0, h.GetMean()+ h.GetRMS()*5)
    h.Draw()
    c.SetLogy(0)
    c.SaveAs("%s/histo1D_%s.png"%(outdir,key))
    
    c.SetLogy() 
    c.SaveAs("%s/log_histo1D_%s.png"%(outdir,key))

ROOT.gStyle.SetOptStat(0)

for key, h in myhistos2D.items():
    c.Clear()
    c.cd()
    h.Draw("COLZ")
    
    c.SetLogy(0)
    c.SaveAs("%s/histo2D_%s.png"%(outdir,key))


### Ene Hits
myhistos1D["hEneHits"].SetStats(0)
c.SetLogy()
c.SetLogx()
myhistos1D["hEneHits"].GetXaxis().SetRangeUser(0.05,pGunEnergy*1.1)
myhistos1D["hEneHits"].Draw("")

c.SaveAs("%s/cSCEP_EneHits.png"%outdir)


c.SetLogx(0)
### Energy
myhistos1D["hTotEne"].SetStats(0)

ROOT.gStyle.SetOptStat(1)
myhistos1D["hTotEne"].SetStats(1)
myhistos1D["hTotEne"].GetXaxis().SetRangeUser(pGunEnergy*0.7,pGunEnergy*1.1)
myhistos1D["hTotEne"].Draw("")

c.SetLogy(1)
c.SaveAs("%s/cSCEP_TotEnergy.png"%outdir)


c.Clear()
c.SetLogy(0)

### Histo multiplicity
ROOT.gStyle.SetOptStat(0)
myhistos2D["hScatterMultiplicity"].SetStats(0)
myhistos2D["hScatterMultiplicity"].GetXaxis().SetRangeUser(10, myhistos1D["hMultiplicityS"].GetMean()+ myhistos1D["hMultiplicityS"].GetRMS()*5)
myhistos2D["hScatterMultiplicity"].GetYaxis().SetRangeUser(10, myhistos1D["hMultiplicityS"].GetMean()+ myhistos1D["hMultiplicityS"].GetRMS()*5)
myhistos2D["hScatterMultiplicity"].Draw("COLZ")
#c.SetLogz()
c.SaveAs("%s/cSCEP_ScatterMultiplicity.png"%outdir)

# ETA
ROOT.gStyle.SetOptStat(0)
myhistos2D["hTotEne_vs_eta"].SetStats(0)
myhistos2D["hTotEne_vs_eta"].GetYaxis().SetRangeUser(pGunEnergy*0.6,pGunEnergy*1.1)
myhistos2D["hTotEne_vs_eta"].Draw("COLZ")
#c.SetLogz()
c.SaveAs("%s/cSCEP_hTotEne_vs_eta.png"%outdir)

#PHI
myhistos2D["hTotEne_vs_phi"].SetStats(0)
myhistos2D["hTotEne_vs_phi"].GetYaxis().SetRangeUser(pGunEnergy*0.6,pGunEnergy*1.1)
myhistos2D["hTotEne_vs_phi"].Draw("COLZ")
#c.SetLogz()
c.SaveAs("%s/cSCEP_hTotEne_vs_phi.png"%outdir)



##### Energy sharing plots
c.Clear()

ROOT.gStyle.SetOptStat(0)
myhistos1D["hTotEne"].Draw()
myhistos1D["hTotEne"].GetXaxis().SetRangeUser(0,pGunEnergy*1.1)
myhistos1D["hTotEne"].SetStats(0)
#myhistos1D["hTotEne"].SetTitle(0)  
myhistos1D["hTotEne"].SetLineWidth(2)
myhistos1D["hTotEne"].GetXaxis().SetTitle("Energy deposited in SCEPCAL [GeV]")
myhistos1D["hTotEne"].GetYaxis().SetTitle("Counts")
myhistos1D["hTotEne"].GetYaxis().SetRangeUser(1, myhistos1D["hTotEne"].GetMaximum()*5)
myhistos1D["hTotEne"].SetLineColor(1)



myhistos1D["hTotEneF"].SetStats(0)
myhistos1D["hTotEneF"].SetLineColor(416  + 1)
myhistos1D["hTotEneF"].SetLineWidth(2)
myhistos1D["hTotEneF"].Draw("same")


myhistos1D["hTotEneR"].SetStats(0)
myhistos1D["hTotEneR"].SetLineColor(600)
myhistos1D["hTotEneR"].SetLineWidth(2)
myhistos1D["hTotEneR"].Draw("same")

leg = ROOT.TLegend(0.15,0.68,0.45,0.88)

h = myhistos1D["hTotEne"]
leg.AddEntry( "hTotEneF" , "Front crystal", "lp")    
leg.AddEntry("hTotEneR"  , "Rear crystal", "lp")    
leg.AddEntry( "hTotEne"  , "Total", "lp")

leg.Draw("same")

c.SetLogy()
c.SaveAs("%s/cSCEP_EneSharing.png"%outdir)

### nHits plots  
c.Clear()

ROOT.gStyle.SetOptStat(0)
myhistos1D["hMultiplicityS"].Draw("")
myhistos1D["hMultiplicityS"].SetStats(0)
myhistos1D["hMultiplicityC"].SetStats(0)
myhistos1D["hMultiplicityS"].GetXaxis().SetTitle("Hits Multiplicity")
myhistos1D["hMultiplicityS"].GetYaxis().SetTitle("Counts")
myhistos1D["hMultiplicityS"].GetYaxis().SetRangeUser(1, myhistos1D["hTotEne"].GetMaximum()*5)

myhistos1D["hMultiplicityS"].SetLineColor(416  + 1)
myhistos1D["hMultiplicityS"].SetLineWidth(2)
myhistos1D["hMultiplicityS"].Draw("")

myhistos1D["hMultiplicityC"].SetLineColor(600)
myhistos1D["hMultiplicityC"].SetLineWidth(2)
myhistos1D["hMultiplicityC"].Draw("same")


leg = ROOT.TLegend(0.15,0.68,0.45,0.88)

leg.AddEntry( "hMultiplicityS" , "Scintillation", "lp")    
leg.AddEntry( "hMultiplicityC"  , "Cherenkov", "lp")    

leg.Draw("same")

c.SetLogy()
c.SaveAs("%s/cSCEP_Multiplicity.png"%outdir)
  






