#Mandatory: List of processes
processList = {
    'p8_ee_ZZ_ecm240':{'chunks':20},#Run the full statistics in 10 jobs in output dir <outputDir>/p8_ee_ZZ_ecm240/chunk<N>.root
    'p8_ee_WW_ecm240':{'chunks':20},#Run the full statistics in 10 jobs in output dir <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
    'p8_ee_ZH_ecm240':{'chunks':20} #Run the full statistics in 10 jobs in output dir <outputDir>/p8_ee_ZH_ecm240/chunk<N>.root
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local dir
outputDir   = "ZH_mumu_recoil_batch/stage1"

#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = True

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

#Optional output directory on eos, if specified files will be copied there once the batch job is done, default is empty
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/"

#Optional type for eos, needed when <outputDirEos> is specified. The default is FCC eos which is eospublic
eosType = "eospublic"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
            # define an alias for muon index collection
            .Alias("Muon0", "Muon#0.index")
            # define the muon collection
            .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            #select muons on pT
            .Define("selected_muons", "ReconstructedParticle::sel_pt(10.)(muons)")
            # create branch with muon transverse momentum
            .Define("selected_muons_pt", "ReconstructedParticle::get_pt(selected_muons)")
            # create branch with muon rapidity
            .Define("selected_muons_y",  "ReconstructedParticle::get_y(selected_muons)")
            # create branch with muon total momentum
            .Define("selected_muons_p",     "ReconstructedParticle::get_p(selected_muons)")
            # create branch with muon energy
            .Define("selected_muons_e",     "ReconstructedParticle::get_e(selected_muons)")
            # find zed candidates from  di-muon resonances
            .Define("zed_leptonic",         "ReconstructedParticle::resonanceBuilder(91)(selected_muons)")
            # create branch with zed mass
            .Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
            # create branch with zed transverse momenta
            .Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
            # calculate recoil of zed_leptonic
            .Define("zed_leptonic_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
            # create branch with recoil mass
            .Define("zed_leptonic_recoil_m","ReconstructedParticle::get_mass(zed_leptonic_recoil)")
            # create branch with leptonic charge
            .Define("zed_leptonic_charge","ReconstructedParticle::get_charge(zed_leptonic)")
            # Filter at least one candidate
            .Filter("zed_leptonic_recoil_m.size()>0")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "selected_muons_pt",
            "selected_muons_y",
            "selected_muons_p",
            "selected_muons_e",
            "zed_leptonic_pt",
            "zed_leptonic_m",
            "zed_leptonic_charge",
            "zed_leptonic_recoil_m"
        ]
        return branchList
