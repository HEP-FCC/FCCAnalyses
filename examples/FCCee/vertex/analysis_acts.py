import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
#ROOT.gSystem.Load("libActsCore")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)


#
# Example file : /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_Zuds_ecm91/events_199980034.root
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
        df2 = (self.df.Range(0,10000)
        #df2 = (self.df

               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               #.Define("ntracks","Vertexing::get_nTracks(EFlowTrack_1)")
               .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

               # Select tracks with d0 and z0 significance < 3 sigmas
		   # note: d0 and z0 are defined w.r.t. (0,0,0)
		   # hence do not use such criteria to select primary tracks
		   # if the events were generated with a vertex distribution
               .Define("VertexObject","VertexingACTS::VertexFinder( EFlowTrack_1)")
               .Define("Vertex",   "VertexingUtils::get_VertexData( VertexObject )")   # primary vertex, in mm

               #.Define("nSeltracks",  "getRP_n(SelTracks)")
               # Reconstruct the vertex from these tracks :
               #.Define("Vertex",  "Vertexing::VertexFitter( 1, SelTracks, EFlowTrack_1 )")	# primary vertex, in mm

               # Select primary tracks based on the matching to MC
		  # This can be used  to select primary tracks when the
		  # gen-level primary vertex  is not  (0,0,0)
               #.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               #.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               #.Define("PrimaryTracks",  "Vertexing::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
               #.Define("nPrimaryTracks", "getRP_n(PrimaryTracks)")
               ## Reconstruct the vertex from these primary tracks :
               #.Define("Vertex_primaryTracks",  "Vertexing::VertexFitter ( 1, PrimaryTracks, EFlowTrack_1) ")   # primary vertex, in mm

        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_PrimaryVertex",
                "ntracks",
                #"nSeltracks",
                "Vertex",
                #"nPrimaryTracks",
                #"Vertex_primaryTracks"     # on Zuds: both track selections lead to very similar results for the vertex

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
