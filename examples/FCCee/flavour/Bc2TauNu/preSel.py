

#python examples/FCCee/flavour/generic-analysis/preSel.py

from config.common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp_v03/"
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)
process_list=[
    #'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
    #'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU',    
    'p8_ee_Zbb_ecm91',
    'p8_ee_Zcc_ecm91',
    'p8_ee_Zuds_ecm91'
]

output_list=[]

fraction=1.

#import config.runDataFrame as rdf
#myana=rdf.runDataFrame(basedir,process_list, outlist=output_list)
#myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)

import config.runDataFrameBatch as rdf
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=200 ,outDir=outdir)
