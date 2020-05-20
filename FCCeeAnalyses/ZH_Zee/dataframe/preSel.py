#python FCCeeAnalyses/ZH_Zmumu/dataframe/preSel.py 

basedir="/afs/cern.ch/work/h/helsens/public/FCCDicts/yaml/FCCee/fcc_v01/"
outdir="FCCee/ZH_Zmumu/"
NUM_CPUS = 15
process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']
fraction=0.01

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
