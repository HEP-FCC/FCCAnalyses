"""
this configuration file contains the:
- list of flavors to be considered
- reconstruction sequence stored as two dicts: definition and alias
- the list of variables used in the tagger as well as their range for validation plotting
"""

#### list of flavors f = g, q, c, s, ...(will look for input file name ccontaining "[Hff]")
flavors = ["g", "q", "s", "c", "b"]
### definition of the reco sequences
### and aliases

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

definition["FCCAnalysesJets_ee_genkt"] = "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)"
# ] = "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)"

# get the jets out of the struct
definition["jets_ee_genkt"] = "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_genkt)"
# get the jets constituents out of the struct
definition["jetconstituents_ee_genkt"] = "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt)"

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

definition["pfcand_isMu"] = "JetConstituentsUtils::get_isMu(JetsConstituents)"
definition["pfcand_isEl"] = "JetConstituentsUtils::get_isEl(JetsConstituents)"

definition["pfcand_isChargedHad"] = "JetConstituentsUtils::get_isChargedHad(JetsConstituents)"

definition["pfcand_isGamma"] = "JetConstituentsUtils::get_isGamma(JetsConstituents)"

definition["pfcand_isNeutralHad"] = "JetConstituentsUtils::get_isNeutralHad(JetsConstituents)"

# kinematics, displacement, PID
definition["pfcand_e"] = "JetConstituentsUtils::get_e(JetsConstituents)"
definition["pfcand_p"] = "JetConstituentsUtils::get_p(JetsConstituents)"
definition["pfcand_theta"] = "JetConstituentsUtils::get_theta(JetsConstituents)"
definition["pfcand_phi"] = "JetConstituentsUtils::get_phi(JetsConstituents)"
definition["pfcand_charge"] = "JetConstituentsUtils::get_charge(JetsConstituents)"
definition["pfcand_erel"] = "JetConstituentsUtils::get_erel_cluster(jets_ee_genkt, JetsConstituents)"

definition["pfcand_erel_log"] = "JetConstituentsUtils::get_erel_log_cluster(jets_ee_genkt, JetsConstituents)"

definition["pfcand_thetarel"] = "JetConstituentsUtils::get_thetarel_cluster(jets_ee_genkt, JetsConstituents)"

definition["pfcand_phirel"] = "JetConstituentsUtils::get_phirel_cluster(jets_ee_genkt, JetsConstituents)"

definition[
    "pfcand_dndx"
] = "JetConstituentsUtils::get_dndx(JetsConstituents, EFlowTrack_2, EFlowTrack, pfcand_isChargedHad)"

definition[
    "pfcand_mtof"
] = "JetConstituentsUtils::get_mtof(JetsConstituents, EFlowTrack_L, EFlowTrack, TrackerHits, EFlowPhoton, EFlowNeutralHadron, CalorimeterHits, MC_PrimaryVertexP4)"

definition["pfcand_d0_wrt0"] = "JetConstituentsUtils::get_d0(JetsConstituents, EFlowTrack_1)"

definition["pfcand_z0_wrt0"] = "JetConstituentsUtils::get_z0(JetsConstituents, EFlowTrack_1)"

definition["pfcand_phi0_wrt0"] = "JetConstituentsUtils::get_phi0(JetsConstituents, EFlowTrack_1)"

definition["pfcand_omega_wrt0"] = "JetConstituentsUtils::get_omega(JetsConstituents, EFlowTrack_1)"

definition["pfcand_tanlambda_wrt0"] = "JetConstituentsUtils::get_tanLambda(JetsConstituents, EFlowTrack_1)"

definition["Bz"] = "magFieldBz[0]"

definition["pfcand_dxy"] = "JetConstituentsUtils::XPtoPar_dxy(JetsConstituents, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"

definition["pfcand_dz"] = "JetConstituentsUtils::XPtoPar_dz(JetsConstituents, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"

