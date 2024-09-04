
from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB

# list of processes (mandatory)
processList = {
    'p8_ee_WW_ecm240': {'fraction': 0.1},
    'wzp6_ee_mumuH_ecm240': {'fraction': 1},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

# Output directory
outputDir   = f"outputs/FCCee/higgs/mva/preselection/"

# Multithreading: -1 means using all cores
nCPUS       = -1

# Batch settings
#runBatch    = False
#batchQueue  = "longlunch"
#compGroup = "group_u_FCC.local_gen"

doInference = False

class RDFanalysis():

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon", "Muon#0.index")
        df = df.Alias("Electron", "Electron#0.index")

        # all leptons (bare)
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon, ReconstructedParticles)")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron, ReconstructedParticles)")

        # define good muons and electrons
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)")

        # electron veto
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
        df = df.Filter("electrons_no == 0")

        # photon veto
        df = df.Alias("Photon0", "Photon#0.index")
        df = df.Define("photons_all", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
        df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::sel_p(40)(photons_all)")
        df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
        df = df.Filter("photons_no == 0")

        # basic cuts: two OS leptons
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
        df = df.Filter("muons_no == 2 && Sum(muons_q) == 0")

        # build Z resonance
        df = df.Define("zmumu", "ReconstructedParticle::resonanceBuilder(91)(muons)")
        df = df.Define("zmumu_m", "ReconstructedParticle::get_mass(zmumu)[0]")
        df = df.Define("zmumu_p", "ReconstructedParticle::get_p(zmumu)[0]")
        df = df.Define("zmumu_recoil", "ReconstructedParticle::recoilBuilder(240)(zmumu)")
        df = df.Define("zmumu_recoil_m", "ReconstructedParticle::get_mass(zmumu_recoil)[0]")

        # kinematic cuts
        df = df.Filter("zmumu_m > 86 && zmumu_m < 96")
        df = df.Filter("zmumu_p > 20 && zmumu_p < 70")
        df = df.Filter("zmumu_recoil_m < 140 && zmumu_recoil_m > 120")

        df = df.Define("muon1_p", "muons_p[0]")
        df = df.Define("muon2_p", "muons_p[1]")
        df = df.Define("muon1_theta", "muons_theta[0]")
        df = df.Define("muon2_theta", "muons_theta[1]")

        df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
        df = df.Filter("cosTheta_miss < 0.98")

        df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(muons)")
        df = df.Define("acolinearity", "FCCAnalyses::acolinearity(muons)")


        if doInference:
            tmva_helper = TMVAHelperXGB("outputs/FCCee/higgs/mva/bdt_model_example.root", "bdt_model") # read the XGBoost training
            df = tmva_helper.run_inference(df, col_name="mva_score") # by default, makes a new column mva_score

        return df

    # define output branches to be saved
    def output():
        branchList = ["muon1_p", "muon2_p", "muon1_theta", "muon2_theta", "zmumu_p", "zmumu_m", "zmumu_recoil_m", "acoplanarity", "acolinearity", "cosTheta_miss"]
        if doInference:
            branchList.append("mva_score")
        return branchList
