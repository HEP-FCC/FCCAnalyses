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
        df2 = (self.df
               .Define("cell_phi",     "getCaloHit_phi(ECalBarrelPositions)")
               .Define("cell_theta",   "getCaloHit_theta(ECalBarrelPositions)")
               .Define("cell_energy",   "getCaloHit_energy(ECalBarrelPositions)")
               .Define("cell_vec",   "getCaloHit_vector(ECalBarrelPositions)")
               .Define("cluster_energy",   "getCaloCluster_energy(CaloClusters)")
                     )

        


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "cell_phi",
                "cell_theta",
                "cell_energy",
                "cell_vec",
                "cluster_energy",
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call
# python FCCeePerformance/Calo/analysis.py /eos/experiment/fcc/ee/simulation/calorimeter/dummy/fccsw_output_pdgID_22_pMin_50000_pMax_50000_thetaMin_90_thetaMax_90_jobid_20.root
if __name__ == "__main__":

    if len(sys.argv) == 1:
        print ("usage:")
        print ("python ", sys.argv[0], " file.root")
        print ("python ", sys.argv[0], " \"dir/*.root\"")
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
    outFile = outDir+sys.argv[1].split('/')[-1]
    outFile = outFile.replace("*", "all")
    ncpus = 8
    analysis = analysis(fileListRoot, outFile, ncpus)
    analysis.run()
    print (outFile, " written.")
