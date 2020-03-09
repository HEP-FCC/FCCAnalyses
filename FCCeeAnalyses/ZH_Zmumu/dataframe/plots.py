import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = "e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X"
delphesVersion = "3.4.2"
energy         = 240.0
collider       = "FCC-ee"
inputDir       = "FCCee/ZH_Zmumu/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'FCCee/ZH_Zmumu/plots/'

variables = ['mz','mz_zoom','nbjets','leptonic_recoil_m']

selections = {}
selections['ZH']   = ["sel0","sel1","sel2"]
selections['ZH_2'] = ["sel0","sel2"]

extralabel = {}
extralabel['sel0'] = "Selection: N_{Z} = 1"
extralabel['sel1'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV"
extralabel['sel2'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV; N_{b} = 2"


colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['VV'] = ROOT.kGreen+3

plots = {}
plots['ZH'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
               'backgrounds':{'WW':['p8_ee_WW_ecm240'],
                              'ZZ':['p8_ee_ZZ_ecm240']}
           }


plots['ZH_2'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
                 'backgrounds':{'VV':['p8_ee_WW_ecm240','p8_ee_ZZ_ecm240']}
             }

legend = {}
legend['ZH'] = 'ZH boson'
legend['WW'] = 'WW boson'
legend['ZZ'] = 'ZZ boson'
legend['VV'] = 'VV boson'




