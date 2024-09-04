import ROOT

flavor = "mumu" # mumu, ee

intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir      = f"outputs/FCCee/higgs/mass-xsec/combine/{flavor}/"
mc_stats       = True
rebin          = 10

# get histograms from histmaker step
#inputDir       = f"outputs/FCCee/higgs/mass-xsec/histmaker/{flavor}/"

# get histograms from final step, selection to be defined
inputDir       = f"outputs/FCCee/higgs/mass-xsec/final_selection/{flavor}/"
selection      = "sel3"


sig_procs = {'sig':['wzp6_ee_mumuH_ecm240']}
bkg_procs = {'bkg':['p8_ee_WW_ecm240', 'p8_ee_ZZ_ecm240']}


categories = ["recoil"]
hist_names = ["zll_recoil_m_final"]


systs = {}

systs['bkg_norm'] = {
    'type': 'lnN',
    'value': 1.10,
    'procs': ['bkg'],
}

systs['lumi'] = {
    'type': 'lnN',
    'value': 1.01,
    'procs': '.*',
}
