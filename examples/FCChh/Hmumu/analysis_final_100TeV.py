import sys

print(sys.argv)
print(sys.argv[3])
exit()

#Input directory where the files produced at the pre-selection level are
# inputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Hmumu_valid/"
inputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/Hmumu_analysis/100TeV/"

#Input directory where the files produced at the pre-selection level are
# outputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Hmumu_valid/final/"
outputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/Hmumu_analysis/100TeV/final/"

processList = {
    # @ 100 TeV
    'mgp8_pp_h012j_5f_hmumu':{}, 
    'mgp8_pp_vbf_h01j_5f_hmumu':{}, 
    'mgp8_pp_tth01j_5f_hmumu':{}, 
    'mgp8_pp_vh012j_5f_hmumu':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_0_100':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_100_300':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_300_500':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_500_700':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_700_900':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100':{}, 
    'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000':{}, 
}

#Link to the dictonary that contains all the cross section informations etc...
# procDict = "/afs/cern.ch/user/b/bistapf/main_FCCAnalyses/FCCAnalyses/FCChh_dict_local.json" #old handwritten
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json" #autogen by EventProducer
#Note the numbeOfEvents and sumOfWeights are placeholders that get overwritten with the correct values in the samples

#How to add a process that is not in the official dictionary:
# procDictAdd={"pwp8_pp_hh_5f_hhbbyy": {"numberOfEvents": 4980000, "sumOfWeights": 4980000.0, "crossSection": 0.0029844128399999998, "kfactor": 1.075363, "matchingEfficiency": 1.0}}

# Expected integrated luminosity
intLumi = 30e+06  # pb-1

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
            "sel1_mumupair":"n_os_muon_pairs > 0", 
            "sel2_mH":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.)", #FIX THE NAMES !!!!
            "sel3_pTH50":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 50.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH100":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 100.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH150":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 150.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH200":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 200.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH250":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 250.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH300":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 300.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH350":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 350.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH400":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 400.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH450":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 450.) ", # increasing pT cuts on the pTmumu 
            "sel3_pTH500":"(n_os_muon_pairs > 0) && (m_mumu[0] > 124. && m_mumu[0] < 126.) && (pT_mumu[0] > 500.) ", # increasing pT cuts on the pTmumu 
            "sel_extra_njets0":"(n_os_muon_pairs > 0) && (n_jets == 0)", # tester selection for the split HT samples
            "sel_extra_njets1":"(n_os_muon_pairs > 0) && (n_jets > 0)", # tester selection for the split HT samples
            }

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "m_mumu":{"name":"m_mumu","title":"m_{#mu#mu} [GeV]","bin":50,"xmin":75,"xmax":200},
    "m_mumu_zoom":{"name":"m_mumu","title":"m_{#mu#mu} [GeV]","bin":100,"xmin":110,"xmax":140},
    "m_mumu_1bin":{"name":"m_mumu","title":"m_{#mu#mu} [GeV]","bin":1,"xmin":124,"xmax":126},
    "pT_mumu":{"name":"pT_mumu","title":"pT_{#mu#mu} [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_mumu_full":{"name":"pT_mumu","title":"pT_{#mu#mu} [GeV]","bin":12,"xmin":0.,"xmax":1200.},
    "pT_muplus":{"name":"mu_plus_pt","title":"pT_{#mu^+} [GeV]","bin":50,"xmin":0.,"xmax":200.},
    "pT_muminus":{"name":"mu_minus_pt","title":"pT_{#mu^-} [GeV]","bin":50,"xmin":0.,"xmax":200.},
}