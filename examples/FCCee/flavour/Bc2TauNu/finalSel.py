#python examples/FCCee/flavour/Bc2TauNu/finalSel.py

from config.common_defaults import deffccdicts
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_stage2/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_tmp_v03.json"

process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU',
              'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU',
              'p8_ee_Zbb_ecm91',
              'p8_ee_Zcc_ecm91',
              'p8_ee_Zuds_ecm91']

define_list={
    "EVT_minRhoMass":"if (EVT_CandRho1Mass<EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;",
    "EVT_maxRhoMass":"if (EVT_CandRho1Mass>EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;"
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"EVT_MVA2>0.6",
            "sel1":"EVT_MVA>0.9 && EVT_MVA2>0.9",
            "sel2":"EVT_MVA>0.95 && EVT_MVA2>0.95",
            "sel3":"EVT_MVA>0.98 && EVT_MVA2>0.98",
            "sel4":"EVT_MVA>0.99 && EVT_MVA2>0.99",
            }

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {

    "EVT_CandMass":{"name":"EVT_CandMass","title":"mass [GeV]","bin":100,"xmin":0,"xmax":2.},
    "EVT_minRhoMass":{"name":"EVT_minRhoMass","title":"mass [GeV]","bin":100,"xmin":0,"xmax":2.},
    "EVT_maxRhoMass":{"name":"EVT_maxRhoMass","title":"mass [GeV]","bin":100,"xmin":0,"xmax":2.},
    
    #"EVT_thrust_val":{"name":"EVT_thrust_val","title":"Event Thrust","bin":100,"xmin":0.4,"xmax":1.},
    #"EVT_thrusthemis_emax":{"name":"EVT_thrutshemis_emax","title":"Hemisphere energy (max) [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_thrusthemis_emin":{"name":"EVT_thrutshemis_emin","title":"Hemisphere energy (min) [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_Ediff":{"name":"EVT_Ediff","title":"Hemisphere energy difference [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_Echarged_max":{"name":"EVT_Echarged_max","title":"Hemisphere charged energy (max) [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_Echarged_min":{"name":"EVT_Echarged_min","title":"Hemisphere charged energy (min) [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_Eneutral_max":{"name":"EVT_Eneutral_max","title":"Hemisphere neutral energy (max) [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_Eneutral_min":{"name":"EVT_Eneutral_min","title":"Hemisphere neutral energy (min) [GeV]","bin":120,"xmin":0.,"xmax":60},
    #"EVT_Ncharged_max":{"name":"EVT_Ncharged_max","title":"Hemisphere charged multiplicity (max)","bin":25,"xmin":0.,"xmax":25},
    #"EVT_Ncharged_min":{"name":"EVT_Ncharged_min","title":"Hemisphere charged multiplicity (min)","bin":25,"xmin":0.,"xmax":25},
    #"EVT_Nneutral_max":{"name":"EVT_Nneutral_max","title":"Hemisphere neutral multiplicity (max)","bin":25,"xmin":0.,"xmax":25},
    #"EVT_Nneutral_min":{"name":"EVT_Nneutral_min","title":"Hemisphere neutral multiplicity (min)","bin":25,"xmin":0.,"xmax":25}
}

###Number of CPUs to use
NUM_CPUS = 2

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
#myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables,defines=define_list)
myana.run(ncpu=NUM_CPUS, doTree=True)
