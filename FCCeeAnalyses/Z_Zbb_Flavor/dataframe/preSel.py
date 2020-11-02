from common_defaults import deffccdicts
 #python FCCeeAnalyses/Z_Zbb_Flavor/dataframe/preSel.py 
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp/"
outdir="/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Flavor/"
NUM_CPUS = 30
process_list=['p8_ee_Zbb_ecm91', 'p8_ee_Zcc_ecm91', 'p8_ee_Zbb_ecm91_EvtGen_Bu2D0Pi']
fraction=0.1

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
