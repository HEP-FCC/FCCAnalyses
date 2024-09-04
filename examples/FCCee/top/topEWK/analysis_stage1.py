#Mandatory: List of processes
processList = {
#             'wzp6_ee_tt_pol_ecm365':{'chunks':50},
#             'wzp6_ee_Z_tt_leplep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_Z_tt_tlepThad_pol_ecm365':{'chunks':10,},
#             'wzp6_ee_Z_tt_thadTlep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_Z_tt_hadhad_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_leplep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_tlepThad_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_thadTlep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_hadhad_pol_ecm365':{'chunks':10}
#             'wzp6_ee_SM_tt_leplep_pol_ecm365':{'chunks':50},
#             'wzp6_ee_SM_tt_tlepThad_pol_ecm365':{'chunks':50},
#             'wzp6_ee_SM_tt_thadTlep_pol_ecm365':{'chunks':50},
             'wzp6_ee_SM_tt_hadhad_pol_ecm365':{'chunks':50}

            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/top/hadronic/analysis_stage1/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topEWK/flatNtuples/winter2023"


#Optional
nCPUS       = 8
runBatch    = True
batchQueue = "workday"
compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               .Define("genTop",      "FCCAnalyses::MCParticle::sel_pdgID(6, true)(Particle)")
               .Define("genW",        "FCCAnalyses::MCParticle::sel_pdgID(24, true)(Particle)")
               .Define("genMuon",     "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
               .Define("genElectron", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
               .Define("n_genTops",      "FCCAnalyses::MCParticle::get_n(genTop)")
               .Define("n_genWs",        "FCCAnalyses::MCParticle::get_n(genW)")
               .Define("n_genMuons",     "FCCAnalyses::MCParticle::get_n(genMuon)")
               .Define("n_genElectrons", "FCCAnalyses::MCParticle::get_n(genElectron)")

               .Define("genTop_px",     "FCCAnalyses::MCParticle::get_px(genTop)")
               .Define("genTop_py",     "FCCAnalyses::MCParticle::get_py(genTop)")
               .Define("genTop_pz",     "FCCAnalyses::MCParticle::get_pz(genTop)")
               .Define("genTop_energy", "FCCAnalyses::MCParticle::get_e(genTop)")
               .Define("genTop_mass",   "FCCAnalyses::MCParticle::get_mass(genTop)")
               .Define("genTop_charge", "FCCAnalyses::MCParticle::get_charge(genTop)")

               .Define("genW_px",     "FCCAnalyses::MCParticle::get_px(genW)")
               .Define("genW_py",     "FCCAnalyses::MCParticle::get_py(genW)")
               .Define("genW_pz",     "FCCAnalyses::MCParticle::get_pz(genW)")
               .Define("genW_energy", "FCCAnalyses::MCParticle::get_e(genW)")
               .Define("genW_mass",   "FCCAnalyses::MCParticle::get_mass(genW)")
               .Define("genW_charge", "FCCAnalyses::MCParticle::get_charge(genW)")

               .Define("genMuon_px",        "FCCAnalyses::MCParticle::get_px(genMuon)")
               .Define("genMuon_py",        "FCCAnalyses::MCParticle::get_py(genMuon)")
               .Define("genMuon_pz",        "FCCAnalyses::MCParticle::get_pz(genMuon)")
               .Define("genMuon_energy",    "FCCAnalyses::MCParticle::get_e(genMuon)")
               .Define("genMuon_mass",      "FCCAnalyses::MCParticle::get_mass(genMuon)")
               .Define("genMuon_charge",    "FCCAnalyses::MCParticle::get_charge(genMuon)")
               .Define("genMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(genMuon,Particle,Particle0)")

               .Define("genElectron_px",        "FCCAnalyses::MCParticle::get_px(genElectron)")
               .Define("genElectron_py",        "FCCAnalyses::MCParticle::get_py(genElectron)")
               .Define("genElectron_pz",        "FCCAnalyses::MCParticle::get_pz(genElectron)")
               .Define("genElectron_energy",    "FCCAnalyses::MCParticle::get_e(genElectron)")
               .Define("genElectron_mass",      "FCCAnalyses::MCParticle::get_mass(genElectron)")
               .Define("genElectron_charge",    "FCCAnalyses::MCParticle::get_charge(genElectron)")
               .Define("genElectron_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(genElectron,Particle,Particle0)") 

               .Alias("Muon0",      "Muon#0.index")
               .Alias("Electron0",  "Electron#0.index")
               .Alias("Photon0",    "Photon#0.index")
               .Define("muons",     "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               .Define("electrons", "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
               .Define("photons",   "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
 
               .Define("n_muons",     "ReconstructedParticle::get_n(muons)")
               .Define("n_electrons", "ReconstructedParticle::get_n(electrons)")
               .Define("n_photons",   "ReconstructedParticle::get_n(photons)")
               .Define("n_jets",      "ReconstructedParticle::get_n(Jet)")

               .Define("muon_px",          "ReconstructedParticle::get_px(muons)")
               .Define("muon_py",          "ReconstructedParticle::get_py(muons)")
               .Define("muon_pz",          "ReconstructedParticle::get_pz(muons)")
               .Define("muon_energy",      "ReconstructedParticle::get_e(muons)")
               .Define("muon_mass",        "ReconstructedParticle::get_mass(muons)")
               .Define("muon_charge",      "ReconstructedParticle::get_charge(muons)")

               .Define("electron_px",          "ReconstructedParticle::get_px(electrons)")
               .Define("electron_py",          "ReconstructedParticle::get_py(electrons)")
               .Define("electron_pz",          "ReconstructedParticle::get_pz(electrons)")
               .Define("electron_energy",      "ReconstructedParticle::get_e(electrons)")
               .Define("electron_mass",        "ReconstructedParticle::get_mass(electrons)")
               .Define("electron_charge",      "ReconstructedParticle::get_charge(electrons)")

               .Define("photon_px",          "ReconstructedParticle::get_px(photons)")
               .Define("photon_py",          "ReconstructedParticle::get_py(photons)")
               .Define("photon_pz",          "ReconstructedParticle::get_pz(photons)")
               .Define("photon_energy",      "ReconstructedParticle::get_e(photons)")
               .Define("photon_mass",        "ReconstructedParticle::get_mass(photons)")
               .Define("photon_charge",      "ReconstructedParticle::get_charge(photons)")

               .Define("jet_px",          "ReconstructedParticle::get_px(Jet)")
               .Define("jet_py",          "ReconstructedParticle::get_py(Jet)")
               .Define("jet_pz",          "ReconstructedParticle::get_pz(Jet)")
               .Define("jet_energy",      "ReconstructedParticle::get_e(Jet)")
               .Define("jet_mass",        "ReconstructedParticle::get_mass(Jet)")
               .Define("jet_charge",      "ReconstructedParticle::get_charge(Jet)")

               .Alias("Jet3","Jet#3.index")
               .Define("jet_btag", "ReconstructedParticle::getJet_btag(Jet3, ParticleIDs, ParticleIDs_0)")
 
        )
        return df2




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTops", "n_genWs", "n_genMuons", "n_genElectrons", 
                 "genTop_px", "genTop_py", "genTop_pz", "genTop_energy", "genTop_mass", "genTop_charge",
                 "genW_px", "genW_py", "genW_pz", "genW_energy", "genW_mass", "genW_charge",
                 "genMuon_px", "genMuon_py", "genMuon_pz", "genMuon_energy", "genMuon_mass", "genMuon_charge", "genMuon_parentPDG",
                 "genElectron_px", "genElectron_py", "genElectron_pz", "genElectron_energy", "genElectron_mass", "genElectron_charge", "genElectron_parentPDG",
                 "n_muons", "n_electrons", "n_photons", "n_jets",
                 "muon_px", "muon_py", "muon_pz", "muon_energy", "muon_mass", "muon_charge",
                 "electron_px", "electron_py", "electron_pz", "electron_energy", "electron_mass", "electron_charge",
                 "photon_px", "photon_py", "photon_pz", "photon_energy", "photon_mass", "photon_charge",
                 "jet_px", "jet_py", "jet_pz", "jet_energy", "jet_mass", "jet_charge", "jet_btag"
                ]
        return branchList
