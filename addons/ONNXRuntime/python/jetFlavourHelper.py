import sys
import json
import ROOT

ROOT.gROOT.SetBatch(True)

class JetFlavourHelper:
    def __init__(self, coll, jet, jetc, tag=""):

        self.jet = jet
        self.const = jetc

        self.tag = tag
        if tag != "":
            self.tag = "_{}".format(tag)

        self.particle = coll["GenParticles"]
        self.pfcand = coll["PFParticles"]
        self.pftrack = coll["PFTracks"]
        self.pfphoton = coll["PFPhotons"]
        self.pfnh = coll["PFNeutralHadrons"]
        self.trackstate = coll["TrackState"]
        self.trackerhits = coll["TrackerHits"]
        self.calohits = coll["CalorimeterHits"]
        self.dndx = coll["dNdx"]
        self.l = coll["PathLength"]
        self.bz = coll["Bz"]

        self.definition = dict()

        # ===== VERTEX
        # MC primary vertex
        self.definition["pv{}".format(self.tag)] = "FCCAnalyses::MCParticle::get_EventPrimaryVertexP4()( {} )".format(
            self.particle
        )

        # build jet constituents lists
        self.definition["pfcand_isMu{}".format(self.tag)] = "JetConstituentsUtils::get_isMu({})".format(self.const)
        self.definition["pfcand_isEl{}".format(self.tag)] = "JetConstituentsUtils::get_isEl({})".format(self.const)
        self.definition["pfcand_isChargedHad{}".format(self.tag)] = "JetConstituentsUtils::get_isChargedHad({})".format(
            self.const
        )
        self.definition["pfcand_isGamma{}".format(self.tag)] = "JetConstituentsUtils::get_isGamma({})".format(
            self.const
        )
        self.definition["pfcand_isNeutralHad{}".format(self.tag)] = "JetConstituentsUtils::get_isNeutralHad({})".format(
            self.const
        )

        # kinematics, displacement, PID
        self.definition["pfcand_e{}".format(self.tag)] = "JetConstituentsUtils::get_e({})".format(self.const)
        self.definition["pfcand_p{}".format(self.tag)] = "JetConstituentsUtils::get_p({})".format(self.const)
        self.definition["pfcand_theta{}".format(self.tag)] = "JetConstituentsUtils::get_theta({})".format(self.const)
        self.definition["pfcand_phi{}".format(self.tag)] = "JetConstituentsUtils::get_phi({})".format(self.const)
        self.definition["pfcand_charge{}".format(self.tag)] = "JetConstituentsUtils::get_charge({})".format(self.const)
        self.definition["pfcand_type{}".format(self.tag)] = "JetConstituentsUtils::get_type({})".format(self.const)
        self.definition["pfcand_erel{}".format(self.tag)] = "JetConstituentsUtils::get_erel_cluster({}, {})".format(
            jet, self.const
        )

        self.definition[
            "pfcand_erel_log{}".format(self.tag)
        ] = "JetConstituentsUtils::get_erel_log_cluster({}, {})".format(jet, self.const)

        self.definition[
            "pfcand_thetarel{}".format(self.tag)
        ] = "JetConstituentsUtils::get_thetarel_cluster({}, {})".format(jet, self.const)

        self.definition["pfcand_phirel{}".format(self.tag)] = "JetConstituentsUtils::get_phirel_cluster({}, {})".format(
            jet, self.const
        )

        self.definition[
            "pfcand_dndx{}".format(self.tag)
        ] = "JetConstituentsUtils::get_dndx({}, {}, {}, pfcand_isChargedHad{})".format(
            self.const, self.dndx, self.pftrack, self.tag
        )

        self.definition[
            "pfcand_mtof{}".format(self.tag)
        ] = "JetConstituentsUtils::get_mtof({}, {}, {}, {}, {}, {}, {}, pv{})".format(
            self.const, self.l, self.pftrack, self.trackerhits, self.pfphoton, self.pfnh, self.calohits, self.tag
        )

        self.definition["Bz{}".format(self.tag)] = "{}[0]".format(self.bz)

        self.definition[
            "pfcand_dxy{}".format(self.tag)
        ] = "JetConstituentsUtils::XPtoPar_dxy({}, {}, pv{}, Bz{})".format(
            self.const, self.trackstate, self.tag, self.tag
        )

        self.definition["pfcand_dz{}".format(self.tag)] = "JetConstituentsUtils::XPtoPar_dz({}, {}, pv{}, Bz{})".format(
            self.const, self.trackstate, self.tag, self.tag
        )

        self.definition[
            "pfcand_phi0{}".format(self.tag)
        ] = "JetConstituentsUtils::XPtoPar_phi({}, {}, pv{}, Bz{})".format(
            self.const, self.trackstate, self.tag, self.tag
        )

        self.definition["pfcand_C{}".format(self.tag)] = "JetConstituentsUtils::XPtoPar_C({}, {}, Bz{})".format(
            self.const, self.trackstate, self.tag
        )

        self.definition["pfcand_ct{}".format(self.tag)] = "JetConstituentsUtils::XPtoPar_ct({}, {}, Bz{})".format(
            self.const, self.trackstate, self.tag
        )

        self.definition["pfcand_dptdpt{}".format(self.tag)] = "JetConstituentsUtils::get_omega_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dxydxy{}".format(self.tag)] = "JetConstituentsUtils::get_d0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dzdz{}".format(self.tag)] = "JetConstituentsUtils::get_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dphidphi{}".format(self.tag)] = "JetConstituentsUtils::get_phi0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition[
            "pfcand_detadeta{}".format(self.tag)
        ] = "JetConstituentsUtils::get_tanlambda_cov({}, {})".format(self.const, self.trackstate)

        self.definition["pfcand_dxydz{}".format(self.tag)] = "JetConstituentsUtils::get_d0_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dphidxy{}".format(self.tag)] = "JetConstituentsUtils::get_phi0_d0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_phidz{}".format(self.tag)] = "JetConstituentsUtils::get_phi0_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition[
            "pfcand_phictgtheta{}".format(self.tag)
        ] = "JetConstituentsUtils::get_tanlambda_phi0_cov({}, {})".format(self.const, self.trackstate)

        self.definition[
            "pfcand_dxyctgtheta{}".format(self.tag)
        ] = "JetConstituentsUtils::get_tanlambda_d0_cov({}, {})".format(self.const, self.trackstate)

        self.definition[
            "pfcand_dlambdadz{}".format(self.tag)
        ] = "JetConstituentsUtils::get_tanlambda_z0_cov({}, {})".format(self.const, self.trackstate)

        self.definition[
            "pfcand_cctgtheta{}".format(self.tag)
        ] = "JetConstituentsUtils::get_omega_tanlambda_cov({}, {})".format(self.const, self.trackstate)

        self.definition["pfcand_phic{}".format(self.tag)] = "JetConstituentsUtils::get_omega_phi0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dxyc{}".format(self.tag)] = "JetConstituentsUtils::get_omega_d0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_cdz{}".format(self.tag)] = "JetConstituentsUtils::get_omega_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition[
            "pfcand_btagSip2dVal{}".format(self.tag)
        ] = "JetConstituentsUtils::get_Sip2dVal_clusterV({}, pfcand_dxy{}, pfcand_phi0{}, Bz{})".format(
            jet, self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagSip2dSig{}".format(self.tag)
        ] = "JetConstituentsUtils::get_Sip2dSig(pfcand_btagSip2dVal{}, pfcand_dxydxy{})".format(self.tag, self.tag)

        self.definition[
            "pfcand_btagSip3dVal{}".format(self.tag)
        ] = "JetConstituentsUtils::get_Sip3dVal_clusterV({}, pfcand_dxy{}, pfcand_dz{}, pfcand_phi0{}, Bz{})".format(
            jet, self.tag, self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagSip3dSig{}".format(self.tag)
        ] = "JetConstituentsUtils::get_Sip3dSig(pfcand_btagSip3dVal{}, pfcand_dxydxy{}, pfcand_dzdz{})".format(
            self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagJetDistVal{}".format(self.tag)
        ] = "JetConstituentsUtils::get_JetDistVal_clusterV({}, {}, pfcand_dxy{}, pfcand_dz{}, pfcand_phi0{}, Bz{})".format(
            jet, self.const, self.tag, self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagJetDistSig{}".format(self.tag)
        ] = "JetConstituentsUtils::get_JetDistSig(pfcand_btagJetDistVal{}, pfcand_dxydxy{}, pfcand_dzdz{})".format(
            self.tag, self.tag, self.tag
        )

        self.definition["jet_nmu{}".format(self.tag)] = "JetConstituentsUtils::count_type(pfcand_isMu{})".format(
            self.tag
        )
        self.definition["jet_nel{}".format(self.tag)] = "JetConstituentsUtils::count_type(pfcand_isEl{})".format(
            self.tag
        )
        self.definition[
            "jet_nchad{}".format(self.tag)
        ] = "JetConstituentsUtils::count_type(pfcand_isChargedHad{})".format(self.tag)
        self.definition["jet_ngamma{}".format(self.tag)] = "JetConstituentsUtils::count_type(pfcand_isGamma{})".format(
            self.tag
        )
        self.definition[
            "jet_nnhad{}".format(self.tag)
        ] = "JetConstituentsUtils::count_type(pfcand_isNeutralHad{})".format(self.tag)

    def define(self, df):

        for var, call in self.definition.items():
            df = df.Define(var, call)

        return df

    def inference(self, jsonCfg, onnxCfg, df):

        ## extract input variables/score name and ordering from json file
        initvars, self.variables, self.scores = [], [], []
        f = open(jsonCfg)
        data = json.load(f)

        for varname in data["pf_features"]["var_names"]:
            initvars.append(varname)
            self.variables.append("{}{}".format(varname, self.tag))

        for varname in data["pf_vectors"]["var_names"]:
            initvars.append(varname)
            self.variables.append("{}{}".format(varname, self.tag))

        for scorename in data["output_names"]:
            # self.scores.append(scorename)
            # self.scores.append(scorename.replace("jet", "jet{}".format(self.tag)))
            self.scores.append("{}{}".format(scorename, self.tag))

        f.close()
        # convert to tuple
        initvars = tuple(initvars)

        # then funcs
        for varname in self.variables:
            matches = [obs for obs in self.definition.keys() if obs == varname]
            if len(matches) != 1:
                print("ERROR: {} variables was not defined.".format(varname))
                sys.exit()

        self.get_weight_str = "JetFlavourUtils::get_weights(rdfslot_, "
        for var in self.variables:
            self.get_weight_str += "{},".format(var)
        self.get_weight_str = "{})".format(self.get_weight_str[:-1])

        from ROOT import JetFlavourUtils

        weaver = JetFlavourUtils.setup_weaver(
            onnxCfg,  # name of the trained model exported
            jsonCfg,  # .json file produced by weaver during training
            initvars,
            ROOT.GetThreadPoolSize() if ROOT.GetThreadPoolSize() > 0 else 1,
        )

        # run inference and cast scores
        df = df.Define("MVAVec_{}".format(self.tag), self.get_weight_str)

        for i, scorename in enumerate(self.scores):
            df = df.Define(scorename, "JetFlavourUtils::get_weight(MVAVec_{}, {})".format(self.tag, i))

        return df

    def outputBranches(self):

        out = self.scores
        out += [obs for obs in self.definition.keys() if "jet_" in obs]
        return out
