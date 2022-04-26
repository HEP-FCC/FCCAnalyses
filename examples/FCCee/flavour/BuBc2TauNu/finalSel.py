#python examples/FCCee/flavour/Bc2TauNu/finalSel.py

from config.common_defaults import deffccdicts
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Analysis_stage2_BuBc2TauNu/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_spring2021_IDEA.json"


process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU',
              'p8_ee_Zbb_ecm91_EvtGen',
              'p8_ee_Zbb_ecm91',
              'p8_ee_Zcc_ecm91',
              'p8_ee_Zuds_ecm91',
              
              'p8_ee_Zbb_ecm91_EvtGen_Bd2D3Pi',
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


define_list={
#    "EVT_minRhoMass":"if (EVT_CandRho1Mass<EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;",
#    "EVT_maxRhoMass":"if (EVT_CandRho1Mass>EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;",
#    "EVT_Ediff":"EVT_ThrustEmax_E-EVT_ThrustEmin_E"
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {#"sel0":"EVT_MVA1>0.8 && EVT_MVA2>0.8",
            #"sel1":"EVT_MVA1>0.9 && EVT_MVA2>0.9",
            #"sel2":"EVT_MVA1>0.95 && EVT_MVA2>0.95",
            #"sel3":"EVT_MVA1>0.98 && EVT_MVA2>0.98",
            #"sel4":"EVT_MVA1>0.99 && EVT_MVA2>0.99",
            #"sel5":"EVT_MVA1>0.9998979591836735 && EVT_MVA2>0.9956122448979592 && EVT_ThrustDiff_E > 10",
            "selBase":"EVT_MVA1>0.9 && (EVT_MVA2_bu>0.8 || EVT_MVA2_bc>0.8) && EVT_ThrustDiff_E > 10",
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {

    "EVT_CandMass"           :{"name":"EVT_CandMass","title":"mass [GeV]","bin":100,"xmin":0,"xmax":2.},
    "EVT_ThrustEmin_E"       :{"name":"EVT_ThrustEmin_E","title":"Hemisphere energy (min) [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustEmax_E"       :{"name":"EVT_ThrustEmax_E","title":"Hemisphere energy (max) [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustEmin_Echarged":{"name":"EVT_ThrustEmin_Echarged","title":"Hemisphere charged energy (min) [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustEmax_Echarged":{"name":"EVT_ThrustEmax_Echarged","title":"Hemisphere charged energy (max) [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustEmin_Eneutral":{"name":"EVT_ThrustEmin_Eneutral","title":"Hemisphere neutral energy (min) [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustEmax_Eneutral":{"name":"EVT_ThrustEmax_Eneutral","title":"Hemisphere neutral energy (max) [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustEmin_Ncharged":{"name":"EVT_ThrustEmin_Ncharged","title":"Hemisphere charged multiplicity (min)","bin":25,"xmin":0.,"xmax":25},
    "EVT_ThrustEmax_Ncharged":{"name":"EVT_ThrustEmax_Ncharged","title":"Hemisphere charged multiplicity (max)","bin":25,"xmin":0.,"xmax":25},
    "EVT_ThrustEmin_Nneutral":{"name":"EVT_ThrustEmin_Nneutral","title":"Hemisphere neutral multiplicity (min)","bin":25,"xmin":0.,"xmax":25},
    "EVT_ThrustEmax_Nneutral":{"name":"EVT_ThrustEmax_Nneutral","title":"Hemisphere neutral multiplicity (max)","bin":25,"xmin":0.,"xmax":25},
    "EVT_ThrustEmin_NDV"     :{"name":"EVT_ThrustEmin_NDV","title":"Hemisphere DV multiplicity (min)","bin":5,"xmin":0.,"xmax":5},
    "EVT_ThrustEmax_NDV"     :{"name":"EVT_ThrustEmax_NDV","title":"Hemisphere DV multiplicity (max)","bin":5,"xmin":0.,"xmax":5},
    "EVT_ThrustDiff_E"       :{"name":"EVT_ThrustDiff_E","title":"Hemisphere difference energy [GeV]","bin":120,"xmin":0.,"xmax":60},
    "EVT_ThrustDiff_Echarged":{"name":"EVT_ThrustDiff_Echarged","title":"Hemisphere difference charged energy [GeV]","bin":40,"xmin":-20.,"xmax":20},
    "EVT_ThrustDiff_Eneutral":{"name":"EVT_ThrustDiff_Eneutral","title":"Hemisphere difference neutral energy [GeV]","bin":40,"xmin":-20.,"xmax":20},
    "EVT_ThrustDiff_N"       :{"name":"EVT_ThrustDiff_N","title":"Hemisphere difference multiplicity","bin":40,"xmin":-20.,"xmax":20},
    "EVT_ThrustDiff_Ncharged":{"name":"EVT_ThrustDiff_Ncharged","title":"Hemisphere difference charged multiplicity","bin":40,"xmin":-20.,"xmax":20},
    "EVT_ThrustDiff_Nneutral":{"name":"EVT_ThrustDiff_Nneutral","title":"Hemisphere difference neutral multiplicity","bin":40,"xmin":-20.,"xmax":20},
    "EVT_CandVtxFD"          :{"name":"EVT_CandVtxFD","title":"Fligth distance to PV (mm)","bin":100,"xmin":0.,"xmax":10.},
    "EVT_CandAngleThrust"    :{"name":"EVT_CandAngleThrust","title":"Angle between candidate and thrust","bin":100,"xmin":0.,"xmax":2.},
    "EVT_CandAngleThrust_2"  :{"name":"EVT_CandAngleThrust","title":"Angle between candidate and thrust","bin":50,"xmin":0.,"xmax":0.5},
    "EVT_MVA1"               :{"name":"EVT_MVA1","title":"MVA1 score","bin":100,"xmin":0.6,"xmax":1.},
    "EVT_MVA2_bu"            :{"name":"EVT_MVA2_bu","title":"MVA2 bu score","bin":100,"xmin":0.6,"xmax":1.},
    "EVT_MVA2_bc"            :{"name":"EVT_MVA2_bc","title":"MVA2 bc score","bin":100,"xmin":0.6,"xmax":1.},
    "EVT_Nominal_B_E"        :{"name":"EVT_Nominal_B_E","title":"Nominal B Energy [GeV]","bin":100,"xmin":0.,"xmax":50.},
    "EVT_PVmass"             :{"name":"EVT_PVmass","title":"Primary Vertex Mass [GeV]","bin":100,"xmin":0.,"xmax":10.},
    "EVT_DVmass_min"         :{"name":"EVT_DVmass_min","title":"Displaced Vertex Mass Min [GeV]","bin":100,"xmin":0.,"xmax":20.},
    "EVT_DVmass_max"         :{"name":"EVT_DVmass_max","title":"Displaced Vertex Mass Max [GeV]","bin":100,"xmin":0.,"xmax":20.},
    "EVT_DVmass_ave"         :{"name":"EVT_DVmass_ave","title":"Displaced Vertex Mass Ave [GeV]","bin":100,"xmin":0.,"xmax":20.},
    "EVT_DVd0_min"           :{"name":"EVT_DVd0_min","title":"Displaced Vertex d0 Min [mm]","bin":100,"xmin":-10.,"xmax":10.},
    "EVT_DVd0_max"           :{"name":"EVT_DVd0_max","title":"Displaced Vertex d0 Max [mm]","bin":100,"xmin":-10.,"xmax":10.},
    "EVT_DVd0_ave"           :{"name":"EVT_DVd0_ave","title":"Displaced Vertex d0 Ave [mm]","bin":100,"xmin":-10.,"xmax":10.},
    "EVT_DVz0_min"           :{"name":"EVT_DVz0_min","title":"Displaced Vertex z0 Min [mm]","bin":100,"xmin":-10.,"xmax":10.},
    "EVT_DVz0_max"           :{"name":"EVT_DVz0_max","title":"Displaced Vertex z0 Max [mm]","bin":100,"xmin":-10.,"xmax":10.},
    "EVT_DVz0_ave"           :{"name":"EVT_DVz0_ave","title":"Displaced Vertex z0 Ave [mm]","bin":100,"xmin":-10.,"xmax":10.},
 
    
}

###Number of CPUs to use
NUM_CPUS = 8

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
#myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables,defines=define_list)
myana.run(ncpu=NUM_CPUS, doTree=True)
