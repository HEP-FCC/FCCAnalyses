#!/usr/bin/env python

import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT
import array

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


LOGGER = logging.getLogger('FCCAnalyses.combine')


def get_param(obj, name, default=None):
    if hasattr(obj, name):
        return getattr(obj, name)
    elif default != None:
        LOGGER.info(f"Use default value of {default} for {name}")
        return default
    else:
        LOGGER.error(f"Parameter {name} not defined but required. Aborting")
        sys.exit(3)

def rebin(h, newbins):
    if isinstance(newbins, int):
        return h.Rebin(newbins, h.GetName())
    else:
        mybins = array.array('d', newbins)
        return h.Rebin(len(mybins)-1, h.GetName(), mybins)

def run(script_path):

    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    module_path = os.path.abspath(script_path)
    module_dir = os.path.dirname(module_path)
    base_name = os.path.splitext(ntpath.basename(script_path))[0]

    sys.path.insert(0, module_dir)
    param = importlib.import_module(base_name)

    inputDir = get_param(param, "inputDir")
    outputDir = get_param(param, "outputDir")


    lspace = 12
    sig_procs = get_param(param, "sig_procs")
    bkg_procs = get_param(param, "bkg_procs")
    procs_sig_names = sorted(list(sig_procs.keys()))
    procs_bkg_names = sorted(list(bkg_procs.keys()))
    procs = procs_sig_names + procs_bkg_names
    proc_dict = sig_procs | bkg_procs
    nprocs = len(procs)
    procs_idx = list(range(-len(sig_procs)+1, len(bkg_procs)+1, 1)) # negative or 0 for signal, positive for bkg

    categories = get_param(param, "categories")
    hist_names = get_param(param, "hist_names")
    ncats = len(categories)

    cats_str = "".join([f"{cat:{' '}{'<'}{lspace}}" for cat in categories])
    procs_str = "".join([f"{proc:{' '}{'<'}{lspace}}" for proc in procs] * ncats)
    cats_procs_str = "".join([f"{cat:{' '}{'<'}{lspace}}" for cat in categories for _ in range(nprocs)])
    cats_procs_idx_str = "".join([f"{str(proc_idx):{' '}{'<'}{lspace}}" for proc_idx in procs_idx] * ncats)
    rates_cats = "".join([f"{'-1':{' '}{'<'}{lspace}}"]*(ncats))
    rates_procs = "".join([f"{'-1':{' '}{'<'}{lspace}}"]*(ncats*nprocs))


    ## datacard header
    dc = ""
    dc += f"imax *\n"
    dc += f"jmax *\n"
    dc += "kmax *\n"
    dc += f"########################################\n"
    dc += f"shapes *        * datacard.root $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n"
    dc += f"shapes data_obs * datacard.root $CHANNEL_asimov\n"
    dc += f"########################################\n"
    dc += f"bin                        {cats_str}\n"
    dc += f"observation                {rates_cats}\n"
    dc += f"########################################\n"
    dc += f"bin                        {cats_procs_str}\n"
    dc += f"process                    {procs_str}\n"
    dc += f"process                    {cats_procs_idx_str}\n"
    dc += f"rate                       {rates_procs}\n"
    dc += f"########################################\n"

    ## systematic uncertainties
    systs = get_param(param, "systs")
    for systName, syst in systs.items():
        syst_type = syst['type']
        syst_val = str(syst['value'])
        procs_to_apply = syst['procs']
        dc_tmp = f"{systName:{' '}{'<'}{15}} {syst_type:{' '}{'<'}{10}} "
        for cat in categories:
            for proc in procs:
                apply_proc = (isinstance(procs_to_apply, list) and proc in procs_to_apply) or (isinstance(procs_to_apply, str) and re.search(procs_to_apply, proc))
                if apply_proc:
                    if syst_type == "shape":
                        LOGGER.warning('Shape uncertainties not yet supported! Skipping')
                        val = "-"
                    else:
                        val = str(syst_val)
                else:
                    val = "-"
                dc_tmp += f"{val:{' '}{'<'}{lspace}}"
        dc += f"{dc_tmp}\n"

    ## auto MC stats
    if get_param(param, "mc_stats"):
        dc += "* autoMCStats 1 1"

    ## get histograms
    new_bins = get_param(param, "rebin", 1)
    sel = get_param(param, "selection", -1)
    intLumi = get_param(param, "intLumi")
    hists = []
    hists_asimov = {}
    for procName, procList in proc_dict.items():
        for i,cat in enumerate(categories):
            hist = None
            for proc in procList:
                if sel == -1:
                    fInName = f"{inputDir}/{proc}.root"
                else:
                    fInName = f"{inputDir}/{proc}_{sel}_histo.root"
                if not os.path.isfile(fInName):
                    LOGGER.error(f'File {fInName} not found! Aborting...')
                    sys.exit(3)
                fIn = ROOT.TFile(fInName, 'READ')
                h = copy.deepcopy(fIn.Get(hist_names[i]))
                if hist == None:
                    hist = h
                else:
                    hist.Add(h)
            hist.SetName(f"{cat}_{procName}")
            hist.Scale(intLumi)
            hist = rebin(hist, new_bins)
            hists.append(copy.deepcopy(hist))
            if not cat in hists_asimov:
                hist_asimov = copy.deepcopy(hist)
                hist_asimov.SetName(f"{cat}_asimov")
                hists_asimov[cat] = hist_asimov
            else:
                hists_asimov[cat].Add(hist)

    # write cards
    if not os.path.exists(outputDir):
        os.system(f"mkdir -p {outputDir}")

    f = open(f"{outputDir}/datacard.txt", 'w')
    f.write(dc)
    f.close()
    fOut = ROOT.TFile(f"{outputDir}/datacard.root", "RECREATE")
    for hist in hists:
        hist.Write()
    for hist in hists_asimov.values():
        hist.Write()
    fOut.Close()

    print(dc)


def do_combine(parser):
    args, _ = parser.parse_known_args()

    if args.command != 'combine':
        LOGGER.error('Wrong sub-command!\nAborting...')

    if not os.path.isfile(args.script_path):
        LOGGER.error('Plots script "%s" not found!\nAborting...',
                     args.script_path)
        sys.exit(3)

    run(args.script_path)