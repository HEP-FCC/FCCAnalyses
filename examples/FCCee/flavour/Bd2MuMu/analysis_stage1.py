Mandatory: List of processes
processList = {
    'p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu':{},
    'p8_ee_Zbb_ecm91':{'fraction':0.1}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = ""
outputDirEos   = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2MuMu/flatNtuples/spring2021/analysis_stage1/"
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

               #############################################
               ##               Build MC Vertex           ##
               #############################################
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")

               #############################################
               ##              Build Reco Vertex          ##
               #############################################
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")

               #############################################
               ##          Build PV var and filter        ##
               #############################################
               .Define("EVT_hasPV",     "myUtils::hasPV(VertexObject)")
               .Define("EVT_NtracksPV", "myUtils::get_PV_ntracks(VertexObject)")
               .Define("EVT_NVertex",   "VertexObject.size()")
               .Filter("EVT_hasPV==1")

               #############################################
               ##          Build new RecoP with PID       ##
               #############################################
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")

               #############################################
               ##  Build new RecoP with PID at vertex     ##
               #############################################
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

               #############################################
               ##        Build B0 -> MuMu candidates      ##
               #############################################
               .Define("Bd2MuMuCandidates",         "myUtils::build_Bd2MuMu(VertexObject,RecoPartPIDAtVertex)")

               #############################################
               ##       Filter B0 -> MuMu candidates      ##
               #############################################
               .Define("EVT_NBd2MuMu",              "float(myUtils::getFCCAnalysesComposite_N(Bd2MuMuCandidates))")
               .Filter("EVT_NBd2MuMu==1")

               #############################################
               ##    Get the B0 -> MuMu candidate mass    ##
               #############################################
               .Define("Bd2MuMu_mass",    "myUtils::getFCCAnalysesComposite_mass(Bd2MuMuCandidates)")
           )
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = ["Bd2MuMu_mass"]
        return branchList
