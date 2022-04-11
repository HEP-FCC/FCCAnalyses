#python examples/FCCee/flavour/BuBc2TauNu/preSel_BatchTraining.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os


basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021_training/IDEA/"
NUM_CPUS=8
output_list=[]

##To produce variables for MVA stage 1 training
fcc_dir = os.getcwd().split("FCCAnalyses",1)[0]
inputana=fcc_dir+"FCCAnalyses/examples/FCCee/flavour/BuBc2TauNu/analysis_stage1.py"

# May need a different path name
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2022/prod_04/Batch_Training_4stage1/"

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
