import ROOT as r
from math import sqrt
r.gROOT.Reset()
r.gROOT.SetBatch(True)
r.gROOT.ForceStyle()
r.gStyle.SetOptStat(0)


f = r.TFile("/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses/flat_ee_Zbb_vertexPerf.root")
f = r.TFile("/eos/experiment/fcc/ee/tmp/flat_ee_Zbb_VertexPerf.root")
tree = f.Get("events")

fout = r.TFile("forDonal.root","RECREATE")

#--------------------------------------------#
#--------------------------------------------#
#     Plots that do not need event loop      #
#--------------------------------------------#
#--------------------------------------------#


#---------------------------------#
#  Plot number of vertex MC/Reco  #
#---------------------------------#


###################################################
#All vertex
h_mc = r.TH1F("h_mc",";N vertex;", 20,0,20)
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












#--------------------------------------------#
#--------------------------------------------#
#       Plots that do need event loop        #
#--------------------------------------------#
#--------------------------------------------#


h_mc   = r.TH1F("h_mc",";N vertex;", 20,0,20)
h_recoChi2Cut = r.TH1F("h_recoChi2Cut",";N vertex;", 20,0,20)

h_ntrk_mc_pv = r.TH1F("h_ntrk_mc_pv",";N tracks PV;", 30,0,30)
h_ntrk_rc_pv = r.TH1F("h_ntrk_rc_pv",";N tracks PV;", 30,0,30)
h_ntrk_mc_sv = r.TH1F("h_ntrk_mc_sv",";N tracks SV;", 10,0,10)
h_ntrk_rc_sv = r.TH1F("h_ntrk_rc_sv",";N tracks SV;", 10,0,10)

h_nSV_mc_2trk = r.TH1F("h_nSV_mc_2trk",";N vertex;", 10,0,10)
h_nSV_rc_2trk = r.TH1F("h_nSV_rc_2trk",";N vertex;", 10,0,10)
h_nSV_mc_3trk = r.TH1F("h_nSV_mc_3trk",";N vertex;", 10,0,10)
h_nSV_rc_3trk = r.TH1F("h_nSV_rc_3trk",";N vertex;", 10,0,10)
h_nSV_mc_4trk = r.TH1F("h_nSV_mc_4trk",";N vertex;", 10,0,10)
h_nSV_rc_4trk = r.TH1F("h_nSV_rc_4trk",";N vertex;", 10,0,10)
h_nSV_mc_5trk = r.TH1F("h_nSV_mc_5trk",";N vertex;", 10,0,10)
h_nSV_rc_5trk = r.TH1F("h_nSV_rc_5trk",";N vertex;", 10,0,10)
h_nSV_mc_6trk = r.TH1F("h_nSV_mc_6trk",";N vertex;", 10,0,10)
h_nSV_rc_6trk = r.TH1F("h_nSV_rc_6trk",";N vertex;", 10,0,10)

h_recoeff_SV_2trk = r.TH1F("h_recoeff_SV_2trk",";N tracks MC;", 10,0,10)
h_recoeff_SV_3trk = r.TH1F("h_recoeff_SV_3trk",";N tracks MC;", 10,0,10)
h_recoeff_SV_4trk = r.TH1F("h_recoeff_SV_4trk",";N tracks MC;", 10,0,10)
h_recoeff_SV_5trk = r.TH1F("h_recoeff_SV_5trk",";N tracks MC;", 10,0,10)
h_recoeff_SV_6trk = r.TH1F("h_recoeff_SV_6trk",";N tracks MC;", 10,0,10)


h_PV2MC   = r.TH1F("h_PV2MC",";Distance to MC primary vertex #mum;", 200,0,200)
h_PV2MC_x = r.TH1F("h_PV2MC_x",";Distance to MC primary vertex x #mum;", 200,-100, 100)
h_PV2MC_y = r.TH1F("h_PV2MC_y",";Distance to MC primary vertex y #mum;", 200,-100, 100)
h_PV2MC_z = r.TH1F("h_PV2MC_z",";Distance to MC primary vertex z #mum;", 200,-100, 100)

h_PV2MC_x_pull = r.TH1F("h_PV2MC_x_pull",";Primary Vertex pull x;", 200,-10, 10)
h_PV2MC_y_pull = r.TH1F("h_PV2MC_y_pull",";Primary Vertex pull y;", 200,-10, 10)
h_PV2MC_z_pull = r.TH1F("h_PV2MC_z_pull",";Primary Vertex pull z;", 200,-10, 10)

h_SV2MC_x_pull_2trk = r.TH1F("h_PV2MC_x_pull_2trk",";Secondary Vertex pull x (N tracks = 2);", 200,-10, 10)
h_SV2MC_y_pull_2trk = r.TH1F("h_PV2MC_y_pull_2trk",";Secondary Vertex pull y (N tracks = 2);", 200,-10, 10)
h_SV2MC_z_pull_2trk = r.TH1F("h_PV2MC_z_pull_2trk",";Secondary Vertex pull z (N tracks = 2);", 200,-10, 10)

h_SV2MC_x_pull_3trk = r.TH1F("h_PV2MC_x_pull_3trk",";Secondary Vertex pull x (N tracks = 3);", 200,-10, 10)
h_SV2MC_y_pull_3trk = r.TH1F("h_PV2MC_y_pull_3trk",";Secondary Vertex pull y (N tracks = 3);", 200,-10, 10)
h_SV2MC_z_pull_3trk = r.TH1F("h_PV2MC_z_pull_3trk",";Secondary Vertex pull z (N tracks = 3);", 200,-10, 10)

h_SV2MC_x_pull_4trk = r.TH1F("h_PV2MC_x_pull_4trk",";Secondary Vertex pull x (N tracks = 4);", 200,-10, 10)
h_SV2MC_y_pull_4trk = r.TH1F("h_PV2MC_y_pull_4trk",";Secondary Vertex pull y (N tracks = 4);", 200,-10, 10)
h_SV2MC_z_pull_4trk = r.TH1F("h_PV2MC_z_pull_4trk",";Secondary Vertex pull z (N tracks = 4);", 200,-10, 10)

h_SV2MC_x_pull_5trk = r.TH1F("h_PV2MC_x_pull_5trk",";Secondary Vertex pull x (N tracks = 5);", 200,-10, 10)
h_SV2MC_y_pull_5trk = r.TH1F("h_PV2MC_y_pull_5trk",";Secondary Vertex pull y (N tracks = 5);", 200,-10, 10)
h_SV2MC_z_pull_5trk = r.TH1F("h_PV2MC_z_pull_5trk",";Secondary Vertex pull z (N tracks = 5);", 200,-10, 10)

h_SV2MC_x_pull_6trk = r.TH1F("h_PV2MC_x_pull_6trk",";Secondary Vertex pull x (N tracks = 6);", 200,-10, 10)
h_SV2MC_y_pull_6trk = r.TH1F("h_PV2MC_y_pull_6trk",";Secondary Vertex pull y (N tracks = 6);", 200,-10, 10)
h_SV2MC_z_pull_6trk = r.TH1F("h_PV2MC_z_pull_6trk",";Secondary Vertex pull z (N tracks = 6);", 200,-10, 10)

h_SV2MC_2trk  = r.TH1F("h_SV2MC_2trk",";Distance to MC secondary vertex #mum;", 200,0,200)
h_SV2MC_3trk  = r.TH1F("h_SV2MC_3trk",";Distance to MC secondary vertex #mum;", 200,0,200)
h_SV2MC_4trk  = r.TH1F("h_SV2MC_4trk",";Distance to MC secondary vertex #mum;", 200,0,200)
h_SV2MC_5trk  = r.TH1F("h_SV2MC_5trk",";Distance to MC secondary vertex #mum;", 200,0,200)
h_SV2MC_6trk  = r.TH1F("h_SV2MC_6trk",";Distance to MC secondary vertex #mum;", 200,0,200)

h_SV2MC_x_2trk  = r.TH1F("h_SV2MC_x_2trk",";Distance to MC secondary vertex x #mum;", 200,-100,100)
h_SV2MC_x_3trk  = r.TH1F("h_SV2MC_x_3trk",";Distance to MC secondary vertex x #mum;", 200,-100,100)
h_SV2MC_x_4trk  = r.TH1F("h_SV2MC_x_4trk",";Distance to MC secondary vertex x #mum;", 200,-100,100)
h_SV2MC_x_5trk  = r.TH1F("h_SV2MC_x_5trk",";Distance to MC secondary vertex x #mum;", 200,-100,100)
h_SV2MC_x_6trk  = r.TH1F("h_SV2MC_x_6trk",";Distance to MC secondary vertex x #mum;", 200,-100,100)

h_SV2MC_y_2trk  = r.TH1F("h_SV2MC_y_2trk",";Distance to MC secondary vertex y #mum;", 200,-100,100)
h_SV2MC_y_3trk  = r.TH1F("h_SV2MC_y_3trk",";Distance to MC secondary vertex y #mum;", 200,-100,100)
h_SV2MC_y_4trk  = r.TH1F("h_SV2MC_y_4trk",";Distance to MC secondary vertex y #mum;", 200,-100,100)
h_SV2MC_y_5trk  = r.TH1F("h_SV2MC_y_5trk",";Distance to MC secondary vertex y #mum;", 200,-100,100)
h_SV2MC_y_6trk  = r.TH1F("h_SV2MC_y_6trk",";Distance to MC secondary vertex y #mum;", 200,-100,100)

h_SV2MC_z_2trk  = r.TH1F("h_SV2MC_z_2trk",";Distance to MC secondary vertex z #mum;", 200,-100,100)
h_SV2MC_z_3trk  = r.TH1F("h_SV2MC_z_3trk",";Distance to MC secondary vertex z #mum;", 200,-100,100)
h_SV2MC_z_4trk  = r.TH1F("h_SV2MC_z_4trk",";Distance to MC secondary vertex z #mum;", 200,-100,100)
h_SV2MC_z_5trk  = r.TH1F("h_SV2MC_z_5trk",";Distance to MC secondary vertex z #mum;", 200,-100,100)
h_SV2MC_z_6trk  = r.TH1F("h_SV2MC_z_6trk",";Distance to MC secondary vertex z #mum;", 200,-100,100)


