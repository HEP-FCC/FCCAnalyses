#python examples/FCCee/flavour/Bd2MuMu/preSel.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021/IDEA/"
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2MuMu/flatNtuples/spring2021/Batch/"
NUM_CPUS=8
output_list=[]

fraction=1.

inputana="/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bd2MuMu/analysis.py"
process_list=['p8_ee_Zbb_ecm91']
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana)


process_list=['p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu']
import config.runDataFrame as rdf2
myana=rdf2.runDataFrame(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction ,outDir=outdir)


