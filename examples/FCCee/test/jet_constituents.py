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

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               #############################################
               ##          Aliases for # in python        ##
               #############################################
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               #.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("Jet0", "Jet#0.index")
               .Define("JetsConstituents", "JetConstituentsUtils::build_constituents(Jet, ReconstructedParticles)")
               .Define("JC_pt", "JetConstituentsUtils::get_pt(JetsConstituents)")
               .Define("JC_Jet0", "JetConstituentsUtils::get_constituents(JetsConstituents, Jet0)")
               .Define("JC_Jet0_pt", "JetConstituentsUtils::get_pt(JC_Jet0)")
                # constituents for one single jet
               #.Define("JC_Jet0c", "JetConstituentsUtils::get_jet_constituents(JetsConstituents, 0)")
               #.Define("JC_Jet0c_pt", "ReconstructedParticle::get_pt(JC_Jet0c)")
              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",
                #'JetsConstituents',
                #'JC_Jet0_pt',
                #'JC_Jet0c_pt'
                ]
        return branchList
