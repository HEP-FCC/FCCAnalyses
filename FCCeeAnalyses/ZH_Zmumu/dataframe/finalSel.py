from common_defaults import deffccdicts

#python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py 
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "FCCee/ZH_Zmumu/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_v02.json"

process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"zed_leptonic_m.size() == 1",
            "sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100",
            "sel2":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && nbjets==2",
            "sel3":"zed_leptonic_m.size() == 1 && higgs_hadronic_b_m.size() ==1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && nbjets==2"
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "mz":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":40,"xmin":80,"xmax":100},
    "nbjets":{"name":"nbjets","title":"number of bjets","bin":10,"xmin":0,"xmax":10},
    "leptonic_recoil_m":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom2":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":120,"xmax":140},
    "higgs_hadronic_b_mass":{"name":"higgs_hadronic_b_m","title":"Higgs hadronic bb mass [GeV]","bin":100,"xmin":0,"xmax":200},
}

###Number of CPUs to use
NUM_CPUS = 10

###This part is standard to all analyses
import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)
