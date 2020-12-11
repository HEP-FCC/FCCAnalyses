import ROOT

# global parameters
intLumi        = 10 #in pb-1
ana_tex        = "Z #rightarrow b#bar{b}"
delphesVersion = "3.4.2"
energy         = 91.0
collider       = "FCC-ee"
inputDir       = "outputs/FCCee/flavour/generic-analysis/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'outputs/FCCee/flavour/generic-analysis/plots/'

variables = [ "EVT_thrust_val",
              "EVT_thrutshemis_emax",
              "EVT_thrutshemis_emin",
              "EVT_thrust_x",
              "EVT_thrust_y",
              "EVT_thrust_z"]

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Flavour']   = ["sel0"]

extralabel = {}
extralabel['sel0'] = "Selection: inclusive"

colors = {}
colors['Z_flavour'] = ROOT.kRed
colors['Z_inclusive'] = ROOT.kBlue+1

plots = {}
plots['Flavour'] = {'signal':{'Z_flavour':['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU']},
                    'backgrounds':{'Z_inclusive':['p8_ee_Zbb_ecm91']}
           }


plots['ZH_2'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
                 'backgrounds':{'VV':['p8_ee_WW_ecm240','p8_ee_ZZ_ecm240']}
             }

legend = {}
legend['Z_flavour'] = 'B_{c}#rightarrow #tau#nu (#tau#rightarrow 3#pi)'
legend['Z_inclusive'] = 'inclusive'




