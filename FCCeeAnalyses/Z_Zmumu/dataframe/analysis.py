import sys
import ROOT

print ("Load cxx analyzers ... ")
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

_p = ROOT.fcc.ParticleData()
_s = ROOT.selectParticlesPtIso
print (_s)

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
        # select isolated muons with pt > 5 GeV
        df2 = (self.df.Define("selected_muons",  "selectParticlesPtIso(5, 0.4)(muons, muonITags)") 
                     # create branch with muon transverse momentum
                     .Define("selected_muons_pt",    "get_pt(selected_muons)") 
                     # create branch with muon rapidity
                     .Define("selected_muons_y",     "get_y(selected_muons)") 
                     # create branch with muon total momentum
                     .Define("selected_muons_p",     "get_p(selected_muons)")
                      # create branch with muon energy 
                     .Define("selected_muons_e",     "get_e(selected_muons)")
                      # create branch with event weights (just a renaming operation)
                     .Define("weight",               "id_float(mcEventWeights)")
                      # find zed candidates from  di-muon resonances  
                     .Define("zed_leptonic",         "ResonanceBuilder(23, 91)(selected_muons)")
                      # write branch with zed mass
                     .Define("zed_leptonic_m",       "get_mass(zed_leptonic)")
                      # write branch with zed transverse momenta
                     .Define("zed_leptonic_pt",      "get_pt(zed_leptonic)")
                     )

        


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "selected_muons_pt",
                "selected_muons_y",
                "selected_muons_p",
                "selected_muons_e",
                "zed_leptonic_pt",
                "zed_leptonic_m",
                "weight",
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
