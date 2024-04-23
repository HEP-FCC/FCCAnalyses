import ROOT


# global parameters
intLumi        = 1.
intLumiLabel   = "L = 7.2 ab^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = f"outputs/FCCee/higgs/mva/final_selection/"
formats        = ['png','pdf']
outdir         = f"outputs/FCCee/higgs/mva/plots/"
yaxis          = ['lin','log']
stacksig       = ['nostack']
plotStatUnc    = True




variables = ['zmumu_recoil_m_final', 'mva_score']
rebin = [1, 1] # uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   = ["sel0", "sel1"]

extralabel = {}
extralabel['sel0'] = "Basic selection"
extralabel['sel1'] = "MVA > 0.5"

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1


plots = {}
plots['ZH'] = {'signal':{'ZH':['wzp6_ee_mumuH_ecm240']},
               'backgrounds':{'WW':['p8_ee_WW_ecm240']}
           }

legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
