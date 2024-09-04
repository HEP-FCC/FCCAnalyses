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
import ROOT  # type: ignore

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


LOGGER = logging.getLogger('FCCAnalyses.plot')


# _____________________________________________________________________________
def removekey(d: dict, key: str) -> dict:
    '''
    Remove dictionary element.
    '''
    r = dict(d)
    del r[key]
    return r


def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]


def formatStatUncHist(hists, name, hstyle=3254):
    hist_tot = hists[0].Clone(name + "_unc")
    for h in hists[1:]:
        hist_tot.Add(h)
    hist_tot.SetFillColor(ROOT.kBlack)
    hist_tot.SetMarkerSize(0)
    hist_tot.SetLineWidth(0)
    hist_tot.SetFillStyle(hstyle)
    return hist_tot


# _____________________________________________________________________________
def mapHistos(var, label, sel, param, rebin):
    LOGGER.info('Run plots for var:%s     label:%s     selection:%s',
                var, label, sel)
    signal = param.plots[label]['signal']
    backgrounds = param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s] = []
        for f in signal[s]:
            fin = param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                LOGGER.info('File "%s" not found!\nSkipping it...', fin)
                continue

            with ROOT.TFile(fin, 'READ') as tf:
                h = tf.Get(var)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            scaleSig = 1.
            try:
                scaleSig = param.scaleSig
            except AttributeError:
                LOGGER.debug('No scale signal, using 1.')
                param.scaleSig = scaleSig
            LOGGER.info('ScaleSig: %g', scaleSig)
            hh.Scale(param.intLumi*scaleSig)
            hh.Rebin(rebin)

            if len(hsignal[s]) == 0:
                hsignal[s].append(hh)
            else:
                hh.Add(hsignal[s][0])
                hsignal[s][0] = hh

    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b] = []
        for f in backgrounds[b]:
            fin = param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                LOGGER.info('File "%s" not found!\nSkipping it...', fin)
                continue

            with ROOT.TFile(fin) as tf:
                h = tf.Get(var)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            hh.Scale(param.intLumi)
            hh.Rebin(rebin)
            if len(hbackgrounds[b]) == 0:
                hbackgrounds[b].append(hh)
            else:
                hh.Add(hbackgrounds[b][0])
                hbackgrounds[b][0] = hh

    for s in hsignal:
        if len(hsignal[s]) == 0:
            hsignal = removekey(hsignal, s)

    for b in hbackgrounds:
        if len(hbackgrounds[b]) == 0:
            hbackgrounds = removekey(hbackgrounds, b)

    if not hsignal:
        LOGGER.error('No signal input files found!\nAborting...')
        sys.exit(3)

    return hsignal, hbackgrounds


# _____________________________________________________________________________
def mapHistosFromHistmaker(hName, param, plotCfg):
    rebin = plotCfg['rebin'] if 'rebin' in plotCfg else 1
    LOGGER.info('Get histograms for %s', hName)
    signal = param.procs['signal']
    backgrounds = param.procs['backgrounds']
    scaleSig = plotCfg['scaleSig'] if 'scaleSig' in plotCfg else 1

    hsignal = {}
    for s in signal:
        hsignal[s] = []
        for f in signal[s]:
            fin = f"{param.inputDir}/{f}.root"
            if not os.path.isfile(fin):
                LOGGER.info('File "%s" not found!\nSkipping it...', fin)
                continue

            with ROOT.TFile(fin) as tf:
                h = tf.Get(hName)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            LOGGER.info('ScaleSig: %g', scaleSig)
            hh.Scale(param.intLumi*scaleSig)
            hh.Rebin(rebin)
            if len(hsignal[s]) == 0:
                hsignal[s].append(hh)
            else:
                hh.Add(hsignal[s][0])
                hsignal[s][0] = hh

    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b] = []
        for f in backgrounds[b]:
            fin = f"{param.inputDir}/{f}.root"
            if not os.path.isfile(fin):
                LOGGER.info('File "%s" not found!\nSkipping it...', fin)
                continue

            with ROOT.TFile(fin) as tf:
                h = tf.Get(hName)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            hh.Scale(param.intLumi)
            hh.Rebin(rebin)
            if len(hbackgrounds[b]) == 0:
                hbackgrounds[b].append(hh)
            else:
                hh.Add(hbackgrounds[b][0])
                hbackgrounds[b][0] = hh

    for s in hsignal:
        if len(hsignal[s]) == 0:
            hsignal = removekey(hsignal, s)

    for b in hbackgrounds:
        if len(hbackgrounds[b]) == 0:
            hbackgrounds = removekey(hbackgrounds, b)

    if not hsignal:
        LOGGER.error('No signal input files found!\nAborting...')
        sys.exit(3)

    return hsignal, hbackgrounds


