testFile='http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/kk_tautau_10000.e4h.root'

# Mandatory: RDFanalysis class where the user defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    # Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
 #.Alias("GenParticles0", "GenParticles#0.index")
 .Define("MC_p",    "FCCAnalyses::MCParticle::get_p(GenParticles)")
 .Define("MC_theta","FCCAnalyses::MCParticle::get_theta(GenParticles)")
 .Define("MC_charge","FCCAnalyses::MCParticle::get_charge(GenParticles)")
 .Define("MC_phi","FCCAnalyses::MCParticle::get_phi(GenParticles)")
              )
        return df2

    #__________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "MC_p",
                "MC_theta",
                "MC_charge",
                "MC_phi",
        ]
        return branchList
