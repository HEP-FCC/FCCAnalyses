#python examples/FCCee/flavour/BuBc2TauNu/preSel_Batch.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021/IDEA/"
# May need a different path name 
outdir="/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2022/prod_04/Batch_Analysis_stage1/"
NUM_CPUS=8
output_list=[]

fraction=1.

fcc_dir = os.getcwd().split("FCCAnalyses",1)[0]
inputana=fcc_dir+"FCCAnalyses/examples/FCCee/flavour/BuBc2TauNu/analysis_stage1.py"

process_list=['p8_ee_Zbb_ecm91_EvtGen',
              'p8_ee_Zbb_ecm91',
              'p8_ee_Zcc_ecm91',
              'p8_ee_Zuds_ecm91',
              ]

#myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
#myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana, comp="group_u_ATLAST3.all")


process_list=['p8_ee_Zbb_ecm91_EvtGen_Bd2D3Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Bd2DDs',
              'p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNu',
              'p8_ee_Zbb_ecm91_EvtGen_Bd2Dst3Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Bd2DstDs',
              'p8_ee_Zbb_ecm91_EvtGen_Bd2DstDsst',
              'p8_ee_Zbb_ecm91_EvtGen_Bd2DstTauNu',

              'p8_ee_Zbb_ecm91_EvtGen_Bs2Ds3Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Bs2DsDs',
              'p8_ee_Zbb_ecm91_EvtGen_Bs2DsTauNu',
              'p8_ee_Zbb_ecm91_EvtGen_Bs2Dsst3Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDs',
              'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDsst',
              'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstTauNu',
              
              'p8_ee_Zbb_ecm91_EvtGen_Bu2D03Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2D0Ds',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2D0TauNu',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst03Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Ds',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Dsst',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0TauNu',

              'p8_ee_Zbb_ecm91_EvtGen_Lb2Lc3Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Lb2LcDs',
              'p8_ee_Zbb_ecm91_EvtGen_Lb2LcTauNu',
              'p8_ee_Zbb_ecm91_EvtGen_Lb2Lcst3Pi',
              'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDs',
              'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDsst',
              'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstTauNu',

              ]

#myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
#myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana)


process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',    
              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU'
              ]
#myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
#myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=100 ,outDir=outdir, inputana=inputana, comp="group_u_ATLAST3.all")

process_list=[#'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTau23PiPi0NuTAUOLA',    
    'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTau23PiPi0NuTAUOLA',    
              ]
myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana, comp="group_u_ATLAST3.all")
