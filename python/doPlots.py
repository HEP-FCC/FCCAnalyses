#!/usr/bin/env python
'''
Create plots out of the histograms produced in previous stages
'''
import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


LOGGER = logging.getLogger('FCCAnalyses.plot')

# __________________________________________________________
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def sortedDictValues(dic):
    keys = sorted(dic)
    return [dic[key] for key in keys]

def formatStatUncHist(hists, name, hstyle=3254):
    hTot = hists[0].Clone(name + "_unc")
    for h in hists[1:]:
        hTot.Add(h)
    hTot.SetFillColor(ROOT.kBlack)
    hTot.SetMarkerSize(0)
    hTot.SetLineWidth(0)
    hTot.SetFillStyle(hstyle)    
    return hTot

#__________________________________________________________
def mapHistos(var, label, sel, param, rebin):
    LOGGER.info('Run plots for var:%s     label:%s     selection:%s',
                var, label, sel)
    signal=param.plots[label]['signal']
    backgrounds=param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                LOGGER.info('File %s does not exist!\nSkipping it...', fin)
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                scaleSig=1.
                try:
                    scaleSig=param.scaleSig
                except AttributeError:
                    LOGGER.info('No scale signal, using 1.')
                    param.scaleSig=scaleSig
                LOGGER.info('ScaleSig: %g', scaleSig)
                hh.Scale(param.intLumi*scaleSig)
                hh.Rebin(rebin)

                if len(hsignal[s])==0:
                    hsignal[s].append(hh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=hh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                LOGGER.info('File %s does not exist!\nSkipping it...', fin)
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                hh.Scale(param.intLumi)
                hh.Rebin(rebin)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(hh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=hh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds


#__________________________________________________________
def mapHistosFromHistmaker(hName, param, plotCfg):
    rebin = plotCfg['rebin'] if 'rebin' in plotCfg else 1
    LOGGER('Get histograms for %s', hName)
    signal=param.procs['signal']
    backgrounds=param.procs['backgrounds']
    scaleSig = plotCfg['scaleSig'] if 'scaleSig' in plotCfg else 1

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=f"{param.inputDir}/{f}.root"
            if not os.path.isfile(fin):
                LOGGER.info('File %s does not exist!\nSkipping it...', fin)
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(hName)
                hh = copy.deepcopy(h)
                LOGGER.info('ScaleSig: ', scaleSig)
                hh.Scale(param.intLumi*scaleSig)
                hh.Rebin(rebin)
                if len(hsignal[s])==0:
                    hsignal[s].append(hh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=hh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=f"{param.inputDir}/{f}.root"
            if not os.path.isfile(fin):
                LOGGER.info('File %s does not exist!\nSkipping it...', fin)
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(hName)
                hh = copy.deepcopy(h)
                hh.Scale(param.intLumi)
                hh.Rebin(rebin)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(hh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=hh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds

#__________________________________________________________
def runPlots(var,sel,param,hsignal,hbackgrounds,extralab,splitLeg,plotStatUnc):

    ###Below are settings for separate signal and background legends
    if(splitLeg):
        legsize = 0.04*(len(hsignal))
        legsize2 = 0.04*(len(hbackgrounds))
        legCoord = [0.15,0.60 - legsize,0.50,0.62]
        leg2 = ROOT.TLegend(0.60,0.60 - legsize2,0.88,0.62)
        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(10)
        leg2.SetTextSize(0.035)
        leg2.SetTextFont(42)
    else:
        legsize = 0.04*(len(hbackgrounds)+len(hsignal))
        legCoord=[0.68, 0.86-legsize, 0.96, 0.88]
        try:
            legCoord=param.legendCoord
        except AttributeError:
            LOGGER.info('No legCoord, using default one...')
            legCoord=[0.68, 0.86-legsize, 0.96, 0.88]
        leg2 = None

    leg = ROOT.TLegend(legCoord[0],legCoord[1],legCoord[2],legCoord[3])
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for b in hbackgrounds:
        if(splitLeg):
            leg2.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
        else:
            leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
    for s in hsignal:
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")


    yields={}
    for s in hsignal:
        yields[s]=[param.legend[s],hsignal[s][0].Integral(0,-1), hsignal[s][0].GetEntries()]
    for b in hbackgrounds:
        yields[b]=[param.legend[b],hbackgrounds[b][0].Integral(0,-1), hbackgrounds[b][0].GetEntries()]

    histos=[]
    colors=[]

    nsig=len(hsignal)
    nbkg=len(hbackgrounds)

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    intLumiab = param.intLumi/1e+06
    intLumi = f'L = {intLumiab:.0f} ab^{{-1}}'
    if hasattr(param, "intLumiLabel"):
        intLumi = getattr(param, "intLumiLabel")

    lt = "FCCAnalyses: FCC-hh Simulation (Delphes)"
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {}".format(param.energy,intLumi)

    if 'ee' in param.collider:
        lt = "FCCAnalyses: FCC-ee Simulation (Delphes)"
        rt = "#sqrt{{s}} = {:.1f} GeV,   {}".format(param.energy,intLumi)

    

    customLabel=""
    try:
        customLabel=param.customLabel
    except AttributeError:
        LOGGER.info('No customLable, using nothing...')

    scaleSig=1.
    try:
        scaleSig=param.scaleSig
    except AttributeError:
        LOGGER('No scale signal, using 1.')
        param.scaleSig=scaleSig

    if 'AAAyields' in var:
        drawStack(var, 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, False , True , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc)
        return

    if 'stack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_stack_lin", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, False , True , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc)
        if 'log' in param.yaxis:
            drawStack(var+"_stack_log", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, True , True , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            LOGGER.info('Unrecognised option in formats, should be '
                        '[\'lin\',\'log\']')

    if 'nostack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_nostack_lin", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, False , False , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc)
        if 'log' in param.yaxis:
            drawStack(var+"_nostack_log", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, True , False , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            LOGGER.info('Unrecognised option in formats, should be '
                        '[\'lin\',\'log\']')
    if 'stack' not in param.stacksig and 'nostack' not in param.stacksig:
        LOGGER.info('Unrecognised option in stacksig, should be '
                    '[\'stack\',\'nostack\']')

#__________________________________________________________
def runPlotsHistmaker(hName, param, plotCfg):

    output = plotCfg['output']
    hsignal,hbackgrounds=mapHistosFromHistmaker(hName, param, plotCfg)

    if hasattr(param, "splitLeg"):
        splitLeg = param.splitLeg
    else:
        splitLeg = False

    if hasattr(param, "plotStatUnc"):
        plotStatUnc = param.plotStatUnc
    else:
        plotStatUnc = False

    ###Below are settings for separate signal and background legends
    if(splitLeg):
        legsize = 0.04*(len(hsignal))
        legsize2 = 0.04*(len(hbackgrounds))
        legCoord = [0.15,0.60 - legsize,0.50,0.62]
        leg2 = ROOT.TLegend(0.60,0.60 - legsize2,0.88,0.62)
        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(10)
        leg2.SetTextSize(0.035)
        leg2.SetTextFont(42)
    else:
        legsize = 0.04*(len(hbackgrounds)+len(hsignal))
        legCoord=[0.68, 0.86-legsize, 0.96, 0.88]
        try:
            legCoord=param.legendCoord
        except AttributeError:
            LOGGER.info('No legCoord, using default one...')
            legCoord=[0.68, 0.86-legsize, 0.96, 0.88]
        leg2 = None

    leg = ROOT.TLegend(legCoord[0],legCoord[1],legCoord[2],legCoord[3])
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for b in hbackgrounds:
        if(splitLeg):
            leg2.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
        else:
            leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
    for s in hsignal:
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")


    yields={}
    for s in hsignal:
        yields[s]=[param.legend[s],hsignal[s][0].Integral(0,-1), hsignal[s][0].GetEntries()]
    for b in hbackgrounds:
        yields[b]=[param.legend[b],hbackgrounds[b][0].Integral(0,-1), hbackgrounds[b][0].GetEntries()]

    histos=[]
    colors=[]

    nsig=len(hsignal)
    nbkg=len(hbackgrounds)

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    xtitle = plotCfg['xtitle'] if 'xtitle' in plotCfg else ""
    ytitle = plotCfg['ytitle'] if 'ytitle' in plotCfg else "Events"
    xmin = plotCfg['xmin'] if 'xmin' in plotCfg else -1
    xmax = plotCfg['xmax'] if 'xmax' in plotCfg else -1
    ymin = plotCfg['ymin'] if 'ymin' in plotCfg else -1
    ymax = plotCfg['ymax'] if 'ymax' in plotCfg else -1
    stack = plotCfg['stack'] if 'stack' in plotCfg else False
    logy = plotCfg['logy'] if 'logy' in plotCfg else False
    extralab = plotCfg['extralab'] if 'extralab' in plotCfg else ""
    scaleSig = plotCfg['scaleSig'] if 'scaleSig' in plotCfg else 1


    intLumiab = param.intLumi/1e+06
    intLumi = f'L = {intLumiab:.0f} ab^{{-1}}'
    if hasattr(param, "intLumiLabel"):
        intLumi = getattr(param, "intLumiLabel")

    lt = "FCCAnalyses: FCC-hh Simulation (Delphes)"
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {}".format(param.energy,intLumi)

    if 'ee' in param.collider:
        lt = "FCCAnalyses: FCC-ee Simulation (Delphes)"
        rt = "#sqrt{{s}} = {:.1f} GeV,   {}".format(param.energy,intLumi)

    customLabel=""
    try:
        customLabel=param.customLabel
    except AttributeError:
        LOGGER.info('No customLable, using nothing...')



    if stack:
        if logy:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir, True , True , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, xtitle=xtitle)
        else:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir, False , True , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, xtitle=xtitle)

    else:
        if logy:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir, True , False , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, xtitle=xtitle)
        else:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir, False , False , histos, colors, param.ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, leg2, yields, plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, xtitle=xtitle)




#_____________________________________________________________________________________________________________
def drawStack(name, ylabel, legend, leftText, rightText, formats, directory, logY, stacksig, histos, colors, ana_tex, extralab, scaleSig, customLabel, nsig, nbkg, legend2=None, yields=None, plotStatUnc=False, xmin=-1, xmax=-1, ymin=-1, ymax=-1, xtitle="", ytitle=""):

    canvas = ROOT.TCanvas(name, name, 800, 800)
    canvas.SetLogy(logY)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)

    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)

    unit = 'GeV'
    if 'TeV' in str(histos[0].GetXaxis().GetTitle()):
        unit = 'TeV'

    if unit in str(histos[0].GetXaxis().GetTitle()):
        bwidth=sumhistos.GetBinWidth(1)
        if bwidth.is_integer():
            ylabel+=' / {} {}'.format(int(bwidth), unit)
        else:
            ylabel+=' / {:.2f} {}'.format(bwidth, unit)


    nbins = 1 if not isinstance(xtitle, list) else len(xtitle)
    h_dummy = ROOT.TH1D("h_dummy", "", nbins, 0, nbins)
    if nbins == 1:
        h_dummy.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle() if xtitle == "" else xtitle)
        h_dummy.GetYaxis().SetTitleOffset(1.95)
        h_dummy.GetXaxis().SetTitleOffset(1.2*h_dummy.GetXaxis().GetTitleOffset())
    else: # for cutflow plots
        for i,label in enumerate(xtitle): h_dummy.GetXaxis().SetBinLabel(i+1, label)
        h_dummy.GetXaxis().LabelsOption("u")
        h_dummy.GetXaxis().SetLabelSize(1.1*h_dummy.GetXaxis().GetLabelSize())
        h_dummy.GetXaxis().SetLabelOffset(1.5*h_dummy.GetXaxis().GetLabelOffset())
    h_dummy.GetYaxis().SetTitle(ylabel)


    for h in iterh:
      sumhistos.Add(h)

    maxh = sumhistos.GetMaximum()
    minh = sumhistos.GetMinimum()

    if logY:
       canvas.SetLogy(1)

    # define stacked histo 
    hStack = ROOT.THStack("hstack", "")
    hStackBkg = ROOT.THStack("hstackbkg", "")
    hStackSig = ROOT.THStack("hstacksig","")
    BgMCHistYieldsDic = {}

    # first plot backgrounds (sorted by the yields)
    for i in range(nsig, nsig+nbkg):
        h = histos[i]
        h.SetLineWidth(1)
        h.SetLineColor(ROOT.kBlack)
        h.SetFillColor(colors[i])
        if h.Integral() > 0:
            BgMCHistYieldsDic[h.Integral()] = h
        else:
            BgMCHistYieldsDic[-1*nbkg] = h
    # sort stack by yields (smallest to largest)
    BgMCHistYieldsDic = sortedDictValues(BgMCHistYieldsDic)
    for h in BgMCHistYieldsDic:
        hStack.Add(h)
        hStackBkg.Add(h)

    # add the signal histograms
    for i in range(nsig):
        h = histos[i]
        h.SetLineWidth(3)
        h.SetLineColor(colors[i])
        hStack.Add(h)
        hStackSig.Add(h)


    if xmin != -1 and xmax != -1:
        h_dummy.GetXaxis().SetLimits(xmin, xmax)

    h_dummy.Draw("HIST")
    if stacksig:
        hStack.Draw("HIST SAME")
        if plotStatUnc:
            hUnc_sig_bkg = formatStatUncHist(hStack.GetHists(), "sig_bkg") # sig+bkg uncertainty
            hUnc_sig_bkg.Draw("E2 SAME")
    else:
        hStackBkg.Draw("HIST SAME")
        hStackSig.Draw("HIST SAME NOSTACK")
        if plotStatUnc:
            hUnc_bkg = formatStatUncHist(hStackBkg.GetHists(), "bkg_only") # bkg-only uncertainty
            hUnc_bkg.Draw("E2 SAME")
            for sHist in hStackSig.GetHists():
                hUnc_sig = formatStatUncHist([sHist], "sig", 3245) # sigs uncertainty
                hUnc_sig.Draw("E2 SAME")

    # x limits
    if xmin == -1:
        h_tmp = hStack.GetStack().Last()
        xmin = h_tmp.GetBinLowEdge(1)
    if xmax == -1:
        h_tmp = hStack.GetStack().Last()
        xmax = h_tmp.GetBinLowEdge(h_tmp.GetNbinsX()+1)
    h_dummy.GetXaxis().SetLimits(xmin, xmax)

    # y limits
    def getMinMaxRange(hists, xmin, xmax):
        hTot = hists[0].Clone(name + "_unc")
        for h in hists[1:]: hTot.Add(h)
        vals = []
        for i in range(0, hTot.GetNbinsX()+1):
            if hTot.GetBinLowEdge(i) > xmin or hTot.GetBinLowEdge(i+1) < xmax:
                if hTot.GetBinContent(i) != 0:
                    vals.append(hTot.GetBinContent(i))
        if len(vals) == 0:
            return 1e-5, 1
        return min(vals), max(vals)

    if stacksig:
        ymin_, ymax_ = getMinMaxRange(hStack.GetHists(), xmin, xmax)
    else:
        yminSig, ymaxSig = getMinMaxRange(hStackSig.GetHists(), xmin, xmax)
        yminBkg, ymaxBkg = getMinMaxRange(hStackBkg.GetHists(), xmin, xmax)
        ymin_ = min(yminSig, yminBkg)
        ymax_ = max(ymaxSig, ymaxBkg)
    if ymin == -1:
        ymin = ymin_*0.1 if logY else 0
    if ymax == -1:
        ymax = ymax_*1000. if logY else 1.4*ymax_
    if ymin <= 0 and logY:
        LOGGER.error('Log scale can\'t start at: %i', ymin)
        sys.exit(3)
    h_dummy.SetMaximum(ymax)
    h_dummy.SetMinimum(ymin)

    legend.Draw()
    if legend2 != None:
        legend2.Draw()

    Text = ROOT.TLatex()
    Text.SetNDC()
    Text.SetTextAlign(31);
    Text.SetTextSize(0.04)

    text = '#it{' + leftText +'}'
    Text.DrawLatex(0.90, 0.94, text)

    text = '#it{'+customLabel+'}'
    Text.SetTextAlign(12);
    Text.SetNDC(ROOT.kTRUE)
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.85, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] +'}}'

    Text.SetTextAlign(12);
    Text.SetNDC(ROOT.kTRUE)
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.81, text)

    rightText[1]=rightText[1].replace("   ","")
    text = '#bf{#it{' + rightText[1] +'}}'
    Text.SetTextSize(0.035)
    Text.DrawLatex(0.18, 0.76, text)

    text = '#bf{#it{' + ana_tex +'}}'
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.71, text)

    text = '#bf{#it{' + extralab +'}}'
    Text.SetTextSize(0.025)
    Text.DrawLatex(0.18, 0.66, text)

    text = '#bf{#it{' + 'Signal scale=' + str(scaleSig)+'}}'
    Text.SetTextSize(0.025)
    if scaleSig!=1:Text.DrawLatex(0.18, 0.63, text)

    canvas.RedrawAxis()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    if 'AAAyields' in name:
        dummyh=ROOT.TH1F("","",1,0,1)
        dummyh.SetStats(0)
        dummyh.GetXaxis().SetLabelOffset(999)
        dummyh.GetXaxis().SetLabelSize(0)
        dummyh.GetYaxis().SetLabelOffset(999)
        dummyh.GetYaxis().SetLabelSize(0)
        dummyh.Draw("AH")
        legend.Draw()

        Text.SetNDC()
        Text.SetTextAlign(31);
        Text.SetTextSize(0.04)

        text = '#it{' + leftText +'}'
        Text.DrawLatex(0.90, 0.92, text)

        text = '#bf{#it{' + rightText[0] +'}}'
        Text.SetTextAlign(12);
        Text.SetNDC(ROOT.kTRUE)
        Text.SetTextSize(0.04)
        Text.DrawLatex(0.18, 0.83, text)

        text = '#bf{#it{' + rightText[1] +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.18, 0.78, text)

        text = '#bf{#it{' + ana_tex +'}}'
        Text.SetTextSize(0.04)
        Text.DrawLatex(0.18, 0.73, text)

        text = '#bf{#it{' + extralab +'}}'
        Text.SetTextSize(0.025)
        Text.DrawLatex(0.18, 0.68, text)

        text = '#bf{#it{' + 'Signal scale=' + str(scaleSig)+'}}'
        Text.SetTextSize(0.04)
        Text.DrawLatex(0.18, 0.55, text)

        dy=0
        text = '#bf{#it{' + 'Process' +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.18, 0.45, text)

        text = '#bf{#it{' + 'Yields' +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.5, 0.45, text)

        text = '#bf{#it{' + 'Raw MC' +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.75, 0.45, text)

        for y in yields:
            text = '#bf{#it{' + yields[y][0] +'}}'
            Text.SetTextSize(0.035)
            Text.DrawLatex(0.18, 0.4-dy*0.05, text)

            stry=str(yields[y][1])
            stry=stry.split('.')[0]
            text = '#bf{#it{' + stry +'}}'
            Text.SetTextSize(0.035)
            Text.DrawLatex(0.5, 0.4-dy*0.05, text)

            stry=str(yields[y][2])
            stry=stry.split('.')[0]
            text = '#bf{#it{' + stry +'}}'
            Text.SetTextSize(0.035)
            Text.DrawLatex(0.75, 0.4-dy*0.05, text)


            dy+=1
        #canvas.Modified()
        #canvas.Update()


    printCanvas(canvas, name, formats, directory)




