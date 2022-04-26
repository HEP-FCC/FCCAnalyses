import ROOT
import os, sys
import time
import yaml
import glob
import subprocess
import importlib.util
from array import array
from config.common_defaults import deffccdicts

print ("----> Load cxx analyzers from libFCCAnalyses... ",)
ROOT.gSystem.Load("libFCCAnalyses")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
#Is this still needed?? 01/04/2022 still to be the case
_fcc  = ROOT.dummyLoader

#__________________________________________________________
def getElement(rdfModule, element):
    try:
        return getattr(rdfModule, element)
    except AttributeError:

        #return default values or crash if mandatory
        if element=='processList':
            print('The variable <processList> is mandatory in your analysis.py file, will exit')
            sys.exit(3)

        elif element=='analysers':
            print('The function <analysers> is mandatory in your analysis.py file, will exit')
            sys.exit(3)

        elif element=='output':
            print('The function <output> is mandatory in your analysis.py file, will exit')
            sys.exit(3)

        elif element=='nCPUS':
            print('The variable <nCPUs> is optional in your analysis.py file, return default value 4')
            return 4

        elif element=='runBatch':
            print('The variable <runBatch> is optional in your analysis.py file, return default value False')
            return False

        elif element=='outputDir':
            print('The variable <outputDir> is optional in your analysis.py file, return default value running dir')
            return ""

        elif element=='batchQueue':
            print('The variable <batchQueue> is optional in your analysys.py file, return default value workday')
            return "workday"

        elif element=='compGroup':
             print('The variable <compGroup> is optional in your analysys.py file, return default value group_u_FCC.local_gen')
             return "group_u_FCC.local_gen"

        elif element=='outputDirEos':
            print('The variable <outputDirEos> is optional in your analysis.py file, return default empty string')
            return ""

        elif element=='eosType':
            print('The variable <outputDirEos> is optional in your analysis.py file, return default eospublic')
            return "eospublic"

        elif element=='userBatchConfig':
            print('The variable <userBatchConfig> is optional in your analysis.py file, return default empty string')
            return ""

        return None

#__________________________________________________________
def getElementDict(d, element):
    try:
        value=d[element]
        return value
    except KeyError:
#        print (element, "does not exist using default value")
        return None

#__________________________________________________________
def getProcessInfo(process, prodTag, inputDir):
    if prodTag==None and inputDir==None:
        print('The variable <prodTag> or <inputDir> is mandatory your analysis.py file, will exit')
        sys.exit(3)
    elif prodTag!=None and inputDir!=None:
        print('The variable <prodTag> and <inputDir> can not be set both at the same time in your analysis.py file, will exit')
        sys.exit(3)

    if prodTag!=None:
        return getProcessInfoYaml(process, prodTag)
    elif inputDir!=None:
        return getProcessInfoFiles(process, inputDir)
    else:
        print('problem, why are you here???, exit')
        sys.exist(3)

#__________________________________________________________
def getProcessInfoFiles(process, inputDir):
    filelist=[]
    eventlist=[]
    filetest='{}/{}.root'.format(inputDir, process)
    dirtest='{}/{}'.format(inputDir, process)

    if os.path.isfile(filetest) and os.path.isdir(dirtest):
        print ("----> For process {} both a file {} and a directory {} exist".format(process,filetest,dirtest))
        print ("----> Exactly one should be used, please check. Exit")
        sys.exit(3)

    if not os.path.isfile(filetest) and not os.path.isdir(dirtest):
        print ("----> For process {} neither a file {} nor a directory {} exist".format(process,filetest,dirtest))
        print ("----> Exactly one should be used, please check. Exit")
        sys.exit(3)

    if os.path.isfile(filetest):
        filelist.append(filetest)
        eventlist.append(getEntries(filetest))

    if os.path.isdir(dirtest):
        flist=glob.glob(dirtest+"/*.root")
        for f in flist:
            filelist.append(f)
            eventlist.append(getEntries(f))


    return filelist, eventlist

#__________________________________________________________
def getEntries(f):
    tf=ROOT.TFile.Open(f,"READ")
    tf.cd()
    tt=tf.Get("events")
    nevents=tt.GetEntries()
    tf.Close()
    return nevents

