#python FCCeeAnalyses/ZH_Zmumu/dataframe/preSel.py 

from common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_v02/"
basedir='https://fcc-physics-events.web.cern.ch/fcc-physics-events/sharedFiles/FCCee/fcc_v02/'
outdir="FCCee/ZH_Zmumu/"

NUM_CPUS = 15
process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']
fraction=0.01

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
