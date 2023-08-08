# list of processes (mandatory)
processList = {
    'HNL_50_all_REC_EDM4Hep': {'fraction': 1,
                               'crossSection': 2.29*10**(-8)},
}

# Link to the dictonary that contains all the cross section information
# etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"
procDictAdd = {
    "HNL_50_all_REC_EDM4Hep": {"numberOfEvents": 50000,
                               "sumOfWeights": 50000,
                               "crossSection": 2.29*10**(-8),
                               "kfactor": 1.0,
                               "matchingEfficiency": 1.0},
}

# Define the input dir (optional)
inputDir = "/eos/home-j/jandrea/SampleFCCee_HNL/_HNL_50_RECO_EDM4Hep/merged"

# Output directory, default is local running directory
outputDir = "."

# Ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 150000000  # 150 /ab

# define some binning for various histograms
bins_p_el = (2000, 0, 200)  # 100 MeV bins
bins_d0 = (20, 0, 100)
bins_n_states = (30, 0, 30)

# build_graph function that contains the analysis logic, cuts and histograms
# (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Define("Electron_tracks",
                   "FCCAnalyses::Track::selPDG(11)(SiTracksMCTruthLink)")

    df = df.Define("Electron_nTrackStates",
                   "FCCAnalyses::Track::getNstates(Electron_tracks)")
    df = df.Define("Electron_track_d0",
                   "FCCAnalyses::Track::getD0(Electron_tracks)")

    results.append(df.Histo1D(("electron_track_d0", "", *bins_d0),
                              "Electron_track_d0"))
    results.append(df.Histo1D(("electron_nTractStates", "", *bins_n_states),
                              "Electron_nTrackStates"))

    return results, weightsum