#__________________________________________________________
def getProcessInfoYaml(process, prodTag):
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
            print ('----> yaml file {} succesfully opened'.format(yamlfile))

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
def getCommandOutput(command):
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE,universal_newlines=True)
    (stdout,stderr) = p.communicate()
    return {"stdout":stdout, "stderr":stderr, "returncode":p.returncode}


#__________________________________________________________
def SubmitToCondor(cmd,nbtrials):
    submissionStatus=0
    cmd=cmd.replace('//','/') # -> dav : is it needed?
    for i in range(nbtrials):
        outputCMD = getCommandOutput(cmd)
        stderr=outputCMD["stderr"].split('\n')
        stdout=outputCMD["stdout"].split('\n') # -> dav : is it needed?

        if len(stderr)==1 and stderr[0]=='' :
            print ("----> GOOD SUBMISSION")
            submissionStatus=1
        else:
            print ("----> ERROR submitting, will retry")
            print ("----> Trial : "+str(i)+" / "+str(nbtrials))
            print ("----> stderr : ",len(stderr))
            print (stderr)

            time.sleep(10)

        if submissionStatus==1:
            return 1

        if i==nbtrials-1:
            print ("failed sumbmitting after: "+str(nbtrials)+" trials, stop trying to submit")
            return 0


#__________________________________________________________
def runRDF(rdfModule, inputlist, outFile, nevt):
    ROOT.ROOT.EnableImplicitMT(getElement(rdfModule, "nCPUS"))
    ROOT.EnableThreadSafety()
    df = ROOT.RDataFrame("events", inputlist)

    print ("----> Init done, about to run {} events on {} CPUs".format(nevt, getElement(rdfModule, "nCPUS")))

    df2 = getElement(rdfModule.RDFanalysis, "analysers")(df)

    branchList = getElement(rdfModule.RDFanalysis, "output")()
    branchListVec = ROOT.vector('string')()
    for branchName in branchList:
        branchListVec.push_back(branchName)

    df2.Snapshot("events", outFile, branchListVec)


