
#Mandatory: List of processes
processList = {
    #'p8_ee_ZH_ecm240':{'fraction':0.2, 'chunks':2, 'output':'p8_ee_ZH_ecm240_out'}
    'p8_noBES_ee_H_Hbb_ecm125':{'fraction':0.01, 'chunks':1, 'output':'test_out'}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "."

#Optional
nCPUS       = 8
runBatch    = False
#batchQueue = "longlunch"
#compGroup = "group_u_FCC.local_gen"

#Optional test file
testFile = "/eos/experiment/fcc/ee/tmp/4Lolo/photons_MVA1.root"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        from ROOT import WeaverUtils
        from ROOT import gInterpreter
        from os import getenv
        test_inputs_path = getenv('TEST_INPUT_DATA_DIR', '/eos/experiment/fcc/ee/tutorial/PNet_pi0Gamma/v1')

        gInterpreter.Declare("""
        template <typename T>
        ROOT::VecOps::RVec<ROOT::VecOps::RVec<T> > get_vector(const ROOT::VecOps::RVec<T>& qty) { return ROOT::VecOps::RVec<ROOT::VecOps::RVec<T> >(1, qty); }
        """)
        weaver = WeaverUtils.setup_weaver(test_inputs_path + '/fccee_pi_vs_gamma_v1.onnx',
                                          test_inputs_path + '/preprocess_fccee_pi_vs_gamma_v1.json',
                                          ('recocells_e', 'recocells_theta', 'recocells_phi', 'recocells_radius', 'recocells_layer'))

        df2 = (df
               #.Define("cells_e",      "ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> v; v.push_back(maxEnergyCluster_cells_energy); return v;")
               #.Define("cells_theta",  "ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> v; v.push_back(maxEnergyCluster_cells_theta); return v;")
               #.Define("cells_phi",    "ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> v; v.push_back(maxEnergyCluster_cells_phi); return v;")
               #.Define("cells_radius", "ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> v; v.push_back(maxEnergyCluster_cells_radius); return v;")
               #.Define("cells_layer",  "ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>> v; v.push_back(maxEnergyCluster_cells_layer); return v;")
               .Define("cells_e",      "get_vector(maxEnergyCluster_cells_energy)")
               .Define("cells_theta",  "get_vector(maxEnergyCluster_cells_theta)")
               .Define("cells_phi",    "get_vector(maxEnergyCluster_cells_phi)")
               .Define("cells_radius", "get_vector(maxEnergyCluster_cells_radius)")
               .Define("cells_layer",  "get_vector(maxEnergyCluster_cells_layer)")

               # run inference
               .Define("MVAVec", "WeaverUtils::get_weights(cells_e, cells_theta, cells_phi, cells_radius, cells_layer)")
               #.Define("MVAVec", "WeaverUtils::get_weights(maxEnergyCluster_cells_energy, maxEnergyCluster_cells_theta, maxEnergyCluster_cells_phi, maxEnergyCluster_cells_radius, maxEnergyCluster_cells_layer)")

               # recast output
               .Define("Cluster_isPhoton", "WeaverUtils::get_weight(MVAVec, 0)")
               .Define("Cluster_isPi0", "WeaverUtils::get_weight(MVAVec, 1)")
              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                'Cluster_isPhoton', 'Cluster_isPi0',
                ]
        return branchList
