#test files of single photons and pi0 at 10GeV
#testFile='/eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat_smallSampleNotUsedForTraining/output_caloFullSim_10GeV_pdgId_22_noiseFalse.root'
#testFile='/eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat_smallSampleNotUsedForTraining/output_caloFullSim_10GeV_pdgId_111_noiseFalse.root'

#Get the detector geometry
from os import getenv
FCCDETECTORS=getenv('FCCDETECTORS')
geometryFile = FCCDETECTORS+"/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml"
readoutName  = "ECalBarrelPhiEta"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):

        #util function to get a sub-set of a vector
        import ROOT
        ROOT.gInterpreter.Declare("""
        template<typename T>
        ROOT::VecOps::RVec<T> myRange(ROOT::VecOps::RVec<T>& vec, std::size_t begin, std::size_t end){
            ROOT::VecOps::RVec<T> ret;
            ret.reserve(end - begin);
            for (auto i = begin; i < end; ++i)
                ret.push_back(vec[i]);
            return ret;
        }
""")

        #Get the weaver Deep learning
        from ROOT import WeaverUtils
        from os import getenv
        test_inputs_path = getenv('TEST_INPUT_DATA_DIR', '/eos/experiment/fcc/ee/tutorial/PNet_pi0Gamma/v1')
        weaver = WeaverUtils.setup_weaver(test_inputs_path + '/fccee_pi_vs_gamma_v1.onnx',
                                          test_inputs_path + '/preprocess_fccee_pi_vs_gamma_v1.json',
                                          ('recocells_e', 'recocells_theta', 'recocells_phi', 'recocells_radius', 'recocells_layer'))

        df2 = (df
                #Define the index of the highest and lowest energetic cluster in the CaloClusters collection
                .Define("maxEnergyCluster_index", "std::distance(CaloClusters.energy.begin(),std::max_element(CaloClusters.energy.begin(), CaloClusters.energy.end()))")
                .Define("minEnergyCluster_index", "std::distance(CaloClusters.energy.begin(),std::min_element(CaloClusters.energy.begin(), CaloClusters.energy.end()))")

                #Define the number of clusters and their energies
                .Define("clusters_n",      "CaloClusters.energy.size()")
                .Define("clusters_energy", "CaloClusters.energy")

                #For the max energetic cluster, define the index of the first and last cells in the PositionedCaloClusterCells collection
                .Define("maxEnergyCluster_firstCell_index", "CaloClusters[maxEnergyCluster_index].hits_begin")
                .Define("maxEnergyCluster_lastCell_index" , "CaloClusters[maxEnergyCluster_index].hits_end")

                #Using the first and last cells indices, build a sub-collection of cells. Now we have a collection of Cells from the highest energetic cluster
                .Define("maxEnergyCluster_cells", "myRange(PositionedCaloClusterCells, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")

                #uncomment to filter cells that would not belong to the last two layers of the calorimeter (need comment the previous line)
                #.Define("maxEnergyCluster_cellsFull", "myRange(PositionedCaloClusterCells, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
                #.Define("maxEnergyCluster_cells", ROOT.CaloNtupleizer.sel_layers(0, 10),["maxEnergyCluster_cellsFull"])

                #Define energy, phi, theta, layer and n from the sub cell collection
                .Define("maxEnergyCluster_cells_energy", "CaloNtupleizer::getCaloHit_energy(maxEnergyCluster_cells)" )
                .Define("maxEnergyCluster_cells_phi",    "CaloNtupleizer::getCaloHit_phi(maxEnergyCluster_cells)" )
                .Define("maxEnergyCluster_cells_theta",  "CaloNtupleizer::getCaloHit_theta(maxEnergyCluster_cells)" )
                .Define("maxEnergyCluster_cells_layer" , "CaloNtupleizer::getCaloHit_layer(maxEnergyCluster_cells)" )
                .Define("maxEnergyCluster_cells_n" ,     "maxEnergyCluster_cells.size()" )

                #Define the x and y position to compute the radius
                .Define("maxEnergyCluster_cells_x", "myRange(PositionedCaloClusterCells.position.x, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
                .Define("maxEnergyCluster_cells_y", "myRange(PositionedCaloClusterCells.position.y, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
                .Define("maxEnergyCluster_cells_radius", "sqrt(pow(maxEnergyCluster_cells_x,2)+pow(maxEnergyCluster_cells_y,2))")

                #The Deep learning interface needs to use vectors (as we might want to evaluate several clusters in the same event)
                .Define("cells_e",         "Utils::as_vector(maxEnergyCluster_cells_energy)")
                .Define("cells_theta",     "Utils::as_vector(maxEnergyCluster_cells_theta)")
                .Define("cells_phi",       "Utils::as_vector(maxEnergyCluster_cells_phi)")
                .Define("cells_radius",    "Utils::as_vector(maxEnergyCluster_cells_radius)")
                .Define("cells_layer",     "Utils::as_vector(maxEnergyCluster_cells_layer)")

                #Call the inference
                .Define("MVAVec", "WeaverUtils::get_weights(cells_e, cells_theta, cells_phi, cells_radius, cells_layer)")

                #The result is a vector (type photon or pi0) of vector (number of cluster)
                .Define("Cluster_isPhoton", "WeaverUtils::get_weight(MVAVec, 0)")
                .Define("Cluster_isPi0",    "WeaverUtils::get_weight(MVAVec, 1)")

              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "maxEnergyCluster_index",
            "minEnergyCluster_index",
            "clusters_n",
            "clusters_energy",
            "maxEnergyCluster_cells_energy",
            "maxEnergyCluster_cells_phi",
            "maxEnergyCluster_cells_theta",
            "maxEnergyCluster_cells_layer",
            "maxEnergyCluster_cells_n",
            "maxEnergyCluster_cells_radius",
            "Cluster_isPhoton",
            "Cluster_isPi0"
            ]
        return branchList
