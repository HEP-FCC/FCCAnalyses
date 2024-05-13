import ROOT

flavor = "mumu" # mumu, ee


# global parameters
intLumi        = 1.
intLumiLabel   = "L = 7.2 ab^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = f"outputs/FCCee/higgs/mass-xsec/histmaker/{flavor}/"
formats        = ['png','pdf']
outdir         = f"outputs/FCCee/higgs/mass-xsec/plots/{flavor}/"
plotStatUnc    = True

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2

procs = {}
procs['signal'] = {'ZH':['wzp6_ee_mumuH_ecm240']}
procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}


legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'



hists = {}

hists["zll_recoil_m"] = {
    "output":   "zll_recoil_m",
    "logy":     False,
    "stack":    True,
    "rebin":    100,
    "xmin":     120,
    "xmax":     140,
    "ymin":     0,
    "ymax":     2500,
    "xtitle":   "Recoil (GeV)",
    "ytitle":   "Events / 100 MeV",
}

hists["zll_p"] = {
    "output":   "zll_p",
    "logy":     False,
    "stack":    True,
    "rebin":    2,
    "xmin":     0,
    "xmax":     80,
    "ymin":     0,
    "ymax":     2000,
    "xtitle":   "p(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events ",
}

hists["zll_m"] = {
    "output":   "zll_m",
    "logy":     False,
    "stack":    True,
    "rebin":    2,
    "xmin":     86,
    "xmax":     96,
    "ymin":     0,
    "ymax":     3000,
    "xtitle":   "m(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events ",
}

hists["cosThetaMiss_cut4"] = {
    "output":   "cosThetaMiss_cut4",
    "logy":     True,
    "stack":    True,
    "rebin":    10,
    "xmin":     0,
    "xmax":     1,
    "ymin":     10,
    "ymax":     100000,
    "xtitle":   "cos(#theta_{miss})",
    "ytitle":   "Events ",
    "extralab": "Before cos(#theta_{miss}) cut",
}


hists["cutFlow"] = {
    "output":   "cutFlow",
    "logy":     True,
    "stack":    False,
    "xmin":     0,
    "xmax":     6,
    "ymin":     1e4,
    "ymax":     1e11,
    "xtitle":   ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{miss}| < 0.98", "120 < m_{rec} < 140"],
    "ytitle":   "Events ",
    "scaleSig": 10
}
