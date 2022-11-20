import sys

# Mandatory: List of processes
processList = {
    # prefall2022 samples (generated centrally)
    "p8_ee_ZH_Znunu_Hbb_ecm240": {},  # 1030000 events
    "p8_ee_ZH_Znunu_Hcc_ecm240": {},  # 1060000
    "p8_ee_ZH_Znunu_Hss_ecm240": {},  # 1060000
    "p8_ee_ZH_Znunu_Hgg_ecm240": {"fraction": 0.5},  # 2000000
    "p8_ee_ZH_Znunu_Huu_ecm240": {
        "fraction": 0.5
    },  # we take only half sample for uu,dd because they will go into qq label which contains both
    "p8_ee_ZH_Znunu_Hdd_ecm240": {
        "fraction": 0.5
    },  # and we want for qq same number of jets as other classes; the two files 2080000 events in total, 1040000 each?
}

# Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
# prodTag     = "FCCee/spring2021/IDEA/"
prodTag = "FCCee/pre_fall2022_training/IDEA/"  # for prefall2022 samples

# Optional: output directory, default is local running directory
# outputDir   = "/eos/home-a/adelvecc/FCCevaluate/"

# Optional
nCPUS = 1
runBatch = False
# batchQueue = "longlunch"
# compGroup = "group_u_FCC.local_gen"


model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/pre_fall2022_training/IDEA/selvaggi_2022Oct30/"
weaver_preproc = "{}/preprocess_fccee_flavtagging_edm4hep_v2.json".format(model_dir)
weaver_model = "{}/fccee_flavtagging_edm4hep_v2.onnx".format(model_dir)

## extract input variables/score name and ordering from json file
import json

variables, scores = [], []
f = open(weaver_preproc)
data = json.load(f)
for varname in data["pf_features"]["var_names"]:
    variables.append(varname)
for scorename in data["output_names"]:
    scores.append(scorename)

f.close()
# convert to tuple
variables = tuple(variables)

from examples.FCCee.weaver.stage1 import definition, alias

# first aliases
for var, al in alias.items():
    print(var, al)

# then funcs
for varname in variables:
    if varname not in definition:
        print("ERROR: {} variables was not defined.".format(varname))
        sys.exit()

# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):

        get_weight_str = "JetFlavourUtils::get_weights("
        for var in variables:
            get_weight_str += "{},".format(var)
        get_weight_str = "{})".format(get_weight_str[:-1])

        from ROOT import JetFlavourUtils

        weaver = JetFlavourUtils.setup_weaver(
            weaver_model,  # name of the trained model exported
            weaver_preproc,  # .json file produced by weaver during training
            variables,
        )

        ### COMPUTE THE VARIABLES FOR INFERENCE OF THE TRAINING MODEL
        # first aliases
        for var, al in alias.items():
            df = df.Alias(var, al)
        # then funcs
        for var, call in definition.items():
            df = df.Define(var, call)

        ##### RUN INFERENCE and cast scores (fixed by the previous section)
        df = df.Define("MVAVec", get_weight_str)

        for i, scorename in enumerate(scores):
            df = df.Define(
                scorename, "JetFlavourUtils::get_weight(MVAVec, {})".format(i)
            )

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
        branchList = [
            # predictions
            "recojet_isG",
            "recojet_isQ",
            "recojet_isS",
            "recojet_isC",
            "recojet_isB",
            # observables
            "recojet_mass",
            "recojet_e",
            "recojet_pt",
            "invariant_mass",
            "nconst",
            "nchargedhad",
            "pfcand_e",
            "pfcand_pt",
            "pfcand_phi",
            "pfcand_erel",
            "pfcand_erel_log",
        ]
        return branchList