h_FD2PV_2trk = r.TH1F("h_FD2PV_2trk",";Flight distance from PV 2 tracks mm;", 200,0,10)
h_FD2PV_3trk = r.TH1F("h_FD2PV_3trk",";Flight distance from PV 3 tracks mm;", 200,0,10)
h_FD2PV_4trk = r.TH1F("h_FD2PV_4trk",";Flight distance from PV 4 tracks mm;", 200,0,10)
h_FD2PV_5trk = r.TH1F("h_FD2PV_5trk",";Flight distance from PV 5 tracks mm;", 200,0,10)
h_FD2PV_6trk = r.TH1F("h_FD2PV_6trk",";Flight distance from PV 6 tracks mm;", 200,0,10)

h_FD2PV_x_2trk = r.TH1F("h_FD2PV_x_2trk",";Flight distance x from PV 2 tracks mm;", 200,-10,10)
h_FD2PV_x_3trk = r.TH1F("h_FD2PV_x_3trk",";Flight distance x from PV 3 tracks mm;", 200,-10,10)
h_FD2PV_x_4trk = r.TH1F("h_FD2PV_x_4trk",";Flight distance x from PV 4 tracks mm;", 200,-10,10)
h_FD2PV_x_5trk = r.TH1F("h_FD2PV_x_5trk",";Flight distance x from PV 5 tracks mm;", 200,-10,10)
h_FD2PV_x_6trk = r.TH1F("h_FD2PV_x_6trk",";Flight distance x from PV 6 tracks mm;", 200,-10,10)

h_FD2PV_y_2trk = r.TH1F("h_FD2PV_y_2trk",";Flight distance y from PV 2 tracks mm;", 200,-10,10)
h_FD2PV_y_3trk = r.TH1F("h_FD2PV_y_3trk",";Flight distance y from PV 3 tracks mm;", 200,-10,10)
h_FD2PV_y_4trk = r.TH1F("h_FD2PV_y_4trk",";Flight distance y from PV 4 tracks mm;", 200,-10,10)
h_FD2PV_y_5trk = r.TH1F("h_FD2PV_y_5trk",";Flight distance y from PV 5 tracks mm;", 200,-10,10)
h_FD2PV_y_6trk = r.TH1F("h_FD2PV_y_6trk",";Flight distance y from PV 6 tracks mm;", 200,-10,10)

h_FD2PV_z_2trk = r.TH1F("h_FD2PV_z_2trk",";Flight distance z from PV 2 tracks mm;", 200,-10,10)
h_FD2PV_z_3trk = r.TH1F("h_FD2PV_z_3trk",";Flight distance z from PV 3 tracks mm;", 200,-10,10)
h_FD2PV_z_4trk = r.TH1F("h_FD2PV_z_4trk",";Flight distance z from PV 4 tracks mm;", 200,-10,10)
h_FD2PV_z_5trk = r.TH1F("h_FD2PV_z_5trk",";Flight distance z from PV 5 tracks mm;", 200,-10,10)
h_FD2PV_z_6trk = r.TH1F("h_FD2PV_z_6trk",";Flight distance z from PV 6 tracks mm;", 200,-10,10)

h_FD2PV_2trk_sig = r.TH1F("h_FD2PV_2trk_sig",";Flight distance significance from PV 2 tracks;", 200,0,50)
h_FD2PV_3trk_sig = r.TH1F("h_FD2PV_3trk_sig",";Flight distance significance from PV 3 tracks;", 200,0,50)
h_FD2PV_4trk_sig = r.TH1F("h_FD2PV_4trk_sig",";Flight distance significance from PV 4 tracks;", 200,0,50)
h_FD2PV_5trk_sig = r.TH1F("h_FD2PV_5trk_sig",";Flight distance significance from PV 5 tracks;", 200,0,50)
h_FD2PV_6trk_sig = r.TH1F("h_FD2PV_6trk_sig",";Flight distance significance from PV 6 tracks;", 200,0,50)

h_FD2PV_x_2trk_sig = r.TH1F("h_FD2PV_x_2trk_sig",";Flight distance significance x from PV 2 tracks;", 200,-50,50)
h_FD2PV_x_3trk_sig = r.TH1F("h_FD2PV_x_3trk_sig",";Flight distance significance x from PV 3 tracks;", 200,-50,50)
h_FD2PV_x_4trk_sig = r.TH1F("h_FD2PV_x_4trk_sig",";Flight distance significance x from PV 4 tracks;", 200,-50,50)
h_FD2PV_x_5trk_sig = r.TH1F("h_FD2PV_x_5trk_sig",";Flight distance significance x from PV 5 tracks;", 200,-50,50)
h_FD2PV_x_6trk_sig = r.TH1F("h_FD2PV_x_6trk_sig",";Flight distance significance x from PV 6 tracks;", 200,-50,50)

h_FD2PV_y_2trk_sig = r.TH1F("h_FD2PV_y_2trk_sig",";Flight distance significance y from PV 2 tracks;", 200,-50,50)
h_FD2PV_y_3trk_sig = r.TH1F("h_FD2PV_y_3trk_sig",";Flight distance significance y from PV 3 tracks;", 200,-50,50)
h_FD2PV_y_4trk_sig = r.TH1F("h_FD2PV_y_4trk_sig",";Flight distance significance y from PV 4 tracks;", 200,-50,50)
h_FD2PV_y_5trk_sig = r.TH1F("h_FD2PV_y_5trk_sig",";Flight distance significance y from PV 5 tracks;", 200,-50,50)
h_FD2PV_y_6trk_sig = r.TH1F("h_FD2PV_y_6trk_sig",";Flight distance significance y from PV 6 tracks;", 200,-50,50)

h_FD2PV_z_2trk_sig = r.TH1F("h_FD2PV_z_2trk_sig",";Flight distance significance z from PV 2 tracks;", 200,-50,50)
h_FD2PV_z_3trk_sig = r.TH1F("h_FD2PV_z_3trk_sig",";Flight distance significance z from PV 3 tracks;", 200,-50,50)
h_FD2PV_z_4trk_sig = r.TH1F("h_FD2PV_z_4trk_sig",";Flight distance significance z from PV 4 tracks;", 200,-50,50)
h_FD2PV_z_5trk_sig = r.TH1F("h_FD2PV_z_5trk_sig",";Flight distance significance z from PV 5 tracks;", 200,-50,50)
h_FD2PV_z_6trk_sig = r.TH1F("h_FD2PV_z_6trk_sig",";Flight distance significance z from PV 6 tracks;", 200,-50,50)


h_dmin_DV2DV = r.TH1F("h_dmin_DV2DV",";Minimum distance between DV #mum;", 200,0,5000)
h_dmin_PV2DV = r.TH1F("h_dmin_PV2DV",";Minimum distance between PV and DV #mum;", 200,0,10000)

