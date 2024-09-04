
processList = {
    'wzp6_ee_mumuH_Hbb_ecm240': {'fraction': 1},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Optional: output directory, default is local running directory
outputDir   = f"outputs/FCCee/higgs/jetclustering/histmaker/"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 7200000.0 # 7.2 /ab


# define some binning for various histograms
bins_p_mu = (250, 0, 250)
bins_m_ll = (250, 0, 250)
bins_p_ll = (250, 0, 250)
bins_recoil = (200, 120, 140)
bins_pdgid = (51, -25.5, 25.5)
bins_dijet_m = (80, 70, 150)


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # select muons from Z decay and form Z/recoil mass
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(muons_all)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Filter("muons_no >= 2")

    df = df.Define("zmumu", "ReconstructedParticle::resonanceBuilder(91)(muons)")
    df = df.Define("zmumu_m", "ReconstructedParticle::get_mass(zmumu)[0]")
    df = df.Define("zmumu_p", "ReconstructedParticle::get_p(zmumu)[0]")
    df = df.Define("zmumu_recoil", "ReconstructedParticle::recoilBuilder(240)(zmumu)")
    df = df.Define("zmumu_recoil_m", "ReconstructedParticle::get_mass(zmumu_recoil)[0]")

    # basic selection
    df = df.Filter("zmumu_m > 70 && zmumu_m < 100")
    df = df.Filter("zmumu_p > 20 && zmumu_p < 70")
    df = df.Filter("zmumu_recoil_m < 140 && zmumu_recoil_m > 120")


    # do jet clustering on all particles, except the muons
    df = df.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons)")
    df = df.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons)")
    df = df.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")


    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets)") # 2-jet exclusive clustering

    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_phi", "FCCAnalyses::JetClusteringUtils::get_phi(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    # convert jets to LorentzVectors
    df = df.Define("jets_tlv", "FCCAnalyses::makeLorentzVectors(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jets_truth", "FCCAnalyses::jetTruthFinder(jetconstituents, rps_no_muons, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m", "(jets_tlv[0]+jets_tlv[1]).M()")

    # define histograms
    results.append(df.Histo1D(("zmumu_m", "", *bins_m_ll), "zmumu_m"))
    results.append(df.Histo1D(("zmumu_p", "", *bins_p_ll), "zmumu_p"))
    results.append(df.Histo1D(("zmumu_recoil_m", "", *bins_recoil), "zmumu_recoil_m"))

    results.append(df.Histo1D(("jets_truth", "", *bins_pdgid), "jets_truth"))
    results.append(df.Histo1D(("dijet_higgs_m", "", *bins_dijet_m), "dijet_higgs_m"))

    return results, weightsum

