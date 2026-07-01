#ANALYSIS OF THE 4MU FINAL STATE ONLY FOR NOW 

#Temporary hack to support command line argument at this stage:
energy_point = "100TeV"
import sys

if len(sys.argv) < 4:
    print("Missing command line argument for the energy point - going to use 100 TeV as default.")

else:
    print("Using energy point", sys.argv[3])
    energy_point = sys.argv[3]

#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/H4l_analysis/{}".format(energy_point)

#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/H4l_analysis/{}/final/".format(energy_point)

processList = {}

if energy_point == "100TeV":
    processList = {
        # @ 100 TeV
        'mgp8_pp_h012j_5f_hllll':{}, 
        'mgp8_pp_vbf_h01j_5f_hllll':{}, 
        'mgp8_pp_tth01j_5f_hllll':{}, 
        'mgp8_pp_vh012j_5f_hllll':{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_0_200':{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_200_500':{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_500_1100':{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_1100_100000':{}, 
    }

elif energy_point == "84TeV" or energy_point == "72TeV" or energy_point == "120TeV":
    processList = {
        # @ 84 TeV
        'mgp8_pp_h012j_5f_{}_hllll'.format(energy_point):{}, 
        'mgp8_pp_vbf_h01j_5f_{}_hllll'.format(energy_point):{}, 
        'mgp8_pp_tth01j_5f_{}_hllll'.format(energy_point):{}, 
        'mgp8_pp_vh012j_5f_{}_hllll'.format(energy_point):{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_0_200_{}'.format(energy_point):{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_200_500_{}'.format(energy_point):{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_500_1100_{}'.format(energy_point):{}, 
        'mgp8_pp_llll01j_mhcut_5f_HT_1100_100000_{}'.format(energy_point):{}, 
    }

else:
    raise Exception("Unsupported argumente for energy! Currently only support 100TeV, 84TeV, 72TeV and 120TeV!")

#Link to the dictonary that contains all the cross section informations etc...
# procDict = "/afs/cern.ch/user/b/bistapf/main_FCCAnalyses/FCCAnalyses/FCChh_dict_local.json" #old handwritten
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json" #autogen by EventProducer
#Note the numbeOfEvents and sumOfWeights are placeholders that get overwritten with the correct values in the samples

#How to add a process that is not in the official dictionary:
# procDictAdd={"pwp8_pp_hh_5f_hhbbyy": {"numberOfEvents": 4980000, "sumOfWeights": 4980000.0, "crossSection": 0.0029844128399999998, "kfactor": 1.075363, "matchingEfficiency": 1.0}}

# Expected integrated luminosity
intLumi = 30e+06  # pb-1

if energy_point == "72TeV":
    print("Rescaling lumi to 72 TeV F12PU scenario!")
    intLumi = 30e+06*1300./940. #using the F12PU scenario

if energy_point == "120TeV":
    print("Rescaling lumi to 120 TeV F20 scenario!")
    intLumi = 30e+06*370./940. #using the F12PU scenario


# Whether to scale to expected integrated luminosity
doScale = True

#Number of CPUs to use
nCPUS = 4

#produces ROOT TTrees, default is False
doTree = True

saveTabular = True

# Optional: Use weighted events -> NOT NEEDED ALL SAMPLES ARE @LO
do_weighted = False 

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
            "sel1_Z4l_cand":"ZZ_llll_flavour[0] == 1", 
            "sel2_Zll_minv":"(ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.) ", #FIX THE NAMES !!!!
            "sel3_pTH50":"(pT_llll[0] > 50.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH100":"(pT_llll[0] > 100.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH150":"(pT_llll[0] > 150.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH200":"(pT_llll[0] > 200.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH250":"(pT_llll[0] > 250.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH300":"(pT_llll[0] > 300.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH350":"(pT_llll[0] > 350.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH400":"(pT_llll[0] > 400.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH450":"(pT_llll[0] > 450.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            "sel3_pTH500":"(pT_llll[0] > 500.) && (ZZ_llll_flavour[0] == 1) && (m_ll_leading[0] > 40. && m_ll_leading[0] < 120. && m_ll_subleading[0] > 12. && m_ll_subleading[0] < 120.)", # increasing pT cuts on the pTmumu 
            }

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "Z4l_flavour_flag":{"name":"ZZ_llll_flavour","title":"Flavour of Z4l decay","bin":5,"xmin":0,"xmax":5},
    "m_4mu":{"name":"m_llll","title":"m_{4#mu} [GeV]","bin":50,"xmin":75,"xmax":200},
    "m_4mu_zoom":{"name":"m_llll","title":"m_{4#mu} [GeV]","bin":100,"xmin":120,"xmax":130},
    "m_4mu_fitrange":{"name":"m_llll","title":"m_{4#mu} [GeV]","bin":30,"xmin":110,"xmax":140},
    "m_4mu_1bin":{"name":"m_llll","title":"m_{4#mu} [GeV]","bin":1,"xmin":124,"xmax":126},
    "m_mumu_lead":{"name":"m_ll_leading","title":"m_{#mu#mu} (leading) [GeV]","bin":50,"xmin":30.,"xmax":130.},
    "m_mumu_sublead":{"name":"m_ll_subleading","title":"m_{#mu#mu} (subleading) [GeV]","bin":50,"xmin":30.,"xmax":130.},
    "pT_4mu":{"name":"pT_llll","title":"pT_{4#mu} [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_4mu_full":{"name":"pT_llll","title":"pT_{4#mu} [GeV]","bin":12,"xmin":0.,"xmax":1200.},
    "pT_2mu_lead":{"name":"pT_ll_leading","title":"pT_{#mu#mu} (leading) [GeV]","bin":50,"xmin":0.,"xmax":200.},
    "pT_2mu_sublead":{"name":"pT_ll_subleading","title":"pT_{#mu#mu} (subleading) [GeV]","bin":50,"xmin":0.,"xmax":200.},
}