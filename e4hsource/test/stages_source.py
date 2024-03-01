# list of processes (mandatory)
processList = {
    'p8_ee_WW_ecm240': {'output': 'p8_ee_WW_ecm240_out'}
}

# Production tag when running over EDM4Hep centrally produced events, this
# points to the yaml files for getting sample statistics (mandatory)
prodTag = "FCCee/winter2023/IDEA/"

# Optional: output directory, default is local running directory
outputDir = "."

# Ncpus, default is 4, -1 uses all cores available
# nCPUS = -1

# How to read input files
useDataSource = True

testFile = 'https://fccsw.web.cern.ch/fccsw/testsamples/' \
           'edm4hep1/p8_ee_WW_ecm240_edm4hep.root'

# RDFanalysis class where the use defines the operations on the TTree
# (mandatory)
class RDFanalysis():

    # analysis function to define the analyzers to process, please make sure
    # you return the last dataframe, in this example it is df2
    def analysers(df):

        df2 = (
            df
            .Define(
              "electron_truth",
              "FCCAnalyses::ReconstructedParticle::selPDG(11)(MCRecoAssociations)")

            .Define(
              "electron_truth_pt",
              "FCCAnalyses::ReconstructedParticle::getPt(electron_truth)")
        )

        return df2

    def output():
        branchList = [
                "electron_truth",
                "electron_truth_pt"
        ]

        return branchList
