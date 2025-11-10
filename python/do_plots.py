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
from typing import Any

import ROOT  # type: ignore

from utils import random_string

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
def get_minmax_range(histos: list[Any],
                     xmin: float,
                     xmax: float):
    '''
    Find min and max values for the y-axis among the provided histograms in a
    specified x-axis range.
    '''
    if len(histos) == 0:
        LOGGER.warning('Histograms not provided!')
        return 1e-5, 1

    hist_name = 'hist_tot_' + random_string(12)
    hist_tot = histos[0].Clone(hist_name)
    for hist in histos[1:]:
        hist_tot.Add(hist)

    vals = []
    for i in range(0, hist_tot.GetNbinsX()+1):
        if hist_tot.GetBinLowEdge(i) > xmin or \
                hist_tot.GetBinLowEdge(i+1) < xmax:
            if hist_tot.GetBinContent(i) != 0:
                vals.append(hist_tot.GetBinContent(i))
    if len(vals) == 0:
        return 1e-5, 1

    return min(vals), max(vals)


# _____________________________________________________________________________
def determine_lumi_scaling(config: dict[str, Any],
                           infile: ROOT.TFile,
                           initial_scale: float = 1.0) -> float:
    '''
    Determine whether to (re)scale histograms in the file to luminosity.
    '''
    scale: float = initial_scale

    # Check if histograms were already scaled to lumi
    try:
        scaled: bool = infile.scaled.GetVal()
    except AttributeError:
        LOGGER.error('Input file does not contain scaling '
                     'information!\n  %s\nAborting...', infile.GetName())
        sys.exit(3)

    if scaled:
        try:
            int_lumi_in_file: float = infile.intLumi.GetVal()
        except AttributeError:
            LOGGER.error('Can not load integrated luminosity '
                         'value from the input file!\n  %s\n'
                         'Aborting...', infile.GetName())

        if config['int-lumi'] != int_lumi_in_file:
            LOGGER.warning(
                'Histograms are already scaled to different '
                'luminosity value!\n'
                'Luminosity in the input file is %s pb-1 and '
                'luminosity requested in plots script is %s pb-1.',
                int_lumi_in_file, config['int-lumi'])
            if config['do-scale']:
                LOGGER.warning(
                    'Rescaling from %s pb-1 to %s pb-1...',
                    int_lumi_in_file, config['int-lumi'])
                scale *= config['int-lumi'] / int_lumi_in_file

    else:
        if config['do-scale']:
            scale = scale * config['int-lumi']

    return scale


# _____________________________________________________________________________
def load_hists(var: str,
               label: str,
               sel: str,
               config: dict[str, Any],
               rebin: int) -> tuple[dict[str, Any], dict[str, Any]]:
    '''
    Load all histograms needed for the plot
    '''

    try:
        signal = config['plots'][label]['signal']
    except KeyError:
        signal = {}

    try:
        backgrounds = config['plots'][label]['backgrounds']
    except KeyError:
        backgrounds = {}

    hsignal: dict[str, Any] = {}
    for s in signal:
        hsignal[s] = []
        for filepathstem in signal[s]:
            infilepath = config['input-dir'] + filepathstem + '_' + sel + \
                         '_histo.root'
            if not os.path.isfile(infilepath):
                LOGGER.info('File "%s" not found!\nSkipping it...', infilepath)
                continue

            with ROOT.TFile(infilepath, 'READ') as infile:
                hist = copy.deepcopy(infile.Get(var))
                hist.SetDirectory(0)

                scale = determine_lumi_scaling(config,
                                               infile,
                                               config['scale-sig'])
            hist.Scale(scale)
            hist.Rebin(rebin)

            if len(hsignal[s]) == 0:
                hsignal[s].append(hist)
            else:
                hist.Add(hsignal[s][0])
                hsignal[s][0] = hist

    hbackgrounds: dict[str, Any] = {}
    for b in backgrounds:
        hbackgrounds[b] = []
        for filepathstem in backgrounds[b]:
            infilepath = config['input-dir'] + filepathstem + '_' + sel + \
                         '_histo.root'
            if not os.path.isfile(infilepath):
                LOGGER.info('File "%s" not found!\nSkipping it...', infilepath)
                continue

            with ROOT.TFile(infilepath) as infile:
                hist = copy.deepcopy(infile.Get(var))
                hist.SetDirectory(0)

                scale = determine_lumi_scaling(config,
                                               infile,
                                               config['scale-bkg'])
            hist.Scale(scale)
            hist.Rebin(rebin)

            if len(hbackgrounds[b]) == 0:
                hbackgrounds[b].append(hist)
            else:
                hist.Add(hbackgrounds[b][0])
                hbackgrounds[b][0] = hist

    for s in hsignal:
        if len(hsignal[s]) == 0:
            hsignal = removekey(hsignal, s)

    for b in hbackgrounds:
        if len(hbackgrounds[b]) == 0:
            hbackgrounds = removekey(hbackgrounds, b)

    return hsignal, hbackgrounds