#__________________________________________________________
def sendToBatch(rdfModule, chunkList, process, analysisFile):
    localDir = os.environ["LOCAL_DIR"]
    logDir   = localDir+"/BatchOutputs/{}".format(output)
    if not os.path.exists(logDir):
        os.system("mkdir -p {}".format(logDir))

    outputDir       = getElement(rdfModule, "outputDir")
    outputDirEos    = getElement(rdfModule, "outputDirEos")
    eosType         = getElement(rdfModule, "eosType")
    userBatchConfig = getElement(rdfModule, "userBatchConfig")

    if outputDir!="" and outputDir[-1]!="/": outputDir+="/"

    condor_file_str=''
    for ch in range(len(chunkList)):
        frunname = '{}/job{}_chunk{}.sh'.format(logDir,process,ch)
        print('----> script to run : ',frunname)
        condor_file_str+=frunname+" "

        frun = None
        try:
            frun = open(frunname, 'w')
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            time.sleep(10)
            frun = open(frunname, 'w')

        subprocess.getstatusoutput('chmod 777 %s'%(frunname))
        frun.write('#!/bin/bash\n')
        frun.write('source /cvmfs/sw.hsf.org/key4hep/setup.sh\n')
        frun.write('export PYTHONPATH=$LOCAL_DIR:$PYTHONPATH\n')
        frun.write('export LD_LIBRARY_PATH=$LOCAL_DIR/install/lib:$LD_LIBRARY_PATH\n')
        frun.write('export ROOT_INCLUDE_PATH=$LOCAL_DIR/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH\n')

        #add userBatchConfig if any
        if userBatchConfig!="":
            if not os.path.isfile(userBatchConfig):
                print('----> userBatchConfig file does not exist, will not add it to default config, please check')
            else:
                configFile=open(userBatchConfig)
                for line in configFile:
                    frun.write(line+'\n')

        frun.write('mkdir job{}_chunk{}\n'.format(process,ch))
        frun.write('cd job{}_chunk{}\n'.format(process,ch))

        if not os.path.isabs(outputDir):
            frun.write('python $LOCAL_DIR/config/FCCAnalysisRun.py {} --batch --output {}chunk{}.root --files-list '.format(analysisFile, outputDir, ch))
        else:
            frun.write('python $LOCAL_DIR/config/FCCAnalysisRun.py {} --batch --output {}{}/chunk{}.root --files-list '.format(analysisFile, outputDir, process,ch))

        for ff in range(len(chunkList[ch])):
            frun.write(' %s'%(chunkList[ch][ff]))
        frun.write('\n')
        if not os.path.isabs(outputDir):
            if outputDirEos=="":
                frun.write('cp {}chunk{}.root  {}/{}/{}/chunk{}.root\n'.format(outputDir,ch,localDir,outputDir,process,ch))
            else:
                frun.write('xrdcp {}chunk{}.root  root://{}.cern.ch/{}/{}/chunk{}.root\n'.format(outputDir,ch,eosType,outputDirEos,process,ch))
        else:
            if outputDirEos!="":
                frun.write('xrdcp {}chunk{}.root  root://{}.cern.ch/{}/{}/chunk{}.root\n'.format(outputDir,ch,eosType,outputDirEos,process,ch))

        frun.close()


    condor_file_str=condor_file_str.replace("//","/")
    frunname_condor = 'job_desc_{}.cfg'.format(process)
    frunfull_condor = '%s/%s'%(logDir,frunname_condor)
    frun_condor = None
    try:
        frun_condor = open(frunfull_condor, 'w')
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        time.sleep(10)
        frun_condor = open(frunfull_condor, 'w')
    subprocess.getstatusoutput('chmod 777 {}'.format(frunfull_condor))
    frun_condor.write('executable       = $(filename)\n')
    frun_condor.write('Log              = {}/condor_job.{}.$(ClusterId).$(ProcId).log\n'.format(logDir,process))
    frun_condor.write('Output           = {}/condor_job.{}.$(ClusterId).$(ProcId).out\n'.format(logDir,process))
    frun_condor.write('Error            = {}/condor_job.{}.$(ClusterId).$(ProcId).error\n'.format(logDir,process))
    frun_condor.write('getenv           = True\n')
    frun_condor.write('environment      = "LS_SUBCWD={}"\n'.format(logDir)) # not sure
    frun_condor.write('requirements     = ( (OpSysAndVer =?= "CentOS7") && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n')
    frun_condor.write('on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n')
    frun_condor.write('max_retries      = 3\n')
    frun_condor.write('+JobFlavour      = "{}"\n'.format(getElement(rdfModule, "batchQueue")))
    frun_condor.write('+AccountingGroup = "{}"\n'.format(getElement(rdfModule, "compGroup")))
    frun_condor.write('RequestCpus      = {}\n'.format(getElement(rdfModule, "nCPUS")))
    frun_condor.write('queue filename matching files {}\n'.format(condor_file_str))
    frun_condor.close()

    cmdBatch="condor_submit {}".format(frunfull_condor)
    print ('----> batch command  : ',cmdBatch)
    job=SubmitToCondor(cmdBatch,10)


