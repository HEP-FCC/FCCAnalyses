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
               # define an alias for muon index collection
               .Alias("Electron0", "Electron#0.index")
               # define the muon collection
               .Define("electrons",  "getRP(Electron0, ReconstructedParticles)")
               #select muons on pT
               .Define("selected_electrons", "selRP_pT(10.)(electrons)")
               # create branch with muon transverse momentum
               .Define("selected_electrons_pt", "getRP_pt(selected_electrons)") 
               # create branch with muon rapidity
               .Define("selected_electrons_y",  "getRP_y(selected_electrons)") 
               # create branch with muon total momentum
               .Define("selected_electrons_p",     "getRP_p(selected_electrons)")
               # create branch with muon energy 
               .Define("selected_electrons_e",     "getRP_e(selected_electrons)")
               # find zed candidates from  di-muon resonances  
               .Define("zed_leptonic",         "ResonanceBuilder(23, 91)(selected_electrons)")
               # write branch with zed mass
               .Define("zed_leptonic_m",       "getRP_mass(zed_leptonic)")
               # write branch with zed transverse momenta
               .Define("zed_leptonic_pt",      "getRP_pt(zed_leptonic)")
               # calculate recoil of zed_leptonic
               .Define("zed_leptonic_recoil",  "recoil(240)(zed_leptonic)")
               # write branch with recoil mass
               .Define("zed_leptonic_recoil_m","getRP_mass(zed_leptonic_recoil)") 

        )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "selected_electrons_pt",
                "selected_electrons_y",
                "selected_electrons_p",
                "selected_electrons_e",
                "zed_leptonic_pt",
                "zed_leptonic_m",
                "zed_leptonic_recoil_m"
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python FCCeeAnalyses/higgs/mH-recoil/ee/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_ZH_ecm240/events_058720051.root
if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/FCCee').replace('analysis.py','')+'/'
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
