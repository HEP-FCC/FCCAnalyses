"""ATLAS-style ghost jet labels and constituent truth labels.

The jet labels are obtained by re-running the analysis' own jet clustering with
truth particles added as ghosts, so they are a property of the clustering and
work for any jet algorithm. The clustering helper supplies the algorithm
through its ``clustering_spec``, ``input_pseudojets`` and
``constituent_indices`` attributes.
"""


class JetTruthLabelHelper:
    """Define ghost jet labels and per-constituent truth labels.

    Parameters
    ----------
    coll : dict
        Collection names. Needs ``GenParticles`` and, optionally,
        ``RecoMCLink`` (default ``"RecoMCLink"``; older productions call it
        ``"MCRecoAssociations"``).
    clustering : object
        The jet clustering helper used for the analysis.
    hadron_pt_min : float
        Minimum pT of a ghost hadron or tau, in GeV.
    tag : str
        Suffix appended to every column, to allow several jet collections.
    """

    def __init__(self, coll, clustering, hadron_pt_min=1.0, tag=""):
        self.tag = "_{}".format(tag) if tag else ""
        self.particle = coll["GenParticles"]
        self.link = coll.get("RecoMCLink", "RecoMCLink")
        self.jets = clustering.jets
        self.pjetc = clustering.input_pseudojets
        self.jetc = clustering.constituent_indices
        self.clustering_spec = clustering.clustering_spec
        self.hadron_pt_min = hadron_pt_min

        self.aliases = {
            "TLRecoMCFrom{}".format(self.tag): "_{}_from.index".format(self.link),
            "TLRecoMCTo{}".format(self.tag): "_{}_to.index".format(self.link),
            "TLMCParents{}".format(self.tag): "_{}_parents.index".format(self.particle),
            "TLMCDaughters{}".format(self.tag): "_{}_daughters.index".format(self.particle),
        }

        t = self.tag
        par = self.particle
        self.definition = dict()

        # ghost particle lists: heavy hadrons in both ATLAS conventions, and
        # the last partons before hadronisation
        self.definition["ghost_hadrons{}".format(t)] = (
            "JetGhostLabels::get_ghost_hadrons({}, TLMCParents{}, TLMCDaughters{}, {}, true, true)".format(
                par, t, t, self.hadron_pt_min
            )
        )
        self.definition["ghost_hadrons_initial{}".format(t)] = (
            "JetGhostLabels::get_ghost_hadrons({}, TLMCParents{}, TLMCDaughters{}, {}, false, true)".format(
                par, t, t, self.hadron_pt_min
            )
        )
        self.definition["ghost_partons{}".format(t)] = (
            "JetGhostLabels::get_ghost_partons({}, TLMCDaughters{})".format(par, t)
        )

        # ghost association: re-cluster with the ghosts added
        for name in ("hadrons", "hadrons_initial", "partons"):
            self.definition["ghost_assoc_{}{}".format(name, t)] = (
                "JetGhostLabels::associate_ghosts({}, {}, {}, ghost_{}{})".format(
                    self.clustering_spec, self.pjetc, self.jetc, name, t
                )
            )

        # jet labels, named as in ATLAS
        self.definition["jet_HadronGhostTruthLabelID{}".format(t)] = (
            "JetGhostLabels::get_hadron_label({}, ghost_assoc_hadrons{}, ghost_hadrons{})".format(self.jets, t, t)
        )
        self.definition["jet_HadronGhostExtendedTruthLabelID{}".format(t)] = (
            "JetGhostLabels::get_hadron_extended_label({}, ghost_assoc_hadrons{}, ghost_hadrons{})".format(
                self.jets, t, t
            )
        )
        self.definition["jet_HadronGhostTruthLabelPdgId{}".format(t)] = (
            "JetGhostLabels::get_hadron_label_pdg({}, ghost_assoc_hadrons{}, ghost_hadrons{})".format(self.jets, t, t)
        )
        self.definition["jet_HadronGhostTruthLabelPt{}".format(t)] = (
            "JetGhostLabels::get_hadron_label_pt({}, ghost_assoc_hadrons{}, ghost_hadrons{})".format(self.jets, t, t)
        )

        self.definition["jet_HadronGhostInitialTruthLabelID{}".format(t)] = (
            "JetGhostLabels::get_hadron_label({}, ghost_assoc_hadrons_initial{}, ghost_hadrons_initial{})".format(
                self.jets, t, t
            )
        )
        self.definition["jet_HadronGhostInitialExtendedTruthLabelID{}".format(t)] = (
            "JetGhostLabels::get_hadron_extended_label({}, ghost_assoc_hadrons_initial{}, "
            "ghost_hadrons_initial{})".format(self.jets, t, t)
        )
        self.definition["jet_HadronGhostInitialTruthLabelPdgId{}".format(t)] = (
            "JetGhostLabels::get_hadron_label_pdg({}, ghost_assoc_hadrons_initial{}, "
            "ghost_hadrons_initial{})".format(self.jets, t, t)
        )

        self.definition["jet_GhostBHadronsFinalCount{}".format(t)] = (
            "JetGhostLabels::count_ghosts({}, ghost_assoc_hadrons{}, ghost_hadrons{}, 5)".format(self.jets, t, t)
        )
        self.definition["jet_GhostCHadronsFinalCount{}".format(t)] = (
            "JetGhostLabels::count_ghosts({}, ghost_assoc_hadrons{}, ghost_hadrons{}, 4)".format(self.jets, t, t)
        )

        self.definition["jet_PartonTruthLabelID{}".format(t)] = (
            "JetGhostLabels::get_parton_label({}, ghost_assoc_partons{}, ghost_partons{})".format(self.jets, t, t)
        )
        self.definition["jet_PartonTruthLabelPt{}".format(t)] = (
            "JetGhostLabels::get_parton_label_pt({}, ghost_assoc_partons{}, ghost_partons{})".format(self.jets, t, t)
        )
        self.definition["jet_PartonTruthLabelDR{}".format(t)] = (
            "JetGhostLabels::get_parton_label_dr({}, ghost_assoc_partons{}, ghost_partons{})".format(self.jets, t, t)
        )

        # per-constituent truth labels
        self.definition["pfcand_truthOriginLabel{}".format(t)] = (
            "ConstituentTruthLabels::get_truthOriginLabel(TLRecoMCFrom{}, TLRecoMCTo{}, {}, TLMCParents{}, {})".format(
                t, t, par, t, self.jetc
            )
        )
        self.definition["pfcand_truthTypeLabel{}".format(t)] = (
            "ConstituentTruthLabels::get_truthTypeLabel(TLRecoMCFrom{}, TLRecoMCTo{}, {}, TLMCParents{}, {})".format(
                t, t, par, t, self.jetc
            )
        )
        self.definition["pfcand_truthSourceLabel{}".format(t)] = (
            "ConstituentTruthLabels::get_truthSourceLabel(TLRecoMCFrom{}, TLRecoMCTo{}, {}, TLMCParents{}, {})".format(
                t, t, par, t, self.jetc
            )
        )
        self.definition["pfcand_truthVertexIndex{}".format(t)] = (
            "ConstituentTruthLabels::get_truthVertexIndex(TLRecoMCFrom{}, TLRecoMCTo{}, {}, {})".format(
                t, t, par, self.jetc
            )
        )
        self.definition["pfcand_truthPdgId{}".format(t)] = (
            "ConstituentTruthLabels::get_truthPdgId(TLRecoMCFrom{}, TLRecoMCTo{}, {}, {})".format(t, t, par, self.jetc)
        )

    def define(self, df):
        for alias, target in self.aliases.items():
            df = df.Alias(alias, target)
        for var, call in self.definition.items():
            df = df.Define(var, call)
        return df

    def outputBranches(self):
        """Labels only; the ghost lists and associations stay internal."""
        return [name for name in self.definition if name.startswith(("jet_", "pfcand_"))]