nentries=tree.GetEntries()
centry=0
for entry in tree:
    if centry%1000==1:print('entry : ',centry,'/',nentries)
    centry+=1
    if centry>200000.:break
    #MC vertex with at least 2 tracks
    nvx=0
    nsv2,nsv3,nsv4,nsv5,nsv6=0,0,0,0,0
    for v in range(entry.MC_Vertex_ntrk.size()):
        if entry.MC_Vertex_ntrk.at(v)>1: nvx+=1

        if v==0: h_ntrk_mc_pv.Fill(entry.MC_Vertex_ntrk.at(v))
        else:    h_ntrk_mc_sv.Fill(entry.MC_Vertex_ntrk.at(v))

        if   v!=0 and entry.MC_Vertex_ntrk.at(v)==2: nsv2+=1
        elif v!=0 and entry.MC_Vertex_ntrk.at(v)==3: nsv3+=1
        elif v!=0 and entry.MC_Vertex_ntrk.at(v)==4: nsv4+=1
        elif v!=0 and entry.MC_Vertex_ntrk.at(v)==5: nsv5+=1
        elif v!=0 and entry.MC_Vertex_ntrk.at(v)==6: nsv6+=1

    h_mc.Fill(nvx)

    h_nSV_mc_2trk.Fill(nsv2)
    h_nSV_mc_3trk.Fill(nsv3)
    h_nSV_mc_4trk.Fill(nsv4)
    h_nSV_mc_5trk.Fill(nsv5)
    h_nSV_mc_6trk.Fill(nsv6)
    
    PV_x,PV_y,PV_z=0,0,0
    minPV2DV=999999999999.
    for v in range(entry.Vertex_chi2.size()):
        if entry.Vertex_chi2.at(v)>0 and entry.Vertex_chi2.at(v)<10:
            if entry.Vertex_isPV.at(v)>0:
                PV_x,PV_y,PV_z=entry.Vertex_x.at(v),entry.Vertex_y.at(v),entry.Vertex_z.at(v)
                break
    for v in range(entry.Vertex_chi2.size()):
        if entry.Vertex_chi2.at(v)>0 and entry.Vertex_chi2.at(v)<10 and entry.Vertex_isPV.at(v)==0:
            distancetmp=sqrt((PV_x-entry.Vertex_x.at(v))*(PV_x-entry.Vertex_x.at(v))+
                             (PV_y-entry.Vertex_y.at(v))*(PV_y-entry.Vertex_y.at(v))+
                             (PV_z-entry.Vertex_z.at(v))*(PV_z-entry.Vertex_z.at(v)))
            if distancetmp<minPV2DV: minPV2DV=distancetmp
    if minPV2DV!=999999999999.: h_dmin_PV2DV.Fill(minPV2DV*1000.)
 

    minDV2DV=999999999999.
    for v in range(entry.Vertex_chi2.size()):
        if entry.Vertex_chi2.at(v)>0 and entry.Vertex_chi2.at(v)<10 and entry.Vertex_isPV.at(v)==0:
            DV1_x,DV1_y,DV1_z=entry.Vertex_x.at(v),entry.Vertex_y.at(v),entry.Vertex_z.at(v)
            for w in range(entry.Vertex_chi2.size()):
                if w==v:continue
                if entry.Vertex_chi2.at(w)>0 and entry.Vertex_chi2.at(w)<10 and entry.Vertex_isPV.at(w)==0:
                    DV2_x,DV2_y,DV2_z=entry.Vertex_x.at(w),entry.Vertex_y.at(w),entry.Vertex_z.at(w)
                    distancetmp=sqrt((DV1_x-DV2_x)*(DV1_x-DV2_x)+
                                     (DV1_y-DV2_y)*(DV1_y-DV2_y)+
                                     (DV1_z-DV2_z)*(DV1_z-DV2_z))
                    if distancetmp<minDV2DV: minDV2DV=distancetmp
    if minDV2DV!=999999999999.: h_dmin_DV2DV.Fill(minDV2DV*1000.)
 

   
    #Reco vertex with chi2>0 and <10
    nvx=0
    nsv2,nsv3,nsv4,nsv5,nsv6=0,0,0,0,0
    for v in range(entry.Vertex_chi2.size()):
        if entry.Vertex_chi2.at(v)>0 and entry.Vertex_chi2.at(v)<10:
            nvx+=1
            if entry.Vertex_isPV.at(v)>0:
                h_PV2MC.Fill(entry.Vertex_d2MC.at(v)*1000.)
                h_PV2MC_x.Fill(entry.Vertex_d2MCx.at(v)*1000.)
                h_PV2MC_y.Fill(entry.Vertex_d2MCy.at(v)*1000.)
                h_PV2MC_z.Fill(entry.Vertex_d2MCz.at(v)*1000.)
                h_PV2MC_x_pull.Fill(entry.Vertex_d2MCx.at(v)/entry.Vertex_xErr.at(v))
                h_PV2MC_y_pull.Fill(entry.Vertex_d2MCy.at(v)/entry.Vertex_yErr.at(v))
                h_PV2MC_z_pull.Fill(entry.Vertex_d2MCz.at(v)/entry.Vertex_zErr.at(v))
            else:
                mcind=entry.Vertex_mcind.at(v)
                if entry.Vertex_ntrk.at(v)==2:
                    h_SV2MC_2trk.Fill(entry.Vertex_d2MC.at(v)*1000.)
                    h_SV2MC_x_2trk.Fill(entry.Vertex_d2MCx.at(v)*1000.)
                    h_SV2MC_y_2trk.Fill(entry.Vertex_d2MCy.at(v)*1000.)
                    h_SV2MC_z_2trk.Fill(entry.Vertex_d2MCz.at(v)*1000.)
                    h_recoeff_SV_2trk.Fill(entry.MC_Vertex_ntrk.at(entry.Vertex_mcind.at(v)))
                    h_SV2MC_x_pull_2trk.Fill(entry.Vertex_d2MCx.at(v)/entry.Vertex_xErr.at(v))
                    h_SV2MC_y_pull_2trk.Fill(entry.Vertex_d2MCy.at(v)/entry.Vertex_yErr.at(v))
                    h_SV2MC_z_pull_2trk.Fill(entry.Vertex_d2MCz.at(v)/entry.Vertex_zErr.at(v))
                    h_FD2PV_2trk.Fill(entry.Vertex_d2PV.at(v))
                    h_FD2PV_x_2trk.Fill(entry.Vertex_d2PVx.at(v))
                    h_FD2PV_y_2trk.Fill(entry.Vertex_d2PVy.at(v))
                    h_FD2PV_z_2trk.Fill(entry.Vertex_d2PVz.at(v))
                    h_FD2PV_2trk_sig.Fill(entry.Vertex_d2PVSig.at(v))
                    h_FD2PV_x_2trk_sig.Fill(entry.Vertex_d2PVxSig.at(v))
                    h_FD2PV_y_2trk_sig.Fill(entry.Vertex_d2PVySig.at(v))
                    h_FD2PV_z_2trk_sig.Fill(entry.Vertex_d2PVzSig.at(v))
                elif entry.Vertex_ntrk.at(v)==3:
                    h_SV2MC_3trk.Fill(entry.Vertex_d2MC.at(v)*1000.)
                    h_SV2MC_x_3trk.Fill(entry.Vertex_d2MCx.at(v)*1000.)
                    h_SV2MC_y_3trk.Fill(entry.Vertex_d2MCy.at(v)*1000.)
                    h_SV2MC_z_3trk.Fill(entry.Vertex_d2MCz.at(v)*1000.)
                    h_recoeff_SV_3trk.Fill(entry.MC_Vertex_ntrk.at(entry.Vertex_mcind.at(v)))
                    h_SV2MC_x_pull_3trk.Fill(entry.Vertex_d2MCx.at(v)/entry.Vertex_xErr.at(v))
                    h_SV2MC_y_pull_3trk.Fill(entry.Vertex_d2MCy.at(v)/entry.Vertex_yErr.at(v))
                    h_SV2MC_z_pull_3trk.Fill(entry.Vertex_d2MCz.at(v)/entry.Vertex_zErr.at(v))
                    h_FD2PV_3trk.Fill(entry.Vertex_d2PV.at(v))
                    h_FD2PV_x_3trk.Fill(entry.Vertex_d2PVx.at(v))
                    h_FD2PV_y_3trk.Fill(entry.Vertex_d2PVy.at(v))
                    h_FD2PV_z_3trk.Fill(entry.Vertex_d2PVz.at(v))
                    h_FD2PV_3trk_sig.Fill(entry.Vertex_d2PVSig.at(v))
                    h_FD2PV_x_3trk_sig.Fill(entry.Vertex_d2PVxSig.at(v))
                    h_FD2PV_y_3trk_sig.Fill(entry.Vertex_d2PVySig.at(v))
                    h_FD2PV_z_3trk_sig.Fill(entry.Vertex_d2PVzSig.at(v))
                elif entry.Vertex_ntrk.at(v)==4:
                    h_SV2MC_4trk.Fill(entry.Vertex_d2MC.at(v)*1000.)
                    h_SV2MC_x_4trk.Fill(entry.Vertex_d2MCx.at(v)*1000.)
                    h_SV2MC_y_4trk.Fill(entry.Vertex_d2MCy.at(v)*1000.)
                    h_SV2MC_z_4trk.Fill(entry.Vertex_d2MCz.at(v)*1000.)
                    h_recoeff_SV_4trk.Fill(entry.MC_Vertex_ntrk.at(entry.Vertex_mcind.at(v)))
                    h_SV2MC_x_pull_4trk.Fill(entry.Vertex_d2MCx.at(v)/entry.Vertex_xErr.at(v))
                    h_SV2MC_y_pull_4trk.Fill(entry.Vertex_d2MCy.at(v)/entry.Vertex_yErr.at(v))
                    h_SV2MC_z_pull_4trk.Fill(entry.Vertex_d2MCz.at(v)/entry.Vertex_zErr.at(v))
                    h_FD2PV_4trk.Fill(entry.Vertex_d2PV.at(v))
                    h_FD2PV_x_4trk.Fill(entry.Vertex_d2PVx.at(v))
                    h_FD2PV_y_4trk.Fill(entry.Vertex_d2PVy.at(v))
                    h_FD2PV_z_4trk.Fill(entry.Vertex_d2PVz.at(v))
                    h_FD2PV_4trk_sig.Fill(entry.Vertex_d2PVSig.at(v))
                    h_FD2PV_x_4trk_sig.Fill(entry.Vertex_d2PVxSig.at(v))
                    h_FD2PV_y_4trk_sig.Fill(entry.Vertex_d2PVySig.at(v))
                    h_FD2PV_z_4trk_sig.Fill(entry.Vertex_d2PVzSig.at(v))
                elif entry.Vertex_ntrk.at(v)==5:
                    h_SV2MC_5trk.Fill(entry.Vertex_d2MC.at(v)*1000.)
                    h_SV2MC_x_5trk.Fill(entry.Vertex_d2MCx.at(v)*1000.)
                    h_SV2MC_y_5trk.Fill(entry.Vertex_d2MCy.at(v)*1000.)
                    h_SV2MC_z_5trk.Fill(entry.Vertex_d2MCz.at(v)*1000.)
                    h_recoeff_SV_5trk.Fill(entry.MC_Vertex_ntrk.at(entry.Vertex_mcind.at(v)))
                    h_SV2MC_x_pull_5trk.Fill(entry.Vertex_d2MCx.at(v)/entry.Vertex_xErr.at(v))
                    h_SV2MC_y_pull_5trk.Fill(entry.Vertex_d2MCy.at(v)/entry.Vertex_yErr.at(v))
                    h_SV2MC_z_pull_5trk.Fill(entry.Vertex_d2MCz.at(v)/entry.Vertex_zErr.at(v))
                    h_FD2PV_5trk.Fill(entry.Vertex_d2PV.at(v))
                    h_FD2PV_x_5trk.Fill(entry.Vertex_d2PVx.at(v))
                    h_FD2PV_y_5trk.Fill(entry.Vertex_d2PVy.at(v))
                    h_FD2PV_z_5trk.Fill(entry.Vertex_d2PVz.at(v))
                    h_FD2PV_5trk_sig.Fill(entry.Vertex_d2PVSig.at(v))
                    h_FD2PV_x_5trk_sig.Fill(entry.Vertex_d2PVxSig.at(v))
                    h_FD2PV_y_5trk_sig.Fill(entry.Vertex_d2PVySig.at(v))
                    h_FD2PV_z_5trk_sig.Fill(entry.Vertex_d2PVzSig.at(v))

                elif entry.Vertex_ntrk.at(v)==6:
                    h_SV2MC_6trk.Fill(entry.Vertex_d2MC.at(v)*1000.)
                    h_SV2MC_x_6trk.Fill(entry.Vertex_d2MCx.at(v)*1000.)
                    h_SV2MC_y_6trk.Fill(entry.Vertex_d2MCy.at(v)*1000.)
                    h_SV2MC_z_6trk.Fill(entry.Vertex_d2MCz.at(v)*1000.)
                    h_recoeff_SV_6trk.Fill(entry.MC_Vertex_ntrk.at(entry.Vertex_mcind.at(v)))
                    h_SV2MC_x_pull_6trk.Fill(entry.Vertex_d2MCx.at(v)/entry.Vertex_xErr.at(v))
                    h_SV2MC_y_pull_6trk.Fill(entry.Vertex_d2MCy.at(v)/entry.Vertex_yErr.at(v))
                    h_SV2MC_z_pull_6trk.Fill(entry.Vertex_d2MCz.at(v)/entry.Vertex_zErr.at(v))
                    h_FD2PV_6trk.Fill(entry.Vertex_d2PV.at(v))
                    h_FD2PV_x_6trk.Fill(entry.Vertex_d2PVx.at(v))
                    h_FD2PV_y_6trk.Fill(entry.Vertex_d2PVy.at(v))
                    h_FD2PV_z_6trk.Fill(entry.Vertex_d2PVz.at(v))
                    h_FD2PV_6trk_sig.Fill(entry.Vertex_d2PVSig.at(v))
                    h_FD2PV_x_6trk_sig.Fill(entry.Vertex_d2PVxSig.at(v))
                    h_FD2PV_y_6trk_sig.Fill(entry.Vertex_d2PVySig.at(v))
                    h_FD2PV_z_6trk_sig.Fill(entry.Vertex_d2PVzSig.at(v))

        if entry.Vertex_isPV.at(v)>0: h_ntrk_rc_pv.Fill(entry.Vertex_ntrk.at(v))
        else:                         h_ntrk_rc_sv.Fill(entry.Vertex_ntrk.at(v))

        if entry.Vertex_chi2.at(v)>0 and entry.Vertex_chi2.at(v)<10:
            if   entry.Vertex_isPV.at(v)==0 and entry.Vertex_ntrk.at(v)==2: nsv2+=1
            elif entry.Vertex_isPV.at(v)==0 and entry.Vertex_ntrk.at(v)==3: nsv3+=1
            elif entry.Vertex_isPV.at(v)==0 and entry.Vertex_ntrk.at(v)==4: nsv4+=1
            elif entry.Vertex_isPV.at(v)==0 and entry.Vertex_ntrk.at(v)==5: nsv5+=1
            elif entry.Vertex_isPV.at(v)==0 and entry.Vertex_ntrk.at(v)==6: nsv6+=1

    h_recoChi2Cut.Fill(nvx)

    h_nSV_rc_2trk.Fill(nsv2)
    h_nSV_rc_3trk.Fill(nsv3)
    h_nSV_rc_4trk.Fill(nsv4)
    h_nSV_rc_5trk.Fill(nsv5)
    h_nSV_rc_6trk.Fill(nsv6)




