from common_defaults import deffccdicts

#python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py 
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "FCCee/ttbar/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_tmp.json"

process_list=['p8_ee_ZZ_ecm365','p8_ee_WW_ecm365','p8_ee_ZH_ecm365', 'p8_ee_tt_ecm365']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"selected_muons_pt.size() == 1"
            }

###Optinally Define new variables
define_list = {"selmuon_pT_0":"selected_muons_pt.at(0)"}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "muon_pt":{"name":"selmuon_pT_0","title":"leading muon pT [GeV]","bin":100,"xmin":0,"xmax":100},
}

###Number of CPUs to use
NUM_CPUS = 5

###This part is standard to all analyses
sys.path.append('./bin')
import runDataFrameFinal as rdf
#import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables,defines=define_list)
myana.run(ncpu=NUM_CPUS)
