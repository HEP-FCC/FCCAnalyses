#python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py 
import ROOT

baseDir  = "/afs/cern.ch/user/h/helsens/FCCsoft/FCCAnalyses/FCCee/ZH_Zmumu/"
procDict = "/afs/cern.ch/work/h/helsens/public/FCCDicts/FCCee_procDict_fcc_v01.json"

NUM_CPUS = 5
process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']

cut_list = ['zed_leptonic_m.size() > 0',
            'zed_leptonic_m.size() > 0 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100',
            'zed_leptonic_m.size() > 0 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && nbjets>1']


### variable list
variables = {
    "mz":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom":{"name":"zed_leptonic_m","title":"m_{Z} [GeV]","bin":40,"xmin":80,"xmax":100},
    "nbjets":{"name":"nbjets","title":"number of bjets","bin":10,"xmin":0,"xmax":10},
}


import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)