###################################################
h_reco.SetMinimum(0.)
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
fout.cd()
h_reco.Write()
h_mc.Write()

###################################################

###################################################
h_recoChi2Cut.Scale(1./h_recoChi2Cut.Integral(0,-1))
h_recoChi2Cut.SetMaximum(0.35)
h_recoChi2Cut.SetMinimum(0.)
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

###################################################
h_nSV_mc_2trk.SetLineColor(2)
h_nSV_rc_2trk.SetLineColor(4)
h_nSV_mc_2trk.Scale(1./h_nSV_mc_2trk.Integral(0,-1))
h_nSV_rc_2trk.Scale(1./h_nSV_rc_2trk.Integral(0,-1))
h_nSV_rc_2trk.Draw("HIST,E1")
h_nSV_mc_2trk.Draw("HIST,same,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks=2")
tt.DrawLatexNDC(0.60,0.85  ,"#color[2]{MC}")
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{Reco}")
can.SaveAs("plots/pdf/nSV2Tracks.pdf")
can.SaveAs("plots/png/nSV2Tracks.png")
###################################################

###################################################
h_nSV_mc_3trk.SetLineColor(2)
h_nSV_rc_3trk.SetLineColor(4)
h_nSV_mc_3trk.Scale(1./h_nSV_mc_3trk.Integral(0,-1))
h_nSV_rc_3trk.Scale(1./h_nSV_rc_3trk.Integral(0,-1))
h_nSV_rc_3trk.Draw("HIST,E1")
h_nSV_mc_3trk.Draw("HIST,same,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks=3")
tt.DrawLatexNDC(0.60,0.85  ,"#color[2]{MC}")
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{Reco}")
can.SaveAs("plots/pdf/nSV3Tracks.pdf")
can.SaveAs("plots/png/nSV3Tracks.png")
###################################################

###################################################
h_nSV_mc_4trk.SetLineColor(2)
h_nSV_rc_4trk.SetLineColor(4)
h_nSV_mc_4trk.Scale(1./h_nSV_mc_4trk.Integral(0,-1))
h_nSV_rc_4trk.Scale(1./h_nSV_rc_4trk.Integral(0,-1))
h_nSV_rc_4trk.Draw("HIST,E1")
h_nSV_mc_4trk.Draw("HIST,same,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks=4")
tt.DrawLatexNDC(0.60,0.85  ,"#color[2]{MC}")
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{Reco}")
can.SaveAs("plots/pdf/nSV4Tracks.pdf")
can.SaveAs("plots/png/nSV4Tracks.png")
###################################################

###################################################
h_nSV_mc_5trk.SetLineColor(2)
h_nSV_rc_5trk.SetLineColor(4)
h_nSV_mc_5trk.Scale(1./h_nSV_mc_5trk.Integral(0,-1))
h_nSV_rc_5trk.Scale(1./h_nSV_rc_5trk.Integral(0,-1))
h_nSV_rc_5trk.Draw("HIST,E1")
h_nSV_mc_5trk.Draw("HIST,same,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks=5")
tt.DrawLatexNDC(0.60,0.85  ,"#color[2]{MC}")
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{Reco}")
can.SaveAs("plots/pdf/nSV5Tracks.pdf")
can.SaveAs("plots/png/nSV5Tracks.png")
###################################################

###################################################
h_nSV_mc_6trk.SetLineColor(2)
h_nSV_rc_6trk.SetLineColor(4)
h_nSV_mc_6trk.Scale(1./h_nSV_mc_6trk.Integral(0,-1))
h_nSV_rc_6trk.Scale(1./h_nSV_rc_6trk.Integral(0,-1))
h_nSV_rc_6trk.Draw("HIST,E1")
h_nSV_mc_6trk.Draw("HIST,same,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks=6")
tt.DrawLatexNDC(0.60,0.85  ,"#color[2]{MC}")
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{Reco}")
can.SaveAs("plots/pdf/nSV6Tracks.pdf")
can.SaveAs("plots/png/nSV6Tracks.png")
###################################################

###################################################
h_nSV_rc_2trk.SetLineColor(1)
h_nSV_rc_2trk.Scale(1./h_nSV_rc_2trk.Integral(0,-1))
h_nSV_rc_2trk.SetMaximum(1.)
h_nSV_rc_2trk.SetMinimum(0.0)
h_nSV_rc_2trk.Draw("HIST,E1")

h_nSV_rc_3trk.SetLineColor(2)
h_nSV_rc_3trk.Scale(1./h_nSV_rc_3trk.Integral(0,-1))
h_nSV_rc_3trk.SetMaximum(1.)
h_nSV_rc_3trk.SetMinimum(0.0)
h_nSV_rc_3trk.Draw("HIST,same,E1")

h_nSV_rc_4trk.SetLineColor(3)
h_nSV_rc_4trk.Scale(1./h_nSV_rc_4trk.Integral(0,-1))
h_nSV_rc_4trk.SetMinimum(0.0)
h_nSV_rc_4trk.SetMaximum(1.)
h_nSV_rc_4trk.Draw("HIST,same,E1")

h_nSV_rc_5trk.SetLineColor(4)
h_nSV_rc_5trk.Scale(1./h_nSV_rc_5trk.Integral(0,-1))
h_nSV_rc_5trk.SetMinimum(0.0)
h_nSV_rc_5trk.SetMaximum(1.)
h_nSV_rc_5trk.Draw("HIST,same,E1")

h_nSV_rc_6trk.SetLineColor(6)
h_nSV_rc_6trk.Scale(1./h_nSV_rc_6trk.Integral(0,-1))
h_nSV_rc_6trk.SetMinimum(0.0)
h_nSV_rc_6trk.SetMaximum(1.)
h_nSV_rc_6trk.Draw("HIST,same,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[1]{2 tracks}")
tt.DrawLatexNDC(0.60,0.79  ,"#color[2]{3 tracks}")
tt.DrawLatexNDC(0.60,0.73  ,"#color[3]{4 tracks}")
tt.DrawLatexNDC(0.60,0.67  ,"#color[4]{5 tracks}")
tt.DrawLatexNDC(0.60,0.61  ,"#color[6]{6 tracks}")

#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/nSVTracks.pdf")
can.SaveAs("plots/png/nSVTracks.png")
###################################################

###################################################
h_PV2MC.SetLineColor(4)
h_PV2MC.Scale(1./h_PV2MC.Integral(0,-1))
h_PV2MC.SetMaximum(0.055)
h_PV2MC.SetMinimum(0.0)
h_PV2MC.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MC_bis.pdf")
can.SaveAs("plots/png/dPV2MC_bis.png")
###################################################

###################################################
h_PV2MC_x.SetLineColor(4)
h_PV2MC_x.Scale(1./h_PV2MC_x.Integral(0,-1))
h_PV2MC_x.SetMaximum(0.055)
h_PV2MC_x.SetMinimum(0.0)
h_PV2MC_x.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC_x.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC_x.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MCx.pdf")
can.SaveAs("plots/png/dPV2MCx.png")
###################################################

###################################################
h_PV2MC_y.SetLineColor(4)
h_PV2MC_y.Scale(1./h_PV2MC_y.Integral(0,-1))
h_PV2MC_y.SetMaximum(0.055)
h_PV2MC_y.SetMinimum(0.0)
h_PV2MC_y.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC_y.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC_y.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MCy.pdf")
can.SaveAs("plots/png/dPV2MCy.png")
###################################################

