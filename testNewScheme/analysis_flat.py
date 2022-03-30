#USER DEFINED MANDATORY ARGUMENTS
processList = {'wzp6_egamma_tbnu_ecm240':{'chunks':1}}

processList = {'p8_ee_Zbb_ecm91_out':{'output':'p8_ee_Zbb_ecm91_flat'},
               'p8_ee_Zcc_ecm91':{'output':'p8_ee_Zcc_ecm91_flat'},
               'p8_ee_Zuds_ecm91_out':{'output':'p8_ee_Zuds_ecm91_flat'},
               'wzp6_gammae_tbnu_ecm240':{'output':'wzp6_gammae_tbnu_ecm240_flat'},
               'wzp6_egamma_tbnu_ecm240':{'output':'wzp6_eammae_tbnu_ecm240_flat'}

           }

inputDir    = "/eos/experiment/fcc/ee/tmp/testnewscheme/"
outputDir   = "/eos/experiment/fcc/ee/tmp/testnewscheme/"
nCPUS       = 8
runBatch    = False

#RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    def analysers(df):
        df2 = (df
        .Define("vv", "rdfentry_")
        .Define("ww", "return 1./(v+1)")
        )
        return df2

    #__________________________________________________________
    def output():
        branchList = ["vv","ww"]
        return branchList