definition["pfcand_phi0"] = "JetConstituentsUtils::XPtoPar_phi(JetsConstituents, EFlowTrack_1, MC_PrimaryVertexP4, Bz)"

definition["pfcand_C"] = "JetConstituentsUtils::XPtoPar_C(JetsConstituents, EFlowTrack_1, Bz)"

definition["pfcand_ct"] = "JetConstituentsUtils::XPtoPar_ct(JetsConstituents, EFlowTrack_1, Bz)"

definition["pfcand_dptdpt"] = "JetConstituentsUtils::get_omega_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxydxy"] = "JetConstituentsUtils::get_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dzdz"] = "JetConstituentsUtils::get_z0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dphidphi"] = "JetConstituentsUtils::get_phi0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_detadeta"] = "JetConstituentsUtils::get_tanlambda_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxydz"] = "JetConstituentsUtils::get_d0_z0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dphidxy"] = "JetConstituentsUtils::get_phi0_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_phidz"] = "JetConstituentsUtils::get_phi0_z0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_phictgtheta"] = "JetConstituentsUtils::get_tanlambda_phi0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxyctgtheta"] = "JetConstituentsUtils::get_tanlambda_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dlambdadz"] = "JetConstituentsUtils::get_tanlambda_z0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_cctgtheta"] = "JetConstituentsUtils::get_omega_tanlambda_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_phic"] = "JetConstituentsUtils::get_omega_phi0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_dxyc"] = "JetConstituentsUtils::get_omega_d0_cov(JetsConstituents, EFlowTrack_1)"

definition["pfcand_cdz"] = "JetConstituentsUtils::get_omega_z0_cov(JetsConstituents, EFlowTrack_1)"

definition[
    "pfcand_btagSip2dVal"
] = "JetConstituentsUtils::get_Sip2dVal_clusterV(jets_ee_genkt, pfcand_dxy, pfcand_phi0, Bz)"

definition["pfcand_btagSip2dSig"] = "JetConstituentsUtils::get_Sip2dSig(pfcand_btagSip2dVal, pfcand_dxydxy)"

definition[
    "pfcand_btagSip3dVal"
] = "JetConstituentsUtils::get_Sip3dVal_clusterV(jets_ee_genkt, pfcand_dxy, pfcand_dz, pfcand_phi0, Bz)"

definition[
    "pfcand_btagSip3dSig"
] = "JetConstituentsUtils::get_Sip3dSig(pfcand_btagSip3dVal, pfcand_dxydxy, pfcand_dzdz)"

definition[
    "pfcand_btagJetDistVal"
] = "JetConstituentsUtils::get_JetDistVal_clusterV(jets_ee_genkt, JetsConstituents, pfcand_dxy, pfcand_dz, pfcand_phi0, Bz)"

definition[
    "pfcand_btagJetDistSig"
] = "JetConstituentsUtils::get_JetDistSig(pfcand_btagJetDistVal, pfcand_dxydxy, pfcand_dzdz)"

# counting the types of particles per jet
definition["event_njet"] = "JetConstituentsUtils::count_jets(JetsConstituents)"
definition["jet_nconst"] = "JetConstituentsUtils::count_consts(JetsConstituents)"
definition["jet_nmu"] = "JetConstituentsUtils::count_type(pfcand_isMu)"
definition["jet_nel"] = "JetConstituentsUtils::count_type(pfcand_isEl)"
definition["jet_nchad"] = "JetConstituentsUtils::count_type(pfcand_isChargedHad)"
definition["jet_ngamma"] = "JetConstituentsUtils::count_type(pfcand_isGamma)"
definition["jet_nnhad"] = "JetConstituentsUtils::count_type(pfcand_isNeutralHad)"