#__________________________________________________________
def runLocal(rdfModule, fileList, output, batch):
    #Create list of files to be Processed
    print ("running local from batch = ",batch)
    print ("----> Create dataframe object from files: ", )
    fileListRoot = ROOT.vector('string')()
    nevents_meta = 0
    nevents_local = 0
    for fileName in fileList:
        fileListRoot.push_back(fileName)
        print ("   ",fileName)
        tf=ROOT.TFile.Open(str(fileName),"READ")
        tf.cd()
        for key in tf.GetListOfKeys():
            if 'eventsProcessed' == key.GetName():
                nevents_meta += tf.eventsProcessed.GetVal()
                break
        tt=tf.Get("events")
        nevents_local+=tt.GetEntries()
    print ("----> nevents original={}  local={}".format(nevents_meta,nevents_local))
    outFile = getElement(rdfModule,"outputDir")
    if outFile!="" and outFile[-1]!="/": outFile+="/"

    if batch==False:
        outFile+=output
    else:
        outFile=output
    start_time = time.time()
    #run RDF
    runRDF(rdfModule, fileListRoot, outFile, nevents_local)

    elapsed_time = time.time() - start_time
    outf = ROOT.TFile( outFile, "update" )
    outt = outf.Get("events")
    outn = outt.GetEntries()
    n = array( "i", [ 0 ] )
    n[0]=nevents_local
    if nevents_meta>nevents_local:n[0]=nevents_meta
    p = ROOT.TParameter(int)( "eventsProcessed", n[0])
    p.Write()
    outf.Write()
    outf.Close()

    elapsed_time = time.time() - start_time
    print  ("==============================SUMMARY==============================")
    print  ("Elapsed time (H:M:S)     :  ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ("Events Processed/Second  :  ",int(nevents_local/elapsed_time))
    print  ("Total Events Processed   :  ",int(nevents_local))
    if (nevents_local>0): print  ("Reduction factor local   :  ",outn/nevents_local)
    if (nevents_meta>0):  print  ("Reduction factor total   :  ",outn/nevents_meta)
    print  ("===================================================================")
    print  (" ")
    print  (" ")



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
    internalOptions.add_argument("--batch", action='store_true', help="Submit on batch", default=False)

    args, _ = parser.parse_known_args()
    #check that the analysis file exists
    analysisFile = sys.argv[1]
    if not os.path.isfile(analysisFile):
        print(sys.argv[1], " does not exist")
        sys.exit(3)

    #load the analysis
    analysisFile=os.path.abspath(analysisFile)
    rdfSpec   = importlib.util.spec_from_file_location("rdfanalysis", analysisFile)
    rdfModule = importlib.util.module_from_spec(rdfSpec)
    rdfSpec.loader.exec_module(rdfModule)

    #check if outputDir exist and if not create it
    outputDir = getElement(rdfModule,"outputDir")
    if not os.path.exists(outputDir) and outputDir!='':
        os.system("mkdir -p {}".format(outputDir))

    #check if outputDir exist and if not create it
    outputDirEos = getElement(rdfModule,"outputDirEos")
    if not os.path.exists(outputDirEos) and outputDirEos!='':
        os.system("mkdir -p {}".format(outputDirEos))

    #check first if files are specified, and if so run the analysis on it/them (this will exit after)
    if len(args.files_list)>0:
        print("----> Running  with user defined list of files (either locally or from batch)")
        path, filename = os.path.split(args.output)
        if path!='': os.system("mkdir -p {}".format(path))
        runLocal(rdfModule, args.files_list, args.output, True)
        sys.exit(0)

    #check if batch mode and set start and end file from original list
    runBatch = getElement(rdfModule,"runBatch")

    #check if the process list is specified
    processList = getElement(rdfModule,"processList")

    for process in processList:
        fileList, eventList = getProcessInfo(process, getElement(rdfModule,"prodTag"), getElement(rdfModule, "inputDir"))
        if len(fileList)==0:
            print('----> ERROR: No files to process. Exit')
            sys.exit(3)

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
            print ('----> no values set for process {} will use default values'.format(process))

        print ('----> Running process {} with fraction={}, output={}, chunks={}'.format(process, fraction, output, chunks))

        if fraction<1:fileList = getsubfileList(fileList, eventList, fraction)
        chunkList=[fileList]
        if chunks>1: chunkList = getchunkList(fileList, chunks)

        #create dir if more than 1 chunk
        if chunks>1:
            outputdir=outputDir+"/"+output

            if not os.path.exists(outputdir) and outputdir!='':
                os.system("mkdir -p {}".format(outputdir))

        for ch in range(len(chunkList)):
            outputchunk=''
            if len(chunkList)>1: outputchunk="/{}/chunk{}.root".format(output,ch)
            else:                outputchunk="{}.root".format(output)
            #run locally
            if runBatch == False:
                print ('----> Running Locally')
                runLocal(rdfModule, chunkList[ch], outputchunk, args.batch)

            #run on batch
        if runBatch == True:
            print ('----> Running on Batch')
            if len(chunkList)==1:
                print ('----> \033[4m\033[1m\033[91mWARNING Running on batch with only one chunk might not be optimal\033[0m')
            sendToBatch(rdfModule, chunkList, process, analysisFile)
