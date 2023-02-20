from examples.FCCee.weaver.config import (
    alias,
    definition,
    variables_pfcand,
    variables_jet,
)

# ___________________________________________________________________________________________________
class RDFanalysis:
    def analysers(df):

        # first aliases
        for var, al in alias.items():
            df = df.Alias(var, al)
        # then funcs
        for var, call in definition.items():
            df = df.Define(var, call)

        return df

    def output():

        branches_pfcand = list(variables_pfcand.keys())
        branches_jet = list(variables_jet.keys())
        branches_event = [
            ## global variables
            "event_njet",
            "event_invariant_mass",
        ]

        branchList = branches_event + branches_jet + branches_pfcand
        return branchList
