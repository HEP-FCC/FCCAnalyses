import ROOT

# global parameters
intLumi        = 150000000. #in pb-1
ana_tex        = "Z #rightarrow q#bar{q}"
delphesVersion = "3.4.2"
energy         = 91.0
collider       = "FCC-ee"
inputDir       = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2MuMu/flatNtuples/spring2021/Batch/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = 'plots_Bd2MuMu/'
variables      = ["EVT_CandMass","EVT_CandMass_zoom"]

scaleSig=1.
###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis.
###The name of the selections should be the same than in the final selection
selections = {}
selections['Bd2MuMu']       = ["sel0"]

extralabel = {}
extralabel['sel0'] = "Selection: N B#rightarrow#mu#mu=1"

colors = {}
colors['Z_bb']  = ROOT.kBlue
colors['Z_Bd']  = ROOT.kRed

plots = {}
plots['Bd2MuMu'] = {'signal':{'Z_Bd':['p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu']},
                    'backgrounds':{'Z_bb':['p8_ee_Zbb_ecm91']}
                  }

legend = {}
legend['Z_Bd']    = 'B_{d}#rightarrow #mu#mu'
legend['Z_bb']    = 'Z#rightarrow b#bar{b}'
