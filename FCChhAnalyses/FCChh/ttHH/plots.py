import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = "ttHH inclusive"
delphesVersion = "3.4.2"
energy         = 100
collider       = "FCC-hh"
inputDir       = "FCChh/ttHH/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'FCChh/ttHH/plots/'

variables = ['jet_pt_0','jet_pt_1','jet_pt_2','jet_pt_3','jet_pt_4','jet_pt_5']

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttHH']   = ['sel0']

extralabel = {}
extralabel['sel0'] = "Selection: jet pt > 30GeV"


colors = {}
colors['ttHH'] = ROOT.kRed
colors['ttH'] = ROOT.kBlue+1
colors['ttZ'] = ROOT.kGreen+2
colors['ttZZ'] = ROOT.kGreen+3

plots = {}
plots['ttHH'] = {'signal':{'ttHH':['mgp8_pp_tthh_lambda100_5f']},
                 'backgrounds':{'ttZ':['mgp8_pp_ttz_5f'],
                                'ttZZ':['mgp8_pp_ttzz_5f'],
                                'ttH':['mgp8_pp_tth01j_5f']}
             }


legend = {}
legend['ttHH'] = 'ttHH'
legend['ttH'] = 'ttH'
legend['ttZ'] = 'ttZ'
legend['ttZZ'] = 'ttZZ'




