
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

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        from ROOT import JetFlavourUtils
        weaver = JetFlavourUtils.setup_weaver('/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx',
                                              '/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/preprocess.json',
                                              ('pfcand_e', 'pfcand_theta', 'pfcand_phi', 'pfcand_pid', 'pfcand_charge'))

        df2 = (df
               #############################################
               ##          Aliases for # in python        ##
               #############################################
               .Define("JetsConstituents", "JetConstituentsUtils::build_constituents(Jet, ReconstructedParticles)")

               .Define("JC_e",          "JetConstituentsUtils::get_e(JetsConstituents)")
               .Define("JC_theta",      "JetConstituentsUtils::get_theta(JetsConstituents)")
               .Define("JC_phi",        "JetConstituentsUtils::get_phi(JetsConstituents)")
               .Define("JC_pid",        "JetConstituentsUtils::get_type(JetsConstituents)")
               .Define("JC_charge",     "JetConstituentsUtils::get_charge(JetsConstituents)")

               .Define("MVAVec", "JetFlavourUtils::get_weights(JC_e, JC_theta, JC_phi, JC_pid, JC_charge)")
               #.Define("MVAVec", weaver, ("JC_e", "JC_theta", "JC_phi", "JC_pid", "JC_charge"))

               #.Define("MVAb", "MVAVec.at(0)")
              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                'JetsConstituents',
                'MVAVec',
                #'MVAb',
                ]
        return branchList
