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
               .Alias("Particle1", "Particle#1.index")

               .Define("MC_status1",    "FCCAnalyses::MCParticle::sel_genStatus(1)(Particle)")
               .Define("MC_px",         "FCCAnalyses::MCParticle::get_px(MC_status1)")
               .Define("MC_py",         "FCCAnalyses::MCParticle::get_py(MC_status1)")
               .Define("MC_pz",         "FCCAnalyses::MCParticle::get_pz(MC_status1)")
               .Define("MC_pdg",        "FCCAnalyses::MCParticle::get_pdg(MC_status1)")
               .Define("MC_charge",     "FCCAnalyses::MCParticle::get_charge(MC_status1)")
               .Define("MC_mass",       "FCCAnalyses::MCParticle::get_mass(MC_status1)")
               .Define("MC_e",          "FCCAnalyses::MCParticle::get_e(MC_status1)")
               .Define("MC_theta",      "FCCAnalyses::MCParticle::get_theta(MC_status1)")
               .Define("MC_phi",        "FCCAnalyses::MCParticle::get_phi(MC_status1)")
               .Define("MC_isZbb",      "FCCAnalyses::MCParticle::get_decay(23,5,false)(Particle,Particle1)")
               .Define("MC_isZcc",      "FCCAnalyses::MCParticle::get_decay(23,4,false)(Particle,Particle1)")
               .Define("MC_isZqq",      "FCCAnalyses::MCParticle::get_decay(23,3,true)(Particle,Particle1)")
               .Define("MC_isHgg",      "FCCAnalyses::MCParticle::get_decay(25,21,false)(Particle,Particle1)")

               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_px","MC_py","MC_pz",
                #"MC_p",
                "MC_pdg","MC_charge","MC_mass","MC_e","MC_phi","MC_theta",
                "MC_isZbb","MC_isZcc","MC_isZqq","MC_isHgg",
                #"MC_status","MC_vertex_x","MC_vertex_y","MC_vertex_z",

                #"RP_p",
                #"RP_px",
                #"RP_py",
                #"RP_pz",
                #"RP_charge",
                #"RP_mass",

                #"RP_TRK_D0",
                #"RP_TRK_Z0",

                #"event_thrust_x",
                #"event_thrust_y",
                #"event_thrust_z",
                #"event_thrust_val",
                #"event_thrust",
                #"event_hemis_0",
                #"event_hemis_1",
                #"RP_MC_p",
                #"RP_MC_px",
                #"RP_MC_py",
                #"RP_MC_pz",
                #"RP_MC_pdg","RP_MC_charge","RP_MC_index","RP_MC_parentindex",



                ]:
            branchList.push_back(branchName)

        opts = ROOT.RDF.RSnapshotOptions()
        opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        opts.fCompressionLevel = 3
        opts.fAutoFlush = -1024*1024*branchList.size()
        df2.Snapshot("events", self.outname, branchList, opts)

# example call for standalone file
# python FCCeeAnalyses/eeH/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_H_Hcc_ecm125/events_108949551.root

if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
