#USER DEFINED MANDATORY ARGUMENTS
processList = {'wzp6_egamma_tbnu_ecm240':{'chunks':1}}

processList = {'p8_ee_Zbb_ecm91':{'fraction':0.001,'output':'p8_ee_Zbb_ecm91_out','chunks':2},
               #'p8_ee_Zcc_ecm91':{'fraction':0.001,'chunks':2}}
               'p8_ee_Zuds_ecm91':{'fraction':0.001,'output':'p8_ee_Zuds_ecm91_out','chunks':2}}

prodTag     = "FCCee/spring2021/IDEA/"
outputDir   = "/eos/experiment/fcc/ee/tmp/testnewscheme/"
nCPUS       = 8
runBatch    = False

#RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    def analysers(df):
        df2 = (df
        .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        .Alias("Particle0", "Particle#0.index")
        .Alias("Particle1", "Particle#1.index")
        .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
        .Define("MC_Vertex_x",    "myUtils::get_MCVertex_x(MCVertexObject)")
        .Define("MC_Vertex_y",    "myUtils::get_MCVertex_y(MCVertexObject)")
        .Define("MC_Vertex_z",    "myUtils::get_MCVertex_z(MCVertexObject)")
        .Define("v", "rdfentry_")
        .Define("w", "return 1./(v+1)")
        )
        return df2

    #__________________________________________________________
    def output():
        branchList = ["v","w","MC_Vertex_x","MC_Vertex_y","MC_Vertex_z"]
        return branchList
