#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/ttHyy_analysis/"

#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/ttHyy_analysis/final/"

processList = {
    #Signal
    # 'mgp8_pp_tth01j_5f_haa':{}, #output file from analysis_stage1.py
    #Backgrounds
    # 'mgp8_pp_jjaa_5f':{}, #output file from analysis_stage1.py
    'mgp8_pp_ttaa_semilep_5f_100TeV':{}, #output file from analysis_stage1.py
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
            "sel1_bjets":"n_bjets > 1", # at least two b-jets 
            "sel2_photons":"n_bjets > 1 && n_photons > 1", # at least two b-jets, and two photons
            # add more cuts here: note you need to && them, they are not sequential!
            }

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "n_photons":{"name":"n_photons","title":"Number of photons","bin":10,"xmin":0.,"xmax":10.},
    "n_bjets":{"name":"n_bjets","title":"Number of b-jets","bin":10,"xmin":0.,"xmax":10.},
    "m_yy":{"name":"m_yy","title":"m_{#gamma#gamma}","bin":30,"xmin":110.,"xmax":140.},
}