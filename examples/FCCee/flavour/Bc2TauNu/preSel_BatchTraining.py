#python examples/FCCee/flavour/Bc2TauNu/preSel_BatchTraining.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp_training/"
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batchTraining_21042021/"
NUM_CPUS=8
output_list=[]
inputana="analysis_training_stage1.py"


fraction=0.1
process_list=['p8_ee_Zbb_ecm91',
              'p8_ee_Zcc_ecm91',
              'p8_ee_Zuds_ecm91']
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=15 ,outDir=outdir, inputana=inputana)


fraction=0.5
process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU'
              ]
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=5 ,outDir=outdir, inputana=inputana)
