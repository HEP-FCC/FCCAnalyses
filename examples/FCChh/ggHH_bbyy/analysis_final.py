#Input directory where the files produced at the pre-selection level are
inputDir  = "outputs/FCChh/ggHH_bbyy/presel/"

#Input directory where the files produced at the pre-selection level are
outputDir  = "outputs/FCChh/ggHH_bbyy/final/"

processList = {
    'pwp8_pp_hh_5f_hhbbyy':{},#Run over the full statistics from stage2 input file <inputDir>/p8_ee_ZZ_ecm240.root. Keep the same output name as input
}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json" # will need an FCC-hh one!

#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process TO UPDATE 
procDictAdd={"pwp8_pp_hh_5f_hhbbyy":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 1.0, "kfactor": 1.0, "matchingEfficiency": 1.0}}

#Number of CPUs to use
nCPUS = 2

#produces ROOT TTrees, default is False
doTree = True

saveTabular = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
            "sel0_myy":"m_yy[0] > 100. && m_yy[0] < 180.",
            "sel1_mbb":"(m_yy[0] > 100. && m_yy[0] < 180.) && (m_bb[0] > 80. && m_bb[0] < 200.)",
            }


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "myy":{"name":"m_yy","title":"m_{#gamma#gamma} [GeV]","bin":50,"xmin":0,"xmax":200},
    "myy_zoom":{"name":"m_yy","title":"m_{#gamma#gamma} [GeV]","bin":50,"xmin":100,"xmax":180},
    "y1_pT":{"name":"g1_pt","title":"pT_{#gamma1} [GeV]","bin":50,"xmin":0.,"xmax":200.},
    "y2_pT":{"name":"g2_pt","title":"pT_{#gamma2} [GeV]","bin":50,"xmin":0.,"xmax":200.},
    "pT_y1_vs_y2_2D":{"cols":["g1_pt", "g2_pt"],"title":"m_{Z} - leptonic recoil [GeV]", "bins": [(40,80,100), (100,120,140)]}, # 2D histogram
}