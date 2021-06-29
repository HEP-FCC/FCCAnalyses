import sys
import ROOT
from array import array

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
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print (" init done, about to run")
    #__________________________________________________________
    def run(self):
        df2 = (self.df
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

        #############################################
        ##      select branches for output file    ##
        ############################################# 
        branchList = ROOT.vector('string')()
        for branchName in ["Bd2MuMu_mass" ]:
            branchList.push_back(branchName)

        df2.Snapshot("events", self.outname, branchList)





# example call for standalone file
# python examples/FCCee/flavour/Bd2MuMu/analysis.py p8_ee_Zbb_Bd2MuMu.root /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bd2MuMu/events_108578506.root

# python examples/FCCee/flavour/Bd2MuMu/analysis.py p8_ee_Zbb.root "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91/events_0033*.root"




if __name__ == "__main__":

    if len(sys.argv)<3:
        print ("usage:")
        print ("python ",sys.argv[0]," output.root input.root")
        print ("python ",sys.argv[0]," output.root \"inputdir/*.root\"")
        print ("python ",sys.argv[0]," output.root file1.root file2.root file3.root <nevents>")
        sys.exit(3)


    print ("Create dataframe object from ", )
    fileListRoot = ROOT.vector('string')()
    nevents=0

    print("===============================", sys.argv[2])

    if len(sys.argv)==3 and "*" in sys.argv[2]:
        import glob
        filelist = glob.glob(sys.argv[2])
        for fileName in filelist:
            fileListRoot.push_back(fileName)
            print (fileName, " ",)
            print (" ...")


    elif len(sys.argv)>2:
        for i in range(2,len(sys.argv)):
            try:
                nevents=int(sys.argv[i])
                print ("nevents found (will be in the processed events branch in root tree):",nevents)
            except ValueError:
                fileListRoot.push_back(sys.argv[i])
                print (sys.argv[i], " ",)
                print (" ...")

                         
    outfile=sys.argv[1]
    print("output file:  ",outfile)
    if len(outfile.split("/"))>1:
        import os
        os.system("mkdir -p {}".format(outfile.replace(outfile.split("/")[-1],"")))

    if nevents==0:
        for f in fileListRoot:
            tf=ROOT.TFile.Open(str(f),"READ")
            tt=tf.Get("events")
            nevents+=tt.GetEntries()
    print ("nevents ", nevents)
    
    import time
    start_time = time.time()
    ncpus = 8
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    elapsed_time = time.time() - start_time
    print  ("==============================SUMMARY==============================")
    print  ("Elapsed time (H:M:S)     :  ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ("Events Processed/Second  :  ",int(nevents/elapsed_time))
    print  ("Total Events Processed   :  ",int(nevents))
    print  ("===================================================================")

    
    outf = ROOT.TFile( outfile, "update" )
    meta = ROOT.TTree( "metadata", "metadata informations" )
    n = array( "i", [ 0 ] )
    meta.Branch( "eventsProcessed", n, "eventsProcessed/I" )
    n[0]=nevents
    meta.Fill()
    p = ROOT.TParameter(int)( "eventsProcessed", n[0])
    p.Write()
    outf.Write()
    outf.Close()