# compute the residues jet-constituents on significant kinematic variables as a check
definition["tlv_jets"] = "JetConstituentsUtils::compute_tlv_jets(jets_ee_genkt)"
definition["sum_tlv_jcs"] = "JetConstituentsUtils::sum_tlv_constituents(JetsConstituents)"
definition["jet_de"] = "JetConstituentsUtils::compute_residue_energy(tlv_jets, sum_tlv_jcs)"
definition["jet_dpt"] = "JetConstituentsUtils::compute_residue_pt(tlv_jets, sum_tlv_jcs)"
definition["jet_dphi"] = "JetConstituentsUtils::compute_residue_phi(tlv_jets, sum_tlv_jcs)"
definition["jet_dtheta"] = "JetConstituentsUtils::compute_residue_theta(tlv_jets, sum_tlv_jcs)"
# definition["Invariant_mass"]= "ROOT::VecOps::InvariantMasses(jets_ee_genkt[0].pt(), jets_ee_genkt[0].rap(), jets_ee_genkt[0].phi(), jets_ee_genkt[0].m(), jets_ee_genkt[1].pt(), jets_ee_genkt[1].rap(), jets_ee_genkt[1].phi(), jets_ee_genkt[1].m()));
definition["event_invariant_mass"] = "JetConstituentsUtils::InvariantMass(tlv_jets[0], tlv_jets[1])"


