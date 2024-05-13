
flavor = "mumu" # mumu, ee

# list of processes (mandatory)
processList_mumu = {
    'p8_ee_ZZ_ecm240':{'fraction': 1},
    'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_mumuH_ecm240':{'fraction': 1},
}

processList_ee = {
    'p8_ee_ZZ_ecm240':{'fraction': 1},
    'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_eeH_ecm240':{'fraction': 1},
}

if flavor == "mumu":
    processList = processList_mumu
else:
    processList = processList_ee

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

# Output directory
outputDir   = f"outputs/FCCee/higgs/mass-xsec/preselection/{flavor}/"

# Multithreading: -1 means using all cores
nCPUS       = -1

# Batch settings
#runBatch    = False
#batchQueue  = "longlunch"
#compGroup = "group_u_FCC.local_gen"

class RDFanalysis():

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        # define some aliases to be used later on
        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon0", "Muon#0.index")

        # get all the leptons from the collection
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")

        # select leptons with momentum > 20 GeV
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
        df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")


        # Basic selection: at least 2 OS muons, one isolated
        df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0")
        df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")


        # now we build the Z resonance based on the available leptons.
        # the function resonanceBuilder_mass_recoil returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV
        # the argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization
        # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
        df = df.Define("zbuilder_result", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
        df = df.Define("zll_muons", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 
        df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
        df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
        df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)") # compute the recoil based on the reconstructed Z
        df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
        df = df.Define("zll_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_muons)") # get the momentum of the 2 muons from the Z resonance

        df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy)")

        return df

    # define output branches to be saved
    def output():
        branchList = ["zll_m", "zll_p", "cosTheta_miss", "zll_recoil_m"]
        return branchList
