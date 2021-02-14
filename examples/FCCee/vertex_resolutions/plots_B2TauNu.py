import ROOT as r
r.gROOT.SetBatch(True)
r.gROOT.ForceStyle()
r.gStyle.SetOptStat(0)

#Change your basepath and the name of your output files, below are test files
basepath='/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Bc2TauNu_vertex/'
fBc = 'events_Bc2TauNuTAUHADNU_test.root'
fBu = 'events_Bu2TauNuTAUHADNU_test.root'

tfBc = r.TFile(basepath+fBc)
tfBu = r.TFile(basepath+fBu)

tName='events'
ttBc = tfBc.Get(tName)
ttBu = tfBu.Get(tName)

print ('nevents Bc : ',ttBc.GetEntries())
print ('nevents Bu : ',ttBu.GetEntries())

cut0   = "TauMCDecayVertex.z < 1e10"
cut0_B = "TauMCDecayVertex.z < 1e10 && n_BTracks==3"


########################################
##########Number of tracks##############
########################################
hntr_Bc = r.TH1F("hntr_Bc",";N( B tracks ); a.u.",5,-0.5,4.5)
ttBc.Draw("n_BTracks >>hntr_Bc")
hntr_Bu = r.TH1F("hntr_Bu",";N( B tracks ); a.u.",5,-0.5,4.5)
ttBu.Draw("n_BTracks >>hntr_Bu")
cnt = r.TCanvas("cnt","cnt")
hntr_Bu.Scale(1./hntr_Bu.Integral(0,-1))
hntr_Bu.SetLineColor(4)
hntr_Bu.Draw("HIST,E1")
hntr_Bc.Scale(1./hntr_Bc.Integral(0,-1))
hntr_Bc.SetLineColor(2)
hntr_Bc.Draw("HIST,same,E1")

tt=r.TLatex()
tt.SetTextSize(0.04)
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
r.gPad.SetLogy(1)
cnt.SaveAs(basepath+"plots/nTracks.pdf")
cnt.SaveAs(basepath+"plots/nTracks.png")


print ('ntracks = 1 Bu : ',hntr_Bu.GetBinContent(2),'+/-',hntr_Bu.GetBinError(2))
print ('ntracks = 1 Bc : ',hntr_Bc.GetBinContent(2),'+/-',hntr_Bc.GetBinError(2))
print ('ntracks = 2 Bu : ',hntr_Bu.GetBinContent(3),'+/-',hntr_Bu.GetBinError(3))
print ('ntracks = 2 Bc : ',hntr_Bc.GetBinContent(3),'+/-',hntr_Bc.GetBinError(3))
print ('ntracks = 3 Bu : ',hntr_Bu.GetBinContent(4),'+/-',hntr_Bu.GetBinError(4))
print ('ntracks = 3 Bc : ',hntr_Bc.GetBinContent(4),'+/-',hntr_Bc.GetBinError(4))


########################################
##########Flight  distance##############
########################################


hfd_Bc = r.TH1F("hfd_Bc",";distance to the tertiary reco vertex (mm); a.u.",100,0.,20)
ttBc.Draw("TMath::Sqrt( pow( BVertex.position.x, 2) + pow( BVertex.position.y,2) + pow( BVertex.position.z,2)) >>hfd_Bc",cut0_B+"&& BVertex.chi2>0")
hfd_Bu = r.TH1F("hfd_Bu",";distance to the tertiary reco vertex (mm); a.u.",100,0.,20)
ttBu.Draw("TMath::Sqrt( pow( BVertex.position.x, 2) + pow( BVertex.position.y,2) + pow( BVertex.position.z,2)) >>hfd_Bu",cut0_B+"&& BVertex.chi2>0")
cfd = r.TCanvas("cfd","cfd")
hfd_Bc.Scale(1./hfd_Bc.Integral(0,-1))
hfd_Bc.SetLineColor(2)
hfd_Bc.Draw("HIST")
hfd_Bu.Scale(1./hfd_Bu.Integral(0,-1))
hfd_Bu.SetLineColor(4)
hfd_Bu.Draw("HIST,same")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
r.gPad.SetLogy(0)
tt.DrawLatexNDC(0.5,0.8  ,"#color[4]{Mean B^{#pm}: %f}"%hfd_Bu.GetMean())
tt.DrawLatexNDC(0.5,0.75 ,"#color[2]{Mean B_{c}^{#pm}: %f}"%hfd_Bc.GetMean())
cfd.SaveAs(basepath+"plots/tertiarydist.pdf")
cfd.SaveAs(basepath+"plots/tertiarydist.png")

