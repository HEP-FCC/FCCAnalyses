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

parser.add_argument("-inputFiles", default = '/eos/user/b/brfranco/rootfile_storage/220618_gamma_flat_1_100_noNoise/fccsw_output_pdgID_22_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root', help = "Input rootfiles (can be a single file or a regex)", type = str)
parser.add_argument("-outputFolder", default = os.path.join("outputs", date.today().strftime("%y%m%d")), help = "Output folder for the rootfiles", type = str)
parser.add_argument("-storeCellBranches", default = True, help="Whether or not to store cell information", type = str2bool)
parser.add_argument("-cellBranchNames", default = ["ECalBarrelPositionedCells"], help="Name of the cell branch in the input rootfile. Must have position information!", type = str)
parser.add_argument("-storeClusterBranches", default = True, help="Whether or not to store cluster information", type = str2bool)
parser.add_argument("-clusterBranchNames", default = ["CaloClusters"], help="Name of the cluster branch in the input rootfile", type = str, nargs = '+')
parser.add_argument("-storeClusterCellsBranches", default = False, help="Whether or not to store cluster cells information", type = str2bool)
parser.add_argument("-clusterCellsBranchNames", default = ["PositionedCaloClusterCells"], help="Name of the cluster-attached-cells branches in the input rootfile. Order must follow -clusterBranchNames and the cells must have positions attached!", type = str, nargs = '+')
parser.add_argument("-storeGenBranches", default = True, help="Whether or not to store gen information", type = str2bool)
parser.add_argument("-genBranchName", default = "genParticles", help="Name of the gen particle branch in the input rootfile", type = str)
parser.add_argument("-storeSimParticleSecondaries", default = False, help="Whether to store the SimParticleSecondaries information", type = str2bool)
parser.add_argument("-simParticleSecondariesNames", default = ["SimParticleSecondaries"],  help = "name of the SimParticleSecondaries branch", type = str, nargs = '+')
parser.add_argument("-useGeometry", default = True, help="Whether or not to load the FCCSW geometry. Used to get the detector segmentation for e.g. the definition of the cell layer index.", type = str2bool)
parser.add_argument("-geometryFile", default = '/afs/cern.ch/user/b/brfranco/work/public/Fellow/FCCSW/test_recipe_April2022/FCCDetectors/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml', help = "Path to the xml geometry file", type = str)
parser.add_argument("-readoutName", default = 'ECalBarrelPhiEta',  help = "Name of the readout to use for the layer/phi/theta bin definition", type = str)
parser.add_argument("-extractHighestEnergyClusterCells", default = False, help = "Use it if you need cells attached to the higest energy cluster, will use the first cluster collection in clusterBranchNames", type = str2bool)
parser.add_argument("-isPi0", default = 0, help = "Weaver training needs a branch in the input tree with the target label: set it to 1 when running on pi0 files, 0 for photon files", type = int)
parser.add_argument("-doWeaverInference", default = False, help = "Apply weaver inference on highest energy cluster cell variables, extractHighestEnergyClusterCells must be set to True", type = str2bool)
parser.add_argument("-weaverFiles", default = [os.path.join("/afs/cern.ch/user/b/brfranco/work/public/Fellow/FCCSW/221123/LAr_scripts/machineLearning/weaver_models_theta_phi/", fileName) for fileName in ["fccee_pi_vs_gamma_simpler_best_epoch_state.onnx", "preprocess.json"]], help = "Path to the '.onnx' (first argument) and '.json' (second argument) coming out of your training", type = str, nargs = '+')

args = parser.parse_args()


