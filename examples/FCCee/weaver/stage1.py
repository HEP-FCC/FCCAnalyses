processList = {
    # prefall2022 samples (generated centrally)
    "p8_ee_ZH_Znunu_Hbb_ecm240": {},  # 1030000 events
    "p8_ee_ZH_Znunu_Hcc_ecm240": {},  # 1060000
    "p8_ee_ZH_Znunu_Hss_ecm240": {},  # 1060000
    "p8_ee_ZH_Znunu_Hgg_ecm240": {"fraction": 0.5},  # 2000000
    "p8_ee_ZH_Znunu_Huu_ecm240": {
        "fraction": 0.5
    },  # we take only half sample for uu,dd because they will go into qq label which contains both
    "p8_ee_ZH_Znunu_Hdd_ecm240": {
        "fraction": 0.5
    },  # and we want for qq same number of jets as other classes; the two files 2080000 events in total, 1040000 each?
}


# prodTag     = "FCCee/spring2021/IDEA/" #for spring2022 samples
prodTag = "FCCee/pre_fall2022_training/IDEA/"  # for prefall2022 samples

# outputDir   = ""

# Optional: ncpus, default is 4
nCPUS = 8

definition = dict()
alias = dict()

# ===== VERTEX
# MC primary vertex
definition["MC_PrimaryVertexP4"] = "FCCAnalyses::MCParticle::get_EventPrimaryVertexP4()( Particle )"

# ===== CLUSTERING
# define the RP px, py, pz and e
definition["RP_px"] = "ReconstructedParticle::get_px(ReconstructedParticles)"
definition["RP_py"] = "ReconstructedParticle::get_py(ReconstructedParticles)"
definition["RP_pz"] = "ReconstructedParticle::get_pz(ReconstructedParticles)"
definition["RP_e"] = "ReconstructedParticle::get_e(ReconstructedParticles)"
definition["RP_m"] = "ReconstructedParticle::get_mass(ReconstructedParticles)"
definition["RP_q"] = "ReconstructedParticle::get_charge(ReconstructedParticles)"
# build pseudo jets with the RP, using the interface that takes px,py,pz,E
# definition[]"pseudo_jets"]=    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)"
definition["pseudo_jets"] = "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)"
# run jet clustering with all reconstructed particles. ee_genkt_algorithm, R=1.5, inclusive clustering, E-scheme
definition[
    "FCCAnalysesJets_ee_genkt"
] = "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)"

# get the jets out of the struct
definition["jets_ee_genkt"] = "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_genkt)"
# get the jets constituents out of the struct
definition[
    "jetconstituents_ee_genkt"
] = "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt)"

# ===== OBSERVABLES
# JET LEVEL
###definition["jet_px"]=        "JetClusteringUtils::get_px(jets_ee_genkt)"  #jets_ee_genkt_px
###definition["jet_py"]=        "JetClusteringUtils::get_py(jets_ee_genkt)"
###definition["jet_pz"]=        "JetClusteringUtils::get_pz(jets_ee_genkt)"
definition["jet_p"] = "JetClusteringUtils::get_p(jets_ee_genkt)"
definition["jet_e"] = "JetClusteringUtils::get_e(jets_ee_genkt)"
definition["jet_mass"] = "JetClusteringUtils::get_m(jets_ee_genkt)"
definition["jet_phi"] = "JetClusteringUtils::get_phi(jets_ee_genkt)"
definition["jet_theta"] = "JetClusteringUtils::get_theta(jets_ee_genkt)"
# CONSTITUENT LEVEL
definition[
    "JetsConstituents"
] = "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticles, jetconstituents_ee_genkt)"
# build jet constituents lists

alias["MCRecoAssociations0"] = "MCRecoAssociations#0.index"
alias["MCRecoAssociations1"] = "MCRecoAssociations#1.index"

definition[
    "pfcand_Pids"
] = "JetConstituentsUtils::get_PIDs_cluster(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, jetconstituents_ee_genkt)"

definition["pfcand_ismu"] = "JetConstituentsUtils::get_isMu(pfcand_Pids)"
definition["pfcand_isel"] = "JetConstituentsUtils::get_isEl(pfcand_Pids)"

definition[
    "pfcand_ischad"
] = "JetConstituentsUtils::get_isChargedHad(pfcand_Pids, JetsConstituents)"

definition["pfcand_isgamma"] = "JetConstituentsUtils::get_isGamma(JetsConstituents)"

definition["pfcand_isnhad"] = "JetConstituentsUtils::get_isNeutralHad(JetsConstituents)"

# kinematics, displacement, PID
definition["pfcand_e"] = "JetConstituentsUtils::get_e(JetsConstituents)"
definition["pfcand_p"] = "JetConstituentsUtils::get_p(JetsConstituents)"
definition["pfcand_theta"] = "JetConstituentsUtils::get_theta(JetsConstituents)"
definition["pfcand_phi"] = "JetConstituentsUtils::get_phi(JetsConstituents)"
definition["pfcand_charge"] = "JetConstituentsUtils::get_charge(JetsConstituents)"
definition[
    "pfcand_erel"
] = "JetConstituentsUtils::get_erel_cluster(jets_ee_genkt, JetsConstituents)"

