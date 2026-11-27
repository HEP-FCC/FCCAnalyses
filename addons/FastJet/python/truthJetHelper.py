"""Truth jets matched to reconstructed jets.

Truth jets are clustered with the analysis' own jet clustering, taken from the
clustering helper's ``clustering_spec``, so the matching works for any jet
algorithm.
"""


class TruthJetHelper:
    """Define truth-jet kinematics for every reconstructed jet.

    Parameters
    ----------
    coll : dict
        Collection names. Needs ``GenParticles`` and, optionally,
        ``RecoMCLink`` (default ``"RecoMCLink"``).
    clustering : object
        The jet clustering helper used for the analysis.
    tag : str
        Suffix appended to every column, to allow several jet collections.
    """

    def __init__(self, coll, clustering, tag=""):
        t = "_{}".format(tag) if tag else ""
        particle = coll["GenParticles"]
        link = coll.get("RecoMCLink", "RecoMCLink")
        jets = clustering.jets
        jetc = clustering.constituent_indices

        self.aliases = {
            "TJRecoMCFrom{}".format(t): "_{}_from.index".format(link),
            "TJRecoMCTo{}".format(t): "_{}_to.index".format(link),
        }

        reco_mc = "TJRecoMCFrom{0}, TJRecoMCTo{0}, {1}".format(t, particle)
        self.definition = {
            "truth_jets{}".format(t): "TruthJets::cluster_truth_jets({}, {})".format(
                clustering.clustering_spec, particle
            ),
            "truth_jet_match{}".format(t): "TruthJets::match_truth_jets({}, {}, truth_jets{})".format(
                jetc, reco_mc, t
            ),
            "jet_truthJetPt{}".format(t): "TruthJets::get_truth_jet_pt(truth_jet_match{0}, truth_jets{0})".format(t),
            "jet_truthJetEnergy{}".format(t): "TruthJets::get_truth_jet_energy(truth_jet_match{0}, truth_jets{0})".format(
                t
            ),
            "jet_truthJetDR{}".format(t): "TruthJets::get_truth_jet_dr({0}, truth_jet_match{1}, truth_jets{1})".format(
                jets, t
            ),
            "jet_truthJetPurity{}".format(t): (
                "TruthJets::get_truth_jet_purity({0}, {1}, truth_jet_match{2}, truth_jets{2})".format(jetc, reco_mc, t)
            ),
            "jet_truthJetCompleteness{}".format(t): (
                "TruthJets::get_truth_jet_completeness({0}, {1}, truth_jet_match{2}, truth_jets{2})".format(
                    jetc, reco_mc, t
                )
            ),
        }

    def define(self, df):
        for alias, target in self.aliases.items():
            df = df.Alias(alias, target)
        for var, call in self.definition.items():
            df = df.Define(var, call)
        return df

    def outputBranches(self):
        """Truth-jet kinematics only; the truth-jet collection stays internal."""
        return [name for name in self.definition if name.startswith("jet_")]
