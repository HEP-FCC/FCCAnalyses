import os
import urllib.request
import ROOT
from copy import deepcopy

"""
This example runs the jet clustering sequence with Durham N=2 exclusive algorithm and produces jet scores for the various
flavour with variations of the impact parameter resolution and neutral hadrons energy resolutions.

To run this example:

fccanalysis run examples/FCCee/smearing/smear_jets.py \
--files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_nunuH_Hss_ecm240/events_196755633.root \
--nevents 100 \

"""

# ____________________________________________________________
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


# ____________________________________________________________
def jet_sequence(df, collections, output_branches, tag=""):

    ## define jet clustering parameters
    njets = 2

    jetClusteringHelper = ExclusiveJetClusteringHelper(collections["PFParticles"], njets, tag)
    ## run jet clustering

    df = jetClusteringHelper.define(df)

    output_branches += jetClusteringHelper.outputBranches()

    jets_p4 = "tlv_jets"
    mjj = "mjj"

    if tag != "":
        jets_p4 = "tlv_jets_{}".format(tag)
        mjj = "mjj_{}".format(tag)

    df = df.Define(jets_p4, "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
    df = df.Define(mjj, "JetConstituentsUtils::InvariantMass({}[0], {}[1])".format(jets_p4, jets_p4))
    output_branches.append(mjj)

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

    output_branches += jetFlavourHelper.outputBranches()

    return df


# ____________________________________________________________

## input file needed for unit test in CI
testFile = "https://fccsw.web.cern.ch/fccsw/testsamples/wzp6_ee_nunuH_Hss_ecm240.root"

## latest particle transformer model, trainied on 9M jets in winter2023 samples
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

from addons.ONNXRuntime.python.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.python.jetClusteringHelper import ExclusiveJetClusteringHelper

output_branches = []

# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):

        ## name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "MCRecoMap": "MCRecoAssociations",
            "PFParticles": "ReconstructedParticles",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        ## run full sequence with nominal detector
        df = jet_sequence(df, collections, output_branches)

        ## define MC/Reco links, needed for smearing
        df = (
            df.Alias("mc_reco_0", "{}#0.index".format(collections["MCRecoMap"])).Alias(
                "mc_reco_1", "{}#1.index".format(collections["MCRecoMap"])
            )
            # matching between the RecoParticles and the MCParticles:
            .Define(
                "reco_mc_index",
                "ReconstructedParticle2MC::getRP2MC_index(mc_reco_0,mc_reco_1,{})".format(collections["PFParticles"]),
            )
        )

        ## produce smeared collections

        ### run same sequences but with smeared collection
        scale_factors = [1.0, 2.0, 5.0, 10.0]

        
        for sf in scale_factors:
        
            ## 1. do Impact parameter smearing first

            collections_ip = deepcopy(collections)
            ip_tag = "ip{}".format(sf).replace(".", "p")
            collections_ip["TrackState"] = "TrackState_{}".format(ip_tag)

            # Generate a new set of tracks, re-scaling the covariance matrix
            # order of the scaling factors : smear_d0, smear_phi, smear_omega, smear_z0, smear_tlambda
            # the boolean flag is for debugging
            # here smear only d0, z0
            df = df.Define(
                collections_ip["TrackState"],
                ROOT.SmearObjects.SmearedTracks(sf, 1.0, 1.0, sf, 1.0, False),
                [collections["PFParticles"], collections["TrackState"], "reco_mc_index", collections["GenParticles"]],
            )

            ## run full sequence with covariance smeared detector
            df = jet_sequence(df, collections_ip, output_branches, ip_tag)


            ## 2. do Neutral Hadron energy smearing

            collections_res = deepcopy(collections)
            res_tag = "res{}".format(sf).replace(".", "p")
            collections_res["PFParticles"] = "ReconstructedParticles_{}".format(res_tag)

            df = df.Define(
                collections_res["PFParticles"],
                # type: 11 (electrons), 13 (muons), 130 (neutral hadrons), 22 (photon), 0 (charged hadrons), -1 (all)
                # mode: 0 energy, 1 momentum
                # parameters (scale, type, mode, debug)
                # here re-smear only neutral hadrons (130) in energy mode
                ROOT.SmearObjects.SmearedReconstructedParticle(sf, 130, 0, False),
                [collections["PFParticles"], "reco_mc_index", collections["GenParticles"]],
            )

            ## run full sequence with energy nh smeared
            df = jet_sequence(df, collections_res, output_branches, res_tag)

            ## 3. do dNdx smearing

            collections_dndx = deepcopy(collections)
            dndx_tag = "dndx{}".format(sf).replace(".", "p")
            collections_dndx["dNdx"] = "dNdx_{}".format(dndx_tag)

            df = df.Define(
                collections_dndx["dNdx"],
                ROOT.SmearObjects.SmearedTracksdNdx(sf, False),
                [
                    collections["PFParticles"],
                    collections["dNdx"],
                    collections["PathLength"],
                    "reco_mc_index",
                    collections["GenParticles"],
                ],
            )

            ## run full sequence with energy nh smeared
            df = jet_sequence(df, collections_dndx, output_branches, dndx_tag)


            ## 4. do tof smearing
            collections_tof = deepcopy(collections)
            tof_tag = "tof{}".format(sf).replace(".", "p")
            collections_tof["TrackerHits"] = "tof_{}".format(tof_tag)

            df = df.Define(
                collections_tof["TrackerHits"],
                ROOT.SmearObjects.SmearedTracksTOF(sf, False),
                [
                    collections["PFParticles"],
                    collections["PFTracks"],
                    collections["TrackerHits"],
                    collections["PathLength"],
                    "reco_mc_index",
                    collections["GenParticles"],
                ],
            )

            ## run full sequence with energy nh smeared
            df = jet_sequence(df, collections_tof, output_branches, tof_tag)

        return df

    # __________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list

    def output():
        return output_branches
