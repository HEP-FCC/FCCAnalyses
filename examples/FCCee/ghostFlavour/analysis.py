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
        #df2 = (self.df.Range(0, 10)
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
               
               #pseudo jets defined above, along with Particle, Particle 1 collections are passed to get_ghostflavour
               .Define("ghostFlavour",        "JetTaggingUtils::get_ghostFlavour(3, 0, 2, 2, 1, 0)(Particle, Particle1, pseudo_jets, 0)")

               #the flavour vector can be obtained from the struct by using get_flavour
               .Define("ghostFlavour_flav", "JetTaggingUtils::get_flavour(ghostFlavour)")
                
               #an FCCAnalysesJet struct can be obtain by using get_jets 
               .Define("ghostFlavour_jets", "JetTaggingUtils::get_jets(ghostFlavour)")
               #the pseudojets can then be obtained (as above) using get_pseudojets
               .Define("ghostJets", "JetClusteringUtils::get_pseudoJets(ghostFlavour_jets)")
               #with the kinematics of the pseudojets accessible via their own functions
               .Define("ghostJets_e",          "JetClusteringUtils::get_e(ghostJets)")
               .Define("ghostJets_px",         "JetClusteringUtils::get_px(ghostJets)")
               .Define("ghostJets_py",         "JetClusteringUtils::get_py(ghostJets)")
               .Define("ghostJets_pz",         "JetClusteringUtils::get_pz(ghostJets)")
 
               #the ghostStatus and MCindex vector can likewise be obtained
               .Define("ghostFlavour_MCindex", "JetTaggingUtils::get_MCindex(ghostFlavour)")
               .Define("ghostFlavour_ghostStatus", "JetTaggingUtils::get_ghostStatus(ghostFlavour)")
               
 
 

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
                
                "jets_ee_kt_e",
                "jets_ee_kt_px",
                "jets_ee_kt_py",
                "jets_ee_kt_pz",
                "jets_ee_kt_flavour",
                "jetconstituents_ee_kt",

                "ghostFlavour_flav",
                "ghostFlavour_MCindex",
                "ghostFlavour_ghostStatus",

                "ghostJets_e",
                "ghostJets_px",
                "ghostJets_py",
                "ghostJets_pz",


                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/top/hadronic/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_tt_fullhad_ecm365/events_196309147.root 
if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/FCCee').replace('analysis.py','')+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 2
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()

