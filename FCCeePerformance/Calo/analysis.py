import os, sys, glob, argparse
from datetime import date
import ROOT

print ("Load cxx analyzers ... ")
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

# does not work without these two lines
_p = ROOT.fcc.ParticleData()
_s = ROOT.selectParticlesPtIso

parser = argparse.ArgumentParser()

#parser.add_argument("-inputFilesRegex", default = '/afs/cern.ch/user/b/brfranco/work/public/Fellow/FCCSW/dummy_releases/201203/output_fullCalo_SimAndDigi_withCluster_noMagneticField_10GeV.root', help = "Input rootfiles (can be a single file or a regex)", type = str)
#parser.add_argument("-inputFilesRegex", default = '/eos/user/b/brfranco/rootfile_storage/200912_pythia/fccsw_output_pythia_ee_Z_ee_*321*.root', help = "Input rootfiles (can be a single file or a regex)", type = str)
parser.add_argument("-inputFiles", default = '/eos/user/b/brfranco/rootfile_storage/201012_pythia/fccsw_output_pythia_ee_Z_ee_*131*.root', help = "Input rootfiles (can be a single file or a regex)", type = str)
parser.add_argument("-outputFolder", default = os.path.join("outputs", date.today().strftime("%y%m%d")), help = "Output folder for the rootfiles", type = str)
parser.add_argument("-storeCellBranches", default = True, help="Whether or not to store cell information", type = bool)
parser.add_argument("-cellBranchName", default = "ECalBarrelPositionedCells", help="Name of the cell branch in the input rootfile. Must have position information!", type = str)
parser.add_argument("-storeClusterBranches", default = True, help="Whether or not to store cluster information", type = bool)
parser.add_argument("-clusterBranchNames", default = ["CaloClusters"], help="Name of the cluster branch in the input rootfile", type = str, nargs = '+')
parser.add_argument("-storeClusterCellsBranches", default = True, help="Whether or not to store cluster cells information", type = bool)
parser.add_argument("-clusterCellsBranchNames", default = ["PositionedCaloClusterCells"], help="Name of the cluster-attached-cells branches in the input rootfile. Order must follow -clusterBranchNames and the cells must have positions attached!", type = str, nargs = '+')
parser.add_argument("-storeGenBranches", default = True, help="Whether or not to store gen information", type = bool)
parser.add_argument("-genBranchName", default = "genParticles", help="Name of the gen particle branch in the input rootfile", type = str)

args = parser.parse_args()


class analysis():

    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)

    def run(self):

        dict_outputBranchName_function = {}

        # cells
        if args.storeCellBranches:
            dict_outputBranchName_function["cell_x"] = "getCaloHit_x(%s)"%args.cellBranchName
            dict_outputBranchName_function["cell_y"] = "getCaloHit_y(%s)"%args.cellBranchName
            dict_outputBranchName_function["cell_z"] = "getCaloHit_z(%s)"%args.cellBranchName
            dict_outputBranchName_function["cell_phi"] = "getCaloHit_phi(%s)"%args.cellBranchName
            dict_outputBranchName_function["cell_theta"] = "getCaloHit_phi(%s)"%args.cellBranchName
            dict_outputBranchName_function["cell_eta"] = "getCaloHit_phi(%s)"%args.cellBranchName
            #dict_outputBranchName_function["cell_position"] = "getCaloHit_positionVector3(%s)"%args.cellBranchName
            dict_outputBranchName_function["cell_energy"] = "getCaloHit_energy(%s)"%args.cellBranchName

        # clusters
        if args.storeClusterBranches:
            for clusterBranchName in args.clusterBranchNames:
                dict_outputBranchName_function["%s_energy"%clusterBranchName] = "getCaloCluster_energy(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_position"%clusterBranchName] = "getCaloCluster_positionVector3(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_firstCell"%clusterBranchName] = "getCaloCluster_firstCell(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_lastCell"%clusterBranchName] = "getCaloCluster_lastCell(%s)"%clusterBranchName

        # cells attached to clusters
        if args.storeClusterCellsBranches:
            for clusterCellsBranchName in args.clusterCellsBranchNames:
                dict_outputBranchName_function["%s_position"%clusterCellsBranchName] = "getCaloHit_positionVector3(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_energy"%clusterCellsBranchName] = "getCaloHit_energy(%s)"%clusterCellsBranchName

        # gen particles
        if args.storeGenBranches:
            dict_outputBranchName_function["genParticle_pid"] = "getMC_pid(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_status"] = "getMC_status(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_p4"] = "getMC_lorentzVector(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_phi"] = "getMC_phi(%s)"%args.genBranchName

        df2 = self.df
        branchList = ROOT.vector('string')()
        for branchName in dict_outputBranchName_function:
            branchList.push_back(branchName)
            df2 = df2.Define(branchName, dict_outputBranchName_function[branchName])

        df2.Snapshot("events", self.outname, branchList)


filelist = glob.glob(args.inputFiles)

fileListRoot = ROOT.vector('string')()
print ("Input files:")
for fileName in filelist:
    fileListRoot.push_back(fileName)
    print ("\t", fileName)
    
if not os.path.isdir(args.outputFolder):
    os.makedirs(args.outputFolder)

outputFile = os.path.join(args.outputFolder, args.inputFiles.split('/')[-1].replace("*", "all"))
ncpus = 8
analysis = analysis(fileListRoot, outputFile, ncpus)
print ("Processing...")
analysis.run()
print (os.path.join(os.environ.get("PWD"), outputFile), " written.")
