import ROOT
# plots don't appear while you run
ROOT.gROOT.SetBatch(0)
# no stat box on plots
ROOT.gStyle.SetOptStat(0)
# no title shown 
ROOT.gStyle.SetOptTitle(0)

# list of lists
# each internal list: hist name, x title, y title, rebin (if needed)
p_list = [
     ["RecoMissingEnergy_e", "Reco Electron cos theta", "Entries", 3],

#    ['hnlLT', 'Lifetime [s]', 'Entries'],
#    ['angsepR', 'Reco Cos#theta ee', 'Entries', 5],
#    ['angsep', 'Cos#theta ee', 'Entries', 5],
#    ['et', 'Missing energy [GeV]', 'Entries'],
#    ['eTruthE', 'Electron energy [GeV]', 'Entries'] ,
#    ['eTruthP', 'Positron energy [GeV]', 'Entries'] ,
#    ['eRecoE', 'Reco Electron energy [GeV]', 'Entries'] ,
#    ['eRecoP', 'Reco Positron energy [GeV]', 'Entries'] ,
#    ['etaRE', 'Reco electron #eta', 'Entries'] ,
#    ['etaRP', 'Reco positron #eta', 'Entries'] ,
#    ['phiRE', 'Reco electron #phi', 'Entries'] ,
#    ['phiRP', 'Reco positron #phi', 'Entries'] ,
#    ['deletaR', 'Reco del eta ee', 'Entries'] ,
#    ['delphiR', 'Reco del phi ee', 'Entries'] ,
#    ['delRR', 'Reco del R ee', 'Entries'] ,
#    ['etaE', 'electron #eta', 'Entries'] ,
#    ['etaP', 'positron #eta', 'Entries'] ,
#    ['phiE', 'electron #phi', 'Entries'] ,
#    ['phiP', 'positron #phi', 'Entries'] ,
#    ['deleta', 'del eta ee', 'Entries'] ,
#    ['delphi', 'del phi ee', 'Entries'] ,
#    ['delR', 'del R ee', 'Entries'] ,
#    ['xmRE', 'Reco Px electron [GeV]', 'Entries'] ,
#    ['ymRE', 'Reco Py electron [GeV]', 'Entries'] ,
#    ['zmRE', 'Reco Pz electron [GeV]', 'Entries'] ,
#    ['xmRP', 'Reco Px positron [GeV]', 'Entries'] ,
#    ['ymRP', 'Reco Py positron (GeV', 'Entries'] ,
#    ['zmRP', 'Reco Pz positron [GeV]', 'Entries'] ,
#    ['tmRE', 'Reco pT electron [GeV]', 'Entries'] ,
#    ['tmRP', 'Reco pT positron [GeV]', 'Entries'] ,
#    ['xmTE', 'Px electron [GeV]', 'Entries'] ,
#    ['ymTE', 'Py electron [GeV]', 'Entries'] ,
#    ['zmTE', 'Pz electron [GeV]', 'Entries'] ,
#    ['xmTP', 'Px positron [GeV]', 'Entries'] ,
#    ['ymTP', 'Py positron [GeV]', 'Entries'] ,
#    ['zmTP', 'Pz positron [GeV]', 'Entries'] ,
#    ['tmTE', 'pT electron [GeV]', 'Entries'] ,    
#    ['tmTP', 'pT positron [GeV]', 'Entries'] ,
#   ['dispvrtx', 'displaced vetex [m]', 'Entries']
]

f_list = [
    ['histMajoranaSelect.root', 'Majorana 20 GeV'],
    ['histDiracSelect.root', 'Dirac 20 GeV'],
]

legend_list = [f[1] for f in f_list]
colors = [609, 856, 410, 801, 629, 879, 602, 921, 622]

def make_plot(h_list, plot_info, legend_list):
   #  print('looking at histogram:', plot_info[0])
    c = ROOT.TCanvas("can"+plot_info[0],"can"+plot_info[0],600,600)
    pad1 = ROOT.TPad("pad1", "pad1",0.0,0.35,1.0,1.0,21)
    pad2 = ROOT.TPad("pad2", "pad2",0.0,0.0,1.0,0.35,22)

    pad1.SetFillColor(0)
    pad1.SetBottomMargin(0.01)
    pad1.SetTickx()
    pad1.SetTicky()
    pad1.Draw()

    pad2.SetFillColor(0)
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)
    pad2.Draw()

    leg = ROOT.TLegend(0.55, 0.7, 0.87, 0.87)
    leg.SetFillStyle(0)
    leg.SetLineWidth(0)

    h_max = 0
    for ih,h in enumerate(h_list):
        leg.AddEntry(h, legend_list[ih])
        if len(plot_info)>3:
            h.Rebin(plot_info[3])
        if h.GetMaximum() > h_max:
            h_max = h.GetMaximum()
        h.Sumw2()

    # Draw in the top panel
    pad1.cd()
    for ih,h in enumerate(h_list):
        h.SetLineColor(colors[ih])
        h.SetLineWidth(3)
        h.GetXaxis().SetTitle(plot_info[1])        
        h.GetYaxis().SetTitle(plot_info[2])
        h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*1.5)
        h.GetYaxis().SetTitleOffset(0.8)
        h.SetMaximum(1.25*h_max)
        h.Draw('same')
        h.Draw('same E')
    leg.Draw()
    pad1.RedrawAxis()

    # build ratios
    h_ratios = []
    for ih,h in enumerate(h_list):
        if ih == 0:
            h_ratios.append(h.Clone('h_ratio_0'))
            for ibin in range(-1, h.GetNbinsX()+1):
                h_ratios[0].SetBinContent(ibin,1)
        else:
            h_ratios.append(h.Clone('h_ratio_'+str(ih)))
            h_ratios[ih].Divide(h_list[0])

    # draw in the bottom panel
    pad2.cd()
    for ih,h in enumerate(h_ratios):
        h.SetMaximum(1.5)
        h.SetMinimum(0.5)

        h.GetYaxis().SetTitle("Ratio to "+legend_list[0])
        h.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize()*1.6)
        h.GetYaxis().SetLabelOffset(0.01)
        h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*1.6)
        h.GetYaxis().SetTitleOffset(0.5)

        h.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize()*2.3)
        #h.GetXaxis().SetLabelOffset(0.02)
        h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*3)
        h.GetXaxis().SetTitleOffset(1.05)

        h.Draw('hist same')
        if ih>0:
            h.Draw('same E')
    c.SaveAs("20GeV_plots_rebin/"+plot_info[0]+'.pdf')
    return

for plot_info in p_list:
    h_list = []
    print('looking at histogram:', plot_info[0])
    for ifile,fil in enumerate(f_list):
        f = ROOT.TFile.Open(fil[0])
        h = f.Get(plot_info[0])
        h.SetDirectory(0)
        h_list.append(h)
        f.Close()
    make_plot(h_list, plot_info, legend_list)
