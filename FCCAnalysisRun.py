import ROOT
import os, sys
import time
import yaml
import importlib.util
from array import array
from config.common_defaults import deffccdicts

print ("Load cxx analyzers ... ",)
#ROOT.gSystem.Load("libedm4hep")
#ROOT.gSystem.Load("libpodio")
#ROOT.gSystem.Load("libawkward")
#ROOT.gSystem.Load("libawkward-cpu-kernels")
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
def getElementDict(d, element):
    try:
        value=d[element]
        return value
    except KeyError:
        print (element, "does not exist using default value")
        return None

#__________________________________________________________                                                                                                                                                                    
def getProcessInfo(process, prodTag):

    doc = None
    if prodTag[-1]!="/":prodTag+="/"
    yamlfile=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '')+"yaml/"+prodTag+process+'/merge.yaml'
    with open(yamlfile) as ftmp:
        try:
            doc = yaml.load(ftmp, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
        except IOError as exc:
            print ("I/O error({0}): {1}".format(exc.errno, exc.strerror))
            print ("outfile ",outfile)
        finally:
            print ('yaml file {} succesfully opened'.format(yamlfile))

    filelist  = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
    eventlist = [f[1] for f in doc['merge']['outfiles']]
    return filelist,eventlist

#__________________________________________________________
def getsubfileList(fileList, eventList, fraction):
    nevts=sum(eventList)
    nevts_target=nevts*fraction
    nevts_real=0
    tmplist=[]
    for ev in range(len(eventList)):
        if nevts_real>=nevts_target:break
        nevts_real+=eventList[ev]
        tmplist.append(fileList[ev])
    return tmplist


#__________________________________________________________
def getchunkList(fileList, chunks):
    chunklist=[]
    if chunks>len(fileList):chunks=len(fileList)
    nfilesperchunk=int(len(fileList)/chunks)
    for ch in range(chunks):
        filecount=0
        listtmp=[]
        for fileName in fileList:
            if (filecount>=ch*nfilesperchunk and filecount<(ch+1)*nfilesperchunk) or (filecount>=ch*nfilesperchunk and ch==chunks-1):
                listtmp.append(fileName)
            filecount+=1

        chunklist.append(listtmp)
    return chunklist


#__________________________________________________________
def runRDF(foo, inputlist, outFile, nevt):
    ROOT.ROOT.EnableImplicitMT(getElement(foo, "nCPUS"))
    ROOT.EnableThreadSafety()
    df = ROOT.RDataFrame("events", inputlist)

    print (" init done, about to run {} events on {} CPUs".format(nevt, getElement(foo, "nCPUS")))

    df2 = getElement(foo.RDFanalysis, "analysers")(df)

    branchList = getElement(foo.RDFanalysis, "output")()
    branchListVec = ROOT.vector('string')()
    for branchName in branchList:
        branchListVec.push_back(branchName)

    df2.Snapshot("events", outFile, branchListVec)

#__________________________________________________________
def runLocal(foo, fileList, output):
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
    outFile = getElement(foo,"outputDir")
    if outFile[-1]!="/":outFile+="/"
    outFile+=output

    start_time = time.time()
    #run RDF
    runRDF(foo, fileListRoot, outFile, nevents_local)

    elapsed_time = time.time() - start_time
    print  ("==============================SUMMARY==============================")
    print  ("Elapsed time (H:M:S)     :  ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ("Events Processed/Second  :  ",int(nevents_local/elapsed_time))
    print  ("Total Events Processed   :  ",int(nevents_local))
    print  ("===================================================================")


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
    publicOptions.add_argument("--files-list", help="Specify input file to bypass the processList", default=[], nargs='+')
    publicOptions.add_argument("--output", help="Specify ouput file name to bypass the processList and or outputList, default output.root", type=str, default="output.root")

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

    #check if outputDir exist and if not create it
    outputDir = getElement(foo,"outputDir")
    if not os.path.exists(outputDir) and outputDir!='':
        os.system("mkdir -p {}".format(outputDir))

    #check first if files are specified, and if so run the analysis on it/them (this will exit after)
    if len(args.files_list)>0:
        print("Running locally with user command defined user file list")
        runLocal(foo, args.files_list, args.output)
        sys.exit(0)

    #check if batch mode and set start and end file from original list
    runBatch = getElement(foo,"runBatch")

    #check if the process list is specified                                                                                                                                                                                                
    processList = getElement(foo,"processList")

    #run locally
    #if runBatch == False:
    for process in processList:
        fileList, eventList = getProcessInfo(process, getElement(foo,"prodTag"))
        print ('---- running process  ',process)
        processDict={}
        fraction = 1
        output = process
        chunks = 1
        try:
            processDict=processList[process]
            if getElementDict(processList[process], 'fraction') != None: fraction = getElementDict(processList[process], 'fraction')
            if getElementDict(processList[process], 'output')   != None: output   = getElementDict(processList[process], 'output')
            if getElementDict(processList[process], 'chunks')   != None: chunks   = getElementDict(processList[process], 'chunks')

        except TypeError:
            print ('no values set for process {} will use default values'.format(process))

        print ('fraction={}, output={}, chunks={}'.format(fraction, output, chunks))

        if fraction<1:fileList = getsubfileList(fileList, eventList, fraction)
        print ('file list after fraction ',len(fileList))
        chunkList=[fileList]
        if chunks>1: chunkList = getchunkList(fileList, chunks)

        #create dir if more than 1 chunk
        if chunks>1:
            outputdir=outputDir+"/"+output
            if not os.path.exists(outputdir) and outputdir!='':
                os.system("mkdir -p {}".format(outputdir))

        for ch in range(len(chunkList)):
            #run locally
            outputchunk=''
            if runBatch == False:
                if len(chunkList)>1: 
                    outputchunk="/{}/chunk{}.root".format(output,ch)
                else: 
                    outputchunk="{}.root".format(output)
                print('output  -------   ',output)
                runLocal(foo, chunkList[ch], outputchunk)

            #run on batch
            elif runBatch == True:
                runBatch(foo, chunkList[ch], output)

   # #run on batch
   # startFile=-1
   # endFile=-1
   # if runBatch == True and args.first<0 and args.last<0:
   #     send2Batch(foo)












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
