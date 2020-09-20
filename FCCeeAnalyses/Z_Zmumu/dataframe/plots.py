import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = "e^{+}e^{-} #rightarrow Z/#gamma^{*} #rightarrow #mu^{+}#mu^{-}"
delphesVersion = "3.4.3pre04"
energy         = 91.2
collider       = "FCC-ee"
inputDir       = "FCCee/Z_Zmumu/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'FCCee/Z_Zmumu/plots/'

variables = ['mz','mz_zoom','mz_zoom2','mz_zoom3']

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Z']   = ["sel0","sel1"]

extralabel = {}
extralabel['sel0'] = "Selection: N_{Z} = 1"
extralabel['sel1'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV"


colors = {}
colors['Z_Pythia8'] = ROOT.kRed
colors['Z_Whizard'] = ROOT.kBlue+1

plots = {}
plots['Z'] = {'signal':{'Z_Pythia8':['p8_ee_Z_Zmumu_ecm91']},
               'backgrounds':{'Z_Whizard':['wizhardp8_ee_Z_Zmumu_ecm91']
                          }
           }


legend = {}
legend['Z_Pythia8'] = 'Z Pythia8'
legend['Z_Whizard'] = 'Z Whizard'