########################################
##########Chi2 of the vfit##############
########################################
hchi2_Bc = r.TH1F("hchi2_Bc",";#chi^{2}/n.d.f.; a.u.",100,0.,10.)
ttBc.Draw("BVertex.chi2 >>hchi2_Bc",cut0_B+"&& BVertex.chi2>0")
hchi2_Bu = r.TH1F("hchi2_Bu",";#chi^{2}/n.d.f.; a.u.",100,0.,10.)
ttBu.Draw("BVertex.chi2 >>hchi2_Bu",cut0_B+"&& BVertex.chi2>0")
cchi2 = r.TCanvas("cchi2","cchi2")
hchi2_Bc.Scale(1./hchi2_Bc.Integral(0,-1))
hchi2_Bc.SetLineColor(2)
hchi2_Bc.Draw("HIST")
hchi2_Bu.Scale(1./hchi2_Bu.Integral(0,-1))
hchi2_Bu.SetLineColor(4)
hchi2_Bu.Draw("HIST,same")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
tt.DrawLatexNDC(0.5,0.8  ,"#color[4]{Mean B^{#pm}: %f}"%hchi2_Bu.GetMean())
tt.DrawLatexNDC(0.5,0.75 ,"#color[2]{Mean B_{c}^{#pm}: %f}"%hchi2_Bc.GetMean())

r.gPad.SetLogy(1)
cchi2.SaveAs(basepath+"plots/chi2.pdf")
cchi2.SaveAs(basepath+"plots/chi2.png")



###################################################
##########Pulls of the vertex in x, y, z###########
###################################################
cut_B = cut0_B+" && BVertex.chi2 >= 0 && BVertex.chi2 < 10"

px_Bc = r.TH1F("px_Bc",";Pull x_{vtx}; a.u.",100,-5,5)
ttBc.Draw("(BVertex.position.x-TauMCDecayVertex.x[0])/TMath::Sqrt(BVertex.covMatrix[0])>>px_Bc",cut_B)
py_Bc = r.TH1F("py_Bc",";Pull y_{vtx}; a.u.",100,-5,5)
ttBc.Draw("(BVertex.position.y-TauMCDecayVertex.y[0])/TMath::Sqrt(BVertex.covMatrix[3])>>py_Bc",cut_B)
pz_Bc = r.TH1F("pz_Bc",";Pull z_{vtx}; a.u.",100,-5,5)
ttBc.Draw("(BVertex.position.z-TauMCDecayVertex.z[0])/TMath::Sqrt(BVertex.covMatrix[5])>>pz_Bc",cut_B)

px_Bu = r.TH1F("px_Bu",";Pull x_{vtx}; a.u.",100,-5,5)
ttBu.Draw("(BVertex.position.x-TauMCDecayVertex.x[0])/TMath::Sqrt(BVertex.covMatrix[0])>>px_Bu",cut_B)
py_Bu = r.TH1F("py_Bu",";Pull y_{vtx}; a.u.",100,-5,5)
ttBu.Draw("(BVertex.position.y-TauMCDecayVertex.y[0])/TMath::Sqrt(BVertex.covMatrix[3])>>py_Bu",cut_B)
pz_Bu = r.TH1F("pz_Bu",";Pull z_{vtx}; a.u.",100,-5,5)
ttBu.Draw("(BVertex.position.z-TauMCDecayVertex.z[0])/TMath::Sqrt(BVertex.covMatrix[5])>>pz_Bu",cut_B)


cpulls = r.TCanvas("pulls","pulls")

px_Bu.Scale(1./px_Bu.Integral(0,-1))
px_Bu.SetLineColor(4)
px_Bu.Draw("HIST")
px_Bc.Scale(1./px_Bc.Integral(0,-1))
px_Bc.SetLineColor(2)
px_Bc.Draw("HIST,same")

fBu = r.TF1("fBu","gaus",-5,5)
px_Bu.Fit("fBu","l")
fBu.SetLineColor(4)
fBu.Draw("same")
tt.DrawLatexNDC(0.15,0.75,"#color[4]{#sigma_{x} B^{#pm} = %f}"%fBu.GetParameter(2))
fBc = r.TF1("fBc","gaus",-5,5)
px_Bc.Fit("fBc","l")
fBc.SetLineColor(2)
fBc.Draw("same")
tt.DrawLatexNDC(0.15,0.8,"#color[2]{#sigma_{x} B_{c}^{#pm} = %f}"%fBc.GetParameter(2))

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cpulls.SaveAs(basepath+"plots/pulls_x.pdf");
cpulls.SaveAs(basepath+"plots/pulls_x.png");


