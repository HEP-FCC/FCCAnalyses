import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libawkward")
ROOT.gSystem.Load("libawkward-cpu-kernels")
ROOT.gSystem.Load("libFCCAnalyses")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)


class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        #ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        
        df2 = (self.df.Range(1000)
        #df2 = (self.df
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

               #does not work given the different index when filtering
               #.Define("RecoPartPID_PVFiltered", "myUtils::filter_PV(false)(RecoPartPID, RecoInd_actsFinder)")
               #.Define("Pions_PVFiltered"       ,"myUtils::sel_PID(211)(RecoPartPID_PVFiltered)"  )
               #.Define("Kaons_PVFiltered"       ,"myUtils::sel_PID(321)(RecoPartPID_PVFiltered)"  )
               #.Define("D0Candidates"          ,"myUtils::build_D0(0.05, 1.5)(RecoPartPID_PVFiltered, EFlowTrack_1, Pions_PVFiltered, Kaons_PVFiltered)")
               .Define("nD0", "myUtils::getFCCAnalysesComposite_N(D0Candidates)")
               .Filter("nD0>0")
               .Define("massD0", "myUtils::getFCCAnalysesComposite_mass(D0Candidates)")
               
               .Define("Bu2D0PiCandidates","myUtils::build_Bu2D0Pi(RecoPartPID, D0Candidates, Pions)")
               .Define("nBu2D0Pi", "myUtils::getFCCAnalysesComposite_N(Bu2D0PiCandidates)")
               .Define("massBu2D0Pi", "myUtils::getFCCAnalysesComposite_mass(Bu2D0PiCandidates)")

              
               
               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                #"RecoInd_actsFinder",
                #"Vertex_actsFinder",     # on Zuds: both track selections lead to very similar results for the vertex
               "nTrkPV",
                "nD0",
                "massD0",
                "nBu2D0Pi",
                "massBu2D0Pi",
                #"awk"
                ]:
            branchList.push_back(branchName)

        #opts = ROOT.RDF.RSnapshotOptions()
        #opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        #opts.fCompressionLevel = 3
        #opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/flavour/generic-analysis/analysis_Bu2D0Pi.py /afs/cern.ch/user/h/helsens/FCCsoft/Key4HEP/k4SimDelphes/ee_Zbb_Bu2D0Pi.root


if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        print ("python ",sys.argv[0]," dir/*.root")
        sys.exit(3)


    import glob
    filelist = glob.glob(sys.argv[1])
    
    print ("Create dataframe object from ", )
    fileListRoot = ROOT.vector('string')()
    for fileName in filelist:
        fileListRoot.push_back(fileName)
        print (fileName, " ",)
        print (" ...")
        
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/').replace('analysis_Bc2TauNu.py','')+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+sys.argv[1].split('/')[-1]
    ncpus = 1
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    #tf = ROOT.TFile(infile)
    #entries = tf.events.GetEntries()
    #p = ROOT.TParameter(int)( "eventsProcessed", entries)
    #outf=ROOT.TFile(outfile,"UPDATE")
    #p.Write()