###################################################
h_PV2MC_z.SetLineColor(4)
h_PV2MC_z.Scale(1./h_PV2MC_z.Integral(0,-1))
h_PV2MC_z.SetMaximum(0.055)
h_PV2MC_z.SetMinimum(0.0)
h_PV2MC_z.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC_z.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC_z.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MCz.pdf")
can.SaveAs("plots/png/dPV2MCz.png")
###################################################

###################################################
h_SV2MC_2trk.SetLineColor(4)
h_SV2MC_2trk.Scale(1./h_SV2MC_2trk.Integral(0,-1))
h_SV2MC_2trk.SetMinimum(0.0)
h_SV2MC_2trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_2trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 2}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_2trks.pdf")
can.SaveAs("plots/png/dSV2MC_2trks.png")
###################################################

###################################################
h_SV2MC_3trk.SetLineColor(4)
h_SV2MC_3trk.Scale(1./h_SV2MC_3trk.Integral(0,-1))
h_SV2MC_3trk.SetMinimum(0.0)
h_SV2MC_3trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_3trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 3}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_3trks.pdf")
can.SaveAs("plots/png/dSV2MC_3trks.png")
###################################################

###################################################
h_SV2MC_4trk.SetLineColor(4)
h_SV2MC_4trk.Scale(1./h_SV2MC_4trk.Integral(0,-1))
h_SV2MC_4trk.SetMinimum(0.0)
h_SV2MC_4trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_4trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 4}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_4trks.pdf")
can.SaveAs("plots/png/dSV2MC_4trks.png")
###################################################

###################################################
h_SV2MC_5trk.SetLineColor(4)
h_SV2MC_5trk.Scale(1./h_SV2MC_5trk.Integral(0,-1))
h_SV2MC_5trk.SetMinimum(0.0)
h_SV2MC_5trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_5trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 5}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_5trks.pdf")
can.SaveAs("plots/png/dSV2MC_5trks.png")
###################################################

###################################################
h_SV2MC_6trk.SetLineColor(4)
h_SV2MC_6trk.Scale(1./h_SV2MC_6trk.Integral(0,-1))
h_SV2MC_6trk.SetMinimum(0.0)
h_SV2MC_6trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_6trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 6}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_6trks.pdf")
can.SaveAs("plots/png/dSV2MC_6trks.png")
###################################################

###################################################
h_SV2MC_x_2trk.SetLineColor(4)
h_SV2MC_x_2trk.Scale(1./h_SV2MC_x_2trk.Integral(0,-1))
h_SV2MC_x_2trk.SetMinimum(0.0)
h_SV2MC_x_2trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_2trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 2}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_x_2trks.pdf")
can.SaveAs("plots/png/dSV2MC_x_2trks.png")
###################################################

###################################################
h_SV2MC_x_3trk.SetLineColor(4)
h_SV2MC_x_3trk.Scale(1./h_SV2MC_x_3trk.Integral(0,-1))
h_SV2MC_x_3trk.SetMinimum(0.0)
h_SV2MC_x_3trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_3trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 3}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_x_3trks.pdf")
can.SaveAs("plots/png/dSV2MC_x_3trks.png")
###################################################

###################################################
h_SV2MC_x_4trk.SetLineColor(4)
h_SV2MC_x_4trk.Scale(1./h_SV2MC_x_4trk.Integral(0,-1))
h_SV2MC_x_4trk.SetMinimum(0.0)
h_SV2MC_x_4trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_4trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 4}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_x_4trks.pdf")
can.SaveAs("plots/png/dSV2MC_x_4trks.png")
###################################################

###################################################
h_SV2MC_x_5trk.SetLineColor(4)
h_SV2MC_x_5trk.Scale(1./h_SV2MC_x_5trk.Integral(0,-1))
h_SV2MC_x_5trk.SetMinimum(0.0)
h_SV2MC_x_5trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_5trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 5}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_x_5trks.pdf")
can.SaveAs("plots/png/dSV2MC_x_5trks.png")
###################################################

###################################################
h_SV2MC_x_6trk.SetLineColor(4)
h_SV2MC_x_6trk.Scale(1./h_SV2MC_x_6trk.Integral(0,-1))
h_SV2MC_x_6trk.SetMinimum(0.0)
h_SV2MC_x_6trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_6trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 6}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_x_6trks.pdf")
can.SaveAs("plots/png/dSV2MC_x_6trks.png")
###################################################


###################################################
h_SV2MC_y_2trk.SetLineColor(4)
h_SV2MC_y_2trk.Scale(1./h_SV2MC_y_2trk.Integral(0,-1))
h_SV2MC_y_2trk.SetMinimum(0.0)
h_SV2MC_y_2trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_2trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 2}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_y_2trks.pdf")
can.SaveAs("plots/png/dSV2MC_y_2trks.png")
###################################################

###################################################
h_SV2MC_y_3trk.SetLineColor(4)
h_SV2MC_y_3trk.Scale(1./h_SV2MC_y_3trk.Integral(0,-1))
h_SV2MC_y_3trk.SetMinimum(0.0)
h_SV2MC_y_3trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_3trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 3}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_y_3trks.pdf")
can.SaveAs("plots/png/dSV2MC_y_3trks.png")
###################################################

###################################################
h_SV2MC_y_4trk.SetLineColor(4)
h_SV2MC_y_4trk.Scale(1./h_SV2MC_y_4trk.Integral(0,-1))
h_SV2MC_y_4trk.SetMinimum(0.0)
h_SV2MC_y_4trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_4trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 4}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_y_4trks.pdf")
can.SaveAs("plots/png/dSV2MC_y_4trks.png")
###################################################

###################################################
h_SV2MC_y_5trk.SetLineColor(4)
h_SV2MC_y_5trk.Scale(1./h_SV2MC_y_5trk.Integral(0,-1))
h_SV2MC_y_5trk.SetMinimum(0.0)
h_SV2MC_y_5trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_5trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 5}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_y_5trks.pdf")
can.SaveAs("plots/png/dSV2MC_y_5trks.png")
###################################################

###################################################
h_SV2MC_y_6trk.SetLineColor(4)
h_SV2MC_y_6trk.Scale(1./h_SV2MC_y_6trk.Integral(0,-1))
h_SV2MC_y_6trk.SetMinimum(0.0)
h_SV2MC_y_6trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_6trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 6}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_y_6trks.pdf")
can.SaveAs("plots/png/dSV2MC_y_6trks.png")
###################################################







###################################################
h_SV2MC_z_2trk.SetLineColor(4)
h_SV2MC_z_2trk.Scale(1./h_SV2MC_z_2trk.Integral(0,-1))
h_SV2MC_z_2trk.SetMinimum(0.0)
h_SV2MC_z_2trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_2trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 2}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_z_2trks.pdf")
can.SaveAs("plots/png/dSV2MC_z_2trks.png")
###################################################

###################################################
h_SV2MC_z_3trk.SetLineColor(4)
h_SV2MC_z_3trk.Scale(1./h_SV2MC_z_3trk.Integral(0,-1))
h_SV2MC_z_3trk.SetMinimum(0.0)
h_SV2MC_z_3trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_3trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 3}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_z_3trks.pdf")
can.SaveAs("plots/png/dSV2MC_z_3trks.png")
###################################################

###################################################
h_SV2MC_z_4trk.SetLineColor(4)
h_SV2MC_z_4trk.Scale(1./h_SV2MC_z_4trk.Integral(0,-1))
h_SV2MC_z_4trk.SetMinimum(0.0)
h_SV2MC_z_4trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_4trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 4}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_z_4trks.pdf")
can.SaveAs("plots/png/dSV2MC_z_4trks.png")
###################################################

###################################################
h_SV2MC_z_5trk.SetLineColor(4)
h_SV2MC_z_5trk.Scale(1./h_SV2MC_z_5trk.Integral(0,-1))
h_SV2MC_z_5trk.SetMinimum(0.0)
h_SV2MC_z_5trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_5trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 5}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_z_5trks.pdf")
can.SaveAs("plots/png/dSV2MC_z_5trks.png")
###################################################

###################################################
h_SV2MC_z_6trk.SetLineColor(4)
h_SV2MC_z_6trk.Scale(1./h_SV2MC_z_6trk.Integral(0,-1))
h_SV2MC_z_6trk.SetMinimum(0.0)
h_SV2MC_z_6trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_6trk.GetRMS())
tt.DrawLatexNDC(0.60,0.73  ,"#color[4]{N tracks = 6}")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MC_z_6trks.pdf")
can.SaveAs("plots/png/dSV2MC_z_6trks.png")
###################################################


###################################################
h_PV2MC_x_pull.SetLineColor(4)
h_PV2MC_x_pull.Scale(1./h_PV2MC_x_pull.Integral(0,-1))
h_PV2MC_x_pull.SetMaximum(0.045)
h_PV2MC_x_pull.SetMinimum(0.0)
h_PV2MC_x_pull.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC_x_pull.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC_x_pull.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MCx_pull.pdf")
can.SaveAs("plots/png/dPV2MCx_pull.png")
###################################################

###################################################
h_PV2MC_y_pull.SetLineColor(4)
h_PV2MC_y_pull.Scale(1./h_PV2MC_y_pull.Integral(0,-1))
h_PV2MC_y_pull.SetMaximum(0.045)
h_PV2MC_y_pull.SetMinimum(0.0)
h_PV2MC_y_pull.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC_y_pull.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC_y_pull.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MCy_pull.pdf")
can.SaveAs("plots/png/dPV2MCy_pull.png")
###################################################


###################################################
h_PV2MC_z_pull.SetLineColor(4)
h_PV2MC_z_pull.Scale(1./h_PV2MC_z_pull.Integral(0,-1))
h_PV2MC_z_pull.SetMaximum(0.045)
h_PV2MC_z_pull.SetMinimum(0.0)
h_PV2MC_z_pull.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_PV2MC_z_pull.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_PV2MC_z_pull.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dPV2MCz_pull.pdf")
can.SaveAs("plots/png/dPV2MCz_pull.png")
###################################################



