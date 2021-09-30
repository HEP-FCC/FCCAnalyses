import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = (self.df

               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")
               .Alias("Jet3", "Jet#3.index") #alias for dealing with # in python

               #selecting only final particles (status=1)
               .Define("MC_final", "MCParticle::sel_genStatus(1)(Particle)")

               .Define("MC_px",  "MCParticle::get_px(Particle)")
               .Define("MC_py",  "MCParticle::get_py(Particle)")
               .Define("MC_pz",  "MCParticle::get_pz(Particle)")
               .Define("MC_p",  "MCParticle::get_p(Particle)")
               .Define("MC_e",  "MCParticle::get_e(Particle)")
               .Define("MC_theta",  "MCParticle::get_theta(Particle)")
               .Define("MC_pdg", "MCParticle::get_pdg(Particle)")
               .Define("MC_status", "MCParticle::get_genStatus(Particle)")

               #momenta etc of final particles
               .Define("MC_px_f",  "MCParticle::get_px(MC_final)")
               .Define("MC_py_f",  "MCParticle::get_py(MC_final)")
               .Define("MC_pz_f",  "MCParticle::get_pz(MC_final)")
               .Define("MC_e_f",  "MCParticle::get_e(MC_final)")
               .Define("MC_theta_f",  "MCParticle::get_theta(MC_final)")
               .Define("MC_pdg_f", "MCParticle::get_pdg(MC_final)")

               #get Ks->pi+-
               .Define("K0spipi_indices", "MCParticle::get_indices_ExclusiveDecay(310, {211, -211}, true, true) (Particle, Particle1)")
               .Define("pi0gammagamma_indices", "MCParticle::get_indices_ExclusiveDecay( 111, {22, 22}, true, true) ( Particle, Particle1)" )

               #get parent indices
               #.Define("MC_parent", "MCParticle::get_parentid(Particle0, Particle, Particle0)")
               
               #KT ALGORITHM
               #build psedo-jets with the MC final particles (status = 0)
               .Define("pseudo_jets",        "JetClusteringUtils::set_pseudoJets(MC_px_f, MC_py_f, MC_pz_f, MC_e_f)")

               #run jet clustering with all MC particles. kt_algorithm, R=0.5, exclusive clustering, exactly 2 jets, E-scheme
               .Define("FCCAnalysesJets_kt", "JetClustering::clustering_kt(0.5, 2, 2, 1, 0)(pseudo_jets)")

               #get the jets out of the structure
               .Define("jets_kt",            "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_kt)")

               #get the jet constituents out of the structure
               .Define("jetconstituents_kt", "JetClusteringUtils::get_constituents(FCCAnalysesJets_kt)")

               #get some jet variables
               .Define("jets_kt_e",          "JetClusteringUtils::get_e(jets_kt)")
               .Define("jets_kt_px",         "JetClusteringUtils::get_px(jets_kt)")
               .Define("jets_kt_py",         "JetClusteringUtils::get_py(jets_kt)")
               .Define("jets_kt_pz",         "JetClusteringUtils::get_pz(jets_kt)")
               .Define("jets_kt_flavour", "JetTaggingUtils::get_flavour(jets_kt, Particle)")


               #EE-GENKT ALGORITHM
               #run jet clustering with all reconstructed particles. ee_genkt_algorithm, R=0.5, inclusive clustering, E-scheme 
               .Define("FCCAnalysesJets_ee_genkt","JetClustering::clustering_ee_genkt(0.5, 0, 0, 1, 0, 1)(pseudo_jets)")

               #get the jets out of the struct
               .Define("jets_ee_genkt",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_genkt)")

               #get the jets constituents out of the struct
               .Define("jetconstituents_ee_genkt","JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_genkt)")

               #get some variables
               .Define("jets_ee_genkt_e",         "JetClusteringUtils::get_e(jets_ee_genkt)")
               .Define("jets_ee_genkt_px",        "JetClusteringUtils::get_px(jets_ee_genkt)")
               .Define("jets_ee_genkt_py",        "JetClusteringUtils::get_py(jets_ee_genkt)")
               .Define("jets_ee_genkt_pz",        "JetClusteringUtils::get_pz(jets_ee_genkt)")
               .Define("jets_ee_genkt_flavour",   "JetTaggingUtils::get_flavour(jets_ee_genkt, Particle)")


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

        )

        


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_px",
                "MC_py",
                "MC_pz",
                "MC_p",
                "MC_e",
                "MC_theta",
                "MC_pdg",
                "MC_status",

                "MC_px_f",
                "MC_py_f",
                "MC_pz_f",
                "MC_e_f",
                "MC_theta_f",
                "MC_pdg_f",

                "K0spipi_indices",
                "pi0gammagamma_indices",

                "jets_kt_e",
                "jets_kt_px",
                "jets_kt_py",
                "jets_kt_pz",
                "jets_kt_flavour",
                "jetconstituents_kt",
                
                "jets_ee_genkt_e",
                "jets_ee_genkt_px",
                "jets_ee_genkt_py",
                "jets_ee_genkt_pz",
                "jets_ee_genkt_flavour",
                "jetconstituents_ee_genkt",
                
                "jets_ee_kt_e",
                "jets_ee_kt_px",
                "jets_ee_kt_py",
                "jets_ee_kt_pz",
                "jets_ee_kt_flavour",
                "jetconstituents_ee_kt",
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/higgs/mH-recoil/mumu/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_ZH_ecm240/events_058720051.root
if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs').replace('analysis.py','')+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    print ('outfile  ',outfile)
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
