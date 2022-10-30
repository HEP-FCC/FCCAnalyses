processList = {
    #prefall2022 samples (generated centrally)
    'p8_ee_ZH_Znunu_Hbb_ecm240':{}, #1030000 events
    'p8_ee_ZH_Znunu_Hcc_ecm240':{}, #1060000
    'p8_ee_ZH_Znunu_Hss_ecm240':{}, #1060000
    'p8_ee_ZH_Znunu_Hgg_ecm240':{'fraction':0.5}, #2000000
    'p8_ee_ZH_Znunu_Huu_ecm240':{'fraction':0.5}, #we take only half sample for uu,dd because they will go into qq label which contains both
    'p8_ee_ZH_Znunu_Hdd_ecm240':{'fraction':0.5}, #and we want for qq same number of jets as other classes; the two files 2080000 events in total, 1040000 each? 
}


#prodTag     = "FCCee/spring2021/IDEA/" #for spring2022 samples
prodTag     = "FCCee/pre_fall2022_training/IDEA/" #for prefall2022 samples

#outputDir   = ""

#Optional: ncpus, default is 4                       
nCPUS       = 8


class RDFanalysis():

    def analysers(df):
        
        df2 = (
            df

            #===== VERTEX
            
            #MC primary vertex
            .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

            #===== CLUSTERING
            #define the RP px, py, pz and e
            .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
            .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
            .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
            .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
            .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
            .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
            
            #build pseudo jets with the RP, using the interface that takes px,py,pz,E
            #.Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
            .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
            #run jet clustering with all reconstructed particles. ee_genkt_algorithm, R=1.5, inclusive clustering, E-scheme
            .Define("FCCAnalysesJets_ee_genkt", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
            #get the jets out of the struct
            .Define("jets_ee_genkt",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_genkt)")
            #get the jets constituents out of the struct
            .Define("jetconstituents_ee_genkt","JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt)")


            #===== OBSERVABLES
            #JET LEVEL
            ###.Define("Jets_px",        "JetClusteringUtils::get_px(jets_ee_genkt)")  #jets_ee_genkt_px
            ###.Define("Jets_py",        "JetClusteringUtils::get_py(jets_ee_genkt)")
            ###.Define("Jets_pz",        "JetClusteringUtils::get_pz(jets_ee_genkt)")
            
            .Define("Jets_pt",        "JetClusteringUtils::get_pt(jets_ee_genkt)")
            .Define("Jets_e",        "JetClusteringUtils::get_e(jets_ee_genkt)")
            .Define("Jets_mass",        "JetClusteringUtils::get_m(jets_ee_genkt)")
            .Define("Jets_phi",        "JetClusteringUtils::get_phi(jets_ee_genkt)")
            .Define("Jets_theta",        "JetClusteringUtils::get_theta(jets_ee_genkt)")

            #CONSTITUENT LEVEL
            .Define("JetsConstituents", "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticles, jetconstituents_ee_genkt)") #build jet constituents lists
        
            #getting the types of particles 
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            .Define("JetsConstituents_Pids", "JetConstituentsUtils::get_PIDs_cluster(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, jetconstituents_ee_genkt)")
            .Define("JetsConstituents_isMu", "JetConstituentsUtils::get_isMu(JetsConstituents_Pids)")
            .Define("JetsConstituents_isEl", "JetConstituentsUtils::get_isEl(JetsConstituents_Pids)")
            .Define("JetsConstituents_isChargedHad", "JetConstituentsUtils::get_isChargedHad(JetsConstituents_Pids, JetsConstituents)")
            .Define("JetsConstituents_isGamma", "JetConstituentsUtils::get_isGamma(JetsConstituents_Pids)")
            .Define("JetsConstituents_isNeutralHad", "JetConstituentsUtils::get_isNeutralHad(JetsConstituents_Pids, JetsConstituents)")

            #kinematics, displacement, PID
            .Define("JetsConstituents_e", "JetConstituentsUtils::get_e(JetsConstituents)")
            .Define("JetsConstituents_pt", "JetConstituentsUtils::get_pt(JetsConstituents)")
            .Define("JetsConstituents_theta", "JetConstituentsUtils::get_theta(JetsConstituents)")
            .Define("JetsConstituents_phi", "JetConstituentsUtils::get_phi(JetsConstituents)")
            .Define("JetsConstituents_charge", "JetConstituentsUtils::get_charge(JetsConstituents)")

            .Define("JetsConstituents_erel", "JetConstituentsUtils::get_erel_cluster(jets_ee_genkt, JetsConstituents)")
            .Define("JetsConstituents_erel_log", "JetConstituentsUtils::get_erel_log_cluster(jets_ee_genkt, JetsConstituents)")
            .Define("JetsConstituents_thetarel", "JetConstituentsUtils::get_thetarel_cluster(jets_ee_genkt, JetsConstituents)")
            .Define("JetsConstituents_phirel", "JetConstituentsUtils::get_phirel_cluster(jets_ee_genkt, JetsConstituents)") 
            
            .Define("JetsConstituents_dndx", "JetConstituentsUtils::get_dndx(JetsConstituents, EFlowTrack_2, EFlowTrack, JetsConstituents_isChargedHad)")
            .Define("JetsConstituents_mtof", "JetConstituentsUtils::get_mtof(JetsConstituents, EFlowTrack_L, EFlowTrack, TrackerHits, JetsConstituents_Pids)")
            
            .Define("JetsConstituents_d0_wrt0", "JetConstituentsUtils::get_d0(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_z0_wrt0", "JetConstituentsUtils::get_z0(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_phi0_wrt0", "JetConstituentsUtils::get_phi0(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_omega_wrt0", "JetConstituentsUtils::get_omega(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_tanlambda_wrt0", "JetConstituentsUtils::get_tanLambda(JetsConstituents, EFlowTrack_1)")

            .Define("JetsConstituents_Bz", "JetConstituentsUtils::get_Bz(JetsConstituents, EFlowTrack_1)")
            .Define("Bz", "ReconstructedParticle2Track::Bz(ReconstructedParticles, EFlowTrack_1)")
            
            #.Define("JetsConstituents_Par", "ReconstructedParticle2Track::XPtoPar(ReconstructedParticles, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            #.Define("JetsConstituents_dxy", "JetConstituentsUtils::XPtoPar_dxy(JetsConstituents_Par)")
            #.Define("JetsConstituents_dxy", "JetConstituentsUtils::XPtoPar_dxy(JetsConstituents_Par)")
            #.Define("JetsConstituents_dz", "JetConstituentsUtils::XPtoPar_dz(JetsConstituents_Par)")
            #.Define("JetsConstituents_phi0", "JetConstituentsUtils::XPtoPar_phi0(JetsConstituents_Par)")
            #.Define("JetsConstituents_C", "JetConstituentsUtils::XPtoPar_C(JetsConstituents_Par)")
            #.Define("JetsConstituents_ct", "JetConstituentsUtils::XPtoPar_ct(JetsConstituents_Par)")

            .Define("JetsConstituents_dxy", "JetConstituentsUtils::XPtoPar_dxy(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_dz", "JetConstituentsUtils::XPtoPar_dz(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_phi0", "JetConstituentsUtils::XPtoPar_phi(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_C", "JetConstituentsUtils::XPtoPar_C(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_ct", "JetConstituentsUtils::XPtoPar_ct(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")

            .Define("JetsConstituents_omega_cov", "JetConstituentsUtils::get_omega_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_d0_cov", "JetConstituentsUtils::get_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_z0_cov", "JetConstituentsUtils::get_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_phi0_cov", "JetConstituentsUtils::get_phi0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_tanlambda_cov", "JetConstituentsUtils::get_tanlambda_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_d0_z0_cov", "JetConstituentsUtils::get_d0_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_phi0_d0_cov", "JetConstituentsUtils::get_phi0_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_phi0_z0_cov", "JetConstituentsUtils::get_phi0_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_tanlambda_phi0_cov", "JetConstituentsUtils::get_tanlambda_phi0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_tanlambda_d0_cov", "JetConstituentsUtils::get_tanlambda_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_tanlambda_z0_cov", "JetConstituentsUtils::get_tanlambda_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_omega_tanlambda_cov", "JetConstituentsUtils::get_omega_tanlambda_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_omega_phi0_cov", "JetConstituentsUtils::get_omega_phi0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_omega_d0_cov", "JetConstituentsUtils::get_omega_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("JetsConstituents_omega_z0_cov", "JetConstituentsUtils::get_omega_z0_cov(JetsConstituents, EFlowTrack_1)")
            
            .Define("JetsConstituents_Sip2dVal", "JetConstituentsUtils::get_Sip2dVal_clusterV(jets_ee_genkt, JetsConstituents_dxy, JetsConstituents_phi0, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_Sip2dSig", "JetConstituentsUtils::get_Sip2dSig(JetsConstituents_Sip2dVal, JetsConstituents_d0_cov)")
            .Define("JetsConstituents_Sip3dVal", "JetConstituentsUtils::get_Sip3dVal_clusterV(jets_ee_genkt, JetsConstituents_dxy, JetsConstituents_dz, JetsConstituents_phi0, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_Sip3dSig", "JetConstituentsUtils::get_Sip3dSig(JetsConstituents_Sip3dVal, JetsConstituents_d0_cov, JetsConstituents_z0_cov)")
            .Define("JetsConstituents_JetDistVal", "JetConstituentsUtils::get_JetDistVal_clusterV(jets_ee_genkt, JetsConstituents, JetsConstituents_dxy, JetsConstituents_dz, JetsConstituents_phi0, MC_PrimaryVertex, Bz)")
            .Define("JetsConstituents_JetDistSig", "JetConstituentsUtils::get_JetDistSig(JetsConstituents_JetDistVal, JetsConstituents_d0_cov, JetsConstituents_z0_cov)")

            #counting the types of particles per jet
            .Define("njet", "JetConstituentsUtils::count_jets(JetsConstituents)")
            .Define("nconst", "JetConstituentsUtils::count_consts(JetsConstituents)")
            .Define("nmu", "JetConstituentsUtils::count_type(JetsConstituents_isMu)")
            .Define("nel", "JetConstituentsUtils::count_type(JetsConstituents_isEl)")
            .Define("nchargedhad", "JetConstituentsUtils::count_type(JetsConstituents_isChargedHad)")
            .Define("nphoton", "JetConstituentsUtils::count_type(JetsConstituents_isGamma)")
            .Define("nneutralhad", "JetConstituentsUtils::count_type(JetsConstituents_isNeutralHad)")
        
            #compute the residues jet-constituents on significant kinematic variables as a check
            .Define("tlv_jets", "JetConstituentsUtils::compute_tlv_jets(jets_ee_genkt)")
            .Define("sum_tlv_jcs", "JetConstituentsUtils::sum_tlv_constituents(JetsConstituents)")
            .Define("de", "JetConstituentsUtils::compute_residue_energy(tlv_jets, sum_tlv_jcs)")
            .Define("dpt", "JetConstituentsUtils::compute_residue_pt(tlv_jets, sum_tlv_jcs)")
            .Define("dphi", "JetConstituentsUtils::compute_residue_phi(tlv_jets, sum_tlv_jcs)")
            .Define("dtheta", "JetConstituentsUtils::compute_residue_theta(tlv_jets, sum_tlv_jcs)")
            
            #.Define("Invariant_mass", "ROOT::VecOps::InvariantMasses(jets_ee_genkt[0].pt(), jets_ee_genkt[0].rap(), jets_ee_genkt[0].phi(), jets_ee_genkt[0].m(), jets_ee_genkt[1].pt(), jets_ee_genkt[1].rap(), jets_ee_genkt[1].phi(), jets_ee_genkt[1].m())); 
            .Define("invariant_mass", "JetConstituentsUtils::InvariantMass(tlv_jets[0], tlv_jets[1])")
        )
        return df2

    def output():
        branchList = [
            #'RP_px', 'RP_py','RP_pz','RP_e', 'RP_m', 'RP_q',
            #'Jets_px', 'Jets_py', 'Jets_pz',
            'Jets_e', 'Jets_mass', 'Jets_pt', 'Jets_phi', 'Jets_theta',
            'JetsConstituents_e', 'JetsConstituents_pt', 'JetsConstituents_theta', 'JetsConstituents_phi', 'JetsConstituents_charge',
            'JetsConstituents_erel', 'JetsConstituents_erel_log', 'JetsConstituents_thetarel', 'JetsConstituents_phirel', 
            'JetsConstituents_dndx', 'JetsConstituents_mtof',
            
            'JetsConstituents_d0_wrt0', 'JetsConstituents_z0_wrt0', 'JetsConstituents_phi0_wrt0', 'JetsConstituents_omega_wrt0', 'JetsConstituents_tanlambda_wrt0',
            'Bz', 'JetsConstituents_Bz',
            #'JetsConstituents_Par',
            'JetsConstituents_dxy', 'JetsConstituents_dz', 'JetsConstituents_phi0', 'JetsConstituents_C', 'JetsConstituents_ct',

            'JetsConstituents_omega_cov', 'JetsConstituents_d0_cov', 'JetsConstituents_z0_cov', 'JetsConstituents_phi0_cov', 'JetsConstituents_tanlambda_cov',
            'JetsConstituents_d0_z0_cov', 'JetsConstituents_phi0_d0_cov', 'JetsConstituents_phi0_z0_cov', 
            'JetsConstituents_tanlambda_phi0_cov', 'JetsConstituents_tanlambda_d0_cov', 'JetsConstituents_tanlambda_z0_cov', 
            'JetsConstituents_omega_tanlambda_cov', 'JetsConstituents_omega_phi0_cov', 'JetsConstituents_omega_d0_cov', 'JetsConstituents_omega_z0_cov', 
            'JetsConstituents_Sip2dVal', 'JetsConstituents_Sip2dSig', 
            'JetsConstituents_Sip3dVal', 'JetsConstituents_Sip3dSig', 
            'JetsConstituents_JetDistVal', 'JetsConstituents_JetDistSig',
            #'JC_Jet0_Pids',
            'JetsConstituents_isMu', 
            'JetsConstituents_isEl', 
            'JetsConstituents_isChargedHad',
            'JetsConstituents_isGamma', 
            'JetsConstituents_isNeutralHad',
            'njet', 'nconst', 
            'nmu', 'nel', 'nchargedhad', 'nphoton', 'nneutralhad',
            'de', 'dpt', 'dphi', 'dtheta',
            'invariant_mass'
        ]
        return branchList    
