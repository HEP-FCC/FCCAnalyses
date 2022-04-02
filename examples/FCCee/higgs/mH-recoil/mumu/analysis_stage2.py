processList = {
    'p8_ee_ZZ_ecm240':{},#Run over the full statistics from stage1 input file <inputDir>/p8_ee_ZZ_ecm240.root. Keep the same output name as input
    'p8_ee_WW_ecm240':{}, #Run over the statistics from stage1 input files <inputDir>/p8_ee_WW_ecm240_out/*.root. Keep the same output name as input
    'p8_ee_ZH_ecm240_out':{'output':'MySample_p8_ee_ZH_ecm240'} #Run over the full statistics from stage1 input file <inputDir>/p8_ee_ZH_ecm240_out.root. Change the output name to MySample_p8_ee_ZH_ecm240
}

#Mandatory: input directory when not running over centrally produced edm4hep events. 
#It can still be edm4hep files produced standalone or files from a first analysis step (this is the case in this example it runs over the files produced from analysis.py)
inputDir    = "ZH_mumu_recoil/stage1"

#Optional: output directory, default is local dir
outputDir   = "ZH_mumu_recoil/stage2"

#Optional: ncpus, default is 4
nCPUS       = 2

#Optional running on HTCondor, default is False
runBatch    = False

#USER DEFINED CODE
import ROOT
ROOT.gInterpreter.Declare("""
bool myFilter(ROOT::VecOps::RVec<float> mass) {
    for (size_t i = 0; i < mass.size(); ++i) {
        if (mass.at(i)>80. && mass.at(i)<100.)
            return true;
    }
    return false;
}
""")
#END USER DEFINED CODE

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               #Filter to have exactly one Z candidate
               .Filter("zed_leptonic_m.size() == 1")
               #Define Z candidate mass
               .Define("Zcand_m","zed_leptonic_m[0]")
               #Define Z candidate recoil mass
               .Define("Zcand_recoil_m","zed_leptonic_recoil_m[0]")
               #Define Z candidate pt
               .Define("Zcand_pt","zed_leptonic_pt[0]")
               #Define Z candidate charge
               .Define("Zcand_q","zed_leptonic_charge[0]")
               #Define new var rdf entry (example)
               .Define("entry", "rdfentry_")
               #Define a weight based on entry (inline example of possible operations)
               .Define("weight", "return 1./(entry+1)")
               #Define a variable based on a custom filter
               .Define("MyFilter", "myFilter(zed_leptonic_m)")
               )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.
    def output():
        branchList = [
            "Zcand_m", "Zcand_pt", "Zcand_q","MyFilter","Zcand_recoil_m",
            "entry","weight"
        ]
        return branchList




