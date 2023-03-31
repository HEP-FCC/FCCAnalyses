import json
import ROOT


class ExclusiveJetClusteringHelper:
    def __init__(self, coll, njets, tag=""):

        self.input_coll = coll
        self.njets = njets

        self.tag = tag
        if tag != "":
            self.tag = "_{}".format(tag)

        part_px = "part{}_px".format(self.tag)
        part_py = "part{}_py".format(self.tag)
        part_pz = "part{}_pz".format(self.tag)
        part_e = "part{}_e".format(self.tag)
        part_m = "part{}_m".format(self.tag)
        part_q = "part{}_q".format(self.tag)

        pjetc = "pjetc{}".format(self.tag)

        _jet = "_jet{}".format(self.tag)
        jet = "jet{}".format(self.tag)
        _jetc = "_jetc{}".format(self.tag)
        jetc = "jetc{}".format(self.tag)

        # compute jet observables

        observables = ["p", "e", "mass", "phi", "theta", "nconst"]

        self.jet_obs = dict()
        for obs in observables:
            self.jet_obs[obs] = "jet_{}{}".format(obs, self.tag)
        event_njet = "event_njet{}".format(self.tag)

        self.jets = jet
        self.constituents = jetc

        self.definition = dict()

        # get single particle properties
        self.definition[part_px] = "ReconstructedParticle::get_px({})".format(self.input_coll)
        self.definition[part_py] = "ReconstructedParticle::get_py({})".format(self.input_coll)
        self.definition[part_pz] = "ReconstructedParticle::get_pz({})".format(self.input_coll)
        self.definition[part_e] = "ReconstructedParticle::get_e({})".format(self.input_coll)
        self.definition[part_m] = "ReconstructedParticle::get_mass({})".format(self.input_coll)
        self.definition[part_q] = "ReconstructedParticle::get_charge({})".format(self.input_coll)

        # form fastjet pseudo jets
        self.definition[pjetc] = "JetClusteringUtils::set_pseudoJets({}, {}, {}, {})".format(
            part_px, part_py, part_pz, part_e
        )

        # run jet clustering with all reconstructed particles. ee_kt_algorithm, R=1.5, inclusive clustering, E-scheme
        self.definition[_jet] = "JetClustering::clustering_ee_kt(2, {}, 1, 0)({})".format(njets, pjetc)

        # get the jets out of the struct
        self.definition[jet] = "JetClusteringUtils::get_pseudoJets({})".format(_jet)

        # get the jets constituents out of the struct
        self.definition[_jetc] = "JetClusteringUtils::get_constituents({})".format(_jet)

        # get constituents
        self.definition[jetc] = "JetConstituentsUtils::build_constituents_cluster({}, {})".format(
            self.input_coll, _jetc
        )

        # compute jet observables
        self.definition[self.jet_obs["p"]] = "JetClusteringUtils::get_p({})".format(self.jets)
        self.definition[self.jet_obs["e"]] = "JetClusteringUtils::get_e({})".format(self.jets)
        self.definition[self.jet_obs["mass"]] = "JetClusteringUtils::get_m({})".format(self.jets)
        self.definition[self.jet_obs["phi"]] = "JetClusteringUtils::get_phi({})".format(self.jets)
        self.definition[self.jet_obs["theta"]] = "JetClusteringUtils::get_theta({})".format(self.jets)
        self.definition[self.jet_obs["nconst"]] = "JetConstituentsUtils::count_consts({})".format(self.constituents)
        self.definition[event_njet] = "JetConstituentsUtils::count_jets({})".format(self.constituents)

    def define(self, df):

        for var, call in self.definition.items():
            df = df.Define(var, call)

        return df

    def outputBranches(self):

        out = list(self.jet_obs.values())
        out += [obs for obs in self.definition.keys() if "event_" in obs]
        return out
