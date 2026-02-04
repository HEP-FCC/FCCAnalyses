### Extracting variables form the EDM4HEP files. 
processList = {
    "mgp8_pp_bb_PTmin_5000_5f_84TeV": {"fraction": 1},
     "mgp8_pp_cc_PTmin_5000_5f_84TeV": {"fraction": 1},
      "mgp8_pp_gg_PTmin_5000_5f_84TeV": {"fraction": 1},
       "mgp8_pp_thadthad_PTmin_5000_5f_84TeV": {"fraction": 1},
        "mgp8_pp_tleptlep_PTmin_5000_5f_84TeV": {"fraction": 1},
         "mgp8_pp_uuddss_PTmin_5000_5f_84TeV": {"fraction": 1},
          "mgp8_pp_whadwhad_PTmin_5000_5f_84TeV": {"fraction": 1},
           "mgp8_pp_zhadzhad_PTmin_5000_5f_84TeV": {"fraction": 1},
            
}

outputDir = "./output/FCC-hh-TopTagging"
inputDir = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II_trackCov"
nCPUS = -1



class RDFanalysis:
    def analysers(df):



        coll = {
        "GenParticles": "Particle",
        "PFParticles": "ReconstructedParticles",
        "PFTracks": "EFlowTrack",
        "PFPhotons": "EFlowPhoton",
        "PFNeutralHadrons": "EFlowNeutralHadron",
        "TrackState": "_EFlowTrack_trackStates",
        "TrackerHits": "TrackerHits",
        "CalorimeterHits": "CalorimeterHits",
        "PathLength": "EFlowTrack_L",
        "Bz": "magFieldBz",
        }


        # Define RP kinematics
        ####################################################################################################
        df = df.Define("RP_px", "ReconstructedParticle::get_px(ReconstructedParticles)")
        df = df.Define("RP_py", "ReconstructedParticle::get_py(ReconstructedParticles)")
        df = df.Define("RP_pz", "ReconstructedParticle::get_pz(ReconstructedParticles)")
        df = df.Define("RP_e", "ReconstructedParticle::get_e(ReconstructedParticles)")
        df = df.Define("RP_m", "ReconstructedParticle::get_mass(ReconstructedParticles)")

        # Define pseudo-jets
        ####################################################################################################
        df = df.Define("pjetc", "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
        # Anti-kt clustering and jet constituents
        ####################################################################################################
        df = df.Define("_jet", "JetClustering::clustering_antikt(0.5, 0, 100, 0 , 1)(pjetc)")
        df = df.Define("jets","JetClusteringUtils::get_pseudoJets(_jet)" )
        df = df.Define("_jetc", "JetClusteringUtils::get_constituents(_jet)") 
        df = df.Define("jetc", "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticles, _jetc)")


        ############################################# Event Level Variables #######################################################
        df = df.Define("jet_p4", "JetConstituentsUtils::compute_tlv_jets(jets)" )
        df = df.Define("event_invariant_mass", "JetConstituentsUtils::InvariantMass(jet_p4[0], jet_p4[1])")

        # ===== VERTEX
        # MC primary vertex
        df = df.Define("pv", f'FCCAnalyses::MCParticle::get_EventPrimaryVertexP4()({coll["GenParticles"]})')
        ############################################# Particle Flow Level Variables #######################################################

        df = df.Define("pfcand_isMu",       "JetConstituentsUtils::get_isMu(jetc)") 
        df = df.Define("pfcand_isEl",       "JetConstituentsUtils::get_isEl(jetc)") 
        df = df.Define("pfcand_isChargedHad","JetConstituentsUtils::get_isChargedHad(jetc)") 
        df = df.Define("pfcand_isGamma",    "JetConstituentsUtils::get_isGamma(jetc)") 
        df = df.Define("pfcand_isNeutralHad","JetConstituentsUtils::get_isNeutralHad(jetc)")

        ############################################# Kinematics and PID #######################################################

        df = df.Define("pfcand_e",        "JetConstituentsUtils::get_e(jetc)") 
        df = df.Define("pfmask",          "JetConstituentsUtils::mask(pfcand_e)")
        
        df = df .Define("pfcand_p",        "JetConstituentsUtils::get_p(jetc)") 
        df = df .Define("pfcand_px",        "JetConstituentsUtils::get_px(jetc)") 
        df = df .Define("pfcand_py",        "JetConstituentsUtils::get_py(jetc)") 
        df = df .Define("pfcand_pz",        "JetConstituentsUtils::get_pz(jetc)") 

        
        df = df.Define("pfcand_theta",    "JetConstituentsUtils::get_theta(jetc)") 
        df = df.Define("pfcand_phi",      "JetConstituentsUtils::get_phi(jetc)") 
        df = df.Define("pfcand_charge",   "JetConstituentsUtils::get_charge(jetc)") 
        df = df.Define("pfcand_type",     "JetConstituentsUtils::get_type(jetc)") 
        df = df.Define("pfcand_erel", "JetConstituentsUtils::get_erel_cluster(jets, jetc)")
        df = df.Define("pfcand_erel_log", "JetConstituentsUtils::get_erel_log_cluster(jets, jetc)")
        df = df.Define("pfcand_thetarel","JetConstituentsUtils::get_thetarel_cluster(jets, jetc)")
        df = df.Define("pfcand_phirel",  "JetConstituentsUtils::get_phirel_cluster(jets, jetc)")

        df = df.Define("Bz", f'{coll["Bz"]}[0]')


############################################# Track Parameters and Covariance #######################################################

        df = df.Define("pfcand_dxy",        f'JetConstituentsUtils::XPtoPar_dxy(jetc, {coll["TrackState"]}, pv, Bz)') 
        df = df.Define("pfcand_dz",         f'JetConstituentsUtils::XPtoPar_dz(jetc, {coll["TrackState"]}, pv, Bz)') 
        df = df.Define("pfcand_phi0",       f'JetConstituentsUtils::XPtoPar_phi(jetc, {coll["TrackState"]}, pv, Bz)') 
        df = df.Define("pfcand_C",          f'JetConstituentsUtils::XPtoPar_C(jetc, {coll["TrackState"]}, Bz)') 
        df = df.Define("pfcand_ct",         f'JetConstituentsUtils::XPtoPar_ct(jetc, {coll["TrackState"]}, Bz)') 
        df = df.Define("pfcand_dptdpt",     f'JetConstituentsUtils::get_omega_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dxydxy",     f'JetConstituentsUtils::get_d0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dzdz",       f'JetConstituentsUtils::get_z0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dphidphi",   f'JetConstituentsUtils::get_phi0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_detadeta",   f'JetConstituentsUtils::get_tanlambda_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dxydz",      f'JetConstituentsUtils::get_d0_z0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dphidxy",    f'JetConstituentsUtils::get_phi0_d0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_phidz",      f'JetConstituentsUtils::get_phi0_z0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_phictgtheta",f'JetConstituentsUtils::get_tanlambda_phi0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dxyctgtheta",f'JetConstituentsUtils::get_tanlambda_d0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dlambdadz",  f'JetConstituentsUtils::get_tanlambda_z0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_cctgtheta",  f'JetConstituentsUtils::get_omega_tanlambda_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_phic",       f'JetConstituentsUtils::get_omega_phi0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_dxyc",       f'JetConstituentsUtils::get_omega_d0_cov(jetc, {coll["TrackState"]})') 
        df = df.Define("pfcand_cdz",        f'JetConstituentsUtils::get_omega_z0_cov(jetc, {coll["TrackState"]})')



############################################# Btag Variables #######################################################

        df = df.Define("pfcand_btagSip2dVal",   "JetConstituentsUtils::get_Sip2dVal_clusterV(jets, pfcand_dxy, pfcand_phi0, Bz)") 
        df = df.Define("pfcand_btagSip2dSig",   "JetConstituentsUtils::get_Sip2dSig(pfcand_btagSip2dVal, pfcand_dxydxy)") 
        df = df.Define("pfcand_btagSip3dVal",   "JetConstituentsUtils::get_Sip3dVal_clusterV(jets, pfcand_dxy, pfcand_dz, pfcand_phi0, Bz)") 
        df = df.Define("pfcand_btagSip3dSig",   "JetConstituentsUtils::get_Sip3dSig(pfcand_btagSip3dVal, pfcand_dxydxy, pfcand_dzdz)") 
        df = df.Define("pfcand_btagJetDistVal","JetConstituentsUtils::get_JetDistVal_clusterV(jets, jetc, pfcand_dxy, pfcand_dz, pfcand_phi0, Bz)") 
        df = df.Define("pfcand_btagJetDistSig","JetConstituentsUtils::get_JetDistSig(pfcand_btagJetDistVal, pfcand_dxydxy, pfcand_dzdz)")





        ############################################# Jet Level Variables #######################################################
        df=df.Define("event_njet",   "JetConstituentsUtils::count_jets(jetc)")
        df.Filter("event_njet > 1")
        ##############################################################################################################
        df = df.Define("sumTLVs", "JetConstituentsUtils::sum_tlv_constituents(jetc)")

        #df = df.Define("jet_p", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].P(), sumTLVs[1].P()})")
        #df = df.Define("jet_e", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].E(), sumTLVs[1].E()})")
        #df = df.Define("jet_mass", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].M(), sumTLVs[1].M()})")
        #df = df.Define("jet_phi", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].Phi(), sumTLVs[1].Phi()})")
        #df = df.Define("jet_theta", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].Theta(), sumTLVs[1].Theta()})")
        #df = df.Define("jet_pT", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].Pt(), sumTLVs[1].Pt()})")
        #df = df.Define("jet_eta", "ROOT::VecOps::RVec<Double_t>({sumTLVs[0].Eta(), sumTLVs[1].Eta()})")

        df = df.Define("jet_nconst", "JetConstituentsUtils::count_consts(jetc)") 
        df = df.Define(f"jet_nmu",    f"JetConstituentsUtils::count_type(pfcand_isMu)") 
        df = df.Define(f"jet_nel",    f"JetConstituentsUtils::count_type(pfcand_isEl)") 
        df = df.Define(f"jet_nchad",  f"JetConstituentsUtils::count_type(pfcand_isChargedHad)") 
        df = df.Define(f"jet_ngamma", f"JetConstituentsUtils::count_type(pfcand_isGamma)") 
        df = df.Define(f"jet_nnhad",  f"JetConstituentsUtils::count_type(pfcand_isNeutralHad)")

##### new
                # compute jet observables
        df = df.Define("jet_p", "JetClusteringUtils::get_p(jets)")
        df = df.Define("jet_px", "JetClusteringUtils::get_px(jets)")
        df = df.Define("jet_py", "JetClusteringUtils::get_py(jets)")
        df = df.Define("jet_pz", "JetClusteringUtils::get_pz(jets)")
        df = df.Define("jet_pT", "JetClusteringUtils::get_pt(jets)")

        df = df.Define("jet_e", "JetClusteringUtils::get_e(jets)")
        df = df.Define("jet_mass", "JetClusteringUtils::get_m(jets)")
        df = df.Define("jet_phi", "JetClusteringUtils::get_phi(jets)")
        df = df.Define("jet_theta", "JetClusteringUtils::get_theta(jets)")
        df = df.Define("jet_eta", "JetClusteringUtils::get_eta(jets)")


        return df

    def output():

        return [
                    "pfcand_px", "pfcand_py","pfcand_pz","pfmask",
            
                "event_invariant_mass","event_njet",  "jet_mass","jet_p","jet_e", "jet_phi", "jet_theta", "jet_pT",
                
                "jet_nnhad","jet_ngamma","jet_nchad","jet_nel", "jet_nmu", "jet_nconst",
                
                "pfcand_isMu", "pfcand_isEl", "pfcand_isChargedHad", "pfcand_isGamma", "pfcand_isNeutralHad",
                "pfcand_e", "pfcand_p", "pfcand_theta", "pfcand_phi", "pfcand_charge", "pfcand_type",
                "pfcand_erel", "pfcand_erel_log", "pfcand_thetarel", "pfcand_phirel", 
 
                #"Bz",
 
                "pfcand_dxy", "pfcand_dz", "pfcand_phi0", "pfcand_C", "pfcand_ct",
                "pfcand_dptdpt", "pfcand_dxydxy", "pfcand_dzdz", "pfcand_dphidphi", "pfcand_detadeta",
                "pfcand_dxydz", "pfcand_dphidxy", "pfcand_phidz", "pfcand_phictgtheta", "pfcand_dxyctgtheta",
                "pfcand_dlambdadz", "pfcand_cctgtheta", "pfcand_phic", "pfcand_dxyc", "pfcand_cdz",
 
                "pfcand_btagSip2dVal", "pfcand_btagSip2dSig", "pfcand_btagSip3dVal", "pfcand_btagSip3dSig", 
                "pfcand_btagJetDistVal", "pfcand_btagJetDistSig",
                ]
