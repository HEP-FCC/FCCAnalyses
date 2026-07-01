import ROOT

#Temporary hack to support command line argument at this stage:
energy_point = "100TeV"
import sys

if len(sys.argv) < 4:
    print("Missing command line argument for the energy point - going to use 100 TeV as default.")

else:
    print("Using energy point", sys.argv[3])
    energy_point = sys.argv[3]


# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow H #rightarrow #mu#mu analysis '
delphesVersion = '3.4.2'
energy         = int(energy_point.replace("TeV", ""))
collider       = 'FCC-hh'
inputDir       = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/H4l_analysis/{}/final/'.format(energy_point)
formats        = ['png','pdf']
yaxis          = ['log']
# yaxis          = ['lin','log']
stacksig       = ['stack', 'nostack']
outdir         = '/eos/user/b/bistapf/plots_H4mu_pTbinned_{}/'.format(energy_point)
plotStatUnc    = True

variables = ['m_4mu_fitrange']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Hmumu_analysis']   = ["sel3_pTH50_100", "sel3_pTH100_150", 
                                    "sel3_pTH150_200", "sel3_pTH200_250", "sel3_pTH250_300", "sel3_pTH300_350",
                                    "sel3_pTH350_400", "sel3_pTH400_450", "sel3_pTH450_500", "sel3_pTH500_550" ]

extralabel = {}
extralabel['sel1_mumupair'] = "Pre-selected events"
extralabel['sel2_mH'] = "Selected events"
extralabel['sel3_pTH50_100'] = " 50 < p_{T}(#mu#mu) < 100 GeV"
extralabel['sel3_pTH100_150'] = " 100 < p_{T}(#mu#mu) < 150 GeV"
extralabel['sel3_pTH150_200'] = " 150 < p_{T}(#mu#mu) < 200 GeV"
extralabel['sel3_pTH200_250'] = " 200 < p_{T}(#mu#mu) < 250 GeV"
extralabel['sel3_pTH250_300'] = " 250 < p_{T}(#mu#mu) < 300 GeV"
extralabel['sel3_pTH300_350'] = " 300 < p_{T}(#mu#mu) < 350 GeV"
extralabel['sel3_pTH350_400'] = " 350 < p_{T}(#mu#mu) < 400 GeV"
extralabel['sel3_pTH400_450'] = " 400 < p_{T}(#mu#mu) < 450 GeV"
extralabel['sel3_pTH450_500'] = " 450 < p_{T}(#mu#mu) < 500 GeV"
extralabel['sel3_pTH500_550'] = " p_{T}(#mu#mu)} > 500 GeV"


colors = {}
colors['ggH_mumu_signal'] = 46
colors['mumu_cont'] = 36

plots = {}
if "100TeV" in energy_point:
    plots['Hmumu_analysis'] = {
                                'signal':{'ggH_mumu_signal':[ 
                                                            'mgp8_pp_h012j_5f_hllll',
                                                            'mgp8_pp_tth01j_5f_hllll',
                                                            'mgp8_pp_vbf_h01j_5f_hllll',
                                                            'mgp8_pp_vh012j_5f_hllll',
                                ]},
                                'backgrounds':{'mumu_cont':[ 'mgp8_pp_llll01j_mhcut_5f_HT_0_200', 
                                                            'mgp8_pp_llll01j_mhcut_5f_HT_200_500',
                                                            'mgp8_pp_llll01j_mhcut_5f_HT_500_1100',
                                                            'mgp8_pp_llll01j_mhcut_5f_HT_1100_100000',
                                                            ]},
            }

else:
    plots['Hmumu_analysis'] = {
                                'signal':{'ggH_mumu_signal':[ 
                                                            'mgp8_pp_h012j_5f_{}_hllll'.format(energy_point),
                                                            'mgp8_pp_vbf_h01j_5f_{}_hllll'.format(energy_point),
                                                            'mgp8_pp_tth01j_5f_{}_hllll'.format(energy_point),
                                                            'mgp8_pp_vh012j_5f_{}_hllll'.format(energy_point),
                                ]},
                                'backgrounds':{'mumu_cont':[ 'mgp8_pp_llll01j_mhcut_5f_HT_0_200_{}'.format(energy_point), 
                                                            'mgp8_pp_llll01j_mhcut_5f_HT_200_500_{}'.format(energy_point),
                                                            'mgp8_pp_llll01j_mhcut_5f_HT_500_1100_{}'.format(energy_point),
                                                            'mgp8_pp_llll01j_mhcut_5f_HT_1100_100000_{}'.format(energy_point),
                                                            ]},
            }

legend = {}
legend['ggH_mumu_signal'] = 'H #rightarrow 4#mu'
legend['mumu_cont'] = '4#mu cont.'