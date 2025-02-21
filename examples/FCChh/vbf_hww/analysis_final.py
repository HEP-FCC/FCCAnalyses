import vbf_hww.analysis_config as analysis_config


#Input directory where the files produced at the pre-selection level are
#inputDir  = "outputs/FCChh/vbf_hww/presel_condor/"
inputDir = analysis_config.stage1_output

#Input directory where the files produced at the pre-selection level are
outputDir  = analysis_config.final_output

processList = {}
for proc in analysis_config.process_list:
    processList[proc] : {}

#Link to the dictonary that contains all the cross section informations etc...
#procDict = "/eos/experiment/fcc/hh/tutorials/edm4hep_tutorial_data/FCChh_procDict_tutorial.json"
procDict = '/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json'
#Note the numbeOfEvents and sumOfWeights are placeholders that get overwritten with the correct values in the samples

# BRs
BRHww  = 0.215	# Higgs X-sec working group
BRWlep = 0.108  # PDG
BRZlep = 0.03365 # PDG

#How to add a process that is not in the official dictionary:
procDictAdd={
    "vbf_hww_llvv": {"numberOfEvents": 70000, "sumOfWeights": 70000, "crossSection": 8.411e+01*(BRWlep*3)**2*BRHww , "kfactor": 1.0, "matchingEfficiency": 1.0},
    "ggh_hww_llvv": {"numberOfEvents": 659940, "sumOfWeights": 659940, "crossSection": 5.849e+02*(BRWlep*3)**2*BRHww , "kfactor": 1.0, "matchingEfficiency": 1.0},
    'vv_lep': {"numberOfEvents": 660000  , "sumOfWeights": 660000  , "crossSection": 3.320e+04*(BRWlep*3)**2 , "kfactor": 0.0432, "matchingEfficiency": 1.0}, # 0.02 accounts for ngenW=2 filter
    'ttbar_lep'    : {"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 4.265e+04*(BRWlep*3)**2, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'z_tautau'    : {"numberOfEvents": 751378, "sumOfWeights": 751378, "crossSection": 8.787e+06*BRZlep, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'vbf_z_tautau'    : {"numberOfEvents": 474, "sumOfWeights": 474, "crossSection": 5.133e+03*BRZlep, "kfactor": 1.0, "matchingEfficiency": 1.0},
    }

# Expected integrated luminosity
intLumi = 30e+06  # pb-1

# Whether to scale to expected integrated luminosity
doScale = True

#Number of CPUs to use
nCPUS = 2

#produces ROOT TTrees, default is False
doTree = True

saveTabular = True

# Optional: Use weighted events
do_weighted = False 

# Define new variables
defineList = {
    "n_lep" : "n_el+n_mu",
    "n_genW" : "n_genWp+n_genWm"
}



# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {}
cutList['sel0_all']='1.0'
cutList['sel1_bjeteveto']='n_bjets_loose==0'
cutList['sel2_jeteveto']='n_jets==2'
cutList['sel3_both']=cutList['sel1_bjeteveto'] + ' && ' + cutList['sel2_jeteveto']
cutList['sel4_mjj']=cutList['sel3_both']+ '&& (m_jj[0]>1000.0)&&(deta_jj[0]>4.5)'
cutList['sel5_mem']=cutList['sel3_both']+ '&&(m_em[0]<70.0)'            
cutList['sel6_mjj_dphiem_lepcent']= cutList['sel4_mjj']+ ' && (dphi_em[0]<0.75) && (lep_cent[0]<0.40)'
cutList['sel7_mjj_dphiem_lepcent_mt']= cutList['sel6_mjj_dphiem_lepcent']+ ' && (MT[0]<150.0) && (MT[0]>50.0) '


# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    #"n_el" : {"title":"Number Electrons","bin":10,"xmin":0,"xmax":10},
    #"n_mu" : {"title":"Number Muons","bin":10,"xmin":0,"xmax":10},
    #"n_lep" : {"title":"Number Leptons","bin":10,"xmin":0,"xmax":10},
    "n_jets" : {"title":"Number Jets","bin":10,"xmin":0,"xmax":10},
    'n_centraljets'  : {"title":"Number Centeral Jets","bin":10,"xmin":0,"xmax":10},
    "n_bjets" : {"title":"Number b-Jets","bin":10,"xmin":0,"xmax":10},
    "n_bjets_loose" : {"title":"Number Jets","bin":10,"xmin":0,"xmax":10},
    "n_genb" : {"title":"Number Jets","bin":10,"xmin":0,"xmax":10},
    'n_RecoTracks'  : {"title":"Number Tracks","bin":100,"xmin":0,"xmax":1000},
    "genb_eta" : {"title":"Generator Level b-quark Eta","bin":100,"xmin":-10,"xmax":10},
    "genb_pt" : {"title":"Generator Level b-quark Pt","bin":100,"xmin":0,"xmax":500},
    "j1_eta" : {"title":"Leading Jet Eta","bin":100,"xmin":-10,"xmax":10},
    "j2_eta" : {"title":"Subleading Jet Eta","bin":100,"xmin":-10,"xmax":10},
    "j1_pt" : {"title":"Leading Jet pT","bin":100,"xmin":0,"xmax":500},
    "j2_pt" : {"title":"Subleading Jet Pt","bin":100,"xmin":0,"xmax":500},
    "pt_jj" : {"title":"Di-Jet Pt","bin":100,"xmin":0,"xmax":500},
    "el1_pt" : {"title":"Leading Electron pT","bin":40,"xmin":0,"xmax":200},
    "mu1_pt" : {"title":"Leading Muon pT","bin":40,"xmin":0,"xmax":200},
    "MET" : {"title":"MET","bin":40,"xmin":0,"xmax":1000},
    "m_em":{"title":"m_{#ell#mu} [GeV]","bin":60,"xmin":0,"xmax":300},
    'MT' : {"title":"MT [GeV]","bin":30,"xmin":0,"xmax":300},
    'lep_cent' : {"title":"lepton centrality","bin":60,"xmin":0,"xmax":3},
    "m_jj":{"title":"m_{jj} [GeV]","bin":40,"xmin":0,"xmax":10000},
    "dphi_jj":{"title":"#delta#phi_{jj} ","bin":30,"xmin":0,"xmax":3.1416},
    "deta_jj":{"title":"#delta#eta_{jj} ","bin":120,"xmin":0,"xmax":12.0},
    "dphi_em":{"title":"#delta#phi_{e#mu} ","bin":30,"xmin":0,"xmax":3.1416},
    "deta_em":{"title":"#delta#eta_{e#mu} ","bin":12,"xmin":0,"xmax":12.0},
    'dphi_emMET' : {"title":"#delta#phi(em,MET)","bin":30,"xmin":0,"xmax":3.1415},
    "n_genW" : {"title": "N generator W","bin":10, "xmin":0,"xmax":10},
    "n_genZ" : {"title": "N generator Z","bin":10, "xmin":0,"xmax":10},
    }

for key,val in histoList.items():
    if "name" not in val.keys():
        val["name"]=key