py_Bu.Scale(1./py_Bu.Integral(0,-1))
py_Bu.SetLineColor(4)
py_Bu.Draw("HIST")
py_Bc.Scale(1./py_Bc.Integral(0,-1))
py_Bc.SetLineColor(2)
py_Bc.Draw("HIST,same")
#px_Bc.Fit("gaus")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cpulls.SaveAs(basepath+"plots/pulls_y.pdf");
cpulls.SaveAs(basepath+"plots/pulls_y.png");


pz_Bu.Scale(1./pz_Bu.Integral(0,-1))
pz_Bu.SetLineColor(4)
pz_Bu.Draw("HIST")
pz_Bc.Scale(1./pz_Bc.Integral(0,-1))
pz_Bc.SetLineColor(2)
pz_Bc.Draw("HIST,same")
#px_Bc.Fit("gaus")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cpulls.SaveAs(basepath+"plots/pulls_z.pdf");
cpulls.SaveAs(basepath+"plots/pulls_z.png");


#################################
######### resolutions ###########
#################################
creso = r.TCanvas("reso","reso")
hx_Bc = r.TH1F("hx_Bc",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-100,100)
ttBc.Draw("1e3*(BVertex.position.x-TauMCDecayVertex.x[0]) >>hx_Bc",cut_B)
hx_Bc.Scale(1./hx_Bc.Integral(0,-1))
hx_Bc.SetLineColor(2)

hx_Bu = r.TH1F("hx_Bu",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-100,100)
ttBu.Draw("1e3*(BVertex.position.x-TauMCDecayVertex.x[0]) >>hx_Bu",cut_B)
hx_Bu.Scale(1./hx_Bu.Integral(0,-1))
hx_Bu.SetLineColor(4)

hx_Bc.Draw("HIST")
hx_Bu.Draw("same,HIST")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
creso.SaveAs(basepath+"plots/reso_x.pdf")
creso.SaveAs(basepath+"plots/reso_x.png")

hy_Bc = r.TH1F("hy_Bc",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-100,100)
ttBc.Draw("1e3*(BVertex.position.y-TauMCDecayVertex.y[0]) >>hy_Bc",cut_B)
hy_Bc.Scale(1./hy_Bc.Integral(0,-1))
hy_Bc.SetLineColor(2)

hy_Bu = r.TH1F("hy_Bu",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-100,100)
ttBu.Draw("1e3*(BVertex.position.y-TauMCDecayVertex.y[0]) >>hy_Bu",cut_B)
hy_Bu.Scale(1./hy_Bu.Integral(0,-1))
hy_Bu.SetLineColor(4)

hy_Bc.Draw("HIST")
hy_Bu.Draw("same,HIST")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
creso.SaveAs(basepath+"plots/reso_y.pdf")
creso.SaveAs(basepath+"plots/reso_y.png")

hz_Bc = r.TH1F("hz_Bc",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-100,100)
ttBc.Draw("1e3*(BVertex.position.z-TauMCDecayVertex.z[0]) >>hz_Bc",cut_B)
hz_Bc.Scale(1./hz_Bc.Integral(0,-1))
hz_Bc.SetLineColor(2)

hz_Bu = r.TH1F("hz_Bu",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-100,100)
ttBu.Draw("1e3*(BVertex.position.z-TauMCDecayVertex.z[0]) >>hz_Bu",cut_B)
hz_Bu.Scale(1./hz_Bu.Integral(0,-1))
hz_Bu.SetLineColor(4)

hz_Bc.Draw("HIST")
hz_Bu.Draw("same,HIST")
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
creso.SaveAs(basepath+"plots/reso_z.pdf")
creso.SaveAs(basepath+"plots/reso_z.png")


##############################################
####### resolution on flight  distance #######
##############################################

fld_B  = "TMath::Sqrt( pow( 1e3*BVertex.position.x, 2) + pow( 1e3*BVertex.position.y,2) + pow( 1e3*BVertex.position.z,2))"
fld_gen = "TMath::Sqrt( pow( 1e3*TauMCDecayVertex.x[0], 2) + pow( 1e3*TauMCDecayVertex.y[0],2) + pow( 1e3*TauMCDecayVertex.z[0],2) )"
fldres_B =  fld_B + " - " + fld_gen;

