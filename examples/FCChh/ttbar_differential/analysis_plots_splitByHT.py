import ROOT
#plot the mumu bkg sample in the separate HT slices

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttbar analysis '
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-hh'
inputDir       = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/ttbar_diff_analysis/final/'
formats        = ['png']
# formats        = ['png','pdf']
# yaxis          = ['log']
yaxis          = ['lin','log']
# stacksig       = ['stack']
stacksig       = ['stack','nostack']
outdir         = './plots_ttbar_splitByHT/'
plotStatUnc    = True

variables = ['HT','pT_bjets', 'MET']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttbar_diff_analysis']   = ["sel1_bjets"]

extralabel = {}
extralabel['sel1_bjets'] = ">= 1 b-jet"

colors = {}
colors['ttbar_slice1'] = ROOT.kCyan
colors['ttbar_slice2'] = ROOT.kCyan+3
colors['ttbar_slice3'] = ROOT.kBlue
colors['ttbar_slice4'] = ROOT.kViolet+5
colors['ttbar_slice5'] = ROOT.kMagenta
colors['ttbar_slice6'] = ROOT.kRed-7
colors['ttbar_slice7'] = ROOT.kOrange+7
colors['ttbar_slice8'] = ROOT.kYellow-7
colors['ttbar_slice9'] = ROOT.kGreen
colors['ttbar_slice10'] = ROOT.kGray

plots = {}
plots['ttbar_diff_analysis'] = {
                            'backgrounds':{
                                    'ttbar_slice1':[ 'mgp8_pp_tt012j_5f_HT_0_600' ],
                                    'ttbar_slice2':[ 'mgp8_pp_tt012j_5f_HT_600_1200' ],
                                    'ttbar_slice3':[ 'mgp8_pp_tt012j_5f_HT_1200_2100' ],
                                    'ttbar_slice4':[ 'mgp8_pp_tt012j_5f_HT_2100_3400' ],
                                    'ttbar_slice5':[ 'mgp8_pp_tt012j_5f_HT_3400_5300' ],
                                    'ttbar_slice6':[ 'mgp8_pp_tt012j_5f_HT_5300_8100' ],
                                    'ttbar_slice7':[ 'mgp8_pp_tt012j_5f_HT_8100_15000' ],
                                    'ttbar_slice8':[ 'mgp8_pp_tt012j_5f_HT_15000_25000' ],
                                    'ttbar_slice9':[ 'mgp8_pp_tt012j_5f_HT_25000_35000' ],
                                    'ttbar_slice10':[ 'mgp8_pp_tt012j_5f_HT_35000_100000' ],
                                    },
           }

legend = {}
legend['ttbar_slice1'] = 'HT_0_600'
legend['ttbar_slice2'] = 'HT_600_1200'
legend['ttbar_slice3'] = 'HT_1200_2100'
legend['ttbar_slice4'] = 'HT_2100_3400'
legend['ttbar_slice5'] = 'HT_3400_5300'
legend['ttbar_slice6'] = 'HT_5300_8100'
legend['ttbar_slice7'] = 'HT_8100_15000'
legend['ttbar_slice8'] = 'HT_15000_25000'
legend['ttbar_slice9'] = 'HT_25000_35000'
legend['ttbar_slice10'] = 'HT_35000_100000'



