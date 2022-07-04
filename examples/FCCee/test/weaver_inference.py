
#Mandatory: List of processes
processList = {
    'p8_ee_ZH_ecm240':{'fraction':0.2, 'chunks':2, 'output':'p8_ee_ZH_ecm240_out'}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
#outputDir   = "outputs/FCCee/flavour/B2Kstee/stage1"

#Optional
nCPUS       = 8
runBatch    = False
#batchQueue = "longlunch"
#compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    _wea  = ROOT.WeaverInterface.get('/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx',
                                     '/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/preprocess.json')

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        print('before')
        df2 = (df
               #############################################
               ##          Aliases for # in python        ##
               #############################################
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               .Define("JetsConstituents", "JetConstituentsUtils::build_constituents(Jet, ReconstructedParticles)")

               .Define("JC_e",          "JetConstituentsUtils::get_e(JetsConstituents)")
               .Define("JC_theta",      "JetConstituentsUtils::get_theta(JetsConstituents)")
               .Define("JC_phi",        "JetConstituentsUtils::get_phi(JetsConstituents)")
               .Define("JC_pid",        "JetConstituentsUtils::get_type(JetsConstituents)")
               .Define("JC_charge",     "JetConstituentsUtils::get_charge(JetsConstituents)")

               .Define("MVAVec", "WeaverInterface::get()(JC_e, JC_theta, JC_phi, JC_pid, JC_charge)")
               #.Define("MVAVec", _wea, ("JC_e", "JC_theta", "JC_phi", "JC_pid", "JC_charge"))

               #.Define("MVAb", "MVAVec.at(0)")
              )
        print('after')
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
