import ROOT

# global parameters
intLumi        = 100.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow #tau #tau'
delphesVersion = '3.4.2'
energy         = 91.2
collider       = 'FCC-ee'
inputDir       = 'Tau3Mu/final/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'Tau3Mu/plots/'

variables = ['mTau', 'mTau_zoom', 'Evis' ]

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Tau3Mu']   = ["nocut", "sel0","sel1"]

extralabel = {}
extralabel['nocut'] = "no cut"
extralabel['sel0'] = "Selection: N_{candidate} > 0"
extralabel['sel1'] = "Selection: a candidate with M < 3 GeV"

colors = {}
colors['Tau3Mu'] = ROOT.kRed
colors['Tau3Pi'] = ROOT.kBlue+1

plots = {}
plots['Tau3Mu'] = {'signal':{'Tau3Mu':['p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu']},
               'backgrounds':{'Tau3Pi':['p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu'],
                              }
           }



legend = {}
legend['Tau3Mu'] = 'Tau3Mu'
legend['Tau3Pi'] = 'Tau3Pi'
