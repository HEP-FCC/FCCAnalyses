import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow W^{+}W^{-} jj #rightarrow l#nu l#nu jj'
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-hh'
inputDir       = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Offshell_HWW_Analysis/final/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
# stacksig       = ['stack','nostack']
outdir         = './plots_VBF_HWW_offshell/'
plotStatUnc    = True

variables = ['m_WW_full','m_WW_zoom', 'n_mc_higgses', 'n_mc_Ws', 'n_W_pairs','n_Ws_from_Higgs']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['full_SBI_sample']   = ["sel0_truthW","sel1_W_pair"]
selections['signal_only_incl_offshell']   = ["sel0_truthW","sel1_W_pair"]
selections['SBI_offshell_signal_only']   = ["sel0_truthW","sel1_W_pair"]

extralabel = {}
extralabel['sel0_truthW'] = "At least one truth W"
extralabel['sel1_W_pair'] = "At least one truth W^{+}W{-} pair"

colors = {}
colors['ww_process'] = ROOT.kBlack

plots = {}
plots['full_SBI_sample'] = {'signal':{'ww_process':['mgp8_pp_vbf_ww_lvlv_5f_100TeV']},
           }
plots['signal_only_incl_offshell'] = {'signal':{'ww_process':['mgp8_pp_vbf_h_jjlvlv_5f_100TeV']},
           }
plots['SBI_offshell_signal_only'] = {'signal':{'ww_process':['mgp8_pp_vbf_ww_lvlv_SBI_offshell_5f_100TeV']},
           }

legend = {}
legend['ww_process'] = 'W^{+}W^{-}jj'