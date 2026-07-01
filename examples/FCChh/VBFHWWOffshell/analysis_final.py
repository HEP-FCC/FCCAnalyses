#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Offshell_HWW_Analysis/"

#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Offshell_HWW_Analysis/final/"

processList = {
    'mgp8_pp_vbf_ww_lvlv_5f_100TeV':{}, #output file from analysis_stage1.py
    'mgp8_pp_vbf_h_jjlvlv_5f_100TeV':{}, #output file from analysis_stage1.py
    'mgp8_pp_vbf_ww_lvlv_SBI_offshell_5f_100TeV':{}, #output file from analysis_stage1.py
}

#Link to the dictionary that contains all the cross section informations etc...
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v06_II.json"
#Note the numbeOfEvents and sumOfWeights are placeholders that get overwritten with the correct values in the samples

#How to add a process that is not in the official dictionary:
# procDictAdd={"pwp8_pp_hh_5f_hhbbyy": {"numberOfEvents": 4980000, "sumOfWeights": 4980000.0, "crossSection": 0.0029844128399999998, "kfactor": 1.075363, "matchingEfficiency": 1.0}}

# Expected integrated luminosity
intLumi = 30e+06  # pb-1

# Whether to scale to expected integrated luminosity
doScale = True

#Number of CPUs to use
nCPUS = 2

#produces ROOT TTrees, default is False
doTree = True

saveTabular = True

# Optional: Use weighted events
do_weighted = True 

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
            "sel0_truthW":"n_mc_Ws > 0", #ask for at least one truth W, should have 100% efficiency (placeholder cut)
            "sel1_W_pair":"n_W_pairs > 0", #require one W pair at least so the mWW plot makes sense
            }

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "m_WW_full":{"name":"m_WW_from_pairs","title":"m_{W^{+}W^{-}} [GeV]","bin":50,"xmin":0,"xmax":2000.},
    "m_WW_zoom":{"name":"m_WW_from_pairs","title":"m_{W^{+}W^{-}} [GeV]","bin":50,"xmin":95,"xmax":400},

    "n_mc_higgses":{"name":"n_mc_higgses","title":"n Higgses","bin":5,"xmin":0.,"xmax":5.},
    "n_mc_Ws":{"name":"n_mc_Ws","title":"n Ws","bin":25,"xmin":0.,"xmax":25.},
    "n_W_pairs":{"name":"n_W_pairs","title":"n W^{+}W^{-} pairs","bin":50,"xmin":0.,"xmax":50.},
    "n_Ws_from_Higgs":{"name":"n_Ws_from_Higgs","title":"n Ws from Higgs","bin":5,"xmin":0.,"xmax":5.},
}