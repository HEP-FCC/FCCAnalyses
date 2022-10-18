#Input directory where the files produced at the pre-selection level are
inputDir  = "Tau3Mu/"

#Input directory where the files produced at the pre-selection level are
outputDir  = "Tau3Mu/final/"


processList = {
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu':{}, #Run over the full statistics from stage2 input file <inputDir>/xx.root. Keep the same output name as input
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu':{}
}


#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"

#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
#procDictAdd={"MySample_p8_ee_ZH_ecm240":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.201868, "kfactor": 1.0, "matchingEfficiency": 1.0}}

#Number of CPUs to use
nCPUS = 2

#produces ROOT TTrees, default is False
doTree = False

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {"nocut":"true",
           "sel0":"n_triplets_m > 0",
           "sel1":"Min( TauMass_allCandidates ) < 3"
            }


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mTau":{"name":"TauMass_allCandidates","title":"m_{tau} [GeV]","bin":100,"xmin":0,"xmax":5},
    "mTau_zoom":{"name":"TauMass_allCandidates","title":"m_{tau} [GeV]","bin":100,"xmin":1.7,"xmax":1.9},
    "Evis":{"name":"visible_energy","title":"E_{vis} [GeV]","bin":100,"xmin":0,"xmax":100},
}
