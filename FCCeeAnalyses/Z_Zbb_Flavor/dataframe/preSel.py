from common_defaults import deffccdicts
 #python FCCeeAnalyses/Z_Zbb_Flavor/dataframe/preSel.py 
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp/"
outdir="/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Flavor/"
NUM_CPUS = 30
process_list=[#'p8_ee_Zbb_ecm91',
              #'p8_ee_Zcc_ecm91',
              #'p8_ee_Zuds_ecm91',
              #'p8_ee_Ztautau_ecm91',
              #'p8_ee_Zbb_ecm91_EvtGen_Bu2D0Pi',
              #'p8_ee_Zbb_ecm91_EvtGen_Bd2KstTauTau',
              #'p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu',
              #'p8_ee_Zbb_ecm91_EvtGen_Bd2DstTauNu',
              #'p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNu',#missing
              #'p8_ee_Zbb_ecm91_EvtGen_Bd2KstEE',
              #'p8_ee_Zbb_ecm91_EvtGen_BdKstNuNu',#missing
              'p8_ee_Zbb_ecm91_EvtGen_Bd2KsPi0',
              #'p8_ee_Zbb_ecm91_EvtGen_Bs2PhiGamma',
              #'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTau',
              #'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNu',
              #'p8_ee_Ztautau_ecm91_EvtGen_Tau2MuMuMu',    
              #'p8_ee_Ztautau_ecm91_EvtGen_Tau2MuGamma',
              #'p8_ee_Zcc_ecm91_EvtGen_D2PiPi0',

              ]
fraction=0.5

import bin.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