# _____________________________________________________________________________
def runPlots(config: dict,
             args,
             var,
             sel,
             script_module,
             hsignal,
             hbackgrounds,
             extralab):

    # Below are settings for separate signal and background legends
    if config['split_leg']:
        legsize = 0.04 * (len(hsignal))
        legsize2 = 0.04 * (len(hbackgrounds))
        leg = ROOT.TLegend(0.15, 0.60 - legsize, 0.50, 0.62)
        leg2 = ROOT.TLegend(0.60, 0.60 - legsize2, 0.88, 0.62)

        if config['leg_position'][0] is not None and \
                config['leg_position'][2] is not None:
            leg.SetX1(config['leg_position'][0])
            leg.SetX2((config['leg_position'][0] +
                       config['leg_position'][2]) / 2)
            leg2.SetX2((config['leg_position'][0] +
                        config['leg_position'][2]) / 2)
            leg2.SetX2(config['leg_position'][0])
        if config['leg_position'][1] is not None:
            leg.SetY1(config['leg_position'][1])
            leg2.SetY1(config['leg_position'][1])
        if config['leg_position'][3] is not None:
            leg.SetY2(config['leg_position'][3])
            leg2.SetY2(config['leg_position'][3])

        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(10)
        leg2.SetTextSize(config['legend_text_size'])
        leg2.SetTextFont(42)
    else:
        legsize = 0.04 * (len(hbackgrounds) + len(hsignal))
        leg = ROOT.TLegend(0.68, 0.86 - legsize, 0.96, 0.88)
        leg2 = None

        if config['leg_position'][0] is not None:
            leg.SetX1(config['leg_position'][0])
        if config['leg_position'][1] is not None:
            leg.SetY1(config['leg_position'][1])
        if config['leg_position'][2] is not None:
            leg.SetX2(config['leg_position'][2])
        if config['leg_position'][3] is not None:
            leg.SetY2(config['leg_position'][3])

    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(config['legend_text_size'])
    leg.SetTextFont(42)

    for b in hbackgrounds:
        if config['split_leg']:
            leg2.AddEntry(hbackgrounds[b][0], script_module.legend[b], "f")
        else:
            leg.AddEntry(hbackgrounds[b][0], script_module.legend[b], "f")
    for s in hsignal:
        leg.AddEntry(hsignal[s][0], script_module.legend[s], "l")

    yields = {}
    for s in hsignal:
        yields[s] = [script_module.legend[s],
                     hsignal[s][0].Integral(0, -1),
                     hsignal[s][0].GetEntries()]
    for b in hbackgrounds:
        yields[b] = [script_module.legend[b],
                     hbackgrounds[b][0].Integral(0, -1),
                     hbackgrounds[b][0].GetEntries()]

    histos = []
    colors = []

    nsig = len(hsignal)
    nbkg = len(hbackgrounds)

    for sig in hsignal:
        histos.append(hsignal[sig][0])
        colors.append(script_module.colors[sig])

    for bkg in hbackgrounds:
        histos.append(hbackgrounds[bkg][0])
        colors.append(script_module.colors[bkg])

    intLumiab = script_module.intLumi/1e+06
    intLumi = f'L = {intLumiab:.0f} ab^{{-1}}'
    if hasattr(script_module, "intLumiLabel"):
        intLumi = getattr(script_module, "intLumiLabel")

    lt = 'FCCAnalyses: FCC-hh Simulation (Delphes)'
    rt = f'#sqrt{{s}} = {script_module.energy:.1f} TeV,   L = {intLumi}'

    if 'ee' in script_module.collider:
        lt = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
        rt = f'#sqrt{{s}} = {script_module.energy:.1f} GeV,   {intLumi}'

    customLabel = ""
    try:
        customLabel = script_module.customLabel
    except AttributeError:
        LOGGER.debug('No custom label, using nothing...')

    scaleSig = 1.
    try:
        scaleSig = script_module.scaleSig
    except AttributeError:
        LOGGER.debug('No scale signal, using 1.')
        script_module.scaleSig = scaleSig

    if 'AAAyields' in var:
        drawStack(var, 'events', leg, lt, rt, script_module.formats,
                  script_module.outdir + "/" + sel, False, True, histos,
                  colors, script_module.ana_tex, extralab, scaleSig,
                  customLabel, nsig, nbkg, leg2, yields,
                  config['plot_stat_unc'])
        return

    if 'stack' in script_module.stacksig:
        if 'lin' in script_module.yaxis:
            drawStack(var + "_stack_lin", 'events', leg, lt, rt,
                      script_module.formats, script_module.outdir + "/" + sel,
                      False, True, histos, colors, script_module.ana_tex,
                      extralab, scaleSig, customLabel, nsig, nbkg, leg2,
                      yields, config['plot_stat_unc'])
        if 'log' in script_module.yaxis:
            drawStack(var + "_stack_log", 'events', leg, lt, rt,
                      script_module.formats, script_module.outdir + "/" + sel,
                      True, True, histos, colors, script_module.ana_tex,
                      extralab, scaleSig, customLabel, nsig, nbkg, leg2,
                      yields, config['plot_stat_unc'])
        if 'lin' not in script_module.yaxis and \
                'log' not in script_module.yaxis:
            LOGGER.info('Unrecognized option in formats, should be '
                        '[\'lin\',\'log\']')

    if 'nostack' in script_module.stacksig:
        if 'lin' in script_module.yaxis:
            drawStack(var + "_nostack_lin", 'events', leg, lt, rt,
                      script_module.formats,
                      script_module.outdir + "/" + sel, False, False, histos,
                      colors, script_module.ana_tex, extralab, scaleSig,
                      customLabel, nsig, nbkg, leg2, yields,
                      config['plot_stat_unc'])
        if 'log' in script_module.yaxis:
            drawStack(var + "_nostack_log", 'events', leg, lt, rt,
                      script_module.formats, script_module.outdir + "/" + sel,
                      True, False, histos, colors, script_module.ana_tex,
                      extralab, scaleSig, customLabel, nsig, nbkg, leg2,
                      yields, config['plot_stat_unc'])
        if 'lin' not in script_module.yaxis and \
                'log' not in script_module.yaxis:
            LOGGER.info('Unrecognised option in formats, should be '
                        '[\'lin\',\'log\']')
    if 'stack' not in script_module.stacksig and \
            'nostack' not in script_module.stacksig:
        LOGGER.info('Unrecognized option in stacksig, should be '
                    '[\'stack\',\'nostack\']')


