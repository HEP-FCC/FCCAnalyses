#python examples/FCCee/flavour/Bc2TauNu/preSel_Batch.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp_v03/"
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batch_pdg/"
NUM_CPUS=8
output_list=[]

fraction=1.


inputana="analysis_stage1.py"

process_list=['p8_ee_Zbb_ecm91',
              #'p8_ee_Zcc_ecm91',
              #'p8_ee_Zuds_ecm91'
              ]
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=200 ,outDir=outdir, inputana=inputana)

#process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
#              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU']
#myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
#myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=2 ,outDir=outdir, inputana=inputana)