###################################################
h_recoeff_SV_2trk.SetLineColor(4)
h_recoeff_SV_2trk.Scale(1./h_recoeff_SV_2trk.Integral(0,-1))
h_recoeff_SV_2trk.SetMaximum(1.)
h_recoeff_SV_2trk.SetMinimum(0.0)
h_recoeff_SV_2trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks = 2")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/recoEff_2trk.pdf")
can.SaveAs("plots/png/recoEff_2trk.png")
###################################################

###################################################
h_recoeff_SV_3trk.SetLineColor(4)
h_recoeff_SV_3trk.Scale(1./h_recoeff_SV_3trk.Integral(0,-1))
h_recoeff_SV_3trk.SetMaximum(1.)
h_recoeff_SV_3trk.SetMinimum(0.0)
h_recoeff_SV_3trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks = 3")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/recoEff_3trk.pdf")
can.SaveAs("plots/png/recoEff_3trk.png")
fout.cd()
h_recoeff_SV_3trk.Write()
###################################################

###################################################
h_recoeff_SV_4trk.SetLineColor(4)
h_recoeff_SV_4trk.Scale(1./h_recoeff_SV_4trk.Integral(0,-1))
h_recoeff_SV_4trk.SetMaximum(1.)
h_recoeff_SV_4trk.SetMinimum(0.0)
h_recoeff_SV_4trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks = 4")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/recoEff_4trk.pdf")
can.SaveAs("plots/png/recoEff_4trk.png")
###################################################

###################################################
h_recoeff_SV_5trk.SetLineColor(4)
h_recoeff_SV_5trk.Scale(1./h_recoeff_SV_5trk.Integral(0,-1))
h_recoeff_SV_5trk.SetMaximum(1.)
h_recoeff_SV_5trk.SetMinimum(0.0)
h_recoeff_SV_5trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks = 5")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/recoEff_5trk.pdf")
can.SaveAs("plots/png/recoEff_5trk.png")
###################################################

###################################################
h_recoeff_SV_6trk.SetLineColor(4)
h_recoeff_SV_6trk.Scale(1./h_recoeff_SV_6trk.Integral(0,-1))
h_recoeff_SV_6trk.SetMaximum(1.)
h_recoeff_SV_6trk.SetMinimum(0.0)
h_recoeff_SV_6trk.Draw("HIST,E1")
tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b} N tracks = 6")
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/recoEff_6trk.pdf")
can.SaveAs("plots/png/recoEff_6trk.png")
###################################################


###################################################
h_SV2MC_x_pull_2trk.SetLineColor(4)
h_SV2MC_x_pull_2trk.Scale(1./h_SV2MC_x_pull_2trk.Integral(0,-1))
h_SV2MC_x_pull_2trk.SetMaximum(0.045)
h_SV2MC_x_pull_2trk.SetMinimum(0.0)
h_SV2MC_x_pull_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_pull_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_pull_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCx_pull_2trk.pdf")
can.SaveAs("plots/png/dSV2MCx_pull_2trk.png")
###################################################

###################################################
h_SV2MC_y_pull_2trk.SetLineColor(4)
h_SV2MC_y_pull_2trk.Scale(1./h_SV2MC_y_pull_2trk.Integral(0,-1))
h_SV2MC_y_pull_2trk.SetMaximum(0.045)
h_SV2MC_y_pull_2trk.SetMinimum(0.0)
h_SV2MC_y_pull_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_pull_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_pull_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCy_pull_2trk.pdf")
can.SaveAs("plots/png/dSV2MCy_pull_2trk.png")
###################################################

###################################################
h_SV2MC_z_pull_2trk.SetLineColor(4)
h_SV2MC_z_pull_2trk.Scale(1./h_SV2MC_z_pull_2trk.Integral(0,-1))
h_SV2MC_z_pull_2trk.SetMaximum(0.045)
h_SV2MC_z_pull_2trk.SetMinimum(0.0)
h_SV2MC_z_pull_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_pull_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_pull_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCz_pull_2trk.pdf")
can.SaveAs("plots/png/dSV2MCz_pull_2trk.png")
###################################################


###################################################
h_SV2MC_x_pull_3trk.SetLineColor(4)
h_SV2MC_x_pull_3trk.Scale(1./h_SV2MC_x_pull_3trk.Integral(0,-1))
h_SV2MC_x_pull_3trk.SetMaximum(0.045)
h_SV2MC_x_pull_3trk.SetMinimum(0.0)
h_SV2MC_x_pull_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_pull_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_pull_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCx_pull_3trk.pdf")
can.SaveAs("plots/png/dSV2MCx_pull_3trk.png")
###################################################

###################################################
h_SV2MC_y_pull_3trk.SetLineColor(4)
h_SV2MC_y_pull_3trk.Scale(1./h_SV2MC_y_pull_3trk.Integral(0,-1))
h_SV2MC_y_pull_3trk.SetMaximum(0.045)
h_SV2MC_y_pull_3trk.SetMinimum(0.0)
h_SV2MC_y_pull_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_pull_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_pull_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCy_pull_3trk.pdf")
can.SaveAs("plots/png/dSV2MCy_pull_3trk.png")
###################################################

###################################################
h_SV2MC_z_pull_3trk.SetLineColor(4)
h_SV2MC_z_pull_3trk.Scale(1./h_SV2MC_z_pull_3trk.Integral(0,-1))
h_SV2MC_z_pull_3trk.SetMaximum(0.045)
h_SV2MC_z_pull_3trk.SetMinimum(0.0)
h_SV2MC_z_pull_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_pull_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_pull_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCz_pull_3trk.pdf")
can.SaveAs("plots/png/dSV2MCz_pull_3trk.png")
###################################################


###################################################
h_SV2MC_x_pull_4trk.SetLineColor(4)
h_SV2MC_x_pull_4trk.Scale(1./h_SV2MC_x_pull_4trk.Integral(0,-1))
h_SV2MC_x_pull_4trk.SetMaximum(0.045)
h_SV2MC_x_pull_4trk.SetMinimum(0.0)
h_SV2MC_x_pull_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_pull_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_pull_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCx_pull_4trk.pdf")
can.SaveAs("plots/png/dSV2MCx_pull_4trk.png")
###################################################

###################################################
h_SV2MC_y_pull_4trk.SetLineColor(4)
h_SV2MC_y_pull_4trk.Scale(1./h_SV2MC_y_pull_4trk.Integral(0,-1))
h_SV2MC_y_pull_4trk.SetMaximum(0.045)
h_SV2MC_y_pull_4trk.SetMinimum(0.0)
h_SV2MC_y_pull_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_pull_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_pull_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCy_pull_4trk.pdf")
can.SaveAs("plots/png/dSV2MCy_pull_4trk.png")
###################################################

###################################################
h_SV2MC_z_pull_4trk.SetLineColor(4)
h_SV2MC_z_pull_4trk.Scale(1./h_SV2MC_z_pull_4trk.Integral(0,-1))
h_SV2MC_z_pull_4trk.SetMaximum(0.045)
h_SV2MC_z_pull_4trk.SetMinimum(0.0)
h_SV2MC_z_pull_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_pull_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_pull_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCz_pull_4trk.pdf")
can.SaveAs("plots/png/dSV2MCz_pull_4trk.png")
###################################################

###################################################
h_SV2MC_x_pull_5trk.SetLineColor(4)
h_SV2MC_x_pull_5trk.Scale(1./h_SV2MC_x_pull_5trk.Integral(0,-1))
h_SV2MC_x_pull_5trk.SetMaximum(0.045)
h_SV2MC_x_pull_5trk.SetMinimum(0.0)
h_SV2MC_x_pull_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_pull_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_pull_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCx_pull_5trk.pdf")
can.SaveAs("plots/png/dSV2MCx_pull_5trk.png")
###################################################

###################################################
h_SV2MC_y_pull_5trk.SetLineColor(4)
h_SV2MC_y_pull_5trk.Scale(1./h_SV2MC_y_pull_5trk.Integral(0,-1))
h_SV2MC_y_pull_5trk.SetMaximum(0.045)
h_SV2MC_y_pull_5trk.SetMinimum(0.0)
h_SV2MC_y_pull_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_pull_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_pull_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCy_pull_5trk.pdf")
can.SaveAs("plots/png/dSV2MCy_pull_5trk.png")
###################################################

###################################################
h_SV2MC_z_pull_5trk.SetLineColor(4)
h_SV2MC_z_pull_5trk.Scale(1./h_SV2MC_z_pull_5trk.Integral(0,-1))
h_SV2MC_z_pull_5trk.SetMaximum(0.045)
h_SV2MC_z_pull_5trk.SetMinimum(0.0)
h_SV2MC_z_pull_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_pull_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_pull_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCz_pull_5trk.pdf")
can.SaveAs("plots/png/dSV2MCz_pull_5trk.png")
###################################################

###################################################
h_SV2MC_x_pull_6trk.SetLineColor(4)
h_SV2MC_x_pull_6trk.Scale(1./h_SV2MC_x_pull_6trk.Integral(0,-1))
h_SV2MC_x_pull_6trk.SetMaximum(0.045)
h_SV2MC_x_pull_6trk.SetMinimum(0.0)
h_SV2MC_x_pull_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_x_pull_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_x_pull_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCx_pull_6trk.pdf")
can.SaveAs("plots/png/dSV2MCx_pull_6trk.png")
###################################################

###################################################
h_SV2MC_y_pull_6trk.SetLineColor(4)
h_SV2MC_y_pull_6trk.Scale(1./h_SV2MC_y_pull_6trk.Integral(0,-1))
h_SV2MC_y_pull_6trk.SetMaximum(0.045)
h_SV2MC_y_pull_6trk.SetMinimum(0.0)
h_SV2MC_y_pull_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_y_pull_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_y_pull_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCy_pull_6trk.pdf")
can.SaveAs("plots/png/dSV2MCy_pull_6trk.png")
###################################################

