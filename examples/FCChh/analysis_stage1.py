#Mandatory: List of processes
processList = {
    'yaml_signal':{},
    'yaml_BG':{}
   }
prodTag     = "/eos/home-s/ssadeghi/project30Aug/fccanalysis/FCCAnalyses/stop-pair/"
outputDir   = "outputs/stop-pair/stage1"

#Optional: ncpus, default is 4
#nCPUS       = 8

#Optional running on HTCondor, default is False
#runBatch    = False

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#compGroup = "group_u_FCC.local_gen"

#Optional test file
##testFile ="root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_101027117.root"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
            .Alias("Muon0", "Muon#0.index")
            .Alias("Jet3","Jet#3.index")
          ##  .Define("jets",  "ReconstructedParticle::get(Jet3, ReconstructedParticles)")
            #select electrons on pT
          ##   .Define("selected_jets", "ReconstructedParticle::sel_pt(1000.)(jets)")
             .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
             .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
             .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
             .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
             .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
             .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
          #  .Define("RP_q",           "ReconstructedParticle::get_charge(selected_jets)")
             .Define("FCCAnalysesJets_antikt", "JetClustering::clustering_antikt(0.5, 0, 0, 0, 1)(pseudo_jets)") 
             .Define("jets_antikt",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_antikt)")
             .Define("selected_Jets_pt",     "JetClusteringUtils::get_pt(jets_antikt)")
             .Define("selected_Jets_eta",     "JetClusteringUtils::get_eta(jets_antikt)") 
             .Define("met",      "ReconstructedParticle::sel_pt(4000.)(MissingET)")
             .Define("selected_met",               "ReconstructedParticle::get_pt(met)")  
             .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            #select muons on pT
             .Define("selected_muons", "ReconstructedParticle::sel_pt(200.)(muons)")
               )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
             "selected_Jets_pt",
            "selected_Jets_eta",
            "selected_met",
            "selected_muons",
            "selected_Jets_phi"
        ]
        return branchList
        
