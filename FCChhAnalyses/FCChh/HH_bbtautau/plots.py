import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = "HH bbtautau"
delphesVersion = "3.4.2"
energy         = 100
collider       = "FCC-hh"
inputDir       = "FCChh/HH_bbtautau/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'FCChh/HH_bbtautau/plots/'

variables = ['jet_pt_0','jet_pt_1','jet_pt_2','jet_pt_3','jet_pt_4','jet_pt_5']

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HH_bbtautau']   = ['sel0']

extralabel = {}
extralabel['sel0'] = "Selection: jet pt > 30GeV"


colors = {}
colors['HH_bbtautau'] = ROOT.kRed
colors['tt'] = ROOT.kBlue+1

plots = {}
plots['HH_bbtautau'] = {'signal':{'HH_bbtautau':['pwp8_pp_hh_lambda100_5f_hhbbaa']},
                        'backgrounds':{'tt':['mgp8_pp_tt012j_5f']}
             }

legend = {}
legend['HH_bbtautau'] = 'HH->bbtautau'
legend['tt'] = 'tt'