class analysis():

    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")

        self.df = ROOT.RDataFrame("events", inputlist)
        if args.useGeometry:
            ROOT.CaloNtupleizer.loadGeometry(args.geometryFile, args.readoutName)

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
                dict_outputBranchName_function["%s_energy"%cellBranchName] = "CaloNtupleizer::getCaloHit_energy(%s)"%cellBranchName
                if args.useGeometry:
                    dict_outputBranchName_function["%s_phiBin"%cellBranchName] = "CaloNtupleizer::getCaloHit_phiBin(%s)"%cellBranchName
                    dict_outputBranchName_function["%s_layer"%cellBranchName] = "CaloNtupleizer::getCaloHit_layer(%s)"%cellBranchName
                    dict_outputBranchName_function["%s_etaBin"%cellBranchName] = "CaloNtupleizer::getCaloHit_etaBin(%s)"%cellBranchName

        # clusters
        if args.storeClusterBranches:
            for clusterBranchName in args.clusterBranchNames:
                dict_outputBranchName_function["%s_x"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_x(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_y"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_y(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_z"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_z(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_phi"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_phi(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_theta"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_theta(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_eta"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_eta(%s)"%clusterBranchName
                dict_outputBranchName_function["%s_energy"%clusterBranchName] = "CaloNtupleizer::getCaloCluster_energy(%s)"%clusterBranchName
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
                dict_outputBranchName_function["%s_eta"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_eta(%s)"%clusterCellsBranchName
                dict_outputBranchName_function["%s_energy"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_energy(%s)"%clusterCellsBranchName
                if args.useGeometry:
                    dict_outputBranchName_function["%s_phiBin"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_phiBin(%s)"%clusterCellsBranchName
                    dict_outputBranchName_function["%s_layer"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_layer(%s)"%clusterCellsBranchName
                    dict_outputBranchName_function["%s_etaBin"%clusterCellsBranchName] = "CaloNtupleizer::getCaloHit_etaBin(%s)"%clusterCellsBranchName

        # SimParticleSecondaries
        if args.storeSimParticleSecondaries:
            for SimParticleSecondariesName in args.simParticleSecondariesNames:
                dict_outputBranchName_function["%s_x"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_x(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_y"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_y(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_z"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_z(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_phi"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_phi(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_theta"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_theta(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_eta"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_eta(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_energy"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_energy(%s)"%SimParticleSecondariesName
                dict_outputBranchName_function["%s_PDG"%SimParticleSecondariesName] = "CaloNtupleizer::getSimParticleSecondaries_PDG(%s)"%SimParticleSecondariesName


        # gen particles
        if args.storeGenBranches:
            dict_outputBranchName_function["genParticle_phi"] = "FCCAnalyses::MCParticle::get_phi(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_theta"] = "FCCAnalyses::MCParticle::get_theta(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_energy"] = "FCCAnalyses::MCParticle::get_e(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_pid"] = "FCCAnalyses::MCParticle::get_pdg(%s)"%args.genBranchName
            dict_outputBranchName_function["genParticle_status"] = "FCCAnalyses::MCParticle::get_genStatus(%s)"%args.genBranchName

        if args.extractHighestEnergyClusterCells:
            clusterBranchName = args.clusterBranchNames[0]
            dict_outputBranchName_function["highestEnergyCluster_index"] = "std::distance({0}.energy.begin(), std::max_element({0}.energy.begin(), {0}.energy.end()))".format(clusterBranchName)
            dict_outputBranchName_function["highestEnergyCluster_isPhoton"] = "%d"%(not args.isPi0)
            dict_outputBranchName_function["highestEnergyCluster_isPi0"] = "%d"%args.isPi0
            dict_outputBranchName_function["highestEnergyCluster_energy"] = "%s_energy[highestEnergyCluster_index]"%clusterBranchName
            dict_outputBranchName_function["highestEnergyCluster_phi"] = "%s_phi[highestEnergyCluster_index]"%clusterBranchName
            dict_outputBranchName_function["highestEnergyCluster_theta"] = "%s_theta[highestEnergyCluster_index]"%clusterBranchName
            dict_outputBranchName_function["highestEnergyCluster_firstCell_index"] = "%s[highestEnergyCluster_index].hits_begin"%clusterBranchName
            dict_outputBranchName_function["highestEnergyCluster_lastCell_index"] = "%s[highestEnergyCluster_index].hits_end"%clusterBranchName
            ROOT.gInterpreter.Declare("""
                template<typename T>
                ROOT::VecOps::RVec<T> myRange(ROOT::VecOps::RVec<T>& vec, std::size_t begin, std::size_t end)
                {
                   ROOT::VecOps::RVec<T> ret;
                   ret.reserve(end - begin);
                   for (auto i = begin; i < end; ++i)
                      ret.push_back(vec[i]);
                   return ret;
                }
                """)

            dict_outputBranchName_function["highestEnergyCluster_cells_transient"] = "myRange(PositionedCaloClusterCells, highestEnergyCluster_firstCell_index, highestEnergyCluster_lastCell_index)"
            dict_outputBranchName_function["highestEnergyCluster_cells_energy"] = "CaloNtupleizer::getCaloHit_energy(highestEnergyCluster_cells_transient)"
            dict_outputBranchName_function["highestEnergyCluster_cells_relative_phi"] =    "CaloNtupleizer::getCaloHit_phi(highestEnergyCluster_cells_transient) - highestEnergyCluster_phi"
            dict_outputBranchName_function["highestEnergyCluster_cells_relative_theta"] =  "CaloNtupleizer::getCaloHit_theta(highestEnergyCluster_cells_transient) - highestEnergyCluster_theta"
            dict_outputBranchName_function["highestEnergyCluster_cells_layer"] = "CaloNtupleizer::getCaloHit_layer(highestEnergyCluster_cells_transient)"
            dict_outputBranchName_function["highestEnergyCluster_cells_n"] =     "highestEnergyCluster_cells_transient.size()"
            dict_outputBranchName_function["highestEnergyCluster_cells_x"] = "myRange(PositionedCaloClusterCells.position.x, highestEnergyCluster_firstCell_index, highestEnergyCluster_lastCell_index)"
            dict_outputBranchName_function["highestEnergyCluster_cells_y"] = "myRange(PositionedCaloClusterCells.position.y, highestEnergyCluster_firstCell_index, highestEnergyCluster_lastCell_index)"
            dict_outputBranchName_function["highestEnergyCluster_cells_radius"] = "sqrt(pow(highestEnergyCluster_cells_x,2)+pow(highestEnergyCluster_cells_y,2))"

        df2 = self.df
        branchList = ROOT.vector('string')()

        for branchName in dict_outputBranchName_function:
            df2 = df2.Define(branchName, dict_outputBranchName_function[branchName])
            if not "transient" in branchName:
                branchList.push_back(branchName)
                print(branchName, dict_outputBranchName_function[branchName])


        if args.doWeaverInference:# placed here because Utils::as_vector can not be stored in the output rootfile but we need e.g. highestEnergyCluster_cells_energy to be defined
            if not args.extractHighestEnergyClusterCells:
                print("You must set extractHighestEnergyClusterCells to True to use WeaverInference")
                sys.exit(1)
            from ROOT import WeaverUtils
            weaver = WeaverUtils.setup_weaver(args.weaverFiles[0], args.weaverFiles[1], ('highestEnergyCluster_cells_energy', 'relative_highestEnergyCluster_cells_phi', 'highestEnergyCluster_cells_relative_theta', 'highestEnergyCluster_cells_layer'))
            df2 = (df2.Define("cells_e", "Utils::as_vector(highestEnergyCluster_cells_energy)")
            .Define("cells_theta", "Utils::as_vector(highestEnergyCluster_cells_relative_theta)")
            .Define("cells_phi", "Utils::as_vector(highestEnergyCluster_cells_relative_phi)")
            .Define("cells_layer", "Utils::as_vector(highestEnergyCluster_cells_layer)")
            .Define("MVAVec", "WeaverUtils::get_weights(cells_e, cells_phi, cells_theta, cells_layer)")
            .Define("highestEnergyCluster_isPhoton_inferred", "WeaverUtils::get_weight(MVAVec, 0)")
            .Define("highestEnergyCluster_isPi0_inferred", "WeaverUtils::get_weight(MVAVec, 1)"))

            branchList.push_back("highestEnergyCluster_isPhoton_inferred")
            branchList.push_back("highestEnergyCluster_isPi0_inferred")
            print("highestEnergyCluster_isPhoton_inferred WeaverUtils::get_weight(MVAVec, 0)")
            print("highestEnergyCluster_isPi0_inferred WeaverUtils::get_weight(MVAVec, 1)")




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
