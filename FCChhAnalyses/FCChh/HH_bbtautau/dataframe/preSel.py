from common_defaults import deffccdicts
 #python FCChhAnalyses/FCChh/ttHH/dataframe/preSel.py 
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCC/fcc_v04/"
outdir="FCChh/HH_bbtautau/"
NUM_CPUS = 20
process_list=['pwp8_pp_hh_lambda100_5f_hhbbaa',
              #'mgp8_pp_bbtata_QED',
              #'mgp8_pp_bbtata_QCDQED',
              #'mg_pp_bbjj_QCD_5f',
              'mgp8_pp_tt012j_5f',
              #'mg_pp_h012j_5f',
              #'mg_pp_vh012j_5f',
              #'mg_pp_ttw_5f',
              #'mg_pp_ttww_4f',
              #'mg_pp_ttwz_5f',
              #'mgp8_pp_ttz_5f',
              #'mgp8_pp_ttzz_5f',
              #'mgp8_pp_tth01j_5f'
              ]
fraction=1

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
