
flavor = "mumu" # mumu, ee

#Input directory where the files produced at the pre-selection level are
inputDir   = f"outputs/FCCee/higgs/mass-xsec/preselection/{flavor}/"

#Input directory where the files produced at the pre-selection level are
#Optional: output directory, default is local running directory
outputDir   = f"outputs/FCCee/higgs/mass-xsec/final_selection/{flavor}/"

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
sel0 = "(zll_m > 86 && zll_m < 96)"
sel1 = "(zll_p > 20 && zll_p < 70)"
sel2 = "(cosTheta_miss < 0.98)"
sel3 = "(zll_recoil_m < 140 && zll_recoil_m > 120)"
cutList = {
    "sel0": f"{sel0}",
    "sel1": f"{sel0} && {sel1}",
    "sel2": f"{sel0} && {sel1} && {sel2}",
    "sel3": f"{sel0} && {sel1} && {sel2} && {sel3}"
}


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "zll_m":{"cols": ["zll_m"], "title": "m_{Z} (GeV)", "bins": [(250,0,250)]},
    "zll_p":{"cols": ["zll_p"], "title": "p_{Z} (GeV)", "bins": [(250,0,250)]},
    "zll_recoil_m":{"cols": ["zll_recoil_m"], "title": "Recoil (GeV)", "bins": [(250,0,250)]},
    "zll_recoil_m_final":{"cols": ["zll_recoil_m"], "title": "Recoil (GeV)", "bins": [(200,120,140)]},
}
