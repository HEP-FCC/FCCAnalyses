import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

_p = ROOT.edm4hep.ReconstructedParticleData()
_s = ROOT.getRP_px
_t = ROOT.getRP2TRK_D0

print ('recp ',_s)
print ('recp tra',_t)

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
        df2 = (
               self.df.Define("rec_part_px",     "getRP_px_std(ReconstructedParticles)")
               .Define("rec_part_py",     "getRP_py_std(ReconstructedParticles)")
               .Define("rec_part_pz",     "getRP_pz_std(ReconstructedParticles)")
               .Define("rec_part_mass",   "getRP_mass_std(ReconstructedParticles)")
               .Define("rec_part_charge", "getRP_charge_std(ReconstructedParticles)")
               .Define("rec_part_track_D0", "getRP2TRK_D0_std(ReconstructedParticles, EFlowTrack_1)")
               #.Define("rec_part_track_Z0", "getRP2TRK_Z0_std(ReconstructedParticles, EFlowTrack_1)")
               .Define("rec_part_px_VecOps",     "getRP_px(ReconstructedParticles)")
               .Define("rec_part_py_VecOps",     "getRP_py(ReconstructedParticles)")
               .Define("rec_part_pz_VecOps",     "getRP_pz_std(ReconstructedParticles)")
               
            
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
                #"rec_part_track_Z0",
                 "rec_part_px_VecOps",
                "rec_part_py_VecOps",
                "rec_part_pz_VecOps",
                ]:
            branchList.push_back(branchName)
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
