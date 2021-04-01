import ROOT as r

r.gROOT.Reset()
r.gROOT.SetBatch(True)
r.gROOT.ForceStyle()
r.gStyle.SetOptStat(0)


f = r.TFile("/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses/flat_ee_Zbb_vertexPerf.root")
tree = f.Get("events")

#--------------------------------------------#
#--------------------------------------------#
#     Plots that do not need event loop      #
#--------------------------------------------#
#--------------------------------------------#


#---------------------------------#
#  Plot number of vertex MC/Reco  #
#---------------------------------#

#All vertex
h_mc = r.TH1F("h_mc",";N vertex;", 20,0,20)
tree.Draw("MC_Vertex_n>> h_mc")

h_reco = r.TH1F("h_reco",";N vertex;", 20,0,20)
tree.Draw("Vertex_n>> h_reco")

can = r.TCanvas("can","can")
h_reco.SetLineColor(4)
h_reco.Scale(1./h_reco.Integral(0,-1))
h_reco.SetMaximum(0.35)
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



#--------------------------------------------#
#--------------------------------------------#
#       Plots that do need event loop        #
#--------------------------------------------#
#--------------------------------------------#


h_mc   = r.TH1F("h_mc",";N vertex;", 20,0,20)
h_recoChi2Cut = r.TH1F("h_recoChi2Cut",";N vertex;", 20,0,20)

h_ntrk_mc_pv = r.TH1F("h_ntrk_mc_pv",";N tracks PV;", 30,0,30)
h_ntrk_mc_sv = r.TH1F("h_ntrk_mc_sv",";N tracks SV;", 10,0,10)

h_ntrk_rc_pv = r.TH1F("h_ntrk_rc_pv",";N tracks PV;", 30,0,30)
h_ntrk_rc_sv = r.TH1F("h_ntrk_rc_sv",";N tracks SV;", 10,0,10)

h_nvx_mc_2trk = r.TH1F("h_nvx_mc_2trk",";N vertex;", 20,0,20)
h_nvx_rc_2trk = r.TH1F("h_nvx_rc_2trk",";N vertex;", 20,0,20)

h_nvx_mc_3trk = r.TH1F("h_nvx_mc_3trk",";N vertex;", 20,0,20)
h_nvx_rc_3trk = r.TH1F("h_nvx_rc_3trk",";N vertex;", 20,0,20)

h_nvx_mc_4trk = r.TH1F("h_nvx_mc_4trk",";N vertex;", 20,0,20)
h_nvx_rc_4trk = r.TH1F("h_nvx_rc_4trk",";N vertex;", 20,0,20)

h_nvx_mc_5trk = r.TH1F("h_nvx_mc_5trk",";N vertex;", 20,0,20)
h_nvx_rc_5trk = r.TH1F("h_nvx_rc_5trk",";N vertex;", 20,0,20)


h_recoeff_PV = r.TH1F("h_recoeff_PV",";N tracks;", 20,0,20)
h_recoeff_SV = r.TH1F("h_recoeff_SV",";N tracks;", 20,0,20)


for entry in tree:
    
    #MC vertex with at least 2 tracks
    nvx=0
    for v in range(entry.MC_Vertex_ntrk.size()):
        if entry.MC_Vertex_ntrk.at(v)>1: nvx+=1
        if v==0: h_ntrk_mc_pv.Fill(entry.MC_Vertex_ntrk.at(v))
        else:    h_ntrk_mc_sv.Fill(entry.MC_Vertex_ntrk.at(v))
        
    h_mc.Fill(nvx)
    
    
    #Reco vertex with chi2>0 and <10
    nvx=0
    for v in range(entry.Vertex_chi2.size()):
        if entry.Vertex_chi2.at(v)>0 and entry.Vertex_chi2.at(v)<10:nvx+=1
        if v==0: h_ntrk_rc_pv.Fill(entry.Vertex_ntrk.at(v))
        else:    h_ntrk_rc_sv.Fill(entry.Vertex_ntrk.at(v))

    h_recoChi2Cut.Fill(nvx)


###################################################
h_reco.Draw("HIST,E1")
h_mc.Scale(1./h_mc.Integral(0,-1))
h_mc.SetLineColor(2)
h_mc.Draw("HIST,same,E1")

tt.SetTextSize(0.04)
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85,"#color[2]{MC vertex (N_{ch}>1)}")
tt.DrawLatexNDC(0.60,0.79,"#color[4]{Reco vertex}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/nVertex_MCtrkGT1.pdf")
can.SaveAs("plots/png/nVertex_MCtrkGT1.png")
###################################################



###################################################
h_recoChi2Cut.Scale(1./h_recoChi2Cut.Integral(0,-1))
h_recoChi2Cut.SetMaximum(0.35)
h_recoChi2Cut.Draw("HIST,E1")
h_recoChi2Cut.SetLineColor(4)
h_mc.Draw("HIST,same,E1")

tt.SetTextSize(0.04)
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85,"#color[2]{MC vertex (N_{ch}>1)}")
tt.DrawLatexNDC(0.60,0.79,"#color[4]{Reco vertex (10>#chi^{2}>0})")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/nVertex_MCtrkGT1_RecoChi2.pdf")
can.SaveAs("plots/png/nVertex_MCtrkGT1_RecoChi2.png")
###################################################


