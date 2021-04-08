import ROOT

# global parameters
intLumi        = 100000000. #in pb-1
ana_tex        = "Z #rightarrow q#bar{q}"
delphesVersion = "3.4.2"
energy         = 91.0
collider       = "FCC-ee"
inputDir       = "/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Bc2TauNu/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'outputs/FCCee/flavour/generic-analysis/plots/'

variables = [ "EVT_thrust_val",
              "EVT_thrusthemis_emax",
              "EVT_thrusthemis_emin",
              "EVT_Ediff",
              "EVT_Echarged_max",
              "EVT_Echarged_min",
              "EVT_Eneutral_max",
              "EVT_Eneutral_min",

              "EVT_Ncharged_max",
              "EVT_Ncharged_min",
              "EVT_Nneutral_max",
              "EVT_Nneutral_min"

              ]

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Flavour']   = ["sel0","sel1","sel2","sel3"]

extralabel = {}
extralabel['sel0'] = "Selection: inclusive"
extralabel['sel1'] = "Selection: with cuts"
extralabel['sel2'] = "Selection: with tighter cuts"
extralabel['sel3'] = "Selection: with even tighter cuts"

colors = {}
colors['Z_flavour'] = ROOT.kRed
colors['Z_bb'] = ROOT.kBlue+1
colors['Z_cc'] = ROOT.kGreen+1
colors['Z_uds'] = ROOT.kGreen+2

plots = {}
plots['Flavour'] = {'signal':{'Z_flavour':['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU']},
                    'backgrounds':{'Z_bb':['p8_ee_Zbb_ecm91'],
                                   'Z_cc':['p8_ee_Zcc_ecm91'],
                                   'Z_uds':['p8_ee_Zuds_ecm91']}
           }

legend = {}
legend['Z_flavour'] = 'B_{c}#rightarrow #tau#nu (#tau#rightarrow 3#pi)'
legend['Z_bb'] = 'Z#rightarrow b#bar{b}'
legend['Z_cc'] = 'Z#rightarrow c#bar{c}'
legend['Z_uds'] = 'Z#rightarrow q#bar{q}'