###################################################
h_SV2MC_z_pull_6trk.SetLineColor(4)
h_SV2MC_z_pull_6trk.Scale(1./h_SV2MC_z_pull_6trk.Integral(0,-1))
h_SV2MC_z_pull_6trk.SetMaximum(0.045)
h_SV2MC_z_pull_6trk.SetMinimum(0.0)
h_SV2MC_z_pull_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_SV2MC_z_pull_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_SV2MC_z_pull_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dSV2MCz_pull_6trk.pdf")
can.SaveAs("plots/png/dSV2MCz_pull_6trk.png")
###################################################



###################################################
h_FD2PV_2trk.SetLineColor(4)
h_FD2PV_2trk.Scale(1./h_FD2PV_2trk.Integral(0,-1))
#h_FD2PV_2trk.SetMaximum(0.045)
h_FD2PV_2trk.SetMinimum(0.0)
h_FD2PV_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_2trk.pdf")
can.SaveAs("plots/png/FD2PV_2trk.png")
###################################################

###################################################
h_FD2PV_x_2trk.SetLineColor(4)
h_FD2PV_x_2trk.Scale(1./h_FD2PV_x_2trk.Integral(0,-1))
#h_FD2PV_x_2trk.SetMaximum(0.045)
h_FD2PV_x_2trk.SetMinimum(0.0)
h_FD2PV_x_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_2trk.pdf")
can.SaveAs("plots/png/FD2PV_x_2trk.png")
###################################################

###################################################
h_FD2PV_y_2trk.SetLineColor(4)
h_FD2PV_y_2trk.Scale(1./h_FD2PV_y_2trk.Integral(0,-1))
#h_FD2PV_y_2trk.SetMaximum(0.045)
h_FD2PV_y_2trk.SetMinimum(0.0)
h_FD2PV_y_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_2trk.pdf")
can.SaveAs("plots/png/FD2PV_y_2trk.png")
###################################################

###################################################
h_FD2PV_z_2trk.SetLineColor(4)
h_FD2PV_z_2trk.Scale(1./h_FD2PV_z_2trk.Integral(0,-1))
#h_FD2PV_z_2trk.SetMaximum(0.045)
h_FD2PV_z_2trk.SetMinimum(0.0)
h_FD2PV_z_2trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_2trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_2trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_2trk.pdf")
can.SaveAs("plots/png/FD2PV_z_2trk.png")
###################################################

###################################################
h_FD2PV_2trk_sig.SetLineColor(4)
h_FD2PV_2trk_sig.Scale(1./h_FD2PV_2trk_sig.Integral(0,-1))
#h_FD2PV_2trk_sig.SetMaximum(0.045)
h_FD2PV_2trk_sig.SetMinimum(0.0)
h_FD2PV_2trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_2trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_2trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_2trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_2trk_sig.png")
###################################################

###################################################
h_FD2PV_x_2trk_sig.SetLineColor(4)
h_FD2PV_x_2trk_sig.Scale(1./h_FD2PV_x_2trk_sig.Integral(0,-1))
#h_FD2PV_x_2trk_sig.SetMaximum(0.045)
h_FD2PV_x_2trk_sig.SetMinimum(0.0)
h_FD2PV_x_2trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_2trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_2trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_2trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_x_2trk_sig.png")
###################################################

###################################################
h_FD2PV_y_2trk_sig.SetLineColor(4)
h_FD2PV_y_2trk_sig.Scale(1./h_FD2PV_y_2trk_sig.Integral(0,-1))
#h_FD2PV_y_2trk_sig.SetMaximum(0.045)
h_FD2PV_y_2trk_sig.SetMinimum(0.0)
h_FD2PV_y_2trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_2trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_2trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_2trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_y_2trk_sig.png")
###################################################

###################################################
h_FD2PV_z_2trk_sig.SetLineColor(4)
h_FD2PV_z_2trk_sig.Scale(1./h_FD2PV_z_2trk_sig.Integral(0,-1))
#h_FD2PV_z_2trk_sig.SetMaximum(0.045)
h_FD2PV_z_2trk_sig.SetMinimum(0.0)
h_FD2PV_z_2trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_2trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_2trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_2trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_z_2trk_sig.png")
###################################################







###################################################
h_FD2PV_3trk.SetLineColor(4)
h_FD2PV_3trk.Scale(1./h_FD2PV_3trk.Integral(0,-1))
#h_FD2PV_3trk.SetMaximum(0.045)
h_FD2PV_3trk.SetMinimum(0.0)
h_FD2PV_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_3trk.pdf")
can.SaveAs("plots/png/FD2PV_3trk.png")
###################################################

###################################################
h_FD2PV_x_3trk.SetLineColor(4)
h_FD2PV_x_3trk.Scale(1./h_FD2PV_x_3trk.Integral(0,-1))
#h_FD2PV_x_3trk.SetMaximum(0.045)
h_FD2PV_x_3trk.SetMinimum(0.0)
h_FD2PV_x_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_3trk.pdf")
can.SaveAs("plots/png/FD2PV_x_3trk.png")
###################################################

###################################################
h_FD2PV_y_3trk.SetLineColor(4)
h_FD2PV_y_3trk.Scale(1./h_FD2PV_y_3trk.Integral(0,-1))
#h_FD2PV_y_3trk.SetMaximum(0.045)
h_FD2PV_y_3trk.SetMinimum(0.0)
h_FD2PV_y_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_3trk.pdf")
can.SaveAs("plots/png/FD2PV_y_3trk.png")
###################################################

###################################################
h_FD2PV_z_3trk.SetLineColor(4)
h_FD2PV_z_3trk.Scale(1./h_FD2PV_z_3trk.Integral(0,-1))
#h_FD2PV_z_3trk.SetMaximum(0.045)
h_FD2PV_z_3trk.SetMinimum(0.0)
h_FD2PV_z_3trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_3trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_3trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_3trk.pdf")
can.SaveAs("plots/png/FD2PV_z_3trk.png")
###################################################

###################################################
h_FD2PV_3trk_sig.SetLineColor(4)
h_FD2PV_3trk_sig.Scale(1./h_FD2PV_3trk_sig.Integral(0,-1))
#h_FD2PV_3trk_sig.SetMaximum(0.045)
h_FD2PV_3trk_sig.SetMinimum(0.0)
h_FD2PV_3trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_3trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_3trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_3trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_3trk_sig.png")
###################################################

###################################################
h_FD2PV_x_3trk_sig.SetLineColor(4)
h_FD2PV_x_3trk_sig.Scale(1./h_FD2PV_x_3trk_sig.Integral(0,-1))
#h_FD2PV_x_3trk_sig.SetMaximum(0.045)
h_FD2PV_x_3trk_sig.SetMinimum(0.0)
h_FD2PV_x_3trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_3trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_3trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_3trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_x_3trk_sig.png")
###################################################

###################################################
h_FD2PV_y_3trk_sig.SetLineColor(4)
h_FD2PV_y_3trk_sig.Scale(1./h_FD2PV_y_3trk_sig.Integral(0,-1))
#h_FD2PV_y_3trk_sig.SetMaximum(0.045)
h_FD2PV_y_3trk_sig.SetMinimum(0.0)
h_FD2PV_y_3trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_3trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_3trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_3trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_y_3trk_sig.png")
###################################################

###################################################
h_FD2PV_z_3trk_sig.SetLineColor(4)
h_FD2PV_z_3trk_sig.Scale(1./h_FD2PV_z_3trk_sig.Integral(0,-1))
#h_FD2PV_z_3trk_sig.SetMaximum(0.045)
h_FD2PV_z_3trk_sig.SetMinimum(0.0)
h_FD2PV_z_3trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_3trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_3trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_3trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_z_3trk_sig.png")
###################################################







###################################################
h_FD2PV_4trk.SetLineColor(4)
h_FD2PV_4trk.Scale(1./h_FD2PV_4trk.Integral(0,-1))
#h_FD2PV_4trk.SetMaximum(0.045)
h_FD2PV_4trk.SetMinimum(0.0)
h_FD2PV_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_4trk.pdf")
can.SaveAs("plots/png/FD2PV_4trk.png")
###################################################

###################################################
h_FD2PV_x_4trk.SetLineColor(4)
h_FD2PV_x_4trk.Scale(1./h_FD2PV_x_4trk.Integral(0,-1))
#h_FD2PV_x_4trk.SetMaximum(0.045)
h_FD2PV_x_4trk.SetMinimum(0.0)
h_FD2PV_x_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_4trk.pdf")
can.SaveAs("plots/png/FD2PV_x_4trk.png")
###################################################

###################################################
h_FD2PV_y_4trk.SetLineColor(4)
h_FD2PV_y_4trk.Scale(1./h_FD2PV_y_4trk.Integral(0,-1))
#h_FD2PV_y_4trk.SetMaximum(0.045)
h_FD2PV_y_4trk.SetMinimum(0.0)
h_FD2PV_y_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_4trk.pdf")
can.SaveAs("plots/png/FD2PV_y_4trk.png")
###################################################

###################################################
h_FD2PV_z_4trk.SetLineColor(4)
h_FD2PV_z_4trk.Scale(1./h_FD2PV_z_4trk.Integral(0,-1))
#h_FD2PV_z_4trk.SetMaximum(0.045)
h_FD2PV_z_4trk.SetMinimum(0.0)
h_FD2PV_z_4trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_4trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_4trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_4trk.pdf")
can.SaveAs("plots/png/FD2PV_z_4trk.png")
###################################################

###################################################
h_FD2PV_4trk_sig.SetLineColor(4)
h_FD2PV_4trk_sig.Scale(1./h_FD2PV_4trk_sig.Integral(0,-1))
#h_FD2PV_4trk_sig.SetMaximum(0.045)
h_FD2PV_4trk_sig.SetMinimum(0.0)
h_FD2PV_4trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_4trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_4trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_4trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_4trk_sig.png")
###################################################

