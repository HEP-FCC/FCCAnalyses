"""
January 2023
Abraham Tishelman-Charny

The purpose of this python module is to perform initial selections and variable definitions for processing FCC files.
"""

import os
import urllib.request
import yaml 
import sys

sys.path.append("/usatlas/u/atishelma/FCC/FCCAnalyses/")

from examples.FCCee.weaver.config import collections

#configFile = "/afs/cern.ch/work/a/atishelm/private/FCC/BNL-Analyses/RunConfig.yaml" # for the moment, need to specify full path so that HTCondor node can find this file (since afs is mounted). Need to check how to pass this as an input file to HTCondor job.
#with open(configFile, 'r') as cfg:
#    values = yaml.safe_load(cfg)
    
#    batch = values["batch"]
#    EOSoutput = values["EOSoutput"]
#    JobName = values["JobName"]
#    njets = values["njets"]

# batch with EOS output
batch = 1
EOSoutput = 0
#JobName = "Test_SDCC_Condor"
JobName = "ZHadronic_4JetReco"
njets = 4

#exclusive = 1 

  # flag for exclusive jet clustering. Possible choices are: 
  # 0 = inclusive clustering, for duram kt 
  # 1 = exclusive clustering that would be obtained when running the algorithm with the given dcut, 
  # 2 = exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 
  # 3 = exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets,
  # 4 = exclusive jets obtained at the given ycutei 

# local
#batch = 1
#EOSoutput = 1
#JobName = "Inclusive_R0p4"
#njets = 4
#exclusive = 0 # flag for exclusive jet clustering. Possible choices are: 

print("batch:",batch)
print("EOSoutput:",EOSoutput)
print("name:",JobName)
print("njets:",njets)

