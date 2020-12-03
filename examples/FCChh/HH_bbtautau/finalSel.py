from common_defaults import deffccdicts

#python FCChhAnalyses/FCChh/ttHH/dataframe/finalSel.py 
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "FCChh/HH_bbtautau/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCC_procDict_fcc_v04.json"

process_list=['pwp8_pp_hh_lambda100_5f_hhbbaa',
              'mgp8_pp_bbtata_QED',
              'mgp8_pp_bbtata_QCDQED',
              'mgp8_pp_tt012j_5f',
              ]

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"seljet_pT.size()>6",
            }

###Optinally Define new variables
define_list = {"seljet_pT_0":"seljet_pT.at(0)",
               "seljet_pT_1":"seljet_pT.at(1)",
               "seljet_pT_2":"seljet_pT.at(2)",
               "seljet_pT_3":"seljet_pT.at(3)",
               "seljet_pT_4":"seljet_pT.at(4)",
               "seljet_pT_5":"seljet_pT.at(5)"}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "jet_pt_0":{"name":"seljet_pT_0","title":"Leading jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
    "jet_pt_1":{"name":"seljet_pT_1","title":"Sub leading jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
    "jet_pt_2":{"name":"seljet_pT_2","title":"3rd jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
    "jet_pt_3":{"name":"seljet_pT_3","title":"4th jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
    "jet_pt_4":{"name":"seljet_pT_4","title":"5th jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
    "jet_pt_5":{"name":"seljet_pT_5","title":"6th jet p_{T} [GeV]","bin":100,"xmin":0,"xmax":4000},
}

###Number of CPUs to use
NUM_CPUS = 5

###This part is standard to all analyses
sys.path.append('./bin')
import runDataFrameFinal as rdf
#import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables,defines=define_list)
myana.run(ncpu=NUM_CPUS)
