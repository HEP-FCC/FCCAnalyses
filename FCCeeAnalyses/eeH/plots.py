import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
scaleSig       = 1000000. #in pb-1
ana_tex        = "e^{+}e^{-} #rightarrow H #rightarrow gg"
delphesVersion = "3.4.2"
energy         = 125.0
collider       = "FCC-ee"
inputDir       = "FCCee/eeH/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'FCCee/eeH/plots/'

variables = ["thrust_x","thrust_y","thrust_z","thrust_val","hemis_0","hemis_1"]

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['eeHgg']   = ["sel0"]

extralabel = {}
extralabel['sel0'] = "Selection:NrecP>0"

colors = {}
colors['Hgg'] = ROOT.kRed
colors['Zqq'] = ROOT.kBlue+1

plots = {}
plots['eeHgg'] = {'signal':{'Hgg':['p8_ee_H_Hgg_ecm125']},
                  'backgrounds':{'Zqq':['p8_ee_Z_Zqq_ecm125']}
            }

legend = {}
legend['Hgg'] = 'Hgg*10^{6}'
legend['Zqq'] = 'Zqq'

