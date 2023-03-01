## latest particle transformer model, trainied on 9M jets in winter2023 samples
model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022"
model_name = "fccee_flavtagging_edm4hep_wc_v1"

weaver_preproc = "{}/{}.json".format(model_dir, model_name)
weaver_model = "{}/{}.onnx".format(model_dir, model_name)

from addons.ONNXRuntime.python.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.python.jetClusteringHelper import ExclusiveJetClusteringHelper

jetFlavourHelper = None
jetClusteringHelper = None

# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        global jetClusteringHelper
        global jetFlavourHelper

        from examples.FCCee.weaver.config import collections, njets

        tag = "test"

        ## define jet clustering parameters
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

        ## tagger inference
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        return df

    # __________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():

        ##  outputs jet properties
        branchList = jetClusteringHelper.outputBranches()

        ## outputs jet scores and constituent breakdown
        branchList += jetFlavourHelper.outputBranches()

        return branchList
