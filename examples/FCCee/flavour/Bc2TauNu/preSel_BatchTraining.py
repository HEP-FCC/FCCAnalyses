#python examples/FCCee/flavour/Bc2TauNu/preSel_BatchTraining.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os


basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021/IDEA/"
NUM_CPUS=8
output_list=[]

##To produce variables for MVA stage 1 training
inputana="analysis_training_stage1.py"
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_01/Batch_Training_4stage1/"

fraction=1.

process_list=['p8_ee_Zbb_ecm91',
              'p8_ee_Zcc_ecm91',
              'p8_ee_Zuds_ecm91']
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana)


fraction=1.
process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU'
              ]
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana)
