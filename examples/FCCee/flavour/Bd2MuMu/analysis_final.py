#Input directory where the files produced at the pre-selection level are
inputDir   = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2MuMu/flatNtuples/spring2021/analysis_stage1/"
outputDir  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2MuMu/flatNtuples/spring2021/analysis_final/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"

###Number of CPUs to use
nCPUS = 8

processList = {
    'p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu':{},
    'p8_ee_Zbb_ecm91':{}
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {"sel0":"Bd2MuMu_mass>0"}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "EVT_CandMass"       :{"name":"Bd2MuMu_mass","title":"mass [GeV]","bin":300,"xmin":0,"xmax":6.},
    "EVT_CandMass_zoom"  :{"name":"Bd2MuMu_mass","title":"mass [GeV]","bin":100,"xmin":5.,"xmax":6.}
}