# _____________________________________________________________________________
def runPlotsHistmaker(args, hName, param, plotCfg):

    output = plotCfg['output']
    hsignal, hbackgrounds = mapHistosFromHistmaker(hName, param, plotCfg)

    if hasattr(param, "splitLeg"):
        splitLeg = param.splitLeg
    else:
        splitLeg = False

    if hasattr(param, "plotStatUnc"):
        plotStatUnc = param.plotStatUnc
    else:
        plotStatUnc = False

    # Below are settings for separate signal and background legends
    if splitLeg:
        legsize = 0.04 * (len(hsignal))
        legsize2 = 0.04 * (len(hbackgrounds))
        legCoord = [0.15, 0.60 - legsize, 0.50, 0.62]
        leg2 = ROOT.TLegend(0.60, 0.60 - legsize2, 0.88, 0.62)
        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(10)
        leg2.SetTextSize(args.legend_text_size)
        leg2.SetTextFont(42)
    else:
        legsize = 0.04*(len(hbackgrounds)+len(hsignal))
        legCoord = [0.68, 0.86-legsize, 0.96, 0.88]
        try:
            legCoord = param.legendCoord
        except AttributeError:
            LOGGER.debug('No legCoord, using default one...')
            legCoord = [0.68, 0.86-legsize, 0.96, 0.88]
        leg2 = None

    leg = ROOT.TLegend(
        args.legend_x_min if args.legend_x_min > 0 else legCoord[0],
        args.legend_y_min if args.legend_y_min > 0 else legCoord[1],
        args.legend_x_max if args.legend_x_max > 0 else legCoord[2],
        args.legend_y_max if args.legend_y_max > 0 else legCoord[3])
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(args.legend_text_size)
    leg.SetTextFont(42)

    for b in hbackgrounds:
        if splitLeg:
            leg2.AddEntry(hbackgrounds[b][0], param.legend[b], "f")
        else:
            leg.AddEntry(hbackgrounds[b][0], param.legend[b], "f")
    for s in hsignal:
        leg.AddEntry(hsignal[s][0], param.legend[s], "l")

    yields = {}
    for s in hsignal:
        yields[s] = [param.legend[s],
                     hsignal[s][0].Integral(0, -1),
                     hsignal[s][0].GetEntries()]
    for b in hbackgrounds:
        yields[b] = [param.legend[b],
                     hbackgrounds[b][0].Integral(0, -1),
                     hbackgrounds[b][0].GetEntries()]

    histos = []
    colors = []

    nsig = len(hsignal)
    nbkg = len(hbackgrounds)

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

    lt = 'FCCAnalyses: FCC-hh Simulation (Delphes)'
    rt = f'#sqrt{{s}} = {param.energy:.1f} TeV,   L = {intLumi}'

    if 'ee' in param.collider:
        lt = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
        rt = f'#sqrt{{s}} = {param.energy:.1f} GeV,   {intLumi}'

    customLabel = ""
    try:
        customLabel = param.customLabel
    except AttributeError:
        LOGGER.debug('No customLable, using nothing...')

    if stack:
        if logy:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir,
                      True, True, histos, colors, param.ana_tex, extralab,
                      scaleSig, customLabel, nsig, nbkg, leg2, yields,
                      plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                      xtitle=xtitle)
        else:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir,
                      False, True, histos, colors, param.ana_tex, extralab,
                      scaleSig, customLabel, nsig, nbkg, leg2, yields,
                      plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                      xtitle=xtitle)

    else:
        if logy:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir,
                      True, False, histos, colors, param.ana_tex, extralab,
                      scaleSig, customLabel, nsig, nbkg, leg2, yields,
                      plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                      xtitle=xtitle)
        else:
            drawStack(output, ytitle, leg, lt, rt, param.formats, param.outdir,
                      False, False, histos, colors, param.ana_tex, extralab,
                      scaleSig, customLabel, nsig, nbkg, leg2, yields,
                      plotStatUnc, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                      xtitle=xtitle)