hfld_Bc = r.TH1F("hfld_Bc",";distance to tertiary vertex (rec-true) (#mum); Events",100,-150,150)
ttBc.Draw(fldres_B+ " >> hfld_Bc", cut_B)
hfld_Bc.Scale(1./hfld_Bc.Integral(0,-1))
hfld_Bc.SetLineColor(2)

hfld_Bu = r.TH1F("hfld_Bu",";distance to tertiary vertex (rec-true) (#mum); Events",100,-150,150)
ttBu.Draw(fldres_B+ " >> hfld_Bu", cut_B)
hfld_Bu.Scale(1./hfld_Bu.Integral(0,-1))
hfld_Bu.SetLineColor(4)
tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
hfld_Bu.Draw("HIST")
hfld_Bc.Draw("HIST,same")

fBc = r.TF1("fBc","gaus",-150,150)
hfld_Bc.Fit("fBc","l")
fBc.SetLineColor(2)
fBc.Draw("same")
tt.DrawLatexNDC(0.15,0.8,"#color[2]{#sigma_{x} B_{c}^{#pm} = %f}"%fBc.GetParameter(2))
fBu = r.TF1("fBu","gaus",-150,150)
hfld_Bu.Fit("fBu","l")
fBu.SetLineColor(4)
fBu.Draw("same")
tt.DrawLatexNDC(0.15,0.75,"#color[4]{#sigma_{x} B^{#pm} = %f}"%fBu.GetParameter(2))

creso.SaveAs(basepath+"plots/tertiaryvertexdistance_reso.pdf")
creso.SaveAs(basepath+"plots/tertiaryvertexdistance_reso.png")




########################################
##########Min Pion energy###############
########################################
hminPiE_Bc = r.TH1F("hminPiE_Bc",";Minimum Pion Energy [GeV]; a.u.",100,0.,10.)
ttBc.Draw("minPionE >>hminPiE_Bc")
hminPiE_Bu = r.TH1F("hminPiE_Bu",";Minimum Pion Energy [GeV]; a.u.",100,0.,10.)
ttBu.Draw("minPionE >>hminPiE_Bu")
cnt = r.TCanvas("cnt","cnt")
hminPiE_Bu.Scale(1./hminPiE_Bu.Integral(0,-1))
hminPiE_Bu.SetLineColor(4)
hminPiE_Bu.Draw("HIST,E1")
hminPiE_Bc.Scale(1./hminPiE_Bc.Integral(0,-1))
hminPiE_Bc.SetLineColor(2)
hminPiE_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/minPionE.pdf")
cnt.SaveAs(basepath+"plots/minPionE.png")


########################################
###############B energy#################
########################################
hE_Bc = r.TH1F("hE_Bc",";B Energy [GeV]; a.u.",100,0.,50.)
ttBc.Draw("B_e >>hE_Bc")
hE_Bu = r.TH1F("hE_Bu",";B Energy [GeV]; a.u.",100,0.,50.)
ttBu.Draw("B_e >>hE_Bu")
cnt = r.TCanvas("cnt","cnt")
hE_Bu.Scale(1./hE_Bu.Integral(0,-1))
hE_Bu.SetLineColor(4)
hE_Bu.Draw("HIST,E1")
hE_Bc.Scale(1./hE_Bc.Integral(0,-1))
hE_Bc.SetLineColor(2)
hE_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/Benergy.pdf")
cnt.SaveAs(basepath+"plots/Benergy.png")


########################################
#############Pion1 energy###############
########################################
hE_Pion1_Bc = r.TH1F("hE_Pion1_Bc",";Leading pion energy [GeV]; a.u.",100,0.,50.)
ttBc.Draw("Pion1_e >>hE_Pion1_Bc")
hE_Pion1_Bu = r.TH1F("hE_Pion1_Bu",";Leading pion energy [GeV]; a.u.",100,0.,50.)
ttBu.Draw("Pion1_e >>hE_Pion1_Bu")
cnt = r.TCanvas("cnt","cnt")
hE_Pion1_Bu.Scale(1./hE_Pion1_Bu.Integral(0,-1))
hE_Pion1_Bu.SetLineColor(4)
hE_Pion1_Bu.Draw("HIST,E1")
hE_Pion1_Bc.Scale(1./hE_Pion1_Bc.Integral(0,-1))
hE_Pion1_Bc.SetLineColor(2)
hE_Pion1_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/Pion1energy.pdf")
cnt.SaveAs(basepath+"plots/Pion1energy.png")