processList = {

    # Hadronic ZH
    "wzp6_ee_bbH_Hbb_ecm240" : {'chunks' : 2},
    
    #"""
    #"wzp6_ee_bbH_Hcc_ecm240" : {'chunks' : 2},
    #"wzp6_ee_bbH_Hgg_ecm240" : {'chunks' : 2},
    #"wzp6_ee_bbH_Hss_ecm240" : {'chunks' : 2},
    #"wzp6_ee_bbH_Htautau_ecm240" : {'chunks' : 2},
    #"wzp6_ee_bbH_HWW_ecm240" : {'chunks' : 2},
    #"wzp6_ee_bbH_HZa_ecm240" : {'chunks' : 2},
    #"wzp6_ee_bbH_HZZ_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_Hbb_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_Hcc_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_Hgg_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_Hss_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_Htautau_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_HWW_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_HZa_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ccH_HZZ_ecm240" : {'chunks' : 2},
    #"wzp6_ee_nunuH_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_Hbb_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_Hcc_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_Hgg_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_Hss_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_Htautau_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_HWW_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_HZa_ecm240" : {'chunks' : 2},
    #"wzp6_ee_qqH_HZZ_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_Hbb_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_Hcc_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_Hgg_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_Hss_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_Htautau_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_HWW_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_HZa_ecm240" : {'chunks' : 2},
    #"wzp6_ee_ssH_HZZ_ecm240" : {'chunks' : 2},
    #"""    

    # backgrounds. Option: 'fraction' : frac_value
    #'p8_ee_WW_ecm240' : {'chunks':3740, 'fraction' : 0.0001},
    
    'p8_ee_WW_ecm240' : {'chunks':1000},
    #'p8_ee_ZZ_ecm240' : {'chunks':250},
    #'p8_ee_Zqq_ecm240' : {'chunks':250}
    
    #'p8_ee_WW_ecm240' : {'chunks':3740},
    #'p8_ee_ZZ_ecm240' : {'chunks':562},
    #'p8_ee_Zqq_ecm240' : {'chunks':1007}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/" 
procDict = "FCCee_procDict_winter2023_IDEA.json" 

if(EOSoutput):
    #outputDir = f"{JobName}/stage1/"
    #outputDirEos = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/stage1/" # if you define outputDirEos, this process creates the file locally and copies it to eos.
    #outputDir = f"/eos/user/a/atishelm/ntuples/FCC/ZH_Hadronic_4JetReco/"
    #outputDir = f"/eos/user/a/atishelm/ntuples/FCC/ZH_Hadronic_InclusiveReco/"
    
    eosType = "eosuser"
else:
    outputDir   = f"/usatlas/atlas01/atlasdisk/users/atishelma/{JobName}/stage1/"
    #outputDir   = f"{JobName}/stage1/"

runBatch    = batch
batchQueue = "testmatch" 
#eosType = eosType

# Define any functionality which is not implemented in FCCAnalyses

import ROOT
ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<double> SumFlavorScores(ROOT::VecOps::RVec<double> recojet_isFlavor) {

    double score_1, score_2, pair_score; 
    ROOT::VecOps::RVec<double> recojetpair_isFlavor;

    // cannot compute any mass pair flavour score values, return a single non-physical value
    if(recojet_isFlavor.size() < 2){
        recojetpair_isFlavor.push_back(-99);
        return recojetpair_isFlavor; 
    }


    // For each jet, take its flavor score sum with the remaining jets. Stop at last jet.
    for(int i = 0; i < recojet_isFlavor.size()-1; ++i) {

    score_1 = recojet_isFlavor.at(i); 

        for(int j=i+1; j < recojet_isFlavor.size(); ++j){ // go until end
            score_2 = recojet_isFlavor.at(j);
            pair_score = score_1 + score_2; 
            recojetpair_isFlavor.push_back(pair_score);

        }
    }

    return recojetpair_isFlavor;
}



ROOT::VecOps::RVec<double> all_recoil_masses(ROOT::VecOps::RVec<TLorentzVector> all_jet_4vectors){
  double m_sqrts = 240;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
  TLorentzVector tv1, tv2, tvpair; 
  double E, px, py, pz, recoil_mass;
  ROOT::VecOps::RVec<double> recoil_masses;

  // cannot compute any mass pair values, return a single non-physical value
  if(all_jet_4vectors.size() < 2){
    recoil_masses.push_back(-99);
    return recoil_masses;  
  }

    // For each jet, take its recoil mass using the remaining jets. Stop at last jet.
    for(int i = 0; i < all_jet_4vectors.size()-1; ++i) {

        tv1 = all_jet_4vectors.at(i);

        for(int j=i+1; j < all_jet_4vectors.size(); ++j){ // go until end

            tv2 = all_jet_4vectors.at(j); 
            E = tv1.E() + tv2.E();
            px = tv1.Px() + tv2.Px();
            py = tv1.Py() + tv2.Py();
            pz = tv1.Pz() + tv2.Pz();

            tvpair.SetPxPyPzE(px, py, pz, E);

            recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
            recoil_p4 -= tvpair; 

            recoil_mass = recoil_p4.M();
            recoil_masses.push_back(recoil_mass);

        }
    }

  return recoil_masses;

}

""") 

# ____________________________________________________________
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)

# ____________________________________________________________

## input file needed for unit test in CI
testFile = "https://fccsw.web.cern.ch/fccsw/testsamples/wzp6_ee_nunuH_Hss_ecm240.root"

## latest particle transformer model, trainied on 9M jets in winter2023 samples - need to separate train/test samples?
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from examples.FCCee.weaver.config import (
    variables_pfcand,
    variables_jet,
    #variables_event, # assumes at least 2 jets for event_invariant_mass variable
)

from addons.ONNXRuntime.python.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.python.jetClusteringHelper import ExclusiveJetClusteringHelper

jetFlavourHelper = None
jetClusteringHelper = None

def analysis_sequence(df):
    anatag = ""

    collections["Electrons"] = "Electron"
    collections["Muons"] = "Muon"
    collections["Photons"] = "Photons"

    df = (
        # electrons
        df.Alias("Electron0{}".format(anatag), "{}#0.index".format(collections["Electrons"]))
        .Define(
            "electrons{}".format(anatag),
            "ReconstructedParticle::get(Electron0{}, {})".format(anatag, collections["PFParticles"]),
        )
        .Define("event_nel{}".format(anatag), "electrons{}.size()".format(anatag))  # are these isolated?
        .Define("electrons_p{}".format(anatag), "ReconstructedParticle::get_p(electrons{})[0]".format(anatag))
        
        # muons
        .Alias("Muon0{}".format(anatag), "{}#0.index".format(collections["Muons"]))
        .Define(
            "muons{}".format(anatag),
            "ReconstructedParticle::get(Muon0{}, {})".format(anatag, collections["PFParticles"]),
        )
        .Define("event_nmu{}".format(anatag), "muons{}.size()".format(anatag))
        .Define("muons_p{}".format(anatag), "ReconstructedParticle::get_p(muons{})[0]".format(anatag))

        #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing energy (despite the name, the MissingET collection contains the total missing energy)
        .Define("RecoMissingEnergy_e", "ReconstructedParticle::get_e(MissingET)")
        .Define("RecoMissingEnergy_p", "ReconstructedParticle::get_p(MissingET)")
        .Define("RecoMissingEnergy_pt", "ReconstructedParticle::get_pt(MissingET)")
        .Define("RecoMissingEnergy_px", "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
        .Define("RecoMissingEnergy_py", "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
        .Define("RecoMissingEnergy_pz", "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
        .Define("RecoMissingEnergy_eta", "ReconstructedParticle::get_eta(MissingET)")
        .Define("RecoMissingEnergy_theta", "ReconstructedParticle::get_theta(MissingET)")
        .Define("RecoMissingEnergy_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMissingEnergy
    )

    for x in range(1, 9):
        df = (df.Define("d_{}{}{}".format(x,x+1,anatag), "JetClusteringUtils::get_exclusive_dmerge(_jet{}, {})".format(anatag, x))) #dmerge from x+1 to x

    return df


#def jet_sequence(df, njets, exclusive):
def jet_sequence(df, njets):

    global jetClusteringHelper
    global jetFlavourHelper

    tag = ""

    ## define jet clustering parameters
    #jetClusteringHelper = ExclusiveJetClusteringHelper(collections["PFParticles"], njets, exclusive, tag)
    #jetClusteringHelper = ExclusiveJetClusteringHelper(collections["PFParticles"], njets, exclusive, tag)
    jetClusteringHelper = ExclusiveJetClusteringHelper(collections["PFParticles"], njets, tag)

    ## run jet clustering
    df = jetClusteringHelper.define(df)

    ## define jet flavour tagging parameters
    jetFlavourHelper = JetFlavourHelper(
        collections,
        jetClusteringHelper.jets,
        jetClusteringHelper.constituents,
        tag,
    )

    ## define observables for tagger
    df = jetFlavourHelper.define(df)
    df = df.Define("jet_p4", "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
    df = df.Define("all_invariant_masses", "JetConstituentsUtils::all_invariant_masses(jet_p4)")
    df = df.Define("recoil_masses", "all_recoil_masses(jet_p4)")

    ## tagger inference
    df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df) 

    ## define variables using tagger inference outputs
    df = df.Define("recojetpair_isC", "SumFlavorScores(recojet_isC)") 
    df = df.Define("recojetpair_isB", "SumFlavorScores(recojet_isB)") 

    return df

# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df = jet_sequence(df, njets)
        #df = jet_sequence(df, njets, exclusive)
        df = analysis_sequence(df)

        return df

    # __________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():

        anatag = ""

        branchList = []

        # jets
        branches_jet = list(variables_jet.keys())
        #branches_event = list(variables_event.keys())

        #branchList = branches_event  + branches_jet 
        branchList = branches_jet 
        branchList += jetFlavourHelper.outputBranches()
        branchList += ["event_njet"]
        
        branchList += ["all_invariant_masses"]
       	branchList += ["recojetpair_isC"]
        branchList += ["recojetpair_isB"]
        branchList += ["recoil_masses"]

        for x in range(1, 9):
            branchList.append("d_{}{}{}".format(x,x+1,anatag))
        
        # leptons
        branchList += ["event_nel"]
        branchList += ["event_nmu"]

        # MET
        MET_vars = ["e", "p", "pt", "px", "pt", "pz", "eta", "theta", "phi"]
        for MET_var in MET_vars:
            branchList += [f"RecoMissingEnergy_{MET_var}"]

        # remove duplicates 
        branchList = list(set(branchList))

        return branchList