# _____________________________________________________________________________
def mapHistosFromHistmaker(config: dict[str, Any],
                           hist_name: str,
                           param,
                           hist_cfg):
    rebin = hist_cfg['rebin'] if 'rebin' in hist_cfg else 1
    LOGGER.info('Get histograms for %s', hist_name)
    signal = param.procs['signal']
    backgrounds = param.procs['backgrounds']
    scaleSig = hist_cfg['scaleSig'] if 'scaleSig' in hist_cfg else 1

    hsignal: dict[str, Any] = {}
    for s in signal:
        hsignal[s] = []
        for f in signal[s]:
            fin = f"{param.inputDir}/{f}.root"
            if not os.path.isfile(fin):
                LOGGER.info('File "%s" not found!\nSkipping it...', fin)
                continue

            with ROOT.TFile(fin) as tf:
                h = tf.Get(hist_name)
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

    hbackgrounds: dict[str, Any] = {}
    for b in backgrounds:
        hbackgrounds[b] = []
        for f in backgrounds[b]:
            fin = f"{param.inputDir}/{f}.root"
            if not os.path.isfile(fin):
                LOGGER.info('File "%s" not found!\nSkipping it...', fin)
                continue

            with ROOT.TFile(fin) as tf:
                h = tf.Get(hist_name)
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
def runPlots(config: dict[str, Any],
             args,
             var,
             sel,
             script_module,
             hsignal,
             hbackgrounds,
             extralab):

    # Below are settings for separate signal and background legends
    if config['split-leg']:
        legsize = 0.04 * (len(hsignal))
        legsize2 = 0.04 * (len(hbackgrounds))
        leg = ROOT.TLegend(0.15, 0.60 - legsize, 0.50, 0.62)
        leg2 = ROOT.TLegend(0.60, 0.60 - legsize2, 0.88, 0.62)

        if config['leg-position'][0] is not None and \
                config['leg-position'][2] is not None:
            leg.SetX1(config['leg-position'][0])
            leg.SetX2((config['leg-position'][0] +
                       config['leg-position'][2]) / 2)
            leg2.SetX2((config['leg-position'][0] +
                        config['leg-position'][2]) / 2)
            leg2.SetX2(config['leg-position'][0])
        if config['leg-position'][1] is not None:
            leg.SetY1(config['leg-position'][1])
            leg2.SetY1(config['leg-position'][1])
        if config['leg-position'][3] is not None:
            leg.SetY2(config['leg-position'][3])
            leg2.SetY2(config['leg-position'][3])

        leg2.SetFillColor(0)
        leg2.SetFillStyle(0)
        leg2.SetLineColor(0)
        leg2.SetShadowColor(10)
        leg2.SetTextSize(config['legend-text-size'])
        leg2.SetTextFont(42)
    else:
        legsize = 0.04 * (len(hbackgrounds) + len(hsignal))
        leg = ROOT.TLegend(0.68, 0.86 - legsize, 0.96, 0.88)
        leg2 = None

        if config['leg-position'][0] is not None:
            leg.SetX1(config['leg-position'][0])
        if config['leg-position'][1] is not None:
            leg.SetY1(config['leg-position'][1])
        if config['leg-position'][2] is not None:
            leg.SetX2(config['leg-position'][2])
        if config['leg-position'][3] is not None:
            leg.SetY2(config['leg-position'][3])

    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(config['legend-text-size'])
    leg.SetTextFont(42)

    for b in hbackgrounds:
        if config['split-leg']:
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

    lt = 'FCCAnalyses: FCC-hh Simulation (Delphes)'
    rt = f'#sqrt{{s}} = {script_module.energy:.1f} TeV,   ' \
         f'{config["int-lumi-label"]}'

    if 'ee' in script_module.collider:
        lt = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
        rt = f'#sqrt{{s}} = {script_module.energy:.1f} GeV,   ' \
             f'{config["int-lumi-label"]}'

    customLabel = ""
    try:
        customLabel = script_module.customLabel
    except AttributeError:
        LOGGER.debug('No custom label, using nothing...')

    if 'AAAyields' in var:
        plot_params = {'xaxis': 'lin',
                       'yaxis': 'lin',
                       'stack-sig': 'stack'}
        draw_plot(config, plot_params,
                  var,
                  'events', leg, lt, rt,
                  script_module.formats,
                  script_module.outdir + "/" + sel, histos,
                  colors, script_module.ana_tex, extralab,
                  customLabel, nsig, nbkg, leg2, yields,
                  config['plot-stat-unc'])
        return

    for sig_stacking in config['stack-sig']:
        plot_params = {'stack-sig': sig_stacking}
        for xaxis_scaling in config['x-axis-scale-types']:
            plot_params_x = {**plot_params, 'xaxis': xaxis_scaling}
            for yaxis_scaling in config['y-axis-scale-types']:
                plot_params_x_y = {**plot_params_x, 'yaxis': yaxis_scaling}
                plot_name = var
                if len(config['stack-sig']) > 1:
                    plot_name += '_' + sig_stacking
                if len(config['x-axis-scale-types']) > 1:
                    plot_name += '_' + xaxis_scaling + 'x'
                if len(config['y-axis-scale-types']) > 1:
                    plot_name += '_' + yaxis_scaling + 'y'
                draw_plot(config, plot_params_x_y,
                          plot_name,
                          'events', leg, lt, rt,
                          script_module.formats,
                          script_module.outdir + "/" + sel,
                          histos, colors, script_module.ana_tex,
                          extralab, customLabel, nsig, nbkg, leg2,
                          yields, config['plot-stat-unc'])


