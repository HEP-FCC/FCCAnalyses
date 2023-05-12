#python FCChhAnalyses/FCChh/ttHH/dataframe/preSel.py

import os
from process import get_process_dict_dirs

basedir = os.path.join(get_process_dict_dirs()[0], "yaml/FCC/fcc_v04/")
outdir="FCChh/ttHH/"
NUM_CPUS = 20
process_list=['mgp8_pp_tthh_lambda100_5f',
              'mgp8_pp_ttz_5f',
              'mgp8_pp_ttzz_5f',
              'mgp8_pp_tth01j_5f'
              ]
fraction=1

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
