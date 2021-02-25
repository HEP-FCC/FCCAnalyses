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


#
# Example file : /eos/experiment/fcc/ee/examples/p8_ecm91GeV_Zuds_IDEAtrkCov.root
#    ( these events were generated at (0,0,0) i.e. no vertex smearing
#


class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        #ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = (self.df.Range(0,5000)
        #df2 = (self.df

               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","getTK_n(EFlowTrack_1)")

               # Select tracks with d0 and z0 significance < 3 sigmas
		   # note: d0 and z0 are defined w.r.t. (0,0,0)
		   # hence do not use such criteria to select primary tracks
		   # if the events were generated with a vertex distribution
               .Define("SelTracks",  "VertexingUtils::selTracks(0.,3.,0.,3.)( ReconstructedParticles, EFlowTrack_1)")
               .Define("nSeltracks",  "ReconstructedParticle::get_n(SelTracks)")
               # Reconstruct the vertex from these tracks :
               .Define("VertexObject",  "VertexFitterSimple::VertexFitter( 1, SelTracks, EFlowTrack_1 )")
               .Define("Vertex",        "VertexingUtils::get_VertexData( VertexObject )")    # primary vertex, in mm
               
               # Select primary tracks based on the matching to MC
		  # This can be used  to select primary tracks when the
		  # gen-level primary vertex  is not  (0,0,0)
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Define("PrimaryTracks",  "VertexingUtils::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
               .Define("nPrimaryTracks", "ReconstructedParticle::get_n(PrimaryTracks)")

               ## Reconstruct the vertex from these primary tracks :
               .Define("VertexObject_primaryTracks",  "VertexFitterSimple::VertexFitter ( 1, PrimaryTracks, EFlowTrack_1) ")  
               .Define("Vertex_primaryTracks",   "VertexingUtils::get_VertexData( VertexObject_primaryTracks )")   # primary vertex, in mm

               #Run the Acts AMVF vertex finder
               .Define("VertexObject_actsFinder","VertexFinderActs::VertexFinderAMVF( EFlowTrack_1)")
               .Define("Vertex_actsFinder",   "VertexingUtils::get_VertexData( VertexObject_actsFinder )")   # primary vertex, in mm
               .Define("nPrimaryTracks_actsFinder", "VertexingUtils::get_VertexNtrk(VertexObject_actsFinder)")

               #Run the Acts full Billoir vertex fitter
               .Define("VertexObject_actsFitter","VertexFitterActs::VertexFitterFullBilloir(SelTracks, EFlowTrack_1)")
               .Define("Vertex_actsFitter",   "VertexingUtils::get_VertexData( VertexObject_actsFitter )")   # primary vertex, in mm

               .Define("VertexObject_primaryTracks_actsFitter","VertexFitterActs::VertexFitterFullBilloir(PrimaryTracks, EFlowTrack_1)")
               .Define("Vertex_primaryTracks_actsFitter", "VertexingUtils::get_VertexData( VertexObject_primaryTracks_actsFitter )")   # primary vertex, in mm



        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_PrimaryVertex",
                "ntracks",
                "nSeltracks",
                "Vertex",
                "nPrimaryTracks",
                "Vertex_primaryTracks",     # on Zuds: both track selections lead to very similar results for the vertex

                "nPrimaryTracks_actsFinder",
                "Vertex_actsFinder",     # on Zuds: both track selections lead to very similar results for the vertex
                "Vertex_actsFitter",     # on Zuds: both track selections lead to very similar results for the vertex
                "Vertex_primaryTracks_actsFitter",     # on Zuds: both track selections lead to very similar results for the vertex


                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)



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
    ncpus = 1
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
