#Mandatory: List of processes
processList = {
    #'p8_ee_ZZ_ecm240':{'chunks':20},#Run the full statistics in 10 jobs in output dir <outputDir>/p8_ee_ZZ_ecm240/chunk<N>.root
    #'p8_ee_WW_ecm240':{'chunks':20},#Run the full statistics in 10 jobs in output dir <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp1':{'output':'e240_bp1_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp1':{'output':'e240_bp1_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp2':{'output':'e240_bp2_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp2':{'output':'e240_bp2_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp3':{'output':'e240_bp3_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp3':{'output':'e240_bp3_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp4':{'output':'e240_bp4_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp4':{'output':'e240_bp4_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp5':{'output':'e240_bp5_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp5':{'output':'e240_bp5_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp6':{'output':'e240_bp6_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp6':{'output':'e240_bp6_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp7':{'output':'e240_bp7_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp7':{'output':'e240_bp7_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp8':{'output':'e240_bp8_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp8':{'output':'e240_bp8_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp9':{'output':'e240_bp9_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp9':{'output':'e240_bp9_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp10':{'output':'e240_bp10_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp10':{'output':'e240_bp10_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp11':{'output':'e240_bp11_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp11':{'output':'e240_bp11_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp12':{'output':'e240_bp12_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp12':{'output':'e240_bp12_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp13':{'output':'e240_bp13_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp13':{'output':'e240_bp13_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp14':{'output':'e240_bp14_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp14':{'output':'e240_bp14_h2h2llvv'},
    ## no phase space at 240 GeV --- 'h2h2ll/Delphes_EDM4HEPevents_e240_bp15':{'output':'e240_bp15_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp15':{'output':'e240_bp15_h2h2llvv'},
    ## no phase space at 240 GeV --- 'h2h2ll/Delphes_EDM4HEPevents_e240_bp16':{'output':'e240_bp16_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp16':{'output':'e240_bp16_h2h2llvv'},
    ## no phase space at 240 GeV --- 'h2h2ll/Delphes_EDM4HEPevents_e240_bp17':{'output':'e240_bp17_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp17':{'output':'e240_bp17_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp18':{'output':'e240_bp18_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp18':{'output':'e240_bp18_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp19':{'output':'e240_bp19_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp19':{'output':'e240_bp19_h2h2llvv'},
    'h2h2ll/Delphes_EDM4HEPevents_e240_bp20':{'output':'e240_bp20_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp20':{'output':'e240_bp20_h2h2llvv'},
#    'Delphes_EDM4HEPevents_e365_bp1',
#    'Delphes_EDM4HEPevents_e365_bp1'
}

#for bp in `seq 1 20`; do echo "'h2h2ll/Delphes_EDM4HEPevents_e240_bp${bp}':{'output':'e240_bp${bp}_h2h2ll'},'h2h2llvv/Delphes_EDM4HEPevents_e240_bp${bp}':{'output':'e240_bp${bp}_h2h2llvv'},"; done


#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/spring2021/IDEA/"

# Define the input dir (optional)
inputDir    = "/eos/user/a/amagnan/FCC/iDMprod/winter2023/"

#Optional: output directory, default is local dir
outputDir   = "root://eosuser//eos/user/a/amagnan/FCC/iDMprod/Analysis/stage1"

#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = False

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

#Optional output directory on eos, if specified files will be copied there once the batch job is done, default is empty
#outputDirEos = "/eos/user/a/amagnan/FCC/iDMprod/h2h2ll/Analysis/"

#Optional type for eos, needed when <outputDirEos> is specified. The default is FCC eos which is eospublic
eosType = "eosuser"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
            #Accessing truth info
            .Alias("Particle1", "Particle#1.index")
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            .Define('RP_MC_index',            "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)") 

            .Define("GenStables", "FCCAnalyses::MCParticle::sel_genStatus(1)(Particle)") #gen status==1 means final state particle (FS)
            .Define("GenMC_pdg", "FCCAnalyses::MCParticle::get_pdg(GenStables)")
            #get DM candidate H = pid 35
            .Define("GenH_PID", "FCCAnalyses::MCParticle::sel_pdgID(35, true)(Particle)")
            .Define("GenH", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenH_PID)") #gen status==1 means final state particle (FS)
            .Define("n_GenH", "FCCAnalyses::MCParticle::get_n(GenH)")
            .Define("GenH_mass", "FCCAnalyses::MCParticle::get_mass(GenH)")
            .Define("GenH_e", "FCCAnalyses::MCParticle::get_e(GenH)")
            .Define("GenH_p", "FCCAnalyses::MCParticle::get_p(GenH)")
            .Define("GenH_pt", "FCCAnalyses::MCParticle::get_pt(GenH)")
            .Define("GenH_eta", "FCCAnalyses::MCParticle::get_eta(GenH)")

            #all final state gen leptons
            .Define("GenElectron_PID", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
            .Define("FSGenElectron", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") #gen status==1 means final state particle (FS)
            .Define("n_FSGenElectron", "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
            #put in dummy values below if there aren't any FSGenElectrons, to avoid seg fault
            .Define("FSGenElectron_e", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_e(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_p", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_p(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_pt", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_pt(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_eta", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_eta(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_phi", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_phi(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_charge", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_charge(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_px", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_px(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_py", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_py(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            .Define("FSGenElectron_pz", "if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_pz(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
            
            # ee invariant mass
            .Define("FSGen_ee_energy", "if (n_FSGenElectron>1) return (FSGenElectron_e.at(0) + FSGenElectron_e.at(1)); else return float(-1.);")
            .Define("FSGen_ee_px", "if (n_FSGenElectron>1) return (FSGenElectron_px.at(0) + FSGenElectron_px.at(1)); else return float(-1.);")
            .Define("FSGen_ee_py", "if (n_FSGenElectron>1) return (FSGenElectron_py.at(0) + FSGenElectron_py.at(1)); else return float(-1.);")
            .Define("FSGen_ee_pz", "if (n_FSGenElectron>1) return (FSGenElectron_pz.at(0) + FSGenElectron_pz.at(1)); else return float(-1.);")
            .Define("FSGen_ee_pt", "if (n_FSGenElectron>1) return sqrt(FSGen_ee_px*FSGen_ee_px + FSGen_ee_py*FSGen_ee_py); else return float(-1.);")
            .Define("FSGen_ee_invMass", "if (n_FSGenElectron>1) return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz ); else return float(-1.);")

            #all final state gen muons
            .Define("GenMuon_PID", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
            .Define("FSGenMuon", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #gen status==1 means final state particle (FS)
            .Define("n_FSGenMuon", "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
            #put in dummy values below if there aren't any FSGenMuons, to avoid seg fault
            .Define("FSGenMuon_e", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_e(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_p", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_p(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_pt", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pt(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_eta", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_eta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_phi", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_phi(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_charge", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_charge(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_px", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_px(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_py", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_py(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            .Define("FSGenMuon_pz", "if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pz(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
            
            # mm invariant mass
            .Define("FSGen_mm_energy", "if (n_FSGenMuon>1) return (FSGenMuon_e.at(0) + FSGenMuon_e.at(1)); else return float(-1.);")
            .Define("FSGen_mm_px", "if (n_FSGenMuon>1) return (FSGenMuon_px.at(0) + FSGenMuon_px.at(1)); else return float(-1.);")
            .Define("FSGen_mm_py", "if (n_FSGenMuon>1) return (FSGenMuon_py.at(0) + FSGenMuon_py.at(1)); else return float(-1.);")
            .Define("FSGen_mm_pz", "if (n_FSGenMuon>1) return (FSGenMuon_pz.at(0) + FSGenMuon_pz.at(1)); else return float(-1.);")
            .Define("FSGen_mm_pt", "if (n_FSGenElectron>1) return sqrt(FSGen_mm_px*FSGen_mm_px + FSGen_mm_py*FSGen_mm_py); else return float(-1.);")
            .Define("FSGen_mm_invMass", "if (n_FSGenMuon>1) return sqrt(FSGen_mm_energy*FSGen_mm_energy - FSGen_mm_px*FSGen_mm_px - FSGen_mm_py*FSGen_mm_py - FSGen_mm_pz*FSGen_mm_pz ); else return float(-1.);")


            #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing transverse energy
            .Define("MET_e", "ReconstructedParticle::get_e(MissingET)") #absolute value of MET
            .Define("MET_p", "ReconstructedParticle::get_p(MissingET)") #absolute value of MET
            .Define("MET_pt", "ReconstructedParticle::get_pt(MissingET)") #absolute value of MET
            .Define("MET_eta", "ReconstructedParticle::get_eta(MissingET)") #absolute value of MET
            .Define("MET_px", "ReconstructedParticle::get_px(MissingET)") #x-component of MET
            .Define("MET_py", "ReconstructedParticle::get_py(MissingET)") #y-component of MET
            .Define("MET_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of MET
            
            #PHOTONS
            .Alias("Photon0", "Photon#0.index")
            .Define("photons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
            #select on pT
            .Define("selected_photons", "ReconstructedParticle::sel_p(5.)(photons)")
            .Define("n_photons",  "ReconstructedParticle::get_n(selected_photons)") #count how many photons are in the event in total

            # define an alias for lepton index collection
            .Alias("Muon0", "Muon#0.index")
            .Alias("Electron0", "Electron#0.index")
            # define the muon collection
            .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            .Define("electrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
            #select muons on pT
            .Define("selected_muons", "ReconstructedParticle::sel_p(5.)(muons)")
            .Define("selected_electrons", "ReconstructedParticle::sel_p(5.)(electrons)")

            #count how many electrons are in the event in total
            .Define("n_muons",  "ReconstructedParticle::get_n(selected_muons)")
            .Define("n_electrons",  "ReconstructedParticle::get_n(selected_electrons)")


            # Filter exactly 2 leptons
            .Filter("n_muons==2 || n_electrons==2")


            # create branch with muon transverse momentum
            .Define("selected_muons_pt", "ReconstructedParticle::get_pt(selected_muons)")
            .Define("selected_electrons_pt", "ReconstructedParticle::get_pt(selected_electrons)")
            .Define("selected_photons_pt", "ReconstructedParticle::get_pt(selected_photons)")
            # create branch with muon rapidity
            .Define("selected_muons_y",  "ReconstructedParticle::get_y(selected_muons)")
            .Define("selected_electrons_y",  "ReconstructedParticle::get_y(selected_electrons)")
            .Define("selected_photons_y",  "ReconstructedParticle::get_y(selected_photons)")
            # create branch with muon rapidity
            .Define("selected_muons_eta",  "ReconstructedParticle::get_eta(selected_muons)")
            .Define("selected_electrons_eta",  "ReconstructedParticle::get_eta(selected_electrons)")
            .Define("selected_photons_eta",  "ReconstructedParticle::get_eta(selected_photons)")
            # create branch with muon rapidity
            .Define("selected_muons_phi",  "ReconstructedParticle::get_phi(selected_muons)")
            .Define("selected_electrons_phi",  "ReconstructedParticle::get_phi(selected_electrons)")
            .Define("selected_photons_phi",  "ReconstructedParticle::get_phi(selected_photons)")
            # create branch with muon total momentum
            .Define("selected_muons_p",     "ReconstructedParticle::get_p(selected_muons)")
            .Define("selected_electrons_p",     "ReconstructedParticle::get_p(selected_electrons)")
            .Define("selected_photons_p",     "ReconstructedParticle::get_p(selected_photons)")
            # create branch with muon energy
            .Define("selected_muons_e",     "ReconstructedParticle::get_e(selected_muons)")
            .Define("selected_electrons_e",     "ReconstructedParticle::get_e(selected_electrons)")
            .Define("selected_photons_e",     "ReconstructedParticle::get_e(selected_photons)")
            # create branch with muon charge
            .Define("selected_muons_charge",     "ReconstructedParticle::get_charge(selected_muons)")
            .Define("selected_electrons_charge",     "ReconstructedParticle::get_charge(selected_electrons)")


            # fill Z candidate from leading lepton pair
            .Define("zed_mumu",         "ReconstructedParticle::resonanceBuilder(91)(selected_muons)")
            .Define("zed_ee",         "ReconstructedParticle::resonanceBuilder(91)(selected_electrons)")
            # create branch with zed mass
            .Define("zed_mumu_m",       "ReconstructedParticle::get_mass(zed_mumu)")
            .Define("zed_ee_m",       "ReconstructedParticle::get_mass(zed_ee)")
           # create branch with zed E
            .Define("zed_mumu_e",       "ReconstructedParticle::get_e(zed_mumu)")
            .Define("zed_ee_e",       "ReconstructedParticle::get_e(zed_ee)")
            # create branch with zed p
            .Define("zed_mumu_p",       "ReconstructedParticle::get_p(zed_mumu)")
            .Define("zed_ee_p",       "ReconstructedParticle::get_p(zed_ee)")
            # create branch with zed pz
            .Define("zed_mumu_pz",       "ReconstructedParticle::get_pz(zed_mumu)")
            .Define("zed_ee_pz",       "ReconstructedParticle::get_pz(zed_ee)")
            # create branch with zed theta
            .Define("zed_mumu_theta",       "ReconstructedParticle::get_theta(zed_mumu)")
            .Define("zed_ee_theta",       "ReconstructedParticle::get_theta(zed_ee)")
            # create branch with zed transverse momenta
            .Define("zed_mumu_pt",      "ReconstructedParticle::get_pt(zed_mumu)")
            .Define("zed_ee_pt",      "ReconstructedParticle::get_pt(zed_ee)")
            # create branch with leptonic charge
            .Define("zed_mumu_charge","ReconstructedParticle::get_charge(zed_mumu)")
            .Define("zed_ee_charge","ReconstructedParticle::get_charge(zed_ee)")

            # calculate recoil of zed_leptonic
            .Define("zed_mumu_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_mumu)")
            .Define("zed_ee_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_ee)")
            # create branch with recoil mass
            .Define("zed_mumu_recoil_m","ReconstructedParticle::get_mass(zed_mumu_recoil)")
            .Define("zed_ee_recoil_m","ReconstructedParticle::get_mass(zed_ee_recoil)")


            #JETS
            .Define("n_jets", "ReconstructedParticle::get_n(Jet)") #count how many jets are in the event in total
            # Jet clustering
            # First remove leptons from the list to be clustered
            .Define("my_reco",  "ReconstructedParticle::remove( ReconstructedParticles,  selected_electrons)")
            .Define("my_recoparticles",  "ReconstructedParticle::remove( my_reco,  selected_muons)")
            .Define("RP_px", "ReconstructedParticle::get_px(my_recoparticles) ")
            .Define("RP_py", "ReconstructedParticle::get_py(my_recoparticles) ")
            .Define("RP_pz", "ReconstructedParticle::get_pz(my_recoparticles) ")
            .Define("RP_e", "ReconstructedParticle::get_e(my_recoparticles) ")

            # build pseudo jets with the RP, using the interface that takes px,py,pz,E
            .Define( "pseudo_jets",  "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)" )
            
            # run jet clustering with all reconstructed particles. Durham algo, exclusive clustering N=2, E-scheme
            .Define( "FCCAnalysesJets_ee_genkt",  "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)" )
            .Define("jets_ee_genkt",  "JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_ee_genkt )")
            # access the jets kinematics :
            .Define("seljet_e",  "JetClusteringUtils::get_e( jets_ee_genkt )")
            .Define("seljet_pt",  "JetClusteringUtils::get_pt( jets_ee_genkt )")
            .Define("seljet_eta",  "JetClusteringUtils::get_eta( jets_ee_genkt )")
            .Define("seljet_phi",  "JetClusteringUtils::get_phi( jets_ee_genkt )")
            
            # access the jet constituents:
            .Define("jetconstituents_ee_genkt", "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt) ")
            
            # access the "dmerge" distances:
            #.Define("dmerge_23", "JetClusteringUtils::get_exclusive_dmerge( FCCAnalysesJets, 2)" )

            #OBJECT SELECTION: Consider only those objects that have pT > certain threshold
            #.Define("selected_jets", "ReconstructedParticle::sel_pt(30.)(Jet)") #select only jets with a pT > 30 GeV            
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            ######## Monte-Carlo particles #######
            "GenMC_pdg",
            "n_GenH",
            "GenH_e",
            "GenH_p",
            "GenH_pt",
            "GenH_eta",
            "GenH_mass",
            "n_FSGenElectron",
            "FSGenElectron_e",
            "FSGenElectron_p",
            "FSGenElectron_pt",
            "FSGenElectron_eta",
            "FSGenElectron_phi",
            "FSGenElectron_charge",
            "FSGen_ee_pt",
            "FSGen_ee_invMass",
            "n_FSGenMuon",
            "FSGenMuon_e",
            "FSGenMuon_p",
            "FSGenMuon_pt",
            "FSGenMuon_eta",
            "FSGenMuon_phi",
            "FSGenMuon_charge",
            "FSGen_mm_pt",
            "FSGen_mm_invMass",
            ##### Reco
            "RP_MC_index",
            "jetconstituents_ee_genkt",
            "n_jets",
            "n_photons",
            "n_electrons",
            "n_muons",
            "seljet_e",
            "seljet_pt",
            "seljet_eta",
            "seljet_phi",
            "MET_e",
            "MET_p",
            "MET_pt",
            "MET_eta",
            "MET_px",
            "MET_py",
            "MET_phi",
            "selected_muons_pt",
            "selected_muons_y",
            "selected_muons_p",
            "selected_muons_e",
            "selected_muons_eta",
            "selected_muons_phi",
            "selected_muons_charge",
            "selected_electrons_pt",
            "selected_electrons_y",
            "selected_electrons_p",
            "selected_electrons_e",
            "selected_electrons_eta",
            "selected_electrons_phi",
            "selected_electrons_charge",
            "selected_photons_pt",
            "selected_photons_y",
            "selected_photons_p",
            "selected_photons_e",
            "selected_photons_eta",
            "selected_photons_phi",
            "zed_mumu_pt",
            "zed_mumu_pz",
            "zed_mumu_p",
            "zed_mumu_e",
            "zed_mumu_theta",
            "zed_mumu_m",
            "zed_mumu_charge",
            "zed_mumu_recoil_m",
            "zed_ee_pt",
            "zed_ee_pz",
            "zed_ee_p",
            "zed_ee_e",
            "zed_ee_theta",
            "zed_ee_m",
            "zed_ee_charge",
            "zed_ee_recoil_m",
        ]
        return branchList
