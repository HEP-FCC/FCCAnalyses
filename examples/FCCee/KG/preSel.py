#python examples/FCCee/KG/preSel.py

from config.common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021/IDEA/"
outdir="outputs/FCCee/KG/"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)

process_list=['p8_ee_Zuds_ecm91']
fraction=0.000001

import config.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
