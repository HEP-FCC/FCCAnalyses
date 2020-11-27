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
        # select isolated muons with pt > 10 GeV
        df2 = (self.df
               .Define("cell_phi",     "getCalo_phi(ECalBarrelPositions)") 
               .Define("cell_theta",   "getCalo_theta(ECalBarrelPositions)") 

                     )

        


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "cell_phi",
                "cell_theta",
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call
# python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/p8_ee_ZZ_ecm240/events_058759855.root
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
        
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+sys.argv[1].split('/')[-1]
    ncpus = 0
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()
