from common_defaults import deffccdicts

#python FCChhAnalyses/FCChh/ttHH/dataframe/finalSel.py 
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "FCChh/ttHH/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCC_procDict_fcc_v04.json"

process_list=['mgp8_pp_tthh_lambda100_5f',
              'mgp8_pp_ttz_5f',
              'mgp8_pp_ttzz_5f',
              'mgp8_pp_tth01j_5f'
              ]

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"seljet_pT.size()>0",
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "jet_pt_1":{"name":"seljet_pT","title":"jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
}

###Number of CPUs to use
NUM_CPUS = 5

###This part is standard to all analyses
sys.path.append('./bin')
import runDataFrameFinal as rdf
#import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)