definition[
    "pfcand_erellog"
] = "JetConstituentsUtils::get_erel_log_cluster(jets_ee_genkt, JetsConstituents)"

definition[
    "pfcand_thetarel"
] = "JetConstituentsUtils::get_thetarel_cluster(jets_ee_genkt, JetsConstituents)"

definition[
    "pfcand_phirel"
] = "JetConstituentsUtils::get_phirel_cluster(jets_ee_genkt, JetsConstituents)"

definition[
    "pfcand_dndx"
] = "JetConstituentsUtils::get_dndx(JetsConstituents, EFlowTrack_2, EFlowTrack, pfcand_ischad)"

definition[
    "pfcand_mtof"
] = "JetConstituentsUtils::get_mtof(JetsConstituents, EFlowTrack_L, EFlowTrack, TrackerHits, EFlowPhoton, EFlowNeutralHadron, CalorimeterHits, MC_PrimaryVertexP4, pfcand_Pids)"

definition["pfcand_d0_wrt0"] = "JetConstituentsUtils::get_d0(JetsConstituents, EFlowTrack_1)"

definition["pfcand_z0_wrt0"] = "JetConstituentsUtils::get_z0(JetsConstituents, EFlowTrack_1)"

definition["pfcand_phi0_wrt0"] = "JetConstituentsUtils::get_phi0(JetsConstituents, EFlowTrack_1)"

definition["pfcand_omega_wrt0"] = "JetConstituentsUtils::get_omega(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_tanlambda_wrt0"
] = "JetConstituentsUtils::get_tanLambda(JetsConstituents, EFlowTrack_1)"

definition["pfcand_Bz"] = "JetConstituentsUtils::get_Bz(JetsConstituents, EFlowTrack_1)"

definition["Bz"] = "ReconstructedParticle2Track::Bz(ReconstructedParticles, EFlowTrack_1)"
# definition["pfcand_Par"]= "ReconstructedParticle2Track::XPtoPar(ReconstructedParticles, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"
# definition["pfcand_dxy"]= "JetConstituentsUtils::XPtoPar_dxy(pfcand_Par)"
# definition["pfcand_dxy"]= "JetConstituentsUtils::XPtoPar_dxy(pfcand_Par)"
# definition["pfcand_dz"]= "JetConstituentsUtils::XPtoPar_dz(pfcand_Par)"
# definition["pfcand_phi0"]= "JetConstituentsUtils::XPtoPar_phi0(pfcand_Par)"
# definition["pfcand_C"]= "JetConstituentsUtils::XPtoPar_C(pfcand_Par)"
# definition["pfcand_ct"]= "JetConstituentsUtils::XPtoPar_ct(pfcand_Par)"
definition[
    "pfcand_dxy"
] = "JetConstituentsUtils::XPtoPar_dxy(JetsConstituents, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"

definition[
    "pfcand_dz"
] = "JetConstituentsUtils::XPtoPar_dz(JetsConstituents, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"

definition[
    "pfcand_phi0"
] = "JetConstituentsUtils::XPtoPar_phi(JetsConstituents, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"

definition["pfcand_C"] = "JetConstituentsUtils::XPtoPar_C(JetsConstituents, EFlowTrack_1, Bz)"

definition["pfcand_ct"] = "JetConstituentsUtils::XPtoPar_ct(JetsConstituents, EFlowTrack_1, Bz)"

definition["pfcand_dptdpt"] = "JetConstituentsUtils::get_omega_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxydxy"] = "JetConstituentsUtils::get_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dzdz"] = "JetConstituentsUtils::get_z0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dphidphi"] = "JetConstituentsUtils::get_phi0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_detadeta"
] = "JetConstituentsUtils::get_tanlambda_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxydz"] = "JetConstituentsUtils::get_d0_z0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_dphidxy"
] = "JetConstituentsUtils::get_phi0_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_phidz"] = "JetConstituentsUtils::get_phi0_z0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_phictgtheta"
] = "JetConstituentsUtils::get_tanlambda_phi0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_dxyctgtheta"
] = "JetConstituentsUtils::get_tanlambda_d0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_dlambdadz"
] = "JetConstituentsUtils::get_tanlambda_z0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_cctgtheta"
] = "JetConstituentsUtils::get_omega_tanlambda_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_phic"
] = "JetConstituentsUtils::get_omega_phi0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxyc"] = "JetConstituentsUtils::get_omega_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_cdz"] = "JetConstituentsUtils::get_omega_z0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_sip2dval"
] = "JetConstituentsUtils::get_Sip2dVal_clusterV(jets_ee_genkt, pfcand_dxy, pfcand_phi0, MC_PrimaryVertexP4, Bz)"

definition["pfcand_sip2dsig"] = "JetConstituentsUtils::get_Sip2dSig(pfcand_sip2dval, pfcand_dxydxy)"