#____________________________________________________
def printCanvas(canvas, name, formats, directory):

    if format != "":
        if not os.path.exists(directory) :
                os.system("mkdir -p "+directory)
        for f in formats:
            outFile = os.path.join(directory, name) + "." + f
            canvas.SaveAs(outFile)



#__________________________________________________________
def run(paramFile):
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    module_path = os.path.abspath(paramFile)
    module_dir = os.path.dirname(module_path)
    base_name = os.path.splitext(ntpath.basename(paramFile))[0]

    sys.path.insert(0, module_dir)
    param = importlib.import_module(base_name)

    if hasattr(param, "splitLeg"):
        splitLeg = param.splitLeg
    else:
        splitLeg = False
        
    if hasattr(param, "plotStatUnc"):
        plotStatUnc = param.plotStatUnc
    else:
        plotStatUnc = False

    if hasattr(param, "hists"):
        for hName,plotCfg in param.hists.items():
            runPlotsHistmaker(hName, param, plotCfg)
        quit()

    counter=0
    for iVar,var in enumerate(param.variables):
        for label, sels in param.selections.items():
            for sel in sels:
                hsignal,hbackgrounds=mapHistos(var,label,sel, param, rebin=param.rebin[iVar] if hasattr(param, "rebin") and len(param.rebin) == len(param.variables) else 1)
                runPlots(var+"_"+label,sel,param,hsignal,hbackgrounds,param.extralabel[sel],splitLeg,plotStatUnc)
                if counter==0: runPlots("AAAyields_"+label,sel,param,hsignal,hbackgrounds,param.extralabel[sel],splitLeg,plotStatUnc)
        counter+=1
