#python FCCeeAnalyses/ZH_Zmumu/dataframe/preSel.py 

from common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp/"
outdir="FCCee/ttbar/"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)

process_list=['p8_ee_ZZ_ecm365','p8_ee_WW_ecm365','p8_ee_ZH_ecm365', 'p8_ee_tt_ecm365']
fraction=0.5

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
