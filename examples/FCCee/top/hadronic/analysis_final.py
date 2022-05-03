#python examples/FCCee/top/hadronic/finalSel.py
#Mandatory: List of processes
processList = {
            'p8_ee_ZZ_ecm365':{},
            'p8_ee_WW_ecm365':{},
            'p8_ee_ZH_ecm365':{},
            'p8_ee_tt_fullhad_ecm365':{},
            'p8_ee_ZZ_fullhad_ecm365':{},
            'p8_ee_WW_fullhad_ecm365':{},
            'p8_ee_tt_fullhad_ecm365':{}
            }

###Input directory where the files produced at the pre-selection level are
inputDir   = "outputs/FCCee/top/hadronic/analysis_stage1/"
outputDir  = "outputs/FCCee/top/hadronic/analysis_final/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_fcc_tmp.json"

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {"sel0":"EVT_thrust_val>0",
            "sel1":"RP_hemis0_mass>100. && RP_hemis1_mass>100."
            }

###Optinally Define new variables
#DefineList = {"selmuon_pT_0":"selected_muons_pt.at(0)"}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "thrust_val":{"name":"EVT_thrust_val","title":"Event Thrust","bin":100,"xmin":0.0,"xmax":1.},
    "sphericity_val":{"name":"EVT_sphericity_val","title":"Event Sphericity","bin":100,"xmin":0.0,"xmax":1.},
    "thrust_angle":{"name":"RP_thrustangle","title":"RP angle thrust","bin":100,"xmin":-1.0,"xmax":1.0},
    "sphericity_angle":{"name":"RP_sphericityangle","title":"RP angle sphericity","bin":100,"xmin":-1.0,"xmax":1.0},
    "hemis0_mass":{"name":"RP_hemis0_mass","title":"mass hemis<0 [GeV]","bin":100,"xmin":0.0,"xmax":250.},
    "hemis1_mass":{"name":"RP_hemis1_mass","title":"mass hemis>0 [GeV]","bin":100,"xmin":0.0,"xmax":250.},
    "total_mass":{"name":"RP_total_mass","title":"total mass [GeV]","bin":100,"xmin":180.0,"xmax":380.},
}