# _____________________________________________________________________________
def drawStack(name, ylabel, legend, leftText, rightText, formats, directory,
              logY, stacksig, histos, colors, ana_tex, extralab, scaleSig,
              customLabel, nsig, nbkg, legend2=None, yields=None,
              plotStatUnc=False, xmin=-1, xmax=-1, ymin=-1, ymax=-1,
              xtitle=""):

    canvas = ROOT.TCanvas(name, name, 800, 800)
    canvas.SetLogy(logY)
    canvas.SetTicks(1, 1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)

    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)

    unit = 'GeV'
    if 'TeV' in str(histos[0].GetXaxis().GetTitle()):
        unit = 'TeV'

    if unit in str(histos[0].GetXaxis().GetTitle()):
        bwidth = sumhistos.GetBinWidth(1)
        if bwidth.is_integer():
            ylabel += f' / {bwidth} {unit}'
        else:
            ylabel += f' / {bwidth:.2f} {unit}'

    nbins = 1 if not isinstance(xtitle, list) else len(xtitle)
    h_dummy = ROOT.TH1D("h_dummy", "", nbins, 0, nbins)
    if nbins == 1:
        h_dummy.GetXaxis().SetTitle(
            histos[0].GetXaxis().GetTitle() if xtitle == "" else xtitle)
        h_dummy.GetYaxis().SetTitleOffset(1.95)
        h_dummy.GetXaxis().SetTitleOffset(
            1.2*h_dummy.GetXaxis().GetTitleOffset())
    else:  # for cutflow plots
        for i, label in enumerate(xtitle):
            h_dummy.GetXaxis().SetBinLabel(i+1, label)
        h_dummy.GetXaxis().LabelsOption("u")
        h_dummy.GetXaxis().SetLabelSize(1.1*h_dummy.GetXaxis().GetLabelSize())
        h_dummy.GetXaxis().SetLabelOffset(
            1.5*h_dummy.GetXaxis().GetLabelOffset())
    h_dummy.GetYaxis().SetTitle(ylabel)

    for h in iterh:
        sumhistos.Add(h)

    if logY:
        canvas.SetLogy(1)

    # define stacked histo
    hStack = ROOT.THStack("hstack", "")
    hStackBkg = ROOT.THStack("hstackbkg", "")
    hStackSig = ROOT.THStack("hstacksig", "")
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
    BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
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
            # sig+bkg uncertainty
            hUnc_sig_bkg = formatStatUncHist(hStack.GetHists(), "sig_bkg")
            hUnc_sig_bkg.Draw("E2 SAME")
    else:
        hStackBkg.Draw("HIST SAME")
        hStackSig.Draw("HIST SAME NOSTACK")
        if plotStatUnc:
            # bkg-only uncertainty
            hUnc_bkg = formatStatUncHist(hStackBkg.GetHists(), "bkg_only")
            hUnc_bkg.Draw("E2 SAME")
            for sHist in hStackSig.GetHists():
                # sigs uncertainty
                hUnc_sig = formatStatUncHist([sHist], "sig", 3245)
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
    def get_minmax_range(hists, xmin, xmax):
        hist_tot = hists[0].Clone(name + "_unc")
        for h in hists[1:]:
            hist_tot.Add(h)
        vals = []
        for i in range(0, hist_tot.GetNbinsX()+1):
            if hist_tot.GetBinLowEdge(i) > xmin or \
                    hist_tot.GetBinLowEdge(i+1) < xmax:
                if hist_tot.GetBinContent(i) != 0:
                    vals.append(hist_tot.GetBinContent(i))
        if len(vals) == 0:
            return 1e-5, 1
        return min(vals), max(vals)

    if stacksig:
        ymin_, ymax_ = get_minmax_range(hStack.GetHists(), xmin, xmax)
    else:
        ymin_sig, ymax_sig = get_minmax_range(hStackSig.GetHists(), xmin, xmax)
        ymin_bkg, ymax_bkg = get_minmax_range(hStackBkg.GetHists(), xmin, xmax)
        ymin_ = min(ymin_sig, ymin_bkg)
        ymax_ = max(ymax_sig, ymax_bkg)
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
    if legend2 is not None:
        legend2.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(31)
    latex.SetTextSize(0.04)

    text = '#it{' + leftText + '}'
    latex.DrawLatex(0.90, 0.94, text)

    text = '#it{'+customLabel+'}'
    latex.SetTextAlign(12)
    latex.SetNDC(ROOT.kTRUE)
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.18, 0.85, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] + '}}'

    latex.SetTextAlign(12)
    latex.SetNDC(ROOT.kTRUE)
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.18, 0.81, text)

    rightText[1] = rightText[1].replace("   ", "")
    text = '#bf{#it{' + rightText[1] + '}}'
    latex.SetTextSize(0.035)
    latex.DrawLatex(0.18, 0.76, text)

    text = '#bf{#it{' + ana_tex + '}}'
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.18, 0.71, text)

    text = '#bf{#it{' + extralab + '}}'
    latex.SetTextSize(0.025)
    latex.DrawLatex(0.18, 0.66, text)

    text = '#bf{#it{' + 'Signal scale=' + str(scaleSig)+'}}'
    latex.SetTextSize(0.025)
    if scaleSig != 1:
        latex.DrawLatex(0.18, 0.63, text)

    canvas.RedrawAxis()
    canvas.GetFrame().SetBorderSize(12)
    canvas.Modified()
    canvas.Update()

    if 'AAAyields' in name:
        dummyh = ROOT.TH1F("", "", 1, 0, 1)
        dummyh.SetStats(0)
        dummyh.GetXaxis().SetLabelOffset(999)
        dummyh.GetXaxis().SetLabelSize(0)
        dummyh.GetYaxis().SetLabelOffset(999)
        dummyh.GetYaxis().SetLabelSize(0)
        dummyh.Draw("AH")
        legend.Draw()

        latex.SetNDC()
        latex.SetTextAlign(31)
        latex.SetTextSize(0.04)

        text = '#it{' + leftText + '}'
        latex.DrawLatex(0.90, 0.92, text)

        text = '#bf{#it{' + rightText[0] + '}}'
        latex.SetTextAlign(12)
        latex.SetNDC(ROOT.kTRUE)
        latex.SetTextSize(0.04)
        latex.DrawLatex(0.18, 0.83, text)

        text = '#bf{#it{' + rightText[1] + '}}'
        latex.SetTextSize(0.035)
        latex.DrawLatex(0.18, 0.78, text)

        text = '#bf{#it{' + ana_tex + '}}'
        latex.SetTextSize(0.04)
        latex.DrawLatex(0.18, 0.73, text)

        text = '#bf{#it{' + extralab + '}}'
        latex.SetTextSize(0.025)
        latex.DrawLatex(0.18, 0.68, text)

        text = '#bf{#it{' + 'Signal scale=' + str(scaleSig) + '}}'
        latex.SetTextSize(0.04)
        latex.DrawLatex(0.18, 0.55, text)

        dy = 0
        text = '#bf{#it{' + 'Process' + '}}'
        latex.SetTextSize(0.035)
        latex.DrawLatex(0.18, 0.45, text)

        text = '#bf{#it{' + 'Yields' + '}}'
        latex.SetTextSize(0.035)
        latex.DrawLatex(0.5, 0.45, text)

        text = '#bf{#it{' + 'Raw MC' + '}}'
        latex.SetTextSize(0.035)
        latex.DrawLatex(0.75, 0.45, text)

        for y in yields:
            text = '#bf{#it{' + yields[y][0] + '}}'
            latex.SetTextSize(0.035)
            latex.DrawLatex(0.18, 0.4-dy*0.05, text)

            stry = str(yields[y][1])
            stry = stry.split('.', maxsplit=1)[0]
            text = '#bf{#it{' + stry + '}}'
            latex.SetTextSize(0.035)
            latex.DrawLatex(0.5, 0.4-dy*0.05, text)

            stry = str(yields[y][2])
            stry = stry.split('.', maxsplit=1)[0]
            text = '#bf{#it{' + stry + '}}'
            latex.SetTextSize(0.035)
            latex.DrawLatex(0.75, 0.4-dy*0.05, text)

            dy += 1
        # canvas.Modified()
        # canvas.Update()

    print_canvas(canvas, name, formats, directory)


