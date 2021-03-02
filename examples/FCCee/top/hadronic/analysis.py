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
        #df2 = (self.df.Range(10)
               #alias for dealing with # in python 
               .Alias("Jet3","Jet#3.index")
               #define the RP px, py, pz and e
               .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
               .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
               .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")               
               .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")

               #build pseudo jets with the RP
               .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

               #run jet clustering with all reconstructed particles. kt_algorithm, R=0.5, exclusive clustering, exactly 6 jets
               .Define("FCCAnalysesJets", "JetClustering::clustering_kt(1, 0.5, 2, 6)(pseudo_jets)")
               #get the jets out of the struct
               .Define("jets",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets)")
               #get the jets constituents out of the struct
               .Define("jetconstituents","JetClusteringUtils::get_constituents(FCCAnalysesJets)")
               #get some variables
               .Define("jets_px",        "JetClusteringUtils::get_px(jets)")
               .Define("jets_py",        "JetClusteringUtils::get_py(jets)")
               .Define("jets_pz",        "JetClusteringUtils::get_pz(jets)")
               
                       
               .Define("JET_btag",       "ReconstructedParticle::getJet_btag(Jet3, ParticleIDs, ParticleIDs_0)")
               .Define("EVT_nbtag",      "ReconstructedParticle::getJet_ntags(JET_btag)")
               
               .Define('EVT_thrust',     'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('RP_thrustangle', 'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')
               .Define('EVT_thrust_x',   "EVT_thrust.at(0)")
               .Define('EVT_thrust_y',   "EVT_thrust.at(1)")
               .Define('EVT_thrust_z',   "EVT_thrust.at(2)")
               .Define('EVT_thrust_val', "EVT_thrust.at(3)")
               
               .Define('EVT_sphericity',     'Algorithms::minimize_sphericity("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('EVT_sphericity_x',   "EVT_sphericity.at(0)")
               .Define('EVT_sphericity_y',   "EVT_sphericity.at(1)")
               .Define('EVT_sphericity_z',   "EVT_sphericity.at(2)")
               .Define('EVT_sphericity_val', "EVT_sphericity.at(3)")
               .Define('RP_sphericityangle', 'Algorithms::getAxisCosTheta(EVT_sphericity, RP_px, RP_py, RP_pz)')

               .Define('RP_hemis0_mass',   "Algorithms::getAxisMass(0)(RP_thrustangle, RP_e, RP_px, RP_py, RP_pz)")
               .Define('RP_hemis1_mass',   "Algorithms::getAxisMass(1)(RP_thrustangle, RP_e, RP_px, RP_py, RP_pz)")

               .Define("RP_total_mass",    "Algorithms::getMass(ReconstructedParticles)")

        )

        


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [

                "JET_btag",
                "EVT_nbtag",

                "EVT_thrust_x",
                "EVT_thrust_y",
                "EVT_thrust_z",
                "EVT_thrust_val",
              
                "EVT_sphericity_x",
                "EVT_sphericity_y",
                "EVT_sphericity_z",
                "EVT_sphericity_val",

                "RP_thrustangle",
                "RP_sphericityangle",

                "RP_hemis0_mass",
                "RP_hemis1_mass",
                "RP_total_mass",

                "jets_px",
                "jets_py",
                "jets_pz",
                "jetconstituents",
                "RP_px"
               
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

