#Mandatory: List of processes
processList = {
    'p8_ee_Zbb_ecm91_EvtGen_Bd2Kstee':{}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/flavour/B2Kstee/stage1"

#Optional: ncpus, default is 4
nCPUS       = 8

#Optional running on HTCondor, default is False
runBatch    = False
#batchQueue = "longlunch"
#compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               #Run the Acts AMVF vertex finder
               .Define("VertexObject_actsFinder"  ,"VertexFinderActs::VertexFinderAMVF( EFlowTrack_1)")
               .Define("NVertexObject_actsFinder" ,"VertexingUtils::get_Nvertex(VertexObject_actsFinder)")
               .Filter("NVertexObject_actsFinder==1")
               .Define("Vertex_actsFinder"      ,"VertexingUtils::get_VertexData( VertexObject_actsFinder, 0)")
               .Define("FCCAnaVertex_actsFinder","VertexingUtils::get_FCCAnalysesVertex( VertexObject_actsFinder, 0)")
               .Define("RecoInd_actsFinder"     ,"VertexingUtils::get_VertexRecoInd(FCCAnaVertex_actsFinder)")
               .Define("nTrkPV", "VertexingUtils::get_VertexNtrk(FCCAnaVertex_actsFinder)")
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")
               .Define("Pions"       ,"myUtils::sel_PID(211)(RecoPartPID)"  )
               .Define("Kaons"       ,"myUtils::sel_PID(321)(RecoPartPID)"  )
               .Define("D0Candidates"          ,"myUtils::build_D0(0.05, 1.5, true)(RecoPartPID, EFlowTrack_1, Pions, Kaons,RecoInd_actsFinder)")

               .Define("nD0", "myUtils::getFCCAnalysesComposite_N(D0Candidates)")
               .Filter("nD0>0")
               .Define("massD0", "myUtils::getFCCAnalysesComposite_mass(D0Candidates)")

               .Define("Bu2D0PiCandidates","myUtils::build_Bu2D0Pi(RecoPartPID, D0Candidates, Pions)")
               .Define("nBu2D0Pi", "myUtils::getFCCAnalysesComposite_N(Bu2D0PiCandidates)")
               .Define("massBu2D0Pi", "myUtils::getFCCAnalysesComposite_mass(Bu2D0PiCandidates)")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
               "nTrkPV",
                "nD0",
                "massD0",
                "nBu2D0Pi",
                "massBu2D0Pi"
        ]
        return branchList
