from common_defaults import deffccdicts

#python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py 
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "FCCee/eeH/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_tmp.json"

process_list=['p8_ee_Z_Zqq_ecm125','p8_ee_H_Hgg_ecm125']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"RP_p.size()>0"
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {

    "thrust_x":{"name":"event_thrust_x","title":"event thrust x","bin":100,"xmin":-1.,"xmax":1.},
    "thrust_y":{"name":"event_thrust_y","title":"event thrust y","bin":100,"xmin":-1,"xmax":1.},
    "thrust_z":{"name":"event_thrust_z","title":"event thrust z","bin":100,"xmin":-1,"xmax":1.},
    "thrust_val":{"name":"event_thrust_val","title":"event thrust val","bin":100,"xmin":0.5,"xmax":1.},
    "hemis_0":{"name":"event_hemis_0","title":"event hemisphere<0","bin":100,"xmin":-1.,"xmax":1.},
    "hemis_1":{"name":"event_hemis_1","title":"event hemisphere>0","bin":100,"xmin":-1.,"xmax":1.},
   
}

###Number of CPUs to use
NUM_CPUS = 10

###This part is standard to all analyses
sys.path.append('./bin')
import runDataFrameFinal as rdf
#import bin.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)
