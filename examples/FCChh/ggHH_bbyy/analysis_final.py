#Input directory where the files produced at the pre-selection level are
inputDir  = "outputs/FCChh/ggHH_bbyy/presel/"

#Input directory where the files produced at the pre-selection level are
outputDir  = "outputs/FCChh/ggHH_bbyy/final/"

processList = {
    'pwp8_pp_hh_5f_hhbbyy':{}, #output file from analysis_stage1.py
}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "/eos/experiment/fcc/hh/tutorials/edm4hep_tutorial_data/FCChh_procDict_tutorial.json"
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
            "sel0_myy":"m_yy[0] > 100. && m_yy[0] < 180.",
            "sel1_mbb":"(m_yy[0] > 100. && m_yy[0] < 180.) && (m_bb[0] > 80. && m_bb[0] < 200.)",
            }

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "myy":{"name":"m_yy","title":"m_{#gamma#gamma} [GeV]","bin":50,"xmin":0,"xmax":200},
    "myy_zoom":{"name":"m_yy","title":"m_{#gamma#gamma} [GeV]","bin":50,"xmin":100,"xmax":180},
    "mbb":{"name":"m_bb","title":"m_{bb} [GeV]","bin":50,"xmin":0,"xmax":250},
    "mbb_zoom":{"name":"m_bb","title":"m_{b} [GeV]","bin":50,"xmin":80,"xmax":200},
    "y1_pT":{"name":"g1_pt","title":"pT_{#gamma1} [GeV]","bin":50,"xmin":0.,"xmax":200.},
    "y2_pT":{"name":"g2_pt","title":"pT_{#gamma2} [GeV]","bin":50,"xmin":0.,"xmax":200.},
    "pT_y1_vs_y2_2D":{"cols":["g1_pt", "g2_pt"],"title":"m_{Z} - leptonic recoil [GeV]", "bins": [(40,80,100), (100,120,140)]}, # 2D histogram
}