###################################################
h_FD2PV_x_4trk_sig.SetLineColor(4)
h_FD2PV_x_4trk_sig.Scale(1./h_FD2PV_x_4trk_sig.Integral(0,-1))
#h_FD2PV_x_4trk_sig.SetMaximum(0.045)
h_FD2PV_x_4trk_sig.SetMinimum(0.0)
h_FD2PV_x_4trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_4trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_4trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_4trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_x_4trk_sig.png")
###################################################

###################################################
h_FD2PV_y_4trk_sig.SetLineColor(4)
h_FD2PV_y_4trk_sig.Scale(1./h_FD2PV_y_4trk_sig.Integral(0,-1))
#h_FD2PV_y_4trk_sig.SetMaximum(0.045)
h_FD2PV_y_4trk_sig.SetMinimum(0.0)
h_FD2PV_y_4trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_4trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_4trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_4trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_y_4trk_sig.png")
###################################################

###################################################
h_FD2PV_z_4trk_sig.SetLineColor(4)
h_FD2PV_z_4trk_sig.Scale(1./h_FD2PV_z_4trk_sig.Integral(0,-1))
#h_FD2PV_z_4trk_sig.SetMaximum(0.045)
h_FD2PV_z_4trk_sig.SetMinimum(0.0)
h_FD2PV_z_4trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_4trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_4trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_4trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_z_4trk_sig.png")
###################################################







###################################################
h_FD2PV_5trk.SetLineColor(4)
h_FD2PV_5trk.Scale(1./h_FD2PV_5trk.Integral(0,-1))
#h_FD2PV_5trk.SetMaximum(0.045)
h_FD2PV_5trk.SetMinimum(0.0)
h_FD2PV_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_5trk.pdf")
can.SaveAs("plots/png/FD2PV_5trk.png")
###################################################

###################################################
h_FD2PV_x_5trk.SetLineColor(4)
h_FD2PV_x_5trk.Scale(1./h_FD2PV_x_5trk.Integral(0,-1))
#h_FD2PV_x_5trk.SetMaximum(0.045)
h_FD2PV_x_5trk.SetMinimum(0.0)
h_FD2PV_x_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_5trk.pdf")
can.SaveAs("plots/png/FD2PV_x_5trk.png")
###################################################

###################################################
h_FD2PV_y_5trk.SetLineColor(4)
h_FD2PV_y_5trk.Scale(1./h_FD2PV_y_5trk.Integral(0,-1))
#h_FD2PV_y_5trk.SetMaximum(0.045)
h_FD2PV_y_5trk.SetMinimum(0.0)
h_FD2PV_y_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_5trk.pdf")
can.SaveAs("plots/png/FD2PV_y_5trk.png")
###################################################

###################################################
h_FD2PV_z_5trk.SetLineColor(4)
h_FD2PV_z_5trk.Scale(1./h_FD2PV_z_5trk.Integral(0,-1))
#h_FD2PV_z_5trk.SetMaximum(0.045)
h_FD2PV_z_5trk.SetMinimum(0.0)
h_FD2PV_z_5trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_5trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_5trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_5trk.pdf")
can.SaveAs("plots/png/FD2PV_z_5trk.png")
###################################################

###################################################
h_FD2PV_5trk_sig.SetLineColor(4)
h_FD2PV_5trk_sig.Scale(1./h_FD2PV_5trk_sig.Integral(0,-1))
#h_FD2PV_5trk_sig.SetMaximum(0.045)
h_FD2PV_5trk_sig.SetMinimum(0.0)
h_FD2PV_5trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_5trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_5trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_5trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_5trk_sig.png")
###################################################

###################################################
h_FD2PV_x_5trk_sig.SetLineColor(4)
h_FD2PV_x_5trk_sig.Scale(1./h_FD2PV_x_5trk_sig.Integral(0,-1))
#h_FD2PV_x_5trk_sig.SetMaximum(0.045)
h_FD2PV_x_5trk_sig.SetMinimum(0.0)
h_FD2PV_x_5trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_5trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_5trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_5trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_x_5trk_sig.png")
###################################################

###################################################
h_FD2PV_y_5trk_sig.SetLineColor(4)
h_FD2PV_y_5trk_sig.Scale(1./h_FD2PV_y_5trk_sig.Integral(0,-1))
#h_FD2PV_y_5trk_sig.SetMaximum(0.045)
h_FD2PV_y_5trk_sig.SetMinimum(0.0)
h_FD2PV_y_5trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_5trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_5trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_5trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_y_5trk_sig.png")
###################################################

###################################################
h_FD2PV_z_5trk_sig.SetLineColor(4)
h_FD2PV_z_5trk_sig.Scale(1./h_FD2PV_z_5trk_sig.Integral(0,-1))
#h_FD2PV_z_5trk_sig.SetMaximum(0.045)
h_FD2PV_z_5trk_sig.SetMinimum(0.0)
h_FD2PV_z_5trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_5trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_5trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_5trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_z_5trk_sig.png")
###################################################




###################################################
h_FD2PV_6trk.SetLineColor(4)
h_FD2PV_6trk.Scale(1./h_FD2PV_6trk.Integral(0,-1))
#h_FD2PV_6trk.SetMaximum(0.045)
h_FD2PV_6trk.SetMinimum(0.0)
h_FD2PV_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_6trk.pdf")
can.SaveAs("plots/png/FD2PV_6trk.png")
###################################################

###################################################
h_FD2PV_x_6trk.SetLineColor(4)
h_FD2PV_x_6trk.Scale(1./h_FD2PV_x_6trk.Integral(0,-1))
#h_FD2PV_x_6trk.SetMaximum(0.045)
h_FD2PV_x_6trk.SetMinimum(0.0)
h_FD2PV_x_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_6trk.pdf")
can.SaveAs("plots/png/FD2PV_x_6trk.png")
###################################################

###################################################
h_FD2PV_y_6trk.SetLineColor(4)
h_FD2PV_y_6trk.Scale(1./h_FD2PV_y_6trk.Integral(0,-1))
#h_FD2PV_y_6trk.SetMaximum(0.045)
h_FD2PV_y_6trk.SetMinimum(0.0)
h_FD2PV_y_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_6trk.pdf")
can.SaveAs("plots/png/FD2PV_y_6trk.png")
###################################################

###################################################
h_FD2PV_z_6trk.SetLineColor(4)
h_FD2PV_z_6trk.Scale(1./h_FD2PV_z_6trk.Integral(0,-1))
#h_FD2PV_z_6trk.SetMaximum(0.045)
h_FD2PV_z_6trk.SetMinimum(0.0)
h_FD2PV_z_6trk.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_6trk.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_6trk.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_6trk.pdf")
can.SaveAs("plots/png/FD2PV_z_6trk.png")
###################################################

###################################################
h_FD2PV_6trk_sig.SetLineColor(4)
h_FD2PV_6trk_sig.Scale(1./h_FD2PV_6trk_sig.Integral(0,-1))
#h_FD2PV_6trk_sig.SetMaximum(0.045)
h_FD2PV_6trk_sig.SetMinimum(0.0)
h_FD2PV_6trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_6trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_6trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_6trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_6trk_sig.png")
###################################################

###################################################
h_FD2PV_x_6trk_sig.SetLineColor(4)
h_FD2PV_x_6trk_sig.Scale(1./h_FD2PV_x_6trk_sig.Integral(0,-1))
#h_FD2PV_x_6trk_sig.SetMaximum(0.045)
h_FD2PV_x_6trk_sig.SetMinimum(0.0)
h_FD2PV_x_6trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_x_6trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_x_6trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_x_6trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_x_6trk_sig.png")
###################################################

###################################################
h_FD2PV_y_6trk_sig.SetLineColor(4)
h_FD2PV_y_6trk_sig.Scale(1./h_FD2PV_y_6trk_sig.Integral(0,-1))
#h_FD2PV_y_6trk_sig.SetMaximum(0.045)
h_FD2PV_y_6trk_sig.SetMinimum(0.0)
h_FD2PV_y_6trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_y_6trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_y_6trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_y_6trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_y_6trk_sig.png")
###################################################

###################################################
h_FD2PV_z_6trk_sig.SetLineColor(4)
h_FD2PV_z_6trk_sig.Scale(1./h_FD2PV_z_6trk_sig.Integral(0,-1))
#h_FD2PV_z_6trk_sig.SetMaximum(0.045)
h_FD2PV_z_6trk_sig.SetMinimum(0.0)
h_FD2PV_z_6trk_sig.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_FD2PV_z_6trk_sig.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_FD2PV_z_6trk_sig.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/FD2PV_z_6trk_sig.pdf")
can.SaveAs("plots/png/FD2PV_z_6trk_sig.png")
###################################################





###################################################
h_dmin_PV2DV.SetLineColor(4)
h_dmin_PV2DV.Scale(1./h_dmin_PV2DV.Integral(0,-1))
#h_dmin_PV2DV.SetMaximum(0.045)
h_dmin_PV2DV.SetMinimum(0.0)
h_dmin_PV2DV.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_dmin_PV2DV.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_dmin_PV2DV.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dmin_PV2DV.pdf")
can.SaveAs("plots/png/dmin_PV2DV.png")
###################################################
###################################################
h_dmin_DV2DV.SetLineColor(4)
h_dmin_DV2DV.Scale(1./h_dmin_DV2DV.Integral(0,-1))
#h_dmin_DV2DV.SetMaximum(0.045)
h_dmin_DV2DV.SetMinimum(0.0)
h_dmin_DV2DV.Draw("HIST,E1")

tt.DrawLatexNDC(0.60,0.92,"Z #rightarrow b#bar{b}")
tt.DrawLatexNDC(0.60,0.85  ,"#color[4]{Mean: %f}"%h_dmin_DV2DV.GetMean())
tt.DrawLatexNDC(0.60,0.79  ,"#color[4]{RMS: %f}"%h_dmin_DV2DV.GetRMS())
#r.gPad.SetLogy(1)
can.SaveAs("plots/pdf/dmin_DV2DV.pdf")
can.SaveAs("plots/png/dmin_DV2DV.png")
###################################################

fout.Write()
fout.Close()
