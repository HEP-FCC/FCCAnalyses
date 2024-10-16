import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow HH #rightarrow b #bar{b} #gamma #gamma '
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-hh'
inputDir       = 'outputs/FCChh/ggHH_bbyy/final/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
# stacksig       = ['stack','nostack']
outdir         = 'outputs/FCChh/ggHH_bbyy/plots/'
plotStatUnc    = True

variables = ['myy','myy_zoom', 'mbb', 'mbb_zoom', 'y1_pT','y2_pT']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['bbyy_analysis']   = ["sel0_myy","sel1_mbb"]

extralabel = {}
extralabel['sel0_myy'] = "Sel.: 100 < m_{#gamma#gamma} < 180 GeV"
extralabel['sel1_mbb'] = "Sel.: 100 < m_{#gamma#gamma} < 180 GeV and 80 < m_{bb} < 200 GeV"

colors = {}
colors['bbyy_signal'] = ROOT.kRed

plots = {}
plots['bbyy_analysis'] = {'signal':{'bbyy_signal':['pwp8_pp_hh_5f_hhbbyy']},
           }

legend = {}
legend['bbyy_signal'] = 'HH'