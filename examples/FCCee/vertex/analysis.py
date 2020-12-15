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
        df2 = (self.df.Range(10)
        #df2 = (self.df
               # number of tracks
               .Define("ntracks","get_nTracks(EFlowTrack_1)")
               .Define("Vertex0","Vertex0(EFlowTrack_1)")
               .Define("Vertex","Vertex(EFlowTrack_1)")
               #.Define("Vertex_z","Vertex(EFlowTrack_1)[2]") 
               #.Define("Vertex_x","Vertex(EFlowTrack_1)[0]")
               #.Define("Vertex_y","Vertex(EFlowTrack_1)[1]")
               #.Define("Vertex_chi2","Vertex(EFlowTrack_1)[3]")
        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "ntracks",
                "Vertex0",
                "Vertex",
                #"Vertex_z",
                #"Vertex_x",
                #"Vertex_y",
                #"Vertex_chi2",

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