definition[
    "pfcand_sip3dval"
] = "JetConstituentsUtils::get_Sip3dVal_clusterV(jets_ee_genkt, pfcand_dxy, pfcand_dz, pfcand_phi0, MC_PrimaryVertexP4, Bz)"

definition[
    "pfcand_sip3dsig"
] = "JetConstituentsUtils::get_Sip3dSig(pfcand_sip3dval, pfcand_dxydxy, pfcand_dzdz)"

definition[
    "pfcand_jetdistval"
] = "JetConstituentsUtils::get_JetDistVal_clusterV(jets_ee_genkt, JetsConstituents, pfcand_dxy, pfcand_dz, pfcand_phi0, MC_PrimaryVertexP4, Bz)"

definition[
    "pfcand_jetdistsig"
] = "JetConstituentsUtils::get_JetDistSig(pfcand_jetdistval, pfcand_dxydxy, pfcand_dzdz)"

# counting the types of particles per jet
definition["event_njet"] = "JetConstituentsUtils::count_jets(JetsConstituents)"
definition["jet_nconst"] = "JetConstituentsUtils::count_consts(JetsConstituents)"
definition["jet_nmu"] = "JetConstituentsUtils::count_type(pfcand_ismu)"
definition["jet_nel"] = "JetConstituentsUtils::count_type(pfcand_isel)"
definition["jet_nchad"] = "JetConstituentsUtils::count_type(pfcand_ischad)"
definition["jet_ngamma"] = "JetConstituentsUtils::count_type(pfcand_isgamma)"
definition["jet_nnhad"] = "JetConstituentsUtils::count_type(pfcand_isnhad)"

# compute the residues jet-constituents on significant kinematic variables as a check
definition["tlv_jets"] = "JetConstituentsUtils::compute_tlv_jets(jets_ee_genkt)"
definition["sum_tlv_jcs"] = "JetConstituentsUtils::sum_tlv_constituents(JetsConstituents)"
definition["jet_de"] = "JetConstituentsUtils::compute_residue_energy(tlv_jets, sum_tlv_jcs)"
definition["jet_dpt"] = "JetConstituentsUtils::compute_residue_pt(tlv_jets, sum_tlv_jcs)"
definition["jet_dphi"] = "JetConstituentsUtils::compute_residue_phi(tlv_jets, sum_tlv_jcs)"
definition["jet_dtheta"] = "JetConstituentsUtils::compute_residue_theta(tlv_jets, sum_tlv_jcs)"
# definition["Invariant_mass"]= "ROOT::VecOps::InvariantMasses(jets_ee_genkt[0].pt(), jets_ee_genkt[0].rap(), jets_ee_genkt[0].phi(), jets_ee_genkt[0].m(), jets_ee_genkt[1].pt(), jets_ee_genkt[1].rap(), jets_ee_genkt[1].phi(), jets_ee_genkt[1].m()));
definition["event_invariant_mass"] = "JetConstituentsUtils::InvariantMass(tlv_jets[0], tlv_jets[1])"


## here define output branches
branches_pfcand = [
    ### jet tagging training variables
    "pfcand_erellog",
    "pfcand_thetarel",
    "pfcand_phirel",
    "pfcand_dptdpt",
    "pfcand_detadeta",
    "pfcand_dphidphi",
    "pfcand_dxydxy",
    "pfcand_dzdz",
    "pfcand_dxydz",
    "pfcand_dphidxy",
    "pfcand_dlambdadz",
    "pfcand_dxyc",
    "pfcand_dxyctgtheta",
    "pfcand_phic",
    "pfcand_phidz",
    "pfcand_phictgtheta",
    "pfcand_cdz",
    "pfcand_cctgtheta",
    "pfcand_mtof",
    "pfcand_dndx",
    "pfcand_charge",
    "pfcand_ismu",
    "pfcand_isel",
    "pfcand_ischad",
    "pfcand_isgamma",
    "pfcand_isnhad",
    "pfcand_dxy",
    "pfcand_dz",
    "pfcand_sip2dval",
    "pfcand_sip2dsig",
    "pfcand_sip3dval",
    "pfcand_sip3dsig",
    "pfcand_jetdistval",
    "pfcand_jetdistsig",
    ### other pf cand observer variables
    "pfcand_e",
    "pfcand_p",
    "pfcand_theta",
    "pfcand_phi",
]

branches_jet = [
    ### jet based variables
    "jet_p",
    "jet_e",
    "jet_mass",
    "jet_phi",
    "jet_theta",
    "jet_nconst",
    "jet_nmu",
    "jet_nel",
    "jet_nchad",
    "jet_ngamma",
    "jet_nnhad",
    "jet_de",
    "jet_dpt",
    "jet_dphi",
    "jet_dtheta",
]

branches_event = [
    ## global variables
    "event_njet",
    "event_invariant_mass",
]
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
        branchList = branches_event + branches_jet + branches_pfcand
        return branchList
