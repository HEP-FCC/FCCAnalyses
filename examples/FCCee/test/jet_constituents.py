#Mandatory: List of processes
processList = {
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
        df2 = (df
               #############################################
               ##          Aliases for # in python        ##
               #############################################
               #.Alias("Jet0", "Jet#0.index")
               .Alias("Jet0", "Jet#3.index")
               .Define("JetsConstituents", "JetConstituentsUtils::build_constituents(Jet, ReconstructedParticles)")
                # constituents for one single jet
               .Define("JC_Jet0", "JetConstituentsUtils::get_constituents(JetsConstituents, Jet0)")
               #.Define("JC_Jet0", "JetConstituentsUtils::get_jet_constituents(JetsConstituents, Jet0)")
               .Define("JC_Jet0_pt", "JetConstituentsUtils::get_pt(JC_Jet0)")
               .Define("JC_Jet0_e", "JetConstituentsUtils::get_e(JC_Jet0)")
               .Define("JC_Jet0_theta", "JetConstituentsUtils::get_theta(JC_Jet0)")
               .Define("JC_Jet0_phi", "JetConstituentsUtils::get_phi(JC_Jet0)")
               .Define("JC_Jet0_pid", "JetConstituentsUtils::get_type(JC_Jet0)")
               .Define("JC_Jet0_charge", "JetConstituentsUtils::get_charge(JC_Jet0)")
              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                'JetsConstituents',
                'JC_Jet0',
                'JC_Jet0_pt', 'JC_Jet0_e', 'JC_Jet0_theta', 'JC_Jet0_phi', 'JC_Jet0_pid', 'JC_Jet0_charge',
                ]
        return branchList
