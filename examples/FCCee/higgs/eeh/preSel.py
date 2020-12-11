#python examples/FCCee/higgs/eeh/preSel.py

from config.common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp/"
outdir="FCCee/eeH/"
NUM_CPUS = 15
process_list=[

    'p8_ee_Z_Zqq_ecm125',
    'p8_ee_Z_Zbb_ecm125',
    'p8_ee_Z_Zcc_ecm125',
    #'p8_ee_H_Htautau_ecm125',
    #'p8_ee_H_Hcc_ecm125',
    #'p8_ee_WW_ecm125',
    #'p8_ee_Z_Ztautau_ecm125',
    #'p8_ee_ZZ_ecm125',
    'p8_ee_H_Hgg_ecm125',
    #'p8_ee_H_Hbb_ecm125',


              ]
fraction=0.5

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
