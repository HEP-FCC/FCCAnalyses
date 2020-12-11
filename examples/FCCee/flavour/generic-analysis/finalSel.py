#python examples/FCCee/flavour/generic-analysis/finalSel.py

from config.common_defaults import deffccdicts
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "outputs/FCCee/flavour/generic-analysis/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_v02.json"
procDict ='https://fcc-physics-events.web.cern.ch/fcc-physics-events/sharedFiles/FCCee_procDict_fcc_v02.json'

process_list=['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU','p8_ee_Zbb_ecm91']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"RP_p.size()>0",
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {

    "EVT_thrust_val":{"name":"EVT_thrust_val","title":"Event Thrust","bin":100,"xmin":0.4,"xmax":1.},
    "EVT_thrutshemis_emax":{"name":"EVT_thrutshemis_emax","title":"Hemisphere with max energy","bin":120,"xmin":0.,"xmax":60},
    "EVT_thrutshemis_emin":{"name":"EVT_thrutshemis_emin","title":"Hemisphere with min energy","bin":120,"xmin":0.,"xmax":60},
    "EVT_thrust_x":{"name":"EVT_thrust_x","title":"Thrust x axis","bin":100,"xmin":-10,"xmax":10},
    "EVT_thrust_y":{"name":"EVT_thrust_y","title":"Thrust y axis","bin":100,"xmin":-10,"xmax":10},
    "EVT_thrust_z":{"name":"EVT_thrust_z","title":"Thrust z axis","bin":100,"xmin":-10,"xmax":10},
    
}

###Number of CPUs to use
NUM_CPUS = 2

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)
