#python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py 
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "FCCee/Z_Zmumu/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "/afs/cern.ch/work/h/helsens/public/FCCDicts/FCCee_procDict_fcc_v01.json"

process_list=['p8_ee_Z_Zmumu_ecm91','wizhardp8_ee_Z_Zmumu_ecm91']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"zed_leptonic_m.size() == 1",
            "sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100",
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "mz":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":100,"xmin":80,"xmax":100},
    "mz_zoom2":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":200,"xmin":88,"xmax":92},
    "mz_zoom3":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":400,"xmin":90,"xmax":94},
}

###Number of CPUs to use
NUM_CPUS = 10

###This part is standard to all analyses
import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)
