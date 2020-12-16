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

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

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
        df2 = (self.df.Range(10000)
        #df2 = (self.df
               # number of tracks
               .Define("ntracks","get_nTracks(EFlowTrack_1)")
               # Select tracks with d0 and z0 significance < 3 sigmas
               .Define("SelTracks","selTracks(0.,3.,0.,3.)( ReconstructedParticles, EFlowTrack_1)")
               .Define("nSeltracks",  "getRP_n(SelTracks)")
               # Reconstruct the vertex from these tracks :
               .Define("Vertex",  "VertexFB( 1, SelTracks, EFlowTrack_1 )")	# primary vertex
               #
               # Select primary tracks based on the matching to MC
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Define("PrimaryTracks",  "SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)" )
               .Define("nPrimaryTracks", "getRP_n(PrimaryTracks)")
               # Reconstruct the vertex from these primary tracks :
               .Define("Vertex_primaryTracks",  "VertexFB ( 1, PrimaryTracks, EFlowTrack_1) ")

        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "ntracks",
                "nSeltracks",
                "Vertex",
                "nPrimaryTracks",
                "Vertex_primaryTracks"     # on Zuds: actually very similar to the vertex from the "selected" tracks

                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/p8_ee_ZZ_ecm240/events_058759855.root
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
