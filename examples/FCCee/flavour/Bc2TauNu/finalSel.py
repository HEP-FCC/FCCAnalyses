#python examples/FCCee/flavour/Bc2TauNu/finalSel.py

from config.common_defaults import deffccdicts
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Analysis_stage2/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_tmp_v03.json"


#baseDir  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Training_4stage2/"
#procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_tmp_training.json"


process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU',
              'p8_ee_Zbb_ecm91',
              'p8_ee_Zcc_ecm91',
              'p8_ee_Zuds_ecm91',
              'p8_ee_Zbb_ecm91_EvtGen_BuCocktail',
              'p8_ee_Zbb_ecm91_EvtGen_BdCocktail',
              'p8_ee_Zbb_ecm91_EvtGen_BsCocktail',
              'p8_ee_Zbb_ecm91_EvtGen_LbCocktail',
              ]

define_list={
#    "EVT_minRhoMass":"if (EVT_CandRho1Mass<EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;",
#    "EVT_maxRhoMass":"if (EVT_CandRho1Mass>EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;",
#    "EVT_Ediff":"EVT_ThrustEmax_E-EVT_ThrustEmin_E"
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"EVT_MVA1>0.8 && EVT_MVA2>0.8",
            "sel1":"EVT_MVA1>0.9 && EVT_MVA2>0.9",
            #"sel2":"EVT_MVA>0.95 && EVT_MVA2>0.95",
            #"sel3":"EVT_MVA>0.98 && EVT_MVA2>0.98",
            #"sel4":"EVT_MVA>0.99 && EVT_MVA2>0.99",
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
    "EVT_ThrustDiff_Ncharged":{"name":"EVT_ThrustDiff_Ncharged","title":"Hemisphere difference charged energy [GeV]","bin":40,"xmin":-20.,"xmax":20},
    "EVT_ThrustDiff_Nneutral":{"name":"EVT_ThrustDiff_Nneutral","title":"Hemisphere difference neutral energy [GeV]","bin":40,"xmin":-20.,"xmax":20},
    "EVT_CandVtxFD"          :{"name":"EVT_CandVtxFD","title":"Fligth distance to PV (mm)","bin":100,"xmin":0.,"xmax":10.},
    "EVT_CandAngleThrust"    :{"name":"EVT_CandAngleThrust","title":"Angle between candidate and thrust","bin":100,"xmin":0.,"xmax":2.},
    "EVT_CandAngleThrust_2"  :{"name":"EVT_CandAngleThrust","title":"Angle between candidate and thrust","bin":50,"xmin":0.,"xmax":0.5},
    "EVT_MVA1"               :{"name":"EVT_MVA1","title":"MVA1 score","bin":100,"xmin":0.6,"xmax":1.},
    "EVT_MVA1"               :{"name":"EVT_MVA2","title":"MVA2 score","bin":100,"xmin":0.6,"xmax":1.},

}

###Number of CPUs to use
NUM_CPUS = 2

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
#myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables,defines=define_list)
myana.run(ncpu=NUM_CPUS, doTree=True)
