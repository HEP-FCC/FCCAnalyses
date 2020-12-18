import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.getMC_px
_fcc2  = ROOT.getRP2MC_p

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)
print ('fccana2  ',_fcc2)
#ROOT.ROOT.EnableThreadSafety()
#ROOT.ROOT.EnableImplicitMT(1)
#ROOT.TTree.SetMaxTreeSize(100000000000)
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

        #df2 = (self.df.Range(10000)
        df2 = (self.df

               .Define("RP_TRK_D0",      "getRP2TRK_D0(ReconstructedParticles, EFlowTrack_1)")    #  d0 and z0 in mm
               .Define("RP_TRK_Z0",      "getRP2TRK_Z0(ReconstructedParticles, EFlowTrack_1)")
               .Define("RP_TRK_omega",   "getRP2TRK_omega(ReconstructedParticles, EFlowTrack_1)")  # rho, in mm-1
               .Define("RP_TRK_phi",     "getRP2TRK_phi(ReconstructedParticles, EFlowTrack_1)")
               .Define("RP_TRK_tanlambda", "getRP2TRK_tanLambda(ReconstructedParticles, EFlowTrack_1)")

               .Define("RP_TRK_D0_cov",      "getRP2TRK_D0_cov(ReconstructedParticles, EFlowTrack_1)")    
               .Define("RP_TRK_Z0_cov",      "getRP2TRK_Z0_cov(ReconstructedParticles, EFlowTrack_1)")
               .Define("RP_TRK_omega_cov",   "getRP2TRK_omega_cov(ReconstructedParticles, EFlowTrack_1)")
               .Define("RP_TRK_phi_cov",     "getRP2TRK_phi_cov(ReconstructedParticles, EFlowTrack_1)")
               .Define("RP_TRK_tanlambda_cov", "getRP2TRK_tanLambda_cov(ReconstructedParticles, EFlowTrack_1)")

               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")

               #.Define('RP_MC_index',    "getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_p',        "getRP2MC_p(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_px',       "getRP2MC_px(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_py',       "getRP2MC_py(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_pz',       "getRP2MC_pz(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_pdg',      "getRP2MC_pdg(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_charge',   "getRP2MC_charge(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_tlv',      "getRP2MC_tlv(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               #.Define('RP_MC_mass',     "getRP2MC_mass(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               #.Define('RP_MC_parentindex', "getRP2MC_parentid(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, Particle0)")

               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "RP_TRK_D0",
                "RP_TRK_Z0",
                "RP_TRK_omega",
                "RP_TRK_phi",
                "RP_TRK_tanlambda",

                "RP_TRK_D0_cov",
                "RP_TRK_Z0_cov",
                "RP_TRK_omega_cov",
                "RP_TRK_phi_cov",
                "RP_TRK_tanlambda_cov",

                "RP_MC_p",
                "RP_MC_px",
                "RP_MC_py",
                "RP_MC_pz",
                "RP_MC_pdg",
                "RP_MC_charge",
                "RP_MC_tlv"
                #"RP_MC_index",
                #"RP_MC_parentindex",

                ]:
            branchList.push_back(branchName)

        opts = ROOT.RDF.RSnapshotOptions()
        opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        opts.fCompressionLevel = 3
        opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python FCCeeAnalyses/Z_Zbb_Flavor/dataframe/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_Ztautau_ecm91/events_012154460.root

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

