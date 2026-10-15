
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
nCPUS       = 6
# nCPUS       = 1

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
    df = df.Define("HadronisationPartons", "FCCAnalyses::MCParticle::get_hadronisation_partons(MCParticles, _Particle_parents.index)")
    df = df.Define("n_hadronisation_partons", "HadronisationPartons.size()")
    results.append(df.Histo1D(("n_hadronisation_partons", "", 50, 0., 50.), "n_hadronisation_partons"))

    # primary hadrons, i.e. the hadrons directly after hadronisation, before they decay
    df = df.Define("PrimaryHadrons", "FCCAnalyses::MCParticle::get_primary_hadrons(MCParticles, _Particle_parents.index)")
    # flavoured pseudojets from the primary hadrons and, for comparison, from the hadronisation partons
    inputs = {
        "hadron_": "PrimaryHadrons",
        "parton_": "HadronisationPartons",
    }
    for prefix, particles in inputs.items():
        df = df.Define(f"{prefix}MC_px", f"FCCAnalyses::MCParticle::get_px({particles})")
        df = df.Define(f"{prefix}MC_py", f"FCCAnalyses::MCParticle::get_py({particles})")
        df = df.Define(f"{prefix}MC_pz", f"FCCAnalyses::MCParticle::get_pz({particles})")
        df = df.Define(f"{prefix}MC_m", f"FCCAnalyses::MCParticle::get_mass({particles})")
        df = df.Define(f"{prefix}MC_e", f"FCCAnalyses::MCParticle::get_e({particles})")
        df = df.Define(f"{prefix}MC_pdg", f"FCCAnalyses::MCParticle::get_pdg({particles})")
        df = df.Define(f"{prefix}pseudo_jets", f"FCCAnalyses::JetClusteringUtils::set_pseudoJets_xyzm_flav({prefix}MC_px, {prefix}MC_py, {prefix}MC_pz, {prefix}MC_m, {prefix}MC_pdg)")

        # 2-jet exclusive flavour-aware clustering, with IFN and with plain net flavour summation for comparison
        clusterings = {
            "ifn": f"JetClustering::flv_ifn_clustering_ee_kt(2, 2, 0, 0)({prefix}pseudo_jets)",
            "net": f"JetClustering::flv_net_clustering_ee_kt(2, 2, 0, 0)({prefix}pseudo_jets)",
        }

        df = df.Define(f"{prefix}MC_e_sum", f"Sum({prefix}MC_e)")
        results.append(df.Histo1D((f"{prefix}MC_e_sum", "", 250, 0., 250.), f"{prefix}MC_e_sum"))

        for algo, clustering in clusterings.items():
            name = f"{prefix}{algo}"
            df = df.Define(f"{name}_clustered_jets", clustering)

            df = df.Define(f"{name}_jets", f"FCCAnalyses::JetClusteringUtils::get_pseudoJets({name}_clustered_jets)")
            # df = df.Define(f"{name}_jetconstituents", f"FCCAnalyses::JetClusteringUtils::get_constituents({name}_clustered_jets)")
            for var in ["e", "px", "py", "pz", "phi", "m"]:
                df = df.Define(f"{name}_jets_{var}", f"FCCAnalyses::JetClusteringUtils::get_{var}({name}_jets)")

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

