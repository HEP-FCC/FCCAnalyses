# list of processes (mandatory)
processList = {
    'p8_ee_WW_ecm240': {'output': 'p8_ee_WW_ecm240_out',
                        'testfile': '/eos/experiment/fcc/ee/generation/'
                                    'DelphesEvents/winter2023/IDEA/'
                                    'p8_ee_WW_ecm240/events_192112516.root'}
}

# Production tag when running over EDM4Hep centrally produced events, this
# points to the yaml files for getting sample statistics (mandatory)
prodTag = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations
# etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Optional: output directory, default is local running directory
outputDir = "."

# Ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
# define some binning for various histograms
bins_pt = (20, 0, 200)

# How to read input files
useDataSource = True

# build_graph function that contains the analysis logic, cuts and histograms
# (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Define(
        "electron_truth",
        "FCCAnalyses::ReconstructedParticle::selPDG(11)(MCRecoAssociations)")

    df = df.Define(
        "electron_truth_pt",
        "FCCAnalyses::ReconstructedParticle::getPt(electron_truth)")

    results.append(df.Histo1D(("h_electron_truth_pt", "", *bins_pt),
                              "electron_truth_pt"))

    return results, weightsum