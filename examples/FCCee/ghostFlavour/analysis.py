#Mandatory: List of processes
processList = {
    'p8_ee_Zbb_ecm91':{'fraction':0.000000000001, 'chunks':1}, #Run 50% of the statistics in two files named <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/ghostFlavour"

#Optional: analysisName, default is ""
#analysisName = "My Analysis"

#Optional: ncpus, default is 4
#nCPUS       = 8
nCPUS       = 1

#Optional running on HTCondor, default is False
#runBatch    = False

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#compGroup = "group_u_FCC.local_gen"

#Optional test file
#testFile ="root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_101027117.root"

#nevents=10

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
            #alias for dealing with # in python
            .Alias("Particle0", "Particle#0.index")
            .Alias("Particle1", "Particle#1.index")
            .Alias("Jet3","Jet#3.index")

            .Define("MC_px",  "MCParticle::get_px(Particle)")
            .Define("MC_py",  "MCParticle::get_py(Particle)")
            .Define("MC_pz",  "MCParticle::get_pz(Particle)")
            .Define("MC_p",  "MCParticle::get_p(Particle)")
            .Define("MC_e",  "MCParticle::get_e(Particle)")
            .Define("MC_m",  "MCParticle::get_mass(Particle)")
            .Define("MC_theta",  "MCParticle::get_theta(Particle)")
            .Define("MC_pdg", "MCParticle::get_pdg(Particle)")
            .Define("MC_status", "MCParticle::get_genStatus(Particle)")


            #define the RP px, py, pz and e
            .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
            .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
            .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
            .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")

            ################
            #Jet Clustering#
            ################

            #build pseudo jets with the RP, using the interface that takes px,py,pz,m for better
            #handling of rounding errors
            .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")

            #EE-KT ALGORITHM
            #run jet clustering with all MC particles. ee_kt_algorithm, exclusive clustering, exactly 2 jets, E-scheme
            .Define("FCCAnalysesJets_ee_kt", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")

            #get the jets out of the structure
            .Define("jets_ee_kt",            "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_kt)")

            #get the jet constituents out of the structure
            .Define("jetconstituents_ee_kt", "JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_kt)")

            #get some jet variables
            .Define("jets_ee_kt_e",          "JetClusteringUtils::get_e(jets_ee_kt)")
            .Define("jets_ee_kt_px",         "JetClusteringUtils::get_px(jets_ee_kt)")
            .Define("jets_ee_kt_py",         "JetClusteringUtils::get_py(jets_ee_kt)")
            .Define("jets_ee_kt_pz",         "JetClusteringUtils::get_pz(jets_ee_kt)")
            .Define("jets_ee_kt_flavour",    "JetTaggingUtils::get_flavour(jets_ee_kt, Particle)")

            ###############
            #Ghost Flavour#
            ###############

            # First the ghost indices are found using the find_ghosts function which returns an int RVec 
            .Define("ghost_MCindices",        "JetTaggingUtils::find_ghosts(Particle, Particle1)")

            # Then the flavour is "set" by writing the ghost flavour to the jets.flavour field defined in the FCCAnalysesJet. This encompases rescaling of ghosts, their appending to the 
            # pseudojet set, the reclustering, and the kinematic check that the reclustered ghost jets have the same p_i as the original jet set. 
            .Define("FCCAnalysesJets_wflavour",        "JetTaggingUtils::set_flavour(Particle, ghost_MCindices, FCCAnalysesJets_ee_kt, pseudo_jets)")

            # The flavour can simply be read-off from the jets.flavour field, returning and int RVec with the jet flavours
            .Define("jet_flavour",        "JetTaggingUtils::get_flavour(FCCAnalysesJets_wflavour)")

            # Or (as most might prefer) the above steps can be combined by overloading and providing all relevant parameters to get_flavour(...)
            .Define("jet_flavour1", "JetTaggingUtils::get_flavour(Particle, Particle1, FCCAnalysesJets_ee_kt, pseudo_jets)")

        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "MC_px",
            "MC_py",
            "MC_pz",
            "MC_p",
            "MC_e",
            "MC_theta",
            "MC_pdg",
            "MC_status",

            "jets_ee_kt_e",
            "jets_ee_kt_px",
            "jets_ee_kt_py",
            "jets_ee_kt_pz",
            "jets_ee_kt_flavour",
            "jetconstituents_ee_kt",


            "ghost_MCindices",
            "jet_flavour",
            "jet_flavour1",
        ]
        return branchList
