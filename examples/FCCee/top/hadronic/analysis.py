import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyloader

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

               .Alias("Jet3","Jet#3.index")
               .Define("RP_px",          "getRP_px(ReconstructedParticles)")
               .Define("RP_py",          "getRP_py(ReconstructedParticles)")
               .Define("RP_pz",          "getRP_pz(ReconstructedParticles)")               
               .Define("RP_e",           "getRP_e(ReconstructedParticles)")

               #run jet clustering with all reconstructed particles. kt_algorithm, R=0.5, exclusive clustering, exactly 6 jets
               .Define("jets",           "JetClustering::clustering(1, 0.5, 2, 6)(RP_px, RP_py, RP_pz, RP_e)")
               .Define("jets_px",        "JetClustering::getJet_px(jets)")
               .Define("jets_py",        "JetClustering::getJet_py(jets)")
               .Define("jets_pz",        "JetClustering::getJet_pz(jets)")
               
                       
               .Define("JET_btag",       "getJet_btag(Jet3, ParticleIDs, ParticleIDs_0)")
               .Define("EVT_nbtag",      "getJet_ntags(JET_btag)")
               
               .Define('EVT_thrust',     'minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('RP_thrustangle', 'axisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')
               .Define('EVT_thrust_x',   "EVT_thrust.at(0)")
               .Define('EVT_thrust_y',   "EVT_thrust.at(1)")
               .Define('EVT_thrust_z',   "EVT_thrust.at(2)")
               .Define('EVT_thrust_val', "EVT_thrust.at(3)")
               
               .Define('EVT_sphericity',     'minimize_sphericity("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('EVT_sphericity_x',   "EVT_sphericity.at(0)")
               .Define('EVT_sphericity_y',   "EVT_sphericity.at(1)")
               .Define('EVT_sphericity_z',   "EVT_sphericity.at(2)")
               .Define('EVT_sphericity_val', "EVT_sphericity.at(3)")
               .Define('RP_sphericityangle', 'axisCosTheta(EVT_sphericity, RP_px, RP_py, RP_pz)')

               .Define('RP_hemis0_mass',   "getAxisMass(0)(RP_thrustangle, RP_e, RP_px, RP_py, RP_pz)")
               .Define('RP_hemis1_mass',   "getAxisMass(1)(RP_thrustangle, RP_e, RP_px, RP_py, RP_pz)")

               .Define("RP_total_mass",    "getMass(ReconstructedParticles)")

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

