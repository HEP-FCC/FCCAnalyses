
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
    df = df.Define("hadr_mask", "FCCAnalyses::MCParticle::get_pdg(MCParticles) == 92")
    df = df.Define("n_showers_92", "Sum(hadr_mask)")
    df = df.Define("hadr_idcs", "std::vector<int> res; for (int i = 0; i < hadr_mask.size(); i++) {if (hadr_mask[i]) {res.push_back(i);} }; return res;")
    df = df.Define("hadr_daughters", """
    ROOT::VecOps::RVec<edm4hep::MCParticleData> res;
    for (auto hadr_idx : hadr_idcs) {
        std::vector<int> idcs = FCCAnalyses::MCParticle::get_list_of_particles_from_decay(hadr_idx, MCParticles, _Particle_daughters.index);
        for (auto idx : idcs) {
            res.push_back(MCParticles[idx]);
        }
    } return res;
    """)
    df = df.Define("VisibleMCParticles", "hadr_daughters")
    df = df.Define("MC_px", "FCCAnalyses::MCParticle::get_px(VisibleMCParticles)")
    df = df.Define("MC_py", "FCCAnalyses::MCParticle::get_py(VisibleMCParticles)")
    df = df.Define("MC_pz","FCCAnalyses::MCParticle::get_pz(VisibleMCParticles)")
    df = df.Define("MC_m", "FCCAnalyses::MCParticle::get_mass(VisibleMCParticles)")
    df = df.Define("MC_e", "FCCAnalyses::MCParticle::get_e(VisibleMCParticles)")
    df = df.Define("MC_pdg", "FCCAnalyses::MCParticle::get_pdg(VisibleMCParticles)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets_xyzm_flav(MC_px, MC_py, MC_pz, MC_m, MC_pdg)")

    # Implemented algorithms and arguments: https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h
    # More info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 0)(pseudo_jets)") # 2-jet exclusive clustering
    df = df.Define("clustered_jets", "JetClustering::flv_clustering_ee_kt(2, 2, 0, 0)(pseudo_jets)") # 2-jet exclusive clustering

    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)") # one-to-one mapping to the input collection (rps_no_muons)
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_phi", "FCCAnalyses::JetClusteringUtils::get_phi(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    # df = df.Define("jets_flv", "FCCAnalyses::JetClusteringUtils::get_flavours(jets)")
    df = df.Define("jets_b_content", "FCCAnalyses::JetClusteringUtils::get_b_content(jets)")
    df = df.Define("jets_c_content", "FCCAnalyses::JetClusteringUtils::get_c_content(jets)")
    df = df.Define("jets_s_content", "FCCAnalyses::JetClusteringUtils::get_s_content(jets)")
    df = df.Define("jets_d_content", "FCCAnalyses::JetClusteringUtils::get_d_content(jets)")
    df = df.Define("jets_u_content", "FCCAnalyses::JetClusteringUtils::get_u_content(jets)")

    # convert jets to LorentzVectors
    df = df.Define("jets_lv", "Construct<ROOT::Math::PxPyPzEVector>(jets_px, jets_py, jets_pz, jets_e)")
    # df = df.Define("jets_truth", "FCCAnalyses::jetTruthFinder(jetconstituents, rps_no_muons, Particle, MCRecoAssociations1)") # returns best-matched PDG ID of the jets
    df = df.Define("dijet_higgs_m", "(jets_lv[0]+jets_lv[1]).M()")

    df = df.Define("MC_e_sum", "Sum(MC_e)")

    # define histograms
    # results.append(df.Histo1D(("zmumu_m", "", *bins_m_ll), "zmumu_m"))
    results.append(df.Histo1D(("jets_e", "", 250, 0., 250.), "jets_e"))
    results.append(df.Histo1D(("M_jj", "", 250, 0., 250.), "dijet_higgs_m"))
    results.append(df.Histo1D(("MC_e_sum", "", 250, 0., 250.), "MC_e_sum"))
    # results.append(df.Histo1D(("jets_flv", "", 50, 0., 50.), "jets_flv"))
    results.append(df.Histo1D(("jets_b_content", "", 10, -5., 5.), "jets_b_content"))
    results.append(df.Histo1D(("jets_c_content", "", 10, -5., 5.), "jets_c_content"))
    results.append(df.Histo1D(("jets_s_content", "", 10, -5., 5.), "jets_s_content"))
    results.append(df.Histo1D(("jets_d_content", "", 10, -5., 5.), "jets_d_content"))
    results.append(df.Histo1D(("jets_u_content", "", 10, -5., 5.), "jets_u_content"))
    results.append(df.Histo1D(("n_showers_92", "", 5, 0., 5.), "n_showers_92"))

    return results, weightsum

