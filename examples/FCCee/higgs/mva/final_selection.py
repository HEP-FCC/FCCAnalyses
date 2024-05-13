

#Input directory where the files produced at the pre-selection level are
inputDir   = f"outputs/FCCee/higgs/mva/preselection/"

#Input directory where the files produced at the pre-selection level are
#Optional: output directory, default is local running directory
outputDir   = f"outputs/FCCee/higgs/mva/final_selection/"

# if no processList or empty dictionary provided, run over all ROOT files in the input directory
processList = {}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Number of CPUs to use
nCPUS = -1

#produces ROOT TTrees, default is False
doTree = False


# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 7200000.0 # 7.2 /ab

saveTabular = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "sel0": "1==1",
    "sel1": "mva_score[0] > 0.5",
}


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mva_score":{"cols": ["mva_score"], "title": "MVA score", "bins": [(100,0,1)]},
    "zmumu_m":{"cols": ["zmumu_m"], "title": "m_{Z} (GeV)", "bins": [(250,0,250)]},
    "zmumu_p":{"cols": ["zmumu_p"], "title": "p_{Z} (GeV)", "bins": [(250,0,250)]},
    "zmumu_recoil_m":{"cols": ["zmumu_recoil_m"], "title": "Recoil (GeV)", "bins": [(250,0,250)]},
    "zmumu_recoil_m_final":{"cols": ["zmumu_recoil_m"], "title": "Recoil (GeV)", "bins": [(200,120,140)]},
}