## define here the branches to be stored as dict
## onyl the name of the var is used here, the metadata is used in stage_plots
variables_pfcand = {
    "pfcand_erel_log": {
        "name": "pfcand_erel_log",
        "title": "log(E_{i}/E_{jet})",
        "bin": 100,
        "xmin": -3,
        "xmax": 0,
        "scale": "log",
    },
    "pfcand_thetarel": {
        "name": "pfcand_thetarel",
        "title": "#theta_{rel}",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 3.0,
        "scale": "lin",
    },
    "pfcand_phirel": {
        "name": "pfcand_phirel",
        "title": "#phi_{rel}",
        "bin": 100,
        "xmin": -3.14,
        "xmax": 3.14,
        "scale": "lin",
    },
    "pfcand_dptdpt": {
        "name": "pfcand_dptdpt",
        "title": "#sigma(#omega)^{2}",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 2e-09,
        "scale": "log",
    },
    "pfcand_detadeta": {
        "name": "pfcand_detadeta",
        "title": "#sigma(tan(#lambda))^{2}",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 0.02,
        "scale": "log",
    },
    "pfcand_dphidphi": {
        "name": "pfcand_dphidphi",
        "title": "#sigma(#phi))^{2}",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 0.0015,
        "scale": "log",
    },
    "pfcand_dxydxy": {
        "name": "pfcand_dxydxy",
        "title": "#sigma(d_{xy}))^{2}",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 0.20,
        "scale": "log",
    },
    "pfcand_dzdz": {
        "name": "pfcand_dzdz",
        "title": "#sigma(d_{z}))^{2}",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 0.50,
        "scale": "log",
    },
    "pfcand_dxydz": {
        "name": "pfcand_dxydz",
        "title": "C(d_{xy},d_{z})",
        "bin": 100,
        "xmin": -10,
        "xmax": 10,
        "scale": "log",
    },
    "pfcand_dphidxy": {
        "name": "pfcand_dphidxy",
        "title": "C(#phi,d_{z})",
        "bin": 100,
        "xmin": -0.1,
        "xmax": 0,
        "scale": "log",
    },
    "pfcand_dlambdadz": {
        "name": "pfcand_dlambdadz",
        "title": "C(tan(#lambda),d_{z})",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.1,
        "scale": "log",
    },
    "pfcand_dxyc": {
        "name": "pfcand_dxyc",
        "title": "C(#omega,d_{xy})",
        "bin": 100,
        "xmin": -0.2,
        "xmax": 0.1,
        "scale": "log",
    },
    "pfcand_dxyctgtheta": {
        "name": "pfcand_dxyctgtheta",
        "title": "C(tan(#lambda),d_{xy})",
        "bin": 100,
        "xmin": -0.025,
        "xmax": 0.025,
        "scale": "log",
    },
    "pfcand_phic": {
        "name": "pfcand_phic",
        "title": "C(#omega,#phi)",
        "bin": 100,
        "xmin": -1e-06,
        "xmax": 1e-06,
        "scale": "log",
    },
    "pfcand_phidz": {
        "name": "pfcand_phidz",
        "title": "C(#phi,d_{z})",
        "bin": 100,
        "xmin": -0.05,
        "xmax": 0.05,
        "scale": "log",
    },
    "pfcand_phictgtheta": {
        "name": "pfcand_phictgtheta",
        "title": "C(tan(#lambda),#phi)",
        "bin": 100,
        "xmin": -0.1e-03,
        "xmax": 0.5e03,
        "scale": "log",
    },
    "pfcand_cdz": {
        "name": "pfcand_cdz",
        "title": "C(#omega,d_{z})",
        "bin": 100,
        "xmin": -0.5e-03,
        "xmax": 0.1e-03,
        "scale": "log",
    },
    "pfcand_cctgtheta": {
        "name": "pfcand_cctgtheta",
        "title": "C(#omega, tan(#lambda))",
        "bin": 100,
        "xmin": -1e-06,
        "xmax": 20e-06,
        "scale": "log",
    },
    "pfcand_mtof": {
        "name": "pfcand_mtof",
        "title": "m_{ToF} [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_dndx": {
        "name": "pfcand_dndx",
        "title": "dN/dx [mm^{-1}]",
        "bin": 100,
        "xmin": 0,
        "xmax": 5,
        "scale": "lin",
    },
    "pfcand_charge": {
        "name": "pfcand_charge",
        "title": "Q",
        "bin": 2,
        "xmin": -0.5,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_isMu": {
        "name": "pfcand_isMu",
        "title": "is muon",
        "bin": 2,
        "xmin": -0.5,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_isEl": {
        "name": "pfcand_isEl",
        "title": "is electron",
        "bin": 2,
        "xmin": -0.5,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_isChargedHad": {
        "name": "pfcand_isChargedHad",
        "title": "is charged hadron",
        "bin": 2,
        "xmin": -0.5,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_isGamma": {
        "name": "pfcand_isGamma",
        "title": "is photon",
        "bin": 2,
        "xmin": -0.5,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_isNeutralHad": {
        "name": "pfcand_isNeutralHad",
        "title": "is neutral hadron",
        "bin": 2,
        "xmin": -0.5,
        "xmax": 1.5,
        "scale": "lin",
    },
    "pfcand_dxy": {
        "name": "pfcand_dxy",
        "title": "d_{xy} [mm]",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.5,
        "scale": "log",
    },
    "pfcand_dz": {
        "name": "pfcand_dz",
        "title": "d_{z} [mm]",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.5,
        "scale": "log",
    },
    "pfcand_btagSip2dVal": {
        "name": "pfcand_btagSip2dVal",
        "title": "2D signed IP [mm]",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 5,
        "scale": "log",
    },
    "pfcand_btagSip2dSig": {
        "name": "pfcand_btagSip2dSig",
        "title": "2D signed IP significance",
        "bin": 100,
        "xmin": -10,
        "xmax": 10,
        "scale": "log",
    },
    "pfcand_btagSip3dVal": {
        "name": "pfcand_btagSip3dVal",
        "title": "3D signed IP [mm]",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 5,
        "scale": "log",
    },
    "pfcand_btagSip3dSig": {
        "name": "pfcand_btagSip3dSig",
        "title": "3D signed IP significance",
        "bin": 100,
        "xmin": -8,
        "xmax": 10,
        "scale": "log",
    },
    "pfcand_btagJetDistVal": {
        "name": "pfcand_btagJetDistVal",
        "title": "distance to jet [mm]",
        "bin": 100,
        "xmin": 0,
        "xmax": 5,
        "scale": "log",
    },
    "pfcand_btagJetDistSig": {
        "name": "pfcand_btagJetDistSig",
        "title": "distance to jet (significance)",
        "bin": 100,
        "xmin": 0,
        "xmax": 10,
        "scale": "log",
    },
    ### other pf cand observer variables
    "pfcand_e": {
        "name": "pfcand_e",
        "title": "E [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 100,
        "scale": "log",
    },
    "pfcand_p": {
        "name": "pfcand_p",
        "title": "p [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 100,
        "scale": "log",
    },
    "pfcand_theta": {
        "name": "pfcand_theta",
        "title": "#theta",
        "bin": 100,
        "xmin": 0,
        "xmax": 3.14,
        "scale": "lin",
    },
    "pfcand_phi": {
        "name": "pfcand_phi",
        "title": "#phi",
        "bin": 100,
        "xmin": -3.14,
        "xmax": 3.14,
        "scale": "lin",
    },
}

variables_jet = {
    ### jet based variables
    "jet_p": {
        "name": "jet_p",
        "title": "p_{jet} [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 100.0,
        "scale": "lin",
    },
    "jet_e": {
        "name": "jet_e",
        "title": "E_{jet} [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 100.0,
        "scale": "lin",
    },
    "jet_mass": {
        "name": "jet_mass",
        "title": "m_{jet} [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 25,
        "scale": "lin",
    },
    "jet_phi": {
        "name": "jet_phi",
        "title": "#phi_{jet}",
        "bin": 100,
        "xmin": -3.14,
        "xmax": 3.14,
        "scale": "lin",
    },
    "jet_theta": {
        "name": "jet_theta",
        "title": "#theta_{jet}",
        "bin": 100,
        "xmin": 0,
        "xmax": 3.14,
        "scale": "lin",
    },
    "jet_nconst": {
        "name": "jet_nconst",
        "title": "N_{const}^{jet}",
        "bin": 100,
        "xmin": 0,
        "xmax": 100,
        "scale": "log",
    },
    "jet_nmu": {
        "name": "jet_nmu",
        "title": "N_{#mu}^{jet}",
        "bin": 5,
        "xmin": 0,
        "xmax": 5,
        "scale": "log",
    },
    "jet_nel": {
        "name": "N_{el}^{jet}",
        "title": "",
        "bin": 5,
        "xmin": 0,
        "xmax": 5,
        "scale": "log",
    },
    "jet_nchad": {
        "name": "jet_nchad",
        "title": "N_{ch.had}^{jet}",
        "bin": 50,
        "xmin": 0,
        "xmax": 50,
        "scale": "log",
    },
    "jet_ngamma": {
        "name": "jet_ngamma",
        "title": "N_{#gamma}^{jet}",
        "bin": 50,
        "xmin": 0,
        "xmax": 50,
        "scale": "log",
    },
    "jet_nnhad": {
        "name": "jet_nnhad",
        "title": "N_{neutr. had}^{jet}",
        "bin": 20,
        "xmin": 0,
        "xmax": 20,
        "scale": "log",
    },
    "jet_de": {
        "name": "jet_de",
        "title": "#Delta E [GeV]",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.5,
        "scale": "log",
    },
    "jet_dpt": {
        "name": "jet_dpt",
        "title": "#Delta p [GeV]",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.5,
        "scale": "log",
    },
    "jet_dphi": {
        "name": "jet_dphi",
        "title": "#Delta #phi",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.5,
        "scale": "log",
    },
    "jet_dtheta": {
        "name": "jet_dtheta",
        "title": "#Delta #theta",
        "bin": 100,
        "xmin": -0.5,
        "xmax": 0.5,
        "scale": "log",
    },
}

variables_event = {
    "event_invariant_mass": {
        "name": "event_invariant_mass",
        "title": "m_{jj} [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 200,
        "scale": "lin",
    },
}