# _____________________________________________________________________________
def runPlotsHistmaker(config: dict[str, Any],
                      args,
                      hist_name: str,
                      param,
                      hist_cfg):

    output = hist_cfg['output']
    hsignal, hbackgrounds = mapHistosFromHistmaker(config,
                                                   hist_name,
                                                   param,
                                                   hist_cfg)

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
        leg2.SetTextSize(config['legend-text-size'])
        leg2.SetTextFont(42)
    else:
        legsize = 0.04*(len(hbackgrounds)+len(hsignal))
        legCoord = [0.68, 0.86 - legsize, 0.96, 0.88]
        try:
            legCoord = param.legendCoord
        except AttributeError:
            LOGGER.debug('No legCoord, using default one...')
            legCoord = [0.68, 0.86-legsize, 0.96, 0.88]
        leg2 = None

    leg = ROOT.TLegend(
        (config['leg-position'][0]
         if config['leg-position'][0] is not None
         else legCoord[0]),
        (config['leg-position'][1]
         if config['leg-position'][1] is not None
         else legCoord[1]),
        (config['leg-position'][2]
         if config['leg-position'][2] is not None
         else legCoord[2]),
        (config['leg-position'][3]
         if config['leg-position'][3] is not None
         else legCoord[3])
    )
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(config['legend-text-size'])
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

    xtitle = hist_cfg['xtitle'] if 'xtitle' in hist_cfg else ""
    ytitle = hist_cfg['ytitle'] if 'ytitle' in hist_cfg else "Events"
    xmin = hist_cfg['xmin'] if 'xmin' in hist_cfg else -1
    xmax = hist_cfg['xmax'] if 'xmax' in hist_cfg else -1
    ymin = hist_cfg['ymin'] if 'ymin' in hist_cfg else -1
    ymax = hist_cfg['ymax'] if 'ymax' in hist_cfg else -1
    stack = hist_cfg['stack'] if 'stack' in hist_cfg else False
    logx = hist_cfg['logx'] if 'logx' in hist_cfg else False
    logy = hist_cfg['logy'] if 'logy' in hist_cfg else False
    extralab = hist_cfg['extralab'] if 'extralab' in hist_cfg else ""

    intLumi = f'L = {param.intLumi / 1e+06:.0f} ab^{{-1}}'
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
        LOGGER.debug('No customLabel, using nothing...')

    plot_params: dict[str, Any] = {}
    plot_params['stack-sig'] = 'stack' if stack else 'nostack'
    plot_params['xaxis'] = 'log' if logx else 'lin'
    plot_params['yaxis'] = 'log' if logy else 'lin'
    draw_plot(config, plot_params,
              output, ytitle,
              leg, lt, rt,
              param.formats,
              param.outdir,
              histos, colors, param.ana_tex,
              extralab, customLabel, nsig, nbkg, leg2,
              yields, plotStatUnc,
              xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
              xtitle=xtitle)

    if 'dumpTable' in hist_cfg and hist_cfg['dumpTable']:
        if type(xtitle) != list:
            LOGGER.error('Can only dump a table of yields for cutflow plots.')
            quit()
        procs = list(hsignal.keys()) + list(hbackgrounds.keys())
        hists = hsignal | hbackgrounds
        scaleSig = hist_cfg['scaleSig'] if 'scaleSig' in hist_cfg else 1.
        hists[procs[0]][0].Scale(1./scaleSig) # undo signal scaling
        cuts = xtitle

        out_orig = sys.stdout
        with open(f"{param.outdir}/{output}.txt", 'w') as f:
            sys.stdout = f

            formatted_row = '{:<10} {:<15} ' + ' '.join(['{:<15}']*len(procs))
            print(formatted_row.format(*(["Cut", "Significance"]+procs)))
            print(formatted_row.format(*(["----------"]+["-------------"]*(len(procs)+1))))
            for i,cut in enumerate(cuts):
                s = hists[procs[0]][0].GetBinContent(i+1)
                s_plus_b = sum([hists[p][0].GetBinContent(i+1) for p in procs])
                significance = s/(s_plus_b**0.5) if s_plus_b > 0 else 0
                row = ["Cut %d"%i, "%.3f"%significance]
                for j,proc in enumerate(procs):
                    yield_ = hists[proc][0].GetBinContent(i+1)
                    row.append("%.4e" % (yield_))

                print(formatted_row.format(*row))
        sys.stdout = out_orig


