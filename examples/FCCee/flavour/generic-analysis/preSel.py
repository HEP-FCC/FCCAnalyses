#python examples/FCCee/flavour/generic-analysis/preSel.py

from config.common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp/"
outdir="/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Flavor_Uproot_test4/"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)
process_list=[

    #'p8_ee_Zuds_ecm91',
    
    'p8_ee_Zbb_ecm91',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2KsPi0',
    #'p8_ee_Zbb_ecm91_EvtGen_Bs2PhiGamma',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2KstEE',
    #'p8_ee_Zbb_ecm91_EvtGen_Bu2D0Pi',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2DstTauNuTAUHADNU',
    #'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTauTAUHADNU',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNuTAUHADNU',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2KstTauTauTAUHADNU',
    #'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',
    #'p8_ee_Zbb_ecm91_EvtGen_Bs2DsK',
    #'p8_ee_Zbb_ecm91_EvtGen_Bd2D0PiPi',

    #'p8_ee_Zcc_ecm91',
    #'p8_ee_Zcc_ecm91_EvtGen_D2PiPi0',

    #'p8_ee_Ztautau_ecm91',
    #'p8_ee_Ztautau_ecm91_EvtGen_Tau2MuMuMu',
    #'p8_ee_Ztautau_ecm91_EvtGen_Tau2MuGamma',


              ]
fraction=0.5

import config.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
