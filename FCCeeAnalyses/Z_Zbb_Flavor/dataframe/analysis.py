import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

_p = ROOT.edm4hep.ReconstructedParticleData()
_s = ROOT.get_p
print (_s)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print(inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = (
               self.df.Define("rec_part_px",     "get_px_std(ReconstructedParticles)")
               .Define("rec_part_py",     "get_py_std(ReconstructedParticles)")
               .Define("rec_part_pz",     "get_pz_std(ReconstructedParticles)")
               .Define("rec_part_mass",   "get_mass_std(ReconstructedParticles)")
               .Define("rec_part_charge", "get_charge_std(ReconstructedParticles)")
               .Define("rec_part_track_D0", "get_D0_std(ReconstructedParticles, EFlowTrack_1)")
               .Define("rec_part_track_Z0", "get_Z0_std(ReconstructedParticles, EFlowTrack_1)")
               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "rec_part_px",
                "rec_part_py",
                "rec_part_pz",
                "rec_part_mass",
                "rec_part_charge",
                "rec_part_track_D0",
                "rec_part_track_Z0"
                ]:
            branchList.push_back(branchName)
        print (branchList)
        print (type(branchList))
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
