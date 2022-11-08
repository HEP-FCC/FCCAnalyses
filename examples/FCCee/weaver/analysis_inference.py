#Mandatory: List of processes
processList = {
    #prefall2022 samples (generated centrally)
    'p8_ee_ZH_Znunu_Hbb_ecm240':{}, #1030000 events
    'p8_ee_ZH_Znunu_Hcc_ecm240':{}, #1060000
    'p8_ee_ZH_Znunu_Hss_ecm240':{}, #1060000 
    'p8_ee_ZH_Znunu_Hgg_ecm240':{'fraction':0.5}, #2000000 
    'p8_ee_ZH_Znunu_Huu_ecm240':{'fraction':0.5}, #we take only half sample for uu,dd because they will go into qq label which contains both
    'p8_ee_ZH_Znunu_Hdd_ecm240':{'fraction':0.5}, #and we want for qq same number of jets as other classes; the two files 2080000 events in total, 1040000 each? 
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/spring2021/IDEA/"
prodTag     = "FCCee/pre_fall2022_training/IDEA/" #for prefall2022 samples 

#Optional: output directory, default is local running directory
#outputDir   = "/eos/home-a/adelvecc/FCCevaluate/"

#Optional
nCPUS       = 8
runBatch    = False
#batchQueue = "longlunch"
#compGroup = "group_u_FCC.local_gen"


#USER DEFINED CODE

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):

        from ROOT import JetFlavourUtils 
        weaver = JetFlavourUtils.setup_weaver(
            "/eos/experiment/fcc/ee/jet_flavour_tagging/pre_fall2022_training/IDEA/selvaggi_2022Oct30/fccee_flavtagging_edm4hep_v2.onnx", #name of the trained model exported 
            "/eos/experiment/fcc/ee/jet_flavour_tagging/pre_fall2022_training/IDEA/selvaggi_2022Oct30/preprocess_fccee_flavtagging_edm4hep_v2.json", #.json file produced by weaver during training
            (
                "pfcand_erel_log", #list of the training variables,
                "pfcand_thetarel", #will be used for predictions as well
                "pfcand_phirel",
                "pfcand_dxy",
                "pfcand_dz",
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
                "pfcand_isMu",
                "pfcand_isEl",
                "pfcand_isChargedHad",
                "pfcand_isGamma",
                "pfcand_isNeutralHad",
                "pfcand_btagSip2dVal",
                "pfcand_btagSip2dSig",
                "pfcand_btagSip3dVal",
                "pfcand_btagSip3dSig",
                "pfcand_btagJetDistVal",
                "pfcand_btagJetDistSig",
            ),
        )

        df2 = (
            df
            ### COMPUTE THE VARIABLES FOR INFERENCE OF THE TRAINING MODEL
            ### This section should be equal to the one used for training

            ### MC primary vertex
            .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

            # CLUSTERING 
            #define the RP px, py, pz and e
            .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
            .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
            .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
            .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
            .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
            .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
            
            #build pseudo jets with the RP
            .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
            #run jet clustering with all reconstructed particles. ee_genkt_algorithm, R=1.5, inclusive clustering, E-scheme
            .Define("FCCAnalysesJets_ee_genkt", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
            #get the jets out of the struct
            .Define("jets_ee_genkt",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_genkt)")
            #get the jets constituents out of the struct 
            .Define("jetconstituents_ee_genkt","JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt)")
            
            #===== COMPUTE TRAINING FEATURES
            
            .Define("JetsConstituents", "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticles, jetconstituents_ee_genkt)") #build jet constituents lists

            ### Types of particles 
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            .Define("JetsConstituents_Pids", "JetConstituentsUtils::get_PIDs_cluster(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, jetconstituents_ee_genkt)")
            
            .Define("pfcand_isMu", "JetConstituentsUtils::get_isMu(JetsConstituents_Pids)")
            .Define("pfcand_isEl", "JetConstituentsUtils::get_isEl(JetsConstituents_Pids)")
            .Define("pfcand_isChargedHad", "JetConstituentsUtils::get_isChargedHad(JetsConstituents_Pids, JetsConstituents)")
            .Define("pfcand_isGamma", "JetConstituentsUtils::get_isGamma(JetsConstituents_Pids)")
            .Define("pfcand_isNeutralHad", "JetConstituentsUtils::get_isNeutralHad(JetsConstituents_Pids, JetsConstituents)")
            
            ### Kinematics, displacement, PID

            .Define("pfcand_erel", "JetConstituentsUtils::get_erel_cluster(jets_ee_genkt, JetsConstituents)")
            .Define("pfcand_erel_log", "JetConstituentsUtils::get_erel_log_cluster(jets_ee_genkt, JetsConstituents)")
            .Define("pfcand_thetarel", "JetConstituentsUtils::get_thetarel_cluster(jets_ee_genkt, JetsConstituents)")
            .Define("pfcand_phirel", "JetConstituentsUtils::get_phirel_cluster(jets_ee_genkt, JetsConstituents)")

            .Define("pfcand_charge", "JetConstituentsUtils::get_charge(JetsConstituents)")
            .Define("pfcand_dndx", "JetConstituentsUtils::get_dndx(JetsConstituents, EFlowTrack_2, EFlowTrack, pfcand_isChargedHad)")
            .Define("pfcand_mtof", "JetConstituentsUtils::get_mtof(JetsConstituents, EFlowTrack_L, EFlowTrack, TrackerHits, JetsConstituents_Pids)")

            .Define("Bz", "ReconstructedParticle2Track::Bz(ReconstructedParticles, EFlowTrack_1)")

            .Define("pfcand_dxy", "JetConstituentsUtils::XPtoPar_dxy(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("pfcand_dz", "JetConstituentsUtils::XPtoPar_dz(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("pfcand_phi0", "JetConstituentsUtils::XPtoPar_phi(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("pfcand_C", "JetConstituentsUtils::XPtoPar_C(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")
            .Define("pfcand_ct", "JetConstituentsUtils::XPtoPar_ct(JetsConstituents, EFlowTrack_1, MC_PrimaryVertex, Bz)")

            .Define("pfcand_dptdpt", "JetConstituentsUtils::get_omega_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dxydxy", "JetConstituentsUtils::get_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dzdz", "JetConstituentsUtils::get_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dphidphi", "JetConstituentsUtils::get_phi0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_detadeta", "JetConstituentsUtils::get_tanlambda_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dxydz", "JetConstituentsUtils::get_d0_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dphidxy", "JetConstituentsUtils::get_phi0_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_phidz", "JetConstituentsUtils::get_phi0_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_phictgtheta", "JetConstituentsUtils::get_tanlambda_phi0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dxyctgtheta", "JetConstituentsUtils::get_tanlambda_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dlambdadz", "JetConstituentsUtils::get_tanlambda_z0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_cctgtheta", "JetConstituentsUtils::get_omega_tanlambda_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_phic", "JetConstituentsUtils::get_omega_phi0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_dxyc", "JetConstituentsUtils::get_omega_d0_cov(JetsConstituents, EFlowTrack_1)")
            .Define("pfcand_cdz", "JetConstituentsUtils::get_omega_z0_cov(JetsConstituents, EFlowTrack_1)")

            .Define("pfcand_btagSip2dVal", "JetConstituentsUtils::get_Sip2dVal_clusterV(jets_ee_genkt, pfcand_dxy, pfcand_phi0, MC_PrimaryVertex, Bz)")
            .Define("pfcand_btagSip2dSig", "JetConstituentsUtils::get_Sip2dSig(pfcand_btagSip2dVal, pfcand_dxydxy)")
            .Define("pfcand_btagSip3dVal", "JetConstituentsUtils::get_Sip3dVal_clusterV(jets_ee_genkt, pfcand_dxy, pfcand_dz, pfcand_phi0, MC_PrimaryVertex, Bz)")
            .Define("pfcand_btagSip3dSig", "JetConstituentsUtils::get_Sip3dSig(pfcand_btagSip3dVal, pfcand_dxydxy, pfcand_dzdz)")
            .Define("pfcand_btagJetDistVal", "JetConstituentsUtils::get_JetDistVal_clusterV(jets_ee_genkt, JetsConstituents, pfcand_dxy, pfcand_dz, pfcand_phi0, MC_PrimaryVertex, Bz)")
            .Define("pfcand_btagJetDistSig", "JetConstituentsUtils::get_JetDistSig(pfcand_btagJetDistVal, pfcand_dxydxy, pfcand_dzdz)")

       
            ##### RUN INFERENCE (fixed by the previous section)

            .Define(
                "MVAVec",
                "JetFlavourUtils::get_weights(\
                    pfcand_erel_log,\
                    pfcand_thetarel,\
                    pfcand_phirel,\
                    pfcand_dxy,\
                    pfcand_dz,\
                    pfcand_dptdpt,\
                    pfcand_dphidphi,\
                    pfcand_detadeta,\
                    pfcand_dxydxy,\
                    pfcand_dzdz,\
                    pfcand_dxydz,\
                    pfcand_dphidxy,\
                    pfcand_dlambdadz,\
                    pfcand_dxyc,\
                    pfcand_dxyctgtheta,\
                    pfcand_phic,\
                    pfcand_phidz,\
                    pfcand_phictgtheta,\
                    pfcand_cdz,\
                    pfcand_cctgtheta,\
                    pfcand_mtof,\
                    pfcand_dndx,\
                    pfcand_charge,\
                    pfcand_isMu,\
                    pfcand_isEl,\
                    pfcand_isChargedHad,\
                    pfcand_isGamma,\
                    pfcand_isNeutralHad,\
                    pfcand_btagSip2dVal,\
                    pfcand_btagSip2dSig,\
                    pfcand_btagSip3dVal,\
                    pfcand_btagSip3dSig,\
                    pfcand_btagJetDistVal,\
                    pfcand_btagJetDistSig\
               )",
            )              
            
            ##### RECAST OUTPUT (get predictions per each sample)
            .Define("recojet_isG", "JetFlavourUtils::get_weight(MVAVec, 0)")
            .Define("recojet_isQ", "JetFlavourUtils::get_weight(MVAVec, 1)")
            .Define("recojet_isS", "JetFlavourUtils::get_weight(MVAVec, 2)")
            .Define("recojet_isC", "JetFlavourUtils::get_weight(MVAVec, 3)")
            .Define("recojet_isB", "JetFlavourUtils::get_weight(MVAVec, 4)")
                        
            ##### COMPUTE OBSERVABLES FOR ANALYSIS 
            #if not changing training etc... but only interested in the analysis using a trained model (fixed classes), you should only operate in this section.
            #if you're interested in saving variables used for training don't need to compute them again, just
            #add them to the list in at the end of the code
            
            #EXAMPLE

            #EVENT LEVEL
            .Define("njet", "JetConstituentsUtils::count_jets(JetsConstituents)")

            #JET LEVEL
            #jet kinematics
            .Define("recojet_pt",        "JetClusteringUtils::get_pt(jets_ee_genkt)")
            .Define("recojet_e",        "JetClusteringUtils::get_e(jets_ee_genkt)")
            .Define("recojet_mass",        "JetClusteringUtils::get_m(jets_ee_genkt)")
            .Define("recojet_phi",        "JetClusteringUtils::get_phi(jets_ee_genkt)")
            .Define("recojet_theta",        "JetClusteringUtils::get_theta(jets_ee_genkt)")

            .Define("tlv_jets", "JetConstituentsUtils::compute_tlv_jets(jets_ee_genkt)")
            .Define("invariant_mass", "JetConstituentsUtils::InvariantMass(tlv_jets[0], tlv_jets[1])")

            #counting types of particles composing the jet
            .Define("nconst", "JetConstituentsUtils::count_consts(JetsConstituents)")
            .Define("nmu", "JetConstituentsUtils::count_type(pfcand_isMu)")
            .Define("nel", "JetConstituentsUtils::count_type(pfcand_isEl)")
            .Define("nchargedhad", "JetConstituentsUtils::count_type(pfcand_isChargedHad)")
            .Define("nphoton", "JetConstituentsUtils::count_type(pfcand_isGamma)")
            .Define("nneutralhad", "JetConstituentsUtils::count_type(pfcand_isNeutralHad)")

            #CONSTITUENTS LEVEL
            .Define("pfcand_e", "JetConstituentsUtils::get_e(JetsConstituents)")
            .Define("pfcand_pt", "JetConstituentsUtils::get_pt(JetsConstituents)")
            .Define("pfcand_theta", "JetConstituentsUtils::get_theta(JetsConstituents)")
            .Define("pfcand_phi", "JetConstituentsUtils::get_phi(JetsConstituents)")

        )

        return df2

    #__________________________________________________________
    #SAVE PREDICTIONS & OBSERVABLES FOR ANALYSIS
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            #predictions
            'recojet_isG', 'recojet_isQ', 'recojet_isS', 'recojet_isC', 'recojet_isB',
            #observables
            'recojet_mass', 'recojet_e', 'recojet_pt',
            'invariant_mass', 
            'nconst', 'nchargedhad',
            'pfcand_e', 'pfcand_pt', 'pfcand_phi',
            'pfcand_erel', 
            'pfcand_erel_log',
        ]
        return branchList
