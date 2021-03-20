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

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        
        #df2 = (self.df.Range(100)
        df2 = (self.df
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")

               #Run the Acts AMVF vertex finder
               .Define("VertexObject_actsFinder"  ,"VertexFinderActs::VertexFinderAMVF( EFlowTrack_1)")
               .Define("NVertex_actsFinder"       ,"VertexingUtils::get_Nvertex(VertexObject_actsFinder)")
               .Define("FCCAnaVertex_actsFinder"  ,"myUtils::sel_PV(true)(VertexObject_actsFinder)")
               .Define("RecoInd_actsFinder"       ,"VertexingUtils::get_VertexRecoInd(FCCAnaVertex_actsFinder)")
               .Define("Vertex_actsFinder"       ,"VertexingUtils::get_VertexData( FCCAnaVertex_actsFinder)")

                       
               #.Filter("NVertexObject_actsFinder==1")
               #.Define("Vertex_actsFinder"      ,"VertexingUtils::get_VertexData( VertexObject_actsFinder, 0)")
               #.Define("FCCAnaVertex_actsFinder","VertexingUtils::get_FCCAnalysesVertex( VertexObject_actsFinder, 0)")
               #.Define("RecoInd_actsFinder"     ,"VertexingUtils::get_VertexRecoInd(FCCAnaVertex_actsFinder)")

               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")
               .Define("Pions"       ,"myUtils::sel_PID(211)(RecoPartPID)"  )

               #.Define("TauCandidates", "myUtils::build_composite_vertex(3, 1, 0.3,3.,1.5, true, true)(RecoPartPID, EFlowTrack_1, Pions ,RecoInd_actsFinder)")
               .Define("TauCandidates", "myUtils::build_tau23pi(1, 0.3 ,3., 1.5, 0.4, true, true, false)(RecoPartPID, EFlowTrack_1, Pions ,RecoInd_actsFinder)")
               .Define("TauCandidates_rho", "myUtils::build_tau23pi(1, 0.3 ,3., 1.5, 0.4, true, true, true)(RecoPartPID, EFlowTrack_1, Pions ,RecoInd_actsFinder)")
               
               .Define("nTau", "myUtils::getFCCAnalysesComposite_N(TauCandidates)")
               .Filter("nTau>0")
               #.Define('RP2MC',            "ReconstructedParticle2MC::getRP2MC_indexVec(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)") 
               .Define('RP2MC',            "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)") 
               .Define("TauCandidatesTruthMatched", "myUtils::add_truthmatched(TauCandidates, Particle, RP2MC, ReconstructedParticles, Particle0)")
               .Define("TauCandidatesTruthMatched_rho", "myUtils::add_truthmatched(TauCandidates_rho, Particle, RP2MC, ReconstructedParticles, Particle0)")

               .Define("nTau23Pi", "myUtils::getFCCAnalysesComposite_N(TauCandidates)")
               .Define("massTau23Pi", "myUtils::getFCCAnalysesComposite_mass(TauCandidates)")
               .Define("Tau23Pi_MC", "myUtils::get_compmc(TauCandidatesTruthMatched)")
               .Define("PV2Tau", "myUtils::get_flightDistanceVertex(TauCandidatesTruthMatched, Vertex_actsFinder)")

               .Define("nTau23Pi_rho", "myUtils::getFCCAnalysesComposite_N(TauCandidates_rho)")
               .Define("massTau23Pi_rho", "myUtils::getFCCAnalysesComposite_mass(TauCandidates_rho)")
               .Define("Tau23Pi_MC_rho", "myUtils::get_compmc(TauCandidatesTruthMatched_rho)")
               .Define("PV2Tau_rho", "myUtils::get_flightDistanceVertex(TauCandidatesTruthMatched_rho, Vertex_actsFinder)")

               
               .Define("nTrkPV", "VertexingUtils::get_VertexNtrk(FCCAnaVertex_actsFinder)")

               .Define("TauRecoParticles_rho", ""
               
               .Define("deltaAlpha_max","ReconstructedParticle::angular_separationBuilder(0)( TauRecoParticles )")
               .Define("deltaAlpha_min","ReconstructedParticle::angular_separationBuilder(1)( TauRecoParticles )")
               .Define("deltaAlpha_ave","ReconstructedParticle::angular_separationBuilder(2)( TauRecoParticles )")

               
               
               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                #"RecoInd_actsFinder",
                #"Vertex_actsFinder",     # on Zuds: both track selections lead to very similar results for the vertex
                "NVertex_actsFinder",
                "nTrkPV",
                
                "nTau23Pi",
                "massTau23Pi",
                "Tau23Pi_MC",
                "PV2Tau",

                "nTau23Pi_rho",
                "massTau23Pi_rho",
                "Tau23Pi_MC_rho",
                "PV2Tau_rho",
                
                ]:
            branchList.push_back(branchName)

        #opts = ROOT.RDF.RSnapshotOptions()
        #opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        #opts.fCompressionLevel = 3
        #opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/flavour/generic-analysis/analysis_Bc2TauNu.py  /afs/cern.ch/user/h/helsens/FCCsoft/Key4HEP/k4SimDelphes/ee_Zbb_Bc2TauNu.root flat_ee_Zbb_Bc2TauNu.root
# python examples/FCCee/flavour/generic-analysis/analysis_Bc2TauNu.py  "/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_02*" flat_ee_Zbb_Bc2TauNu.root
# python examples/FCCee/flavour/generic-analysis/analysis_Bc2TauNu.py  /afs/cern.ch/user/h/helsens/FCCsoft/Key4HEP/k4SimDelphes/ee_Zbb_Bu2TauNu.root flat_ee_Zbb_Bu2TauNu.root 

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
    ncpus = 8
    if len(sys.argv)==3:outfile=sys.argv[2]
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    #tf = ROOT.TFile(infile)
    #entries = tf.events.GetEntries()
    #p = ROOT.TParameter(int)( "eventsProcessed", entries)
    #outf=ROOT.TFile(outfile,"UPDATE")
    #p.Write()