########################################
#############Pion2 energy###############
########################################
hE_Pion2_Bc = r.TH1F("hE_Pion2_Bc",";Sub-leading pion energy [GeV]; a.u.",100,0.,50.)
ttBc.Draw("Pion2_e >>hE_Pion2_Bc")
hE_Pion2_Bu = r.TH1F("hE_Pion2_Bu",";Sub-leading pion energy [GeV]; a.u.",100,0.,50.)
ttBu.Draw("Pion2_e >>hE_Pion2_Bu")
cnt = r.TCanvas("cnt","cnt")
hE_Pion2_Bu.Scale(1./hE_Pion2_Bu.Integral(0,-1))
hE_Pion2_Bu.SetLineColor(4)
hE_Pion2_Bu.Draw("HIST,E1")
hE_Pion2_Bc.Scale(1./hE_Pion2_Bc.Integral(0,-1))
hE_Pion2_Bc.SetLineColor(2)
hE_Pion2_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/Pion2energy.pdf")
cnt.SaveAs(basepath+"plots/Pion2energy.png")


########################################
#############Pion3 energy###############
########################################
hE_Pion3_Bc = r.TH1F("hE_Pion3_Bc",";Sub-sub-leading pion energy [GeV]; a.u.",100,0.,50.)
ttBc.Draw("Pion3_e >>hE_Pion3_Bc")
hE_Pion3_Bu = r.TH1F("hE_Pion3_Bu",";Sub-sub-leading pion energy [GeV]; a.u.",100,0.,50.)
ttBu.Draw("Pion3_e >>hE_Pion3_Bu")
cnt = r.TCanvas("cnt","cnt")
hE_Pion3_Bu.Scale(1./hE_Pion3_Bu.Integral(0,-1))
hE_Pion3_Bu.SetLineColor(4)
hE_Pion3_Bu.Draw("HIST,E1")
hE_Pion3_Bc.Scale(1./hE_Pion3_Bc.Integral(0,-1))
hE_Pion3_Bc.SetLineColor(2)
hE_Pion3_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/Pion3energy.pdf")
cnt.SaveAs(basepath+"plots/Pion3energy.png")

########################################
#############Nu1 energy###############
########################################
hE_Nu1_Bc = r.TH1F("hE_Nu1_Bc",";Leading neutrino energy [GeV]; a.u.",100,0.,50.)
ttBc.Draw("Nu1_e >>hE_Nu1_Bc")
hE_Nu1_Bu = r.TH1F("hE_Nu1_Bu",";leading neutrino energy [GeV]; a.u.",100,0.,50.)
ttBu.Draw("Nu1_e >>hE_Nu1_Bu")
cnt = r.TCanvas("cnt","cnt")
hE_Nu1_Bu.Scale(1./hE_Nu1_Bu.Integral(0,-1))
hE_Nu1_Bu.SetLineColor(4)
hE_Nu1_Bu.Draw("HIST,E1")
hE_Nu1_Bc.Scale(1./hE_Nu1_Bc.Integral(0,-1))
hE_Nu1_Bc.SetLineColor(2)
hE_Nu1_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/Nu1energy.pdf")
cnt.SaveAs(basepath+"plots/Nu1energy.png")

########################################
#############Nu2 energy###############
########################################
hE_Nu2_Bc = r.TH1F("hE_Nu2_Bc",";Sub-leading neutrino energy [GeV]; a.u.",100,0.,50.)
ttBc.Draw("Nu2_e >>hE_Nu2_Bc")
hE_Nu2_Bu = r.TH1F("hE_Nu2_Bu",";Sub-leading neutrino energy [GeV]; a.u.",100,0.,50.)
ttBu.Draw("Nu2_e >>hE_Nu2_Bu")
cnt = r.TCanvas("cnt","cnt")
hE_Nu2_Bu.Scale(1./hE_Nu2_Bu.Integral(0,-1))
hE_Nu2_Bu.SetLineColor(4)
hE_Nu2_Bu.Draw("HIST,E1")
hE_Nu2_Bc.Scale(1./hE_Nu2_Bc.Integral(0,-1))
hE_Nu2_Bc.SetLineColor(2)
hE_Nu2_Bc.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.2,0.96,"#color[2]{B_{c}^{#pm}} or #color[4]{B^{#pm}}  #rightarrow #tau#nu #tau #rightarrow #pi#pi#pi#nu")
cnt.SaveAs(basepath+"plots/Nu2energy.pdf")
cnt.SaveAs(basepath+"plots/Nu2energy.png")
