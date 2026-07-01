import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttH(#rightarrow #gamma#gamma)'
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-hh'
inputDir       = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/ttHyy_analysis/final/'
formats        = ['png'] #['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
# stacksig       = ['stack','nostack']
outdir         = './plots_ttHyy_analysis/'
plotStatUnc    = True

variables = ['n_photons','n_bjets', 'm_yy']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttHyy_analysis']   = ["sel1_bjets","sel2_photons"]

extralabel = {}
extralabel['sel1_bjets'] = "b-jet pair"
extralabel['sel2_photons'] = "b-jet and photon pair"

colors = {}
colors['ttHyy_signal'] = ROOT.kBlack
colors['yy_jets'] = ROOT.kGreen
colors['ttyy'] = ROOT.kCyan

plots = {}
plots['ttHyy_analysis'] = {
                            'signal':{'ttHyy_signal':[ 'mgp8_pp_tth01j_5f_haa']},
                            'backgrounds':{
                                'yy_jets':[ 'mgp8_pp_jjaa_5f'],
                                'ttyy':[ 'mgp8_pp_ttaa_semilep_5f_100TeV'],
                            
                            },
           }


legend = {}
legend['ttHyy_signal'] = 'ttH(#rightarrow #gamma#gamma)'
legend['yy_jets'] = '#gamma#gamma+jets'
legend['ttyy'] = 'tt#gamma#gamma'