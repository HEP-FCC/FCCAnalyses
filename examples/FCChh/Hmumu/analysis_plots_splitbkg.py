import ROOT
#plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow H #rightarrow #mu#mu analysis '
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-hh'
inputDir       = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Hmumu_analysis/final/'
formats        = ['png']
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis          = ['lin','log']
# stacksig       = ['stack']
stacksig       = ['stack','nostack']
outdir         = './plots_Hmumu_splitbkg/'
# outdir         = '/eos/user/b/bistapf/FCChh_SingleHAnalyses/Hmumu'
plotStatUnc    = True

variables = ['m_mumu', 'pT_mumu', 'pT_mumu_full']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Hmumu_analysis']   = ["sel1_mumupair", "sel_extra_njets1"]

extralabel = {}
extralabel['sel1_mumupair'] = "Pre-selected events"
extralabel['sel_extra_njets1'] = "Pre-selected events, njets > 0"

colors = {}
colors['mumu_slice1'] = ROOT.kBlue
colors['mumu_slice2'] = ROOT.kGreen
colors['mumu_slice3'] = ROOT.kYellow
colors['mumu_slice4'] = ROOT.kOrange
colors['mumu_slice5'] = ROOT.kGreen
colors['mumu_slice6'] = ROOT.kCyan
colors['mumu_slice7'] = ROOT.kBlack

plots = {}
plots['Hmumu_analysis'] = {
                            'signal':{
                                    'mumu_slice1':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_0_100' ],
                                    'mumu_slice2':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_100_300' ],
                                    'mumu_slice3':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_300_500' ],
                                    'mumu_slice4':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_500_700' ],
                                    'mumu_slice5':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_700_900' ],
                                    'mumu_slice6':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100' ],
                                    'mumu_slice7':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000' ],
                                    },
           }

legend = {}
legend['mumu_slice1'] = 'HT_0_100'
legend['mumu_slice2'] = 'HT_100_300'
legend['mumu_slice3'] = 'HT_300_500'
legend['mumu_slice4'] = 'HT_500_700'
legend['mumu_slice5'] = 'HT_700_900'
legend['mumu_slice6'] = 'HT_900_1100'
legend['mumu_slice7'] = 'HT_1100_100000'



