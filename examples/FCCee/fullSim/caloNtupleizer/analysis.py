import os, sys, glob, argparse
from datetime import date
import ROOT

print ("Load cxx analyzers ... ")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

_fcc  = ROOT.dummyLoader

parser = argparse.ArgumentParser()

parser.add_argument("-inputFiles", default = '/afs/cern.ch/user/b/brfranco/work/public/Fellow/FCCSW/key4hep_trial3/FCCSW/Examples/options/output_fullCalo_SimAndDigi_withCluster_MagneticField_False_pMin_10000_MeV_ThetaMinMax_45_135_pdgId_11_pythiaFalse.root', help = "Input rootfiles (can be a single file or a regex)", type = str)
parser.add_argument("-outputFolder", default = os.path.join("outputs", date.today().strftime("%y%m%d")), help = "Output folder for the rootfiles", type = str)
parser.add_argument("-storeCellBranches", default = True, help="Whether or not to store cell information", type = str2bool)
parser.add_argument("-cellBranchNames", default = ["ECalBarrelPositionedCells"], help="Name of the cell branch in the input rootfile. Must have position information!", type = str)
parser.add_argument("-storeClusterBranches", default = False, help="Whether or not to store cluster information", type = str2bool)
parser.add_argument("-clusterBranchNames", default = ["CaloClusters"], help="Name of the cluster branch in the input rootfile", type = str, nargs = '+')
parser.add_argument("-storeClusterCellsBranches", default = False, help="Whether or not to store cluster cells information", type = str2bool)
parser.add_argument("-clusterCellsBranchNames", default = ["PositionedCaloClusterCells"], help="Name of the cluster-attached-cells branches in the input rootfile. Order must follow -clusterBranchNames and the cells must have positions attached!", type = str, nargs = '+')
parser.add_argument("-storeGenBranches", default = True, help="Whether or not to store gen information", type = str2bool)
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
            for cellBranchName in args.cellBranchNames:
                dict_outputBranchName_function["%s_x"%cellBranchName] = "CaloNtupleizer::getCaloHit_x(%s)"%cellBranchName
                dict_outputBranchName_function["%s_y"%cellBranchName] = "CaloNtupleizer::getCaloHit_y(%s)"%cellBranchName
                dict_outputBranchName_function["%s_z"%cellBranchName] = "CaloNtupleizer::getCaloHit_z(%s)"%cellBranchName
                dict_outputBranchName_function["%s_phi"%cellBranchName] = "CaloNtupleizer::getCaloHit_phi(%s)"%cellBranchName
                dict_outputBranchName_function["%s_theta"%cellBranchName] = "CaloNtupleizer::getCaloHit_theta(%s)"%cellBranchName
                dict_outputBranchName_function["%s_eta"%cellBranchName] = "CaloNtupleizer::getCaloHit_eta(%s)"%cellBranchName
                #dict_outputBranchName_function["%s_position"%cellBranchName] = "CaloNtupleizer::getCaloHit_positionVector3(%s)"%cellBranchName
                dict_outputBranchName_function["%s_energy"%cellBranchName] = "CaloNtupleizer::getCaloHit_energy(%s)"%cellBranchName

        # clusters
        if args.storeClusterBranches:
            for clusterBranchName in args.clusterBranchNames:
                dict_outputBranchName_function["%s_x"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_x(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_y"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_y(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_z"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_z(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_phi"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_phi(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_theta"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_theta(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_energy"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_energy(%s)"%clusterBranchName
                #dict_outputBranchName_function["%s_position"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_positionVector3(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_firstCell"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_firstCell(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_lastCell"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_lastCell(%s)"%clusterBranchName

        # cells attached to clusters
        if args.storeClusterCellsBranches:
            for clusterCellsBranchName in args.clusterCellsBranchNames:
                dict_outputBranchName_function["%s_x"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_x(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_y"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_y(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_z"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_z(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_phi"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_phi(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_theta"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_theta(%s)"%clusterCellsBranchName
                #dict_outputBranchName_function["%s_position"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_positionVector3(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_energy"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_energy(%s)"%clusterCellsBranchName

        # gen particles
        if args.storeGenBranches:
            dict_outputBranchName_function["genParticle_phi"] = "MCParticle::get_phi(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_theta"] = "MCParticle::get_theta(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_energy"] = "MCParticle::get_e(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_pid"] = "MCParticle::get_pdg(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_status"] = "MCParticle::get_genStatus(%s)"%args.genBranchName

        df2 = self.df
        branchList = ROOT.vector('string')()


        for branchName in dict_outputBranchName_function:
            branchList.push_back(branchName)
            print(branchName, dict_outputBranchName_function[branchName])
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
