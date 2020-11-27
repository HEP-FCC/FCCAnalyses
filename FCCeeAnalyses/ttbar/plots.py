import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = "e^{+}e^{-} #rightarrow t#bar{t}"

delphesVersion = "3.4.2"
energy         = 365.0
collider       = "FCC-ee"
inputDir       = "FCCee/ttbar/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'FCCee/ttbar/plots/'

variables = ['muon_pt']

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttbar']   = ["sel0"]

extralabel = {}
extralabel['sel0'] = "Selection: N_{muons} == 1, p_{T}>10 [GeV]"

colors = {}
colors['tt'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['ZH'] = ROOT.kGreen+3

plots = {}
plots['ttbar'] = {'signal':{'tt':['p8_ee_tt_ecm365']},
                  'backgrounds':{'WW':['p8_ee_WW_ecm365'],
                                 'ZZ':['p8_ee_ZZ_ecm365'],
                                 'ZH':['p8_ee_ZH_ecm365']}
           }

legend = {}
legend['tt'] = 'tt'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['ZH'] = 'ZH'




