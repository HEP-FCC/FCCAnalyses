testFile="root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_Zbb_ecm91/events_066726720.root"

#Mandatory: List of processes
processList = {
    'p8_ee_Zuds_ecm91':{'fraction':0.0001}, #Run 0.01% statistics in one output file named <outputDir>/p8_ee_Zuds_ecm91.root
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/KG"

#Optional: ncpus, default is 4
nCPUS       = 8

#Optional running on HTCondor, default is False
#runBatch    = False

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
            .Alias("Particle1", "Particle#1.index")
            
            # get all the MC particles to check for Ks                                                                                                                    
            .Define("MC_pdg", "FCCAnalyses::MCParticle::get_pdg(Particle)")
            # get momenta & mass of all particles                                                                                                                         
            .Define("MC_p4", "FCCAnalyses::MCParticle::get_tlv(Particle)")
            .Define("MC_mass", "FCCAnalyses::MCParticle::get_mass(Particle)")
            
            # Ks -> pi+pi-                                                                                                                                                
            .Define("K0spipi_indices", "FCCAnalyses::MCParticle::get_indices_ExclusiveDecay(310, {211, -211}, true, true) (Particle, Particle1)")
            # Lambda0 -> p+pi-                                                                                                                                            
            .Define("Lambda0ppi_indices", "FCCAnalyses::MCParticle::get_indices_ExclusiveDecay(3122, {2212, -211}, true, true) (Particle, Particle1)")
            
            # determime the primary (and secondary) tracks without using the MC-matching:                                                                                 
            
            # Select the tracks that are reconstructed  as primaries                                                                                                      
            .Define("RecoedPrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)")

            .Define("n_RecoedPrimaryTracks",  "ReconstructedParticle2Track::getTK_n( RecoedPrimaryTracks )")
            # the final primary vertex :                                                                                                                                  
            .Define("PrimaryVertexObject",   "VertexFitterSimple::VertexFitter_Tk ( 1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300) ")
            .Define("PrimaryVertex",   "VertexingUtils::get_VertexData( PrimaryVertexObject )")

            # the secondary tracks                                                                                                                                        
            .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1,  RecoedPrimaryTracks )")
            .Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )

            # which of the tracks are primary according to the reco algprithm                                                                                             
            .Define("IsPrimary_based_on_reco",  "VertexFitterSimple::IsPrimary_forTracks( EFlowTrack_1,  RecoedPrimaryTracks )")

            # jet clustering
            .Define("RP_px",        "ReconstructedParticle::get_px(ReconstructedParticles)")
            .Define("RP_py",        "ReconstructedParticle::get_py(ReconstructedParticles)")
            .Define("RP_pz",        "ReconstructedParticle::get_pz(ReconstructedParticles)")               
            .Define("RP_m",         "ReconstructedParticle::get_mass(ReconstructedParticles)")
            # build psedo-jets with the Reconstructed final particles
            .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
            # run jet clustering with all reco particles. ee_kt_algorithm, exclusive clustering, exactly 2 jets, E-scheme
            .Define("FCCAnalysesJets_ee_kt", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
            # get the jets out of the structure
            .Define("jets_ee_kt", "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_kt)")
            # get the jet constituents out of the structure
            .Define("jetconstituents", "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_kt)")

            
            # find V0s
            #.Define("V0_evt", "VertexFinderLCFIPlus::get_V0s(SecondaryTracks, PrimaryVertexObject, true)")
            .Define("V0", "VertexFinderLCFIPlus::get_V0s_jet(ReconstructedParticles, EFlowTrack_1, IsPrimary_based_on_reco, jets_ee_kt, jetconstituents, PrimaryVertexObject)")
            .Define("V0_jet", "VertexingUtils::get_svInJets(V0.vtx, V0.nSV_jet)")
            # get pdg vector out                                                                                                                                          
            #.Define("V0_pdg", "VertexingUtils::get_pdg_V0(V0)")
            .Define("V0_pdg", "VertexingUtils::get_pdg_V0(V0.pdgAbs, V0.nSV_jet)")
            # get invariant mass vector out
            .Define("V0_invM", "VertexingUtils::get_invM_V0(V0.invM, V0.nSV_jet)")
            # get the position
            .Define("V0_pos", "VertexingUtils::get_position_SV(V0_jet)")
            # get the chi2
            #.Define("V0_chi2", "VertexingUtils::get_chi2_SV(V0)")
            .Define("V0_chi2", "VertexingUtils::get_chi2_SV(V0_jet)")
            # get the momenta
            .Define("V0_p", "VertexingUtils::get_p_SV(V0_jet)")

            # more V0 properties
            # .Define("v0_pid",     "VertexingUtils::get_pdg_V0(V0.pdgAbs, V0.nSV_jet)") # V0 pdg id
            # .Define("v0_mass",    "VertexingUtils::get_invM_V0(V0.invM, V0.nSV_jet)") # V0 invariant mass
            # .Define("v0_p",       "VertexingUtils::get_pMag_SV(V0_jet)") # V0 momentum (magnitude)
            # .Define("v0_ntracks", "VertexingUtils::get_VertexNtrk(V0_jet)") # V0 daughters (no of tracks)
            # .Define("v0_chi2",    "VertexingUtils::get_chi2_SV(V0_jet)") # V0 chi2 (not normalised)
            # .Define("v0_normchi2","VertexingUtils::get_norm_chi2_SV(V0_jet)") # V0 chi2 (normalised but same as above)
            # .Define("v0_ndf",     "VertexingUtils::get_nDOF_SV(V0_jet)") # V0 no of DOF (always 1)
            # .Define("v0_theta",   "VertexingUtils::get_theta_SV(V0_jet)") # V0 polar angle (theta)
            # .Define("v0_phi",     "VertexingUtils::get_phi_SV(V0_jet)") # V0 azimuthal angle (phi)

            )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            # MC particles
            "MC_pdg",
            "MC_p4",
            "MC_mass",

            # Ks -> pi+pi- & Lambda0->p+pi-
            "K0spipi_indices",
            "Lambda0ppi_indices",
            
            #  primary vertex and primary tracks w/o any MC-matching :
            "IsPrimary_based_on_reco",
            "PrimaryVertex",
            
            # V0 object
            "V0",
            "V0_jet",
            "V0_pdg",
            "V0_invM",
            "V0_pos",
            "V0_chi2",
            "V0_p",

            # more V0 properties
            # 'v0_pid',
            # 'v0_mass',
            # 'v0_p',
            # 'v0_ntracks',
            # 'v0_chi2',
            # 'v0_normchi2',
            # 'v0_ndf',
            # 'v0_theta',
            # 'v0_phi',

        ]
        return branchList