# _____________________________________________________________________________
def draw_plot(config: dict[str, Any],
              plot_params: dict[str, Any],
              plot_name: str, ylabel, legend, leftText, rightText, formats,
              out_dir, histos, colors, ana_tex, extralab,
              customLabel, nsig, nbkg, legend2=None, yields=None,
              plotStatUnc=False, xmin=-1, xmax=-1, ymin=-1, ymax=-1,
              xtitle=""):
    '''
    Do the actual drawing of the plot onto the ROOT's canvas.
    '''

    if len(histos) == 0:
        LOGGER.warning('No histograms provided!\n  - plot name: "%s"\n'
                       'Continuing...', plot_name)
        return

    # Setup canvas
    canvas = ROOT.TCanvas(plot_name, plot_name, 800, 800)
    if plot_params['xaxis'] == 'lin':
        canvas.SetLogx(0)
    else:
        canvas.SetLogx(1)
    if plot_params['yaxis'] == 'lin':
        canvas.SetLogy(0)
    else:
        canvas.SetLogy(1)
    canvas.SetTicks(1, 1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)

    # Adjust y-axis label
    hist0_name = str(histos[0].GetXaxis().GetTitle())
    if any(unit in hist0_name for unit in ['GeV', 'TeV']):
        unit = 'GeV'
        if 'TeV' in str(histos[0].GetXaxis().GetTitle()):
            unit = 'TeV'

        bwidth = histos[0].GetBinWidth(1)
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

    # define stacked histo
    hStack = ROOT.THStack("hstack", "")
    hStackBkg = ROOT.THStack("hstackbkg", "")
    hStackSig = ROOT.THStack("hstacksig", "")
    BgMCHistYieldsDic = {}

    # first plot backgrounds (sorted by the yields)
    for i in range(nsig, nsig+nbkg):
        hist = histos[i]
        hist.SetLineWidth(1)
        hist.SetLineColor(ROOT.kBlack)
        hist.SetFillColor(colors[i])
        if hist.Integral() > 0:
            BgMCHistYieldsDic[hist.Integral()] = hist
        else:
            BgMCHistYieldsDic[-1*nbkg] = hist
    # sort stack by yields (smallest to largest)
    BgMCHistYieldsSorted = sorted_dict_values(BgMCHistYieldsDic)
    for hist in BgMCHistYieldsSorted:
        hStack.Add(hist)
        hStackBkg.Add(hist)

    # add the signal histograms
    for i in range(nsig):
        hist = histos[i]
        hist.SetLineWidth(3)
        hist.SetLineColor(colors[i])
        hStack.Add(hist)
        hStackSig.Add(hist)

    if xmin != -1 and xmax != -1:
        h_dummy.GetXaxis().SetLimits(xmin, xmax)

    h_dummy.Draw("HIST")
    if plot_params['stack-sig'] == 'stack':
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
            if hStackBkg.GetNhists() != 0:
                hUnc_bkg = formatStatUncHist(hStackBkg.GetHists(), "bkg_only")
                hUnc_bkg.Draw("E2 SAME")
            for sHist in hStackSig.GetHists():
                # sigs uncertainty
                hUnc_sig = formatStatUncHist([sHist], "sig", 3245)
                hUnc_sig.Draw("E2 SAME")

    # x limits
    if xmin == -1:
        xmin = hStack.GetStack().Last().GetBinLowEdge(1)
    if xmax == -1:
        xmax = hStack.GetStack().Last().GetBinLowEdge(
            hStack.GetStack().Last().GetNbinsX() + 1
        )
    if plot_params['xaxis'] == 'log':
        if xmin <= 0.:
            LOGGER.error('Log scale for x-axis can\'t start at: %g\n'
                         '  - plot name: %s\nContinuing...', xmin, plot_name)
            return
        if xmax <= 0.:
            LOGGER.error('Log scale for x-axis can\'t end at: %g\n'
                         '  - plot name: %s\nContinuing...', xmax, plot_name)
            return
    h_dummy.GetXaxis().SetLimits(xmin, xmax)

    # y limits
    if plot_params['stack-sig'] == 'stack':
        ymin_, ymax_ = get_minmax_range(hStack.GetHists(), xmin, xmax)
    else:
        if hStackSig.GetNhists() != 0 and hStackBkg.GetNhists() != 0:
            ymin_sig, ymax_sig = get_minmax_range(hStackSig.GetHists(),
                                                  xmin, xmax)
            ymin_bkg, ymax_bkg = get_minmax_range(hStackBkg.GetHists(),
                                                  xmin, xmax)
            ymin_ = min(ymin_sig, ymin_bkg)
            ymax_ = max(ymax_sig, ymax_bkg)
        elif hStackSig.GetNhists() == 0:
            ymin_, ymax_ = get_minmax_range(hStackBkg.GetHists(), xmin, xmax)
        elif hStackBkg.GetNhists() == 0:
            ymin_, ymax_ = get_minmax_range(hStackSig.GetHists(), xmin, xmax)
    if ymin == -1:
        ymin = ymin_*0.1 if plot_params['yaxis'] == 'log' else 0
    if ymax == -1:
        ymax = ymax_*1000. if plot_params['yaxis'] == 'log' else 1.4*ymax_
    if plot_params['yaxis'] == 'log':
        if ymin <= 0.:
            LOGGER.error('Log scale for y-axis can\'t start at: %g\n'
                         '  - plot name: %s\nContinuing...', ymin, plot_name)
            return
        if ymax <= 0.:
            LOGGER.error('Log scale for y-axis can\'t end at: %g\n'
                         '  - plot name: %s\nContinuing...', ymax, plot_name)
            return
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

    if config['scale-sig'] != 1.0:
        text = '#bf{#it{Signal Scaling = ' + f'{config["scale-sig"]:.3g}' + \
               '}}'
        latex.SetTextSize(0.025)
        latex.DrawLatex(0.18, 0.63, text)

    if config['scale-bkg'] != 1.0:
        text = '#bf{#it{Background Scaling = ' + \
                f'{config["scale-bkg"]:.3g}' + '}}'
        latex.SetTextSize(0.025)
        latex.DrawLatex(0.18, 0.63, text)

    canvas.RedrawAxis()
    canvas.GetFrame().SetBorderSize(12)
    canvas.Modified()
    canvas.Update()

    if 'AAAyields' in plot_name:
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

        text = '#bf{#it{Signal Scaling = ' + f'{config["scale-sig"]:.3g}' + \
               '}}'
        latex.SetTextSize(0.04)
        latex.DrawLatex(0.18, 0.57, text)

        text = '#bf{#it{Background Scaling = ' + \
            f'{config["scale-bkg"]:.3g}' + '}}'
        latex.SetTextSize(0.04)
        latex.DrawLatex(0.18, 0.52, text)

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

    save_canvas(canvas, plot_name, formats, out_dir)


