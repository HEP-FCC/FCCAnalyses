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

ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt("Bc2TauNu_BDT2", "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/xgb_bdt_stage2.root");

computeModel = TMVA::Experimental::Compute<18, float>(bdt);
''')


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
        #df2 = (self.df.Range(1000)        
        df2 = (self.df
               #a candidate is found with a mass
               .Define("CUT_CandInd",     "myFinalSel::selTauCand(Tau23PiCandidates_mass, Tau23PiCandidates_vertex, Vertex_chi2 )")
               .Filter("CUT_CandInd>-1")

               .Define("CUT_CandRho",      "if ((Tau23PiCandidates_rho1mass.at(CUT_CandInd)<1. && Tau23PiCandidates_rho2mass.at(CUT_CandInd)>0.5 && Tau23PiCandidates_rho2mass.at(CUT_CandInd)<1.0)|| (Tau23PiCandidates_rho2mass.at(CUT_CandInd)<0.9 && Tau23PiCandidates_rho1mass.at(CUT_CandInd)>0.5 && Tau23PiCandidates_rho1mass.at(CUT_CandInd)<1.)) return 1; else return 0;")
               .Filter("CUT_CandRho>0")

               .Define("EVT_CandMass",     "Tau23PiCandidates_mass.at(CUT_CandInd)")
               .Filter("EVT_CandMass<1.8")

               .Define("LOCAL_CandVtxInd", "Tau23PiCandidates_vertex.at(CUT_CandInd)")
               .Define("CUT_CandVtxThrustEmin", "Vertex_thrusthemis_emin.at(LOCAL_CandVtxInd)")
               .Filter("CUT_CandVtxThrustEmin>0")
               
               .Define("EVT_CandN",        "float(Tau23PiCandidates_vertex.size())")
               .Define("CUT_CandTruth",    "myFinalSel::selTauCandTM(Tau23PiCandidates_mcvertex, TrueTau23Pi_vertex, CUT_CandInd)")
               .Define("EVT_CandPx",       "Tau23PiCandidates_px.at(CUT_CandInd)")
               #.Define("EVT_CandPy",       "Tau23PiCandidates_py.at(CUT_CandInd)")
               .Define("EVT_CandPz",       "Tau23PiCandidates_pz.at(CUT_CandInd)")
               .Define("EVT_CandP",        "Tau23PiCandidates_p.at(CUT_CandInd)")
               .Define("EVT_CandD0",       "Tau23PiCandidates_d0.at(CUT_CandInd)")
               .Define("EVT_CandZ0",       "Tau23PiCandidates_z0.at(CUT_CandInd)")

               
               .Define("EVT_CandRho1Mass", "Tau23PiCandidates_rho1mass.at(CUT_CandInd)" )
               .Define("EVT_CandRho2Mass", "Tau23PiCandidates_rho2mass.at(CUT_CandInd)")
               
               .Define("EVT_CandVtxFD",    "Vertex_d2PV.at(LOCAL_CandVtxInd)")
               .Define("EVT_CandVtxFDErr", "Vertex_d2PVErr.at(LOCAL_CandVtxInd)")
               .Define("EVT_CandVtxChi2",  "Vertex_chi2.at(LOCAL_CandVtxInd)")
               .Define("EVT_MVA",  "MVA")
               
               .Define("EVT_CandPion1P",          "Tau23PiCandidates_pion1p.at(CUT_CandInd)")
               .Define("EVT_CandPion2P",          "Tau23PiCandidates_pion2p.at(CUT_CandInd)")
               .Define("EVT_CandPion3P",          "Tau23PiCandidates_pion3p.at(CUT_CandInd)")
               
               .Define("EVT_CandPion1D0",         "Tau23PiCandidates_pion1d0.at(CUT_CandInd)")
               .Define("EVT_CandPion2D0",         "Tau23PiCandidates_pion2d0.at(CUT_CandInd)")
               .Define("EVT_CandPion3D0",         "Tau23PiCandidates_pion3d0.at(CUT_CandInd)")

               .Define("EVT_CandPion1Z0",         "Tau23PiCandidates_pion1z0.at(CUT_CandInd)")
               .Define("EVT_CandPion2Z0",         "Tau23PiCandidates_pion2z0.at(CUT_CandInd)")
               .Define("EVT_CandPion3Z0",         "Tau23PiCandidates_pion3z0.at(CUT_CandInd)")

               .Define("MVAVec", ROOT.computeModel, ())
               .Define("EVT_MVA2", "MVAVec.at(0)")
               #.Filter("EVT_MVA2>0.6")

           )
        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "CUT_CandTruth",
                "CUT_CandRho",
                "CUT_CandVtxThrustEmin",
                "EVT_CandMass","EVT_CandRho1Mass","EVT_CandRho2Mass",
                "EVT_CandN",
                "EVT_CandVtxFD","EVT_CandVtxFDErr", "EVT_CandVtxChi2",
                "EVT_CandPx","EVT_CandP","EVT_CandPz",##"EVT_CandPy",
                "EVT_CandD0","EVT_CandZ0",

                "EVT_MVA", 
                "EVT_CandPion1P","EVT_CandPion1D0","EVT_CandPion1Z0",
                "EVT_CandPion2P","EVT_CandPion2D0","EVT_CandPion2Z0",
                "EVT_CandPion3P","EVT_CandPion3D0","EVT_CandPion3Z0",
                
                
        ]:
            branchList.push_back(branchName)

        #opts = ROOT.RDF.RSnapshotOptions()
        #opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        #opts.fCompressionLevel = 3
        #opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/flavour/Bc2TauNu/analysis_presel.py p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batch/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/*.root"

# python examples/FCCee/flavour/Bc2TauNu/analysis_presel.py p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batchTraining/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/*.root"

# python examples/FCCee/flavour/Bc2TauNu/analysis_presel.py p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batchTraining/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU/*.root"

# python examples/FCCee/flavour/Bc2TauNu/analysis_presel.py p8_ee_Zbb_ecm91.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batchTraining/p8_ee_Zbb_ecm91/*.root"

# python examples/FCCee/flavour/Bc2TauNu/analysis_presel.py p8_ee_Zcc_ecm91.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batchTraining/p8_ee_Zcc_ecm91/*.root"

# python examples/FCCee/flavour/Bc2TauNu/analysis_presel.py p8_ee_Zuds_ecm91.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples_batchTraining/p8_ee_Zuds_ecm91/*.root"

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
                print ('nevents found (will be in the processed events branch in roo tree):',nevents)
            except ValueError:
                fileListRoot.push_back(sys.argv[i])
                print (sys.argv[i], " ",)
                print (" ...")

                         
    outfile=sys.argv[1]
    print('output file:  ',outfile)
    if len(outfile.split('/'))>1:
        import os
        os.system("mkdir -p {}".format(outfile.replace(outfile.split('/')[-1],'')))

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
    print  ('==============================SUMMARY==============================')
    print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ('Events Processed/Second  :  ',int(nevents/elapsed_time))
    print  ('Total Events Processed   :  ',int(nevents))
    print  ('===================================================================')

    
    outf = ROOT.TFile( outfile, 'update' )
    meta = ROOT.TTree( 'metadata', 'metadata informations' )
    n = array( 'i', [ 0 ] )
    meta.Branch( 'eventsProcessed', n, 'eventsProcessed/I' )
    n[0]=nevents
    meta.Fill()
    p = ROOT.TParameter(int)( "eventsProcessed", n[0])
    p.Write()
    outf.Write()
    outf.Close()