# _____________________________________________________________________________
def print_canvas(canvas, name, formats, directory):
    '''
    Saving canvas in multiple formats.
    '''

    if not formats:
        LOGGER.error('No output formats specified!\nAborting...')
        sys.exit(3)

    if not os.path.exists(directory):
        os.system("mkdir -p " + directory)

    for f in formats:
        out_file = os.path.join(directory, name) + "." + f
        canvas.SaveAs(out_file)


# _____________________________________________________________________________
def run(args):
    '''
    Run over all the plots.
    '''
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    module_path = os.path.abspath(args.script_path)
    module_dir = os.path.dirname(module_path)
    base_name = os.path.splitext(ntpath.basename(args.script_path))[0]

    # Load plot script as module
    sys.path.insert(0, module_dir)
    script_module = importlib.import_module(base_name)

    # Merge script and command line arguments into one configuration object
    config = {}

    config['split_leg'] = False
    if hasattr(script_module, 'splitLeg'):
        config['split_leg'] = script_module.splitLeg

    config['leg_position'] = [None, None, None, None]
    if hasattr(script_module, 'legendCoord'):
        config['leg_position'] = script_module.legendCoord
    if args.legend_x_min is not None:
        config['leg_position'][0] = args.legend_x_min
    if args.legend_y_min is not None:
        config['leg_position'][1] = args.legend_y_min
    if args.legend_x_max is not None:
        config['leg_position'][2] = args.legend_x_max
    if args.legend_y_max is not None:
        config['leg_position'][3] = args.legend_y_max

    config['plot_stat_unc'] = False
    if hasattr(script_module, 'plotStatUnc'):
        config['plot_stat_unc'] = script_module.plotStatUnc

    config['legend_text_size'] = 0.035
    if hasattr(script_module, 'legendTextSize'):
        config['legend_text_size'] = script_module.legendTextSize
    if args.legend_text_size is not None:
        config['legend_text_size'] = args.legend_text_size

    # Handle plots for Histmaker analyses and exit
    if hasattr(script_module, 'hists'):
        for hist_name, plot_cfg in script_module.hists.items():
            runPlotsHistmaker(args, hist_name, script_module, plot_cfg)
        sys.exit()

    counter = 0
    for var_index, var in enumerate(script_module.variables):
        for label, sels in script_module.selections.items():
            for sel in sels:
                rebin_tmp = 1
                if hasattr(script_module, "rebin"):
                    if len(script_module.rebin) == \
                            len(script_module.variables):
                        rebin_tmp = script_module.rebin[var_index]
                hsignal, hbackgrounds = mapHistos(var,
                                                  label,
                                                  sel,
                                                  script_module,
                                                  rebin=rebin_tmp)
                runPlots(config,
                         args,
                         var + "_" + label,
                         sel,
                         script_module,
                         hsignal,
                         hbackgrounds,
                         script_module.extralabel[sel])
                if counter == 0:
                    runPlots(config,
                             args,
                             "AAAyields_"+label,
                             sel,
                             script_module,
                             hsignal,
                             hbackgrounds,
                             script_module.extralabel[sel])
        counter += 1


def do_plots(parser):
    '''
    Run plots generation
    '''

    args, _ = parser.parse_known_args()

    if args.command != 'plots':
        LOGGER.error('Wrong sub-command!\nAborting...')

    if not os.path.isfile(args.script_path):
        LOGGER.error('Plots script "%s" not found!\nAborting...',
                     args.script_path)
        sys.exit(3)

    run(args)