# _____________________________________________________________________________
def save_canvas(canvas, plot_name: str, formats: list[str], out_dir: str):
    '''
    Saving canvas in multiple formats.
    '''

    if not formats:
        LOGGER.error('No output formats specified!\nAborting...')
        sys.exit(3)

    if not os.path.exists(out_dir):
        os.system("mkdir -p " + out_dir)

    for ext in formats:
        out_path = os.path.join(out_dir, plot_name) + "." + ext
        canvas.SaveAs(out_path)
        LOGGER.debug(out_path)


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
    # Also check the script attributes
    config: dict[str, Any] = {}

    # Input directory
    config['input-dir'] = os.getcwd()
    if hasattr(script_module, 'indir'):
        config['input-dir'] = script_module.indir
    if hasattr(script_module, 'inputDir'):
        config['input-dir'] = script_module.inputDir
    if args.input_dir is not None:
        config['input-dir'] = args.input_dir
    LOGGER.info('Input directory: %s', config['input-dir'])

    # Output directory
    config['output-dir'] = os.getcwd()
    if hasattr(script_module, 'outdir'):
        config['output-dir'] = script_module.outdir
    if hasattr(script_module, 'outputDir'):
        config['output-dir'] = script_module.outputDir
    if args.output_dir is not None:
        config['output-dir'] = args.output_dir
    LOGGER.info('Output directory: %s', config['output-dir'])

    # Output file types
    config['output-file-types'] = ['png', 'pdf']
    if hasattr(script_module, 'formats'):
        config['output-file-types'] = script_module.formats
    msg = 'Output file types to be used: [' + \
          ', '.join(config['output-file-types']) + ']'
    LOGGER.info(msg)

    # Integrated luminosity
    config['int-lumi'] = 1.
    if hasattr(script_module, 'intLumi'):
        config['int-lumi'] = script_module.intLumi
    else:
        LOGGER.debug('No integrated luminosity provided, using 1.0 pb-1.')
    LOGGER.info('Integrated luminosity: %g pb-1', config['int-lumi'])

    # Whether to scale histograms to luminosity
    config['do-scale'] = 1.0
    if hasattr(script_module, 'doScale'):
        config['do-scale'] = script_module.doScale
    else:
        LOGGER.debug('No scaling to luminosity requested, scaling won\'t be '
                     'done.')
        config['do-scale'] = False
    if config['do-scale']:
        LOGGER.info('Histograms will be scaled to luminosity.')

    # Scale factor to apply to all signal histograms
    config['scale-sig'] = 1.0
    if hasattr(script_module, 'scaleSig'):
        config['scale-sig'] = script_module.scaleSig
    else:
        LOGGER.debug('No scale factor for signal provided, using 1.0.')
    LOGGER.info('Scale factor for signal: %g', config['scale-sig'])

    # Scale factor to apply to all background histograms
    config['scale-bkg'] = 1.0
    if hasattr(script_module, 'scaleBkg'):
        config['scale-bkg'] = script_module.scaleBkg
    else:
        LOGGER.debug('No scale factor for background provided, using 1.0.')
    LOGGER.info('Scale factor for background: %g', config['scale-sig'])

    # Stacking of the signal histograms
    config['stack-sig'] = ['stack']
    if hasattr(script_module, 'stacksig'):
        config['stack-sig'] = script_module.stacksig
    if any(stacking not in ['stack', 'nostack']
           for stacking in config['stack-sig']):
        config['stack-sig'] = [stacking for stacking
                               in config['stack-sig']
                               if stacking in ['stack', 'nostack']]
        LOGGER.warning('Unrecognized option for the signal stacking!\n'
                       'Should be one of: "stack", "nostack".')
    msg = 'Signal stacking options to be used for the plots: [' + \
          ', '.join(config['stack-sig']) + ']'
    LOGGER.info(msg)

    # Check x-axis scale types
    config['x-axis-scale-types'] = ['lin']
    if hasattr(script_module, 'xaxis'):
        config['x-axis-scale-types'] = script_module.xaxis
    if any(scale_type not in ['lin', 'log']
           for scale_type in config['x-axis-scale-types']):
        config['x-axis-scale-types'] = [scale_type for scale_type
                                        in config['x-axis-scale-types']
                                        if scale_type in ['lin', 'log']]
        LOGGER.warning('Unrecognized option for the x-axis scaling!'
                       '\nShould be one of: "lin", "log".')
    msg = 'X-axis scale types to be used for the plots: [' + \
          ', '.join(config['x-axis-scale-types']) + ']'
    LOGGER.info(msg)

    # Check y-axis scale types
    config['y-axis-scale-types'] = ['lin']
    if hasattr(script_module, 'yaxis'):
        config['y-axis-scale-types'] = script_module.yaxis
    if any(scale_type not in ['lin', 'log']
           for scale_type in config['y-axis-scale-types']):
        config['y-axis-scale-types'] = [scale_type for scale_type
                                        in config['y-axis-scale-types']
                                        if scale_type in ['lin', 'log']]
        LOGGER.warning('Unrecognized option for the y-axis scaling!'
                       '\nShould be one of: "lin", "log".')
    msg = 'Y-axis scale types to be used for the plots: [' + \
          ', '.join(config['y-axis-scale-types']) + ']'
    LOGGER.info(msg)

    # Check if we have plots (staged analysis) or histos (histmaker)
    config['plots']: dict[str, Any] = {}
    config['hists']: dict[str, Any] = {}
    config['ana-type']: str = "none"
    if hasattr(script_module, 'plots'):
        config['plots'] = script_module.plots
        config['ana-type']: str = "staged"
    if hasattr(script_module, 'hists'):
        config['hists'] = script_module.hists
        config['ana-type']: str = "histmaker"

    if config['ana-type'] == "none":
        LOGGER.error('No plot definitions found!\nAborting...')
        sys.exit(3)

    # Splitting legend into two columns
    config['split-leg'] = False
    if hasattr(script_module, 'splitLeg'):
        config['split-leg'] = script_module.splitLeg

    config['leg-position'] = [None, None, None, None]
    if hasattr(script_module, 'legendCoord'):
        config['leg-position'] = script_module.legendCoord
    if args.legend_x_min is not None:
        config['leg-position'][0] = args.legend_x_min
    if args.legend_y_min is not None:
        config['leg-position'][1] = args.legend_y_min
    if args.legend_x_max is not None:
        config['leg-position'][2] = args.legend_x_max
    if args.legend_y_max is not None:
        config['leg-position'][3] = args.legend_y_max

    config['plot-stat-unc'] = False
    if hasattr(script_module, 'plotStatUnc'):
        config['plot-stat-unc'] = script_module.plotStatUnc

    config['legend-text-size'] = 0.035
    if hasattr(script_module, 'legendTextSize'):
        config['legend-text-size'] = script_module.legendTextSize
    if args.legend_text_size is not None:
        config['legend-text-size'] = args.legend_text_size

    # Label for the integrated luminosity
    config['int-lumi-label'] = None
    if hasattr(script_module, "intLumiLabel"):
        config['int-lumi-label'] = script_module.intLumiLabel
    if config['int-lumi-label'] is None:
        if config['int-lumi'] >= 1e6:
            int_lumi_label = config['int-lumi'] / 1e6
            config['int-lumi-label'] = f'L = {int_lumi_label:.2g} ab^{{-1}}'
        elif config['int-lumi'] >= 1e3:
            int_lumi_label = config['int-lumi'] / 1e3
            config['int-lumi-label'] = f'L = {int_lumi_label:.2g} fb^{{-1}}'
        else:
            config['int-lumi-label'] = \
                f'L = {config["int-lumi"]:.2g} pb^{{-1}}'

    # Handle plots for the Histmaker analyses and exit
    if config['ana-type'] == 'histmaker':
        LOGGER.info('Plotting histograms from histmaker step...')
        for hist_name, hist_cfg in script_module.hists.items():
            runPlotsHistmaker(config, args, hist_name, script_module, hist_cfg)
        sys.exit()

    counter = 0
    LOGGER.info('Plotting staged analysis plots...')
    for var_index, var in enumerate(script_module.variables):
        for label, sels in script_module.selections.items():
            for sel in sels:
                rebin_tmp = 1
                if hasattr(script_module, "rebin"):
                    if len(script_module.rebin) == \
                            len(script_module.variables):
                        rebin_tmp = script_module.rebin[var_index]

                LOGGER.info('  var: %s     label: %s     selection: %s',
                            var, label, sel)

                hsignal, hbackgrounds = load_hists(var,
                                                   label,
                                                   sel,
                                                   config,
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
