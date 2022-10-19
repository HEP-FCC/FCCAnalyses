testFile='http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/kk_tautau_10000.e4h.root'

# Mandatory: RDFanalysis class where the user defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    # Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        import ROOT
        ROOT.gInterpreter.Declare("""

        float scalarProduct(const edm4hep::Vector3f& in1, const edm4hep::Vector3f& in2 ){

        return ((in1.x*in2.x + in1.y*in2.y + in1.z*in2.z)/sqrt(pow(in1.x,2)+pow(in1.y,2)+pow(in1.z,2))/sqrt(pow(in2.x,2)+pow(in2.y,2)+pow(in2.z,2) ));
};
""")

        df2 = (df
               
               #namespace FCCAnalyses loaded, could be removed in case
               .Define("MC_p",      "FCCAnalyses::MCParticle::get_p(GenParticles)")
               .Define("MC_theta",  "FCCAnalyses::MCParticle::get_theta(GenParticles)")
               .Define("MC_charge", "FCCAnalyses::MCParticle::get_charge(GenParticles)")
               .Define("MC_phi",    "FCCAnalyses::MCParticle::get_phi(GenParticles)")
               .Define("tauplusvec", ROOT.MCParticle.sel_pdgID(-15, 0),["GenParticles"])
               .Define("tauminusvec", ROOT.MCParticle.sel_pdgID(15, 0),["GenParticles"])
               .Filter("tauminusvec.size()==1")
               .Define("tauplus", "tauplusvec[0]")
               .Define("scalarProd", "scalarProduct(tauminusvec[0].momentum, tauplusvec[0].momentum)")
               .Define("tauplus_px", "tauplus.momentum.x")
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
            "tauplus_px",
            "scalarProd"
        ]
        return branchList
