import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libawkward")
ROOT.gSystem.Load("libawkward-cpu-kernels")
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
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):

        df2 = (self.df
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")


               .Define("MC_p",    "FCCAnalyses::MCParticle::get_p(Particle)")
               .Define("MC_theta","FCCAnalyses::MCParticle::get_theta(Particle)")
               .Define("MC_charge","FCCAnalyses::MCParticle::get_charge(Particle)")
               .Define("MC_phi","FCCAnalyses::MCParticle::get_phi(Particle)")

               .Define("RP_p",    "ReconstructedParticle::get_p(ReconstructedParticles)")
               .Define("RP_theta","ReconstructedParticle::get_theta(ReconstructedParticles)")
               .Define("RP_charge","ReconstructedParticle::get_charge(ReconstructedParticles)")
               .Define("RP_phi","ReconstructedParticle::get_phi(ReconstructedParticles)")


               #Run the Acts AMVF vertex finder
               #.Define("VertexObject_actsFinder"  ,"VertexFinderActs::VertexFinderAMVF( EFlowTrack_1)")
               #.Define("NVertex_actsFinder"       ,"VertexingUtils::get_Nvertex(VertexObject_actsFinder)")
               #.Define("FCCAnaVertex_actsFinder"  ,"myUtils::sel_PV(true)(VertexObject_actsFinder)")
               #.Define("RecoInd_actsFinder"       ,"VertexingUtils::get_VertexRecoInd(FCCAnaVertex_actsFinder)")
               #.Define("Vertex_actsFinder"       ,"VertexingUtils::get_VertexData( FCCAnaVertex_actsFinder)")

               #MC Vertex
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
               .Define("MC_Vertex_x",    "myUtils::get_MCVertex_x(MCVertexObject)")
               .Define("MC_Vertex_y",    "myUtils::get_MCVertex_y(MCVertexObject)")
               .Define("MC_Vertex_z",    "myUtils::get_MCVertex_z(MCVertexObject)")
               .Define("MC_Vertex_ind",  "myUtils::get_MCindMCVertex(MCVertexObject)")
               .Define("MC_Vertex_ntrk", "myUtils::get_NTracksMCVertex(MCVertexObject)")
               .Define("MC_Vertex_n",    "int(MC_Vertex_x.size())")

               #Reco Vertex
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")
               .Define("Vertex_x",     "myUtils::get_Vertex_x(VertexObject)")
               .Define("Vertex_y",     "myUtils::get_Vertex_y(VertexObject)")
               .Define("Vertex_z",     "myUtils::get_Vertex_z(VertexObject)")
               .Define("Vertex_xErr",  "myUtils::get_Vertex_xErr(VertexObject)")
               .Define("Vertex_yErr",  "myUtils::get_Vertex_yErr(VertexObject)")
               .Define("Vertex_zErr",  "myUtils::get_Vertex_zErr(VertexObject)")

               .Define("Vertex_chi2",  "myUtils::get_Vertex_chi2(VertexObject)")
               #.Define("Vertex_mcind", "myUtils::get_Vertex_indMC(VertexObject, MCVertexObject)")
               .Define("Vertex_mcind", "myUtils::get_Vertex_indMC(VertexObject)")
               .Define("Vertex_ind",   "myUtils::get_Vertex_ind(VertexObject)")
               .Define("Vertex_isPV",  "myUtils::get_Vertex_isPV(VertexObject)")
               .Define("Vertex_ntrk",  "myUtils::get_Vertex_ntracks(VertexObject)")
               .Define("Vertex_n",     "int(Vertex_x.size())")

               .Define("Vertex_d2PV",  "myUtils::get_Vertex_d2PV(VertexObject,-1)")
               .Define("Vertex_d2PVx", "myUtils::get_Vertex_d2PV(VertexObject,0)")
               .Define("Vertex_d2PVy", "myUtils::get_Vertex_d2PV(VertexObject,1)")
               .Define("Vertex_d2PVz", "myUtils::get_Vertex_d2PV(VertexObject,2)")

               .Define("Vertex_d2PVErr", "myUtils::get_Vertex_d2PVError(VertexObject,-1)")
               .Define("Vertex_d2PVxErr","myUtils::get_Vertex_d2PVError(VertexObject,0)")
               .Define("Vertex_d2PVyErr","myUtils::get_Vertex_d2PVError(VertexObject,1)")
               .Define("Vertex_d2PVzErr","myUtils::get_Vertex_d2PVError(VertexObject,2)")

               .Define("Vertex_d2PVSig",  "Vertex_d2PV/Vertex_d2PVErr")
               .Define("Vertex_d2PVxSig", "Vertex_d2PVx/Vertex_d2PVxErr")
               .Define("Vertex_d2PVySig", "Vertex_d2PVy/Vertex_d2PVyErr")
               .Define("Vertex_d2PVzSig", "Vertex_d2PVz/Vertex_d2PVzErr")

               .Define("Vertex_d2MC",   "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,-1)")
               .Define("Vertex_d2MCx",  "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,0)")
               .Define("Vertex_d2MCy",  "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,1)")
               .Define("Vertex_d2MCz",  "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,2)")




           )
        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_p",
                "MC_theta",
                "MC_charge",
                "MC_phi",

                "MC_Vertex_x",
                "MC_Vertex_y",
                "MC_Vertex_z",
                "MC_Vertex_ind",
                "MC_Vertex_n",
                "MC_Vertex_ntrk",

                "RP_p",
                "RP_theta",
                "RP_charge",
                "RP_phi",

                "Vertex_x",
                "Vertex_y",
                "Vertex_z",
                "Vertex_xErr",
                "Vertex_yErr",
                "Vertex_zErr",

                "Vertex_chi2",
                "Vertex_mcind",
                "Vertex_ind",
                "Vertex_isPV",
                "Vertex_ntrk",
                "Vertex_n",

                "Vertex_d2PV",
                "Vertex_d2PVx",
                "Vertex_d2PVy",
                "Vertex_d2PVz",

                "Vertex_d2MC",
                "Vertex_d2MCx",
                "Vertex_d2MCy",
                "Vertex_d2MCz",

                "Vertex_d2PVErr",
                "Vertex_d2PVxErr",
                "Vertex_d2PVyErr",
                "Vertex_d2PVzErr",

                "Vertex_d2PVSig",
                "Vertex_d2PVxSig",
                "Vertex_d2PVySig",
                "Vertex_d2PVzSig",

                ]:
            branchList.push_back(branchName)

        #opts = ROOT.RDF.RSnapshotOptions()
        #opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        #opts.fCompressionLevel = 3
        #opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file

# python examples/FCCee/vertex_perf/analysis.py  /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91/events_021902791.root flat_ee_Zbb_vertexPerf.root
# python examples/FCCee/vertex_perf/analysis.py  "/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91/events_021*.root" flat_ee_Zbb_VertexPerf.root

if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        print ("python ",sys.argv[0]," dir/*.root")
        sys.exit(3)


    import glob
    filelist = glob.glob(sys.argv[1])

    print ("Create dataframe object from ", )
    fileListRoot = ROOT.vector('string')()
    for fileName in filelist:
        fileListRoot.push_back(fileName)
        print (fileName, " ",)
        print (" ...")

    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/').replace('analysis_Bc2TauNu.py','')+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+sys.argv[1].split('/')[-1]
    ncpus = 6
    if len(sys.argv)==3:outfile=sys.argv[2]
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    #tf = ROOT.TFile(infile)
    #entries = tf.events.GetEntries()
    #p = ROOT.TParameter(int)( "eventsProcessed", entries)
    #outf=ROOT.TFile(outfile,"UPDATE")
    #p.Write()
