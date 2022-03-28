#USER DEFINED MANDATORY ARGUMENTS
processList = ['p8_ee_Zbb_ecm91','p8_ee_Zcc_ecm91','p8_ee_Zuds_ecm91']
outputList  = []
prodTag     = "FCCee/spring2021/IDEA/"
outputDir   = "/eos/experiment/fcc/ee/tmp/testnewscheme/"
nCPUS       = 8
fraction    = 1.
runBatch    = False

#RDFanalysis class where the use defines the operations on the TTree
import ROOT
class RDFanalysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print (" init done, about to run")

    #__________________________________________________________
    def analysers(df):
        #df2 = (self.df.Range(100)
        df2 = (df
        .Define("x", "gRandom->Rndm()")
        .Define("y", "gRandom->Rndm()")
        )
        return df2

    #__________________________________________________________
    def output():
        branchList = ROOT.vector('string')()
        branchList.push_back("x")
        branchList.push_back("y")
        return branchList
