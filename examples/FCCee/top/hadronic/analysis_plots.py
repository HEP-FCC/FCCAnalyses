#python bin/doPlots.py FCCeeAnalyses/top/template-analysis/plots.py

import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = "e^{+}e^{-} #rightarrow t#bar{t} full hadronic"

delphesVersion = "3.4.2"
energy         = 365.0
collider       = "FCC-ee"
inputDir       = "outputs/FCCee/top/hadronic/analysis_final/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'outputs/FCCee/top/hadronic/analysis_plots/'

variables = ["thrust_val", "sphericity_val", "thrust_angle", "sphericity_angle", "hemis0_mass", "hemis1_mass", "total_mass"]

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttbar']   = ["sel0","sel1"]

extralabel = {}
extralabel['sel0'] = "Selection: no selection"
extralabel['sel1'] = "Selection: mass hemisphere0/1>100GeV"

colors = {}
colors['tt'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['ZH'] = ROOT.kGreen+3

plots = {}
plots['ttbar'] = {'signal':{'tt':['p8_ee_tt_fullhad_ecm365']},
                  'backgrounds':{'WW':['p8_ee_WW_fullhad_ecm365'],
                                 'ZZ':['p8_ee_ZZ_fullhad_ecm365']}
           }

legend = {}
legend['tt'] = 'tt'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['ZH'] = 'ZH'
