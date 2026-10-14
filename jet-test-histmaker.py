
processList = {
    'wzp6_ee_nunuH_Huu_ecm240': {'fraction': 0.01},
    'wzp6_ee_nunuH_Hdd_ecm240': {'fraction': 0.01},
    'wzp6_ee_nunuH_Hss_ecm240': {'fraction': 0.01},
    'wzp6_ee_nunuH_Hcc_ecm240': {'fraction': 0.01},
    'wzp6_ee_nunuH_Hbb_ecm240': {'fraction': 0.01},
    'wzp6_ee_nunuH_Hgg_ecm240': {'fraction': 0.01},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/pre_summer2026_training/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
# procDict = "FCCee_procDict_pre_summer2026_training_IDEA.json"
procDict = "FCCee_procDict_pre_summer2026_IDEA.json"
# additional/custom C++ functions, defined in header files (optional)
# includePaths = ["functions.h"]

#Optional: output directory, default is local running directory
outputDir   = "outputs/jet-test"

# optional: ncpus, default is 4, -1 uses all cores available
# nCPUS       = 6
nCPUS       = 1

# scale the histograms with the cross-section and integrated luminosity
doScale = False
intLumi = 7200000.0 # 7.2 /ab


# define some binning for various histograms
bins_p_mu = (250, 0, 250)


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Alias("MCParticles", "Particle")

    # df = df.Alias("Particle0", "Particle#0.index")
    # df = df.Alias("Particle1", "Particle#1.index")
    # df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    # df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # # select muons from Z decay and form Z/recoil mass
    # df = df.Alias("Muon0", "Muon#0.index")
    # df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    # df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(muons_all)")
    # df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    # df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    # df = df.Filter("muons_no >= 2")

    # df = df.Define("zmumu", "ReconstructedParticle::resonanceBuilder(91)(muons)")
    # df = df.Define("zmumu_m", "ReconstructedParticle::get_mass(zmumu)[0]")
    # df = df.Define("zmumu_p", "ReconstructedParticle::get_p(zmumu)[0]")
    # df = df.Define("zmumu_recoil", "ReconstructedParticle::recoilBuilder(240)(zmumu)")
    # df = df.Define("zmumu_recoil_m", "ReconstructedParticle::get_mass(zmumu_recoil)[0]")

    # # basic selection
    # df = df.Filter("zmumu_m > 70 && zmumu_m < 100")
    # df = df.Filter("zmumu_p > 20 && zmumu_p < 70")
    # df = df.Filter("zmumu_recoil_m < 140 && zmumu_recoil_m > 120")


    # do jet clustering on all particles, except the muons
    # df = df.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    # df = df.Define("StableMCParticles", "MCParticles[FCCAnalyses::MCParticle::get_genStatus(MCParticles) == 1]")
    # df = df.Define("StableMCParticles", "FCCAnalyses::MCParticle::sel_genStatus(1)(MCParticles)")
    # df = df.Define("VisibleMCParticles", "StableMCParticles")
    # df = df.Define("VisibleMCParticles", "StableMCParticles[abs(FCCAnalyses::MCParticle::get_pdg(StableMCParticles)) != 12 && abs(FCCAnalyses::MCParticle::get_pdg(StableMCParticles)) != 14 && abs(FCCAnalyses::MCParticle::get_pdg(StableMCParticles)) != 16]")
    # df = df.Define("hadr_idx", "ArgMax(FCCAnalyses::MCParticle::get_pdg(MCParticles) == 92)")
    # count the Pythia special hadronisation entries
    hadronisation_pids = {
        88: "junction",
        91: "cluster",
        92: "string",
        93: "indep",  # independent fragmentation
    }
    df = df.Define("MC_pdg_all", "FCCAnalyses::MCParticle::get_pdg(MCParticles)")
    for pid, name in hadronisation_pids.items():
        df = df.Define(f"n_{name}_{pid}", f"Sum(MC_pdg_all == {pid})")
        results.append(df.Histo1D((f"n_{name}_{pid}", "", 10, 0., 10.), f"n_{name}_{pid}"))

    # final partons entering the hadronisation
    df = df.Define("HadronisationPartons", "FCCAnalyses::MCParticle::get_hadronisation_partons(MCParticles, _Particle_parents.index, _Particle_daughters.index)")
    df = df.Define("n_hadronisation_partons", "HadronisationPartons.size()")
    results.append(df.Histo1D(("n_hadronisation_partons", "", 50, 0., 50.), "n_hadronisation_partons"))

    # primary hadrons, i.e. the hadrons directly after hadronisation, before they decay
    df = df.Define("VisibleMCParticles", "FCCAnalyses::MCParticle::get_primary_hadrons(MCParticles, _Particle_daughters.index)")
    df = df.Define("MC_px", "FCCAnalyses::MCParticle::get_px(VisibleMCParticles)")
    df = df.Define("MC_py", "FCCAnalyses::MCParticle::get_py(VisibleMCParticles)")
    df = df.Define("MC_pz","FCCAnalyses::MCParticle::get_pz(VisibleMCParticles)")
    df = df.Define("MC_m", "FCCAnalyses::MCParticle::get_mass(VisibleMCParticles)")
    df = df.Define("MC_e", "FCCAnalyses::MCParticle::get_e(VisibleMCParticles)")
    df = df.Define("MC_pdg", "FCCAnalyses::MCParticle::get_pdg(VisibleMCParticles)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets_xyzm_flav(MC_px, MC_py, MC_pz, MC_m, MC_pdg)")

    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # 2-jet exclusive flavour-aware clustering, with IFN and with plain net flavour summation for comparison
    clusterings = {
        "ifn": "JetClustering::flv_ifn_clustering_ee_kt(2, 2, 0, 0)(pseudo_jets)",
        "net": "JetClustering::flv_net_clustering_ee_kt(2, 2, 0, 0)(pseudo_jets)",
    }

    df = df.Define("MC_e_sum", "Sum(MC_e)")
    results.append(df.Histo1D(("MC_e_sum", "", 250, 0., 250.), "MC_e_sum"))

    for name, clustering in clusterings.items():
        df = df.Define(f"{name}_clustered_jets", clustering)

        df = df.Define(f"{name}_jets", f"FCCAnalyses::JetClusteringUtils::get_pseudoJets({name}_clustered_jets)")
        df = df.Define(f"{name}_jetconstituents", f"FCCAnalyses::JetClusteringUtils::get_constituents({name}_clustered_jets)")
        for var in ["e", "px", "py", "pz", "phi", "m"]:
            df = df.Define(f"{name}_jets_{var}", f"FCCAnalyses::JetClusteringUtils::get_{var}({name}_jets)")

        # df = df.Define(f"{name}_jets_flv", f"FCCAnalyses::JetClusteringUtils::get_flavours({name}_jets)")
        for flv in ["b", "c", "s", "d", "u"]:
            df = df.Define(f"{name}_jets_{flv}_content", f"FCCAnalyses::JetClusteringUtils::get_{flv}_content({name}_jets)")

        # convert jets to LorentzVectors
        df = df.Define(f"{name}_jets_lv", f"Construct<ROOT::Math::PxPyPzEVector>({name}_jets_px, {name}_jets_py, {name}_jets_pz, {name}_jets_e)")
        df = df.Define(f"{name}_dijet_higgs_m", f"({name}_jets_lv[0]+{name}_jets_lv[1]).M()")

        # define histograms
        results.append(df.Histo1D((f"{name}_jets_e", "", 250, 0., 250.), f"{name}_jets_e"))
        results.append(df.Histo1D((f"{name}_M_jj", "", 250, 0., 250.), f"{name}_dijet_higgs_m"))
        for flv in ["b", "c", "s", "d", "u"]:
            results.append(df.Histo1D((f"{name}_jets_{flv}_content", "", 10, -5., 5.), f"{name}_jets_{flv}_content"))

    return results, weightsum

