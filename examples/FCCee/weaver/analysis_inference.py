import sys
import ROOT

# Optional
nCPUS = 8


## latest particle transformer model, trainied on 9M jets in winter2023 samples
model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022"
model_name = "fccee_flavtagging_edm4hep_wc_v1"

weaver_preproc = "{}/{}.json".format(model_dir, model_name)
weaver_model = "{}/{}.onnx".format(model_dir, model_name)

import examples.FCCee.weaver.config as weaverConfig # configuration dictionary of variables
from addons.ONNXRuntime.python.jetFlavourHelper import JetFlavourHelper
jetFlavourHelper = None



# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
    
        global jetFlavourHelper
        jetFlavourHelper = JetFlavourHelper(weaver_preproc, weaver_model, weaverConfig)
        df = jetFlavourHelper.inference(df)
    
        df2 = (
            df
            ##### COMPUTE OBSERVABLES FOR ANALYSIS
            # if not changing training etc... but only interested in the analysis using a trained model (fixed classes), you should only operate in this section.
            # if you're interested in saving variables used for training don't need to compute them again, just
            # add them to the list in at the end of the code
            # EXAMPLE
            # EVENT LEVEL
            # extra jet kinematics (not defined earlier)
            .Define("recojet_pt", "JetClusteringUtils::get_pt(jets_ee_genkt)")
            .Define("recojet_e", "JetClusteringUtils::get_e(jets_ee_genkt)")
            .Define("recojet_mass", "JetClusteringUtils::get_m(jets_ee_genkt)")
            .Define("recojet_phi", "JetClusteringUtils::get_phi(jets_ee_genkt)")
            .Define("recojet_theta", "JetClusteringUtils::get_theta(jets_ee_genkt)")
            # counting types of particles composing the jet
        )

        return df2

    # __________________________________________________________
    # SAVE PREDICTIONS & OBSERVABLES FOR ANALYSIS
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = ["recojet_mass", "recojet_e", "recojet_pt", "event_invariant_mass", "event_njet"]
        branchList += jetFlavourHelper.outputBranches()
        return branchList
