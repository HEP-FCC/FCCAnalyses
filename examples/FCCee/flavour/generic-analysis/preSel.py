#python examples/FCCee/flavour/generic-analysis/preSel.py

from config.common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp_v02/"
outdir="outputs/FCCee/flavour/generic-analysis/"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)
process_list=[
    'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
    #'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
]

output_list=['p8_ee_Zbb_ecm91']
#output_list=[]

fraction=0.05

import config.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list, outlist=output_list)
#myana=rdf.runDataFrame(basedir,process_list, outlist=[])
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
