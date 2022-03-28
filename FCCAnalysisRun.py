import ROOT
import os, sys
import importlib.util

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

#__________________________________________________________
def getElement(foo, element):
    try:
        return getattr(foo, element)
    except AttributeError:
        print (element, "does not exist, please check. Exit")
        sys.exit(3)


#__________________________________________________________
def runRDF(foo, inputlist, outFile):
    ROOT.ROOT.EnableImplicitMT(getElement(foo, "nCPUS"))
    ROOT.EnableThreadSafety()
    df = ROOT.RDataFrame("events", inputlist)
    print (" init done, about to run")
    df2 = getElement(foo.RDFanalysis, "analysers")(df)
    branchList=getElement(foo.RDFanalysis, "output")()
    print(type(branchList))
    print(branchList[0])
    print(branchList[1])

    branchListVec = ROOT.vector('string')()
    for branchName in branchList:
        branchListVec.push_back(branchName)
    #df2.Snapshot("events", outFile, branchListVec)
    df2.Snapshot("events", outFile)


#__________________________________________________________
def runLocal(foo, fileList=""):
    #Create list of files to be Processed
    print ("Create dataframe object from ", )
    fileListRoot = ROOT.vector('string')()
    nevents_meta = 0
    nevents_local = 0
    for fileName in fileList:
        fileListRoot.push_back(fileName)
        print (fileName, " ",)
        print (" ...")
        tf=ROOT.TFile.Open(str(fileName),"READ")
        tf.cd()
        for key in tf.GetListOfKeys():
            if 'eventsProcessed' == key.GetName():
                nevents_meta += tf.eventsProcessed.GetVal()
                break
        tt=tf.Get("events")
        nevents_local+=tt.GetEntries()
    print ("nevents meta  ", nevents_meta)
    print ("nevents local ", nevents_local)
    outFile = getElement(foo,"outputDir")+fileName.split("/")[-1].replace(".root","_output.root")
    runRDF(foo, fileListRoot, outFile)

    outf = ROOT.TFile( outFile, "update" )
    n = array( "i", [ 0 ] )
    n[0]=nevents_local
    if nevents_meta>nevents_local:n[0]=nevents_meta
    p = ROOT.TParameter(int)( "eventsProcessed", n[0])
    p.Write()
    outf.Write()
    outf.Close()

#__________________________________________________________
if __name__ == "__main__":
    #check the arguments
    if len(sys.argv)<2:
        print ("usage:")
        print ("python ",sys.argv[0]," PATHTO/analysis.py <options>")
        print ("python ",sys.argv[0]," --help for help")
        sys.exit(3)

    import argparse
    parser = argparse.ArgumentParser()
    publicOptions = parser.add_argument_group('User options')
    publicOptions.add_argument("-f","--file", type=str, help="Specify input file to bypass the samples for quick tests", default="")

    internalOptions = parser.add_argument_group('\033[4m\033[1m\033[91m Internal options, NOT FOR USERS\033[0m')
    internalOptions.add_argument("--batch", action='store_true', help="Submit on batch")
    internalOptions.add_argument("--process", type=str, help="Process from the processList", default="")
    internalOptions.add_argument("--first", type=int, help="First file for process in the full list", default=-1)
    internalOptions.add_argument("--last", type=int, help="Last file for process in the full list", default=-1)

    args, _ = parser.parse_known_args()
    #check that the analysis file exists
    analysisFile = sys.argv[1]
    if not os.path.isfile(analysisFile):
        print(sys.argv[1], " does not exist")
        sys.exit(3)

    #load the analysis
    analysisFile=os.path.abspath(analysisFile)
    spec = importlib.util.spec_from_file_location("rdfanalysis", analysisFile)
    foo  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    #check if a single file is specified, and if so run the analysis on it
    if args.file!="":
        runLocal(foo, [args.file])
        sys.exit(0)

    #check if batch mode and set start and end file from original list
    runBatch = getElement(foo,"runBatch")
    startFile=-1
    endFile=-1
    if runBatch and args.first<0 and args.last<0:
        send2Batch(foo)














    #check in case run
    #foo.RDFanalysis.run()
    runBatch = getElement(foo.RDFanalysis,"run")



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

    nevents_meta=0
    nevents_local=0
    if nevents==0:
        for f in fileListRoot:
            tf=ROOT.TFile.Open(str(f),"READ")
            tf.cd()
            for key in tf.GetListOfKeys():
                if 'eventsProcessed' == key.GetName():
                    nevents_meta += tf.eventsProcessed.GetVal()
                    break
            tt=tf.Get("events")
            nevents_local+=tt.GetEntries()
    print ("nevents meta  ", nevents_meta)
    print ("nevents local ", nevents_local)


    if nevents_meta>nevents_local:nevents=nevents_meta
    else :nevents=nevents_local

    import time
    start_time = time.time()
    ncpus = 8
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    elapsed_time = time.time() - start_time
    print  ("==============================SUMMARY==============================")
    print  ("Elapsed time (H:M:S)     :  ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ("Events Processed/Second  :  ",int(nevents_local/elapsed_time))
    print  ("Total Events Processed   :  ",int(nevents_local))
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