###################################################
h_ntrk_rc_pv.Draw("HIST,E1")
h_ntrk_rc_pv.Scale(1./h_ntrk_rc_pv.Integral(0,-1))
h_ntrk_rc_pv.SetLineColor(4)
h_ntrk_mc_pv.Draw("HIST,same,E1")
h_ntrk_mc_pv.Scale(1./h_ntrk_mc_pv.Integral(0,-1))
h_ntrk_mc_pv.SetLineColor(2)
tt.SetTextSize(0.04)
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85,"#color[2]{MC N_{tracks} PV}")
tt.DrawLatexNDC(0.60,0.79,"#color[4]{Reco N_{tracks} PV}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/nTracks_PV.pdf")
can.SaveAs("plots/png/nTracks_PV.png")
###################################################


###################################################
h_ntrk_rc_sv.Draw("HIST,E1")
h_ntrk_rc_sv.Scale(1./h_ntrk_rc_sv.Integral(0,-1))
h_ntrk_rc_sv.SetLineColor(4)
h_ntrk_mc_sv.Draw("HIST,same,E1")
h_ntrk_mc_sv.Scale(1./h_ntrk_mc_sv.Integral(0,-1))
h_ntrk_mc_sv.SetLineColor(2)
tt.SetTextSize(0.04)
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85,"#color[2]{MC N_{tracks} SV}")
tt.DrawLatexNDC(0.60,0.79,"#color[4]{Reco N_{tracks} SV}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/nTracks_SV.pdf")
can.SaveAs("plots/png/nTracks_SV.png")
###################################################









#//TString vtx = "Vertex";  // tracks selected based on d0 & z0 significance
#TString vtx = "Vertex_primaryTracks";   // primary tracks selected based on MC-matching

#// plot the normalised chi2 / ndf :
#TH1F* hchi2 = new TH1F("hchi2",";chi2; Events",100,0,10);
#events->Draw(vtx+".chi2>>hchi2",vtx+".chi2<10") ;


#TString cut = vtx+".chi2 <10 ";

#// ---------------------------------------------------------------------------
#//
#// Vertex resolutions 
#// The MC_PrimaryVertex and the reco'ed vertex in the ntuple are both in mm
#//
#//	The resolutions  are of a few microns.
#// ---------------------------------------------------------------------------


#TH1F*  hx = new TH1F("hx",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-40,40);
#events -> Draw( vtx+".position.x * 1e3  - MC_PrimaryVertex.x()*1e3>> hx", cut);    
#hx -> Fit("gaus");

#TH1F*  hy = new TH1F("hy",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-40,40);
#events -> Draw( vtx+".position.y * 1e3 - MC_PrimaryVertex.y()*1e3  >> hy", cut);    
#hy -> Fit("gaus");

#TH1F*  hz = new TH1F("hz",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-40,40);
#events -> Draw( vtx+".position.z * 1e3 - MC_PrimaryVertex.z()*1e3 >> hz", cut);
#hz -> Fit("gaus");



#// ---------------------------------------------------------------
#//
#// Pulls of the reconstructed vertex
#//
#// ---------------------------------------------------------------

#// covMatrix[0] = cov(0,0) = variance of the x position
#// covMatrix[3] = cov(1,1) = variance of the y position
#// covMatrix[5] = cov(2,2) = variance of the z position

#TH1F*  px = new TH1F("px","; Pull x_{vtx}; Events",100,-5,5);
#events -> Draw( " ("+vtx+".position.x - MC_PrimaryVertex.x()) / TMath::Sqrt( "+vtx+".covMatrix[0] ) >> px",cut);
#px->Fit("gaus");

#TH1F*  py = new TH1F("py","; Pull y_{vtx}; Events",100,-5,5);
#events -> Draw( "("+vtx+".position.y - MC_PrimaryVertex.y()) / TMath::Sqrt( "+vtx+".covMatrix[2] ) >> py",cut);
#py->Fit("gaus");

#TH1F*  pz = new TH1F("pz","; Pull z_{vtx}; Events",100,-5,5);
#events -> Draw( "("+vtx+".position.z - MC_PrimaryVertex.z())  / TMath::Sqrt( "+vtx+".covMatrix[5] ) >> pz",cut);
#pz->Fit("gaus");



#// ---------------------------------------------------------------
#//
#// Plots :

#TCanvas* c1 = new TCanvas("c1","c1");
#//gStyle->SetOptStat(0);
#c1 -> Divide(2,2);
#c1 ->cd(1); hchi2 -> Draw();
#c1->cd(2); hx->Draw();
#c1->cd(3); hy -> Draw();
#c1->cd(4); hz->Draw();
#//c1->SaveAs("resolutions.pdf");

#TCanvas* c2 = new TCanvas("c2","c2");
#gStyle->SetOptStat(1111);
#c2->Divide(2,2);
#c2->cd(1); px->Draw();
#c2->cd(2); py->Draw();
#c2->cd(3); pz->Draw();
#//c2->SaveAs("pulls.pdf");

#}

