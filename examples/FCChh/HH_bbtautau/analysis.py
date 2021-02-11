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

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):

        df2 = (self.df
               .Define("selected_jets", "selRP_pT(50.)(Jet)")
               .Define("jet_pT",        "getRP_pt(Jet)")
               .Define("seljet_pT",     "getRP_pt(selected_jets)")
               .Alias("Jet3","Jet#3.index") 
               .Define("JET_btag", "getJet_btag(Jet3, ParticleIDs, ParticleIDs_0)")
               .Define("EVT_nbtag", "getJet_ntags(JET_btag)")

               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "jet_pT",
                "seljet_pT",
                "EVT_nbtag"

                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)



# example call for standalone file
# python examples/FCChh/HH_bbtautau/analysis.py /eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v04/mgp8_pp_tt012j_5f/events_012599692.root 

if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/FCChh').replace('analysis.py','')+'/'
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
