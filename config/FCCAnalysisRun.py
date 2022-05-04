import ROOT
import os, sys
import time
import yaml
import glob
import json
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
def getElement(rdfModule, element, isFinal=False):
    try:
        return getattr(rdfModule, element)
    except AttributeError:

        #return default values or crash if mandatory
        if element=='processList':
            print('The variable <{}> is mandatory in your analysis.py file, will exit'.format(element))
            sys.exit(3)

        elif element=='analysers':
            print('The function <{}> is mandatory in your analysis.py file, will exit'.format(element))
            if isFinal: print('The function <{}> is not part of final analysis'.format(element))
            sys.exit(3)

        elif element=='output':
            print('The function <{}> is mandatory in your analysis.py file, will exit'.format(element))
            if isFinal: print('The function <{}> is not part of final analysis'.format(element))
            sys.exit(3)

        elif element=='nCPUS':
            print('The variable <{}> is optional in your analysis.py file, return default value 4'.format(element))
            return 4

        elif element=='runBatch':
            print('The variable <{}> is optional in your analysis.py file, return default value False'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return False

        elif element=='outputDir':
            print('The variable <{}> is optional in your analysis.py file, return default value running dir'.format(element))
            return ""

        elif element=='batchQueue':
            print('The variable <{}> is optional in your analysys.py file, return default value workday'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return "workday"

        elif element=='compGroup':
             print('The variable <{}> is optional in your analysys.py file, return default value group_u_FCC.local_gen'.format(element))
             if isFinal: print('The option <{}> is not available in final analysis'.format(element))
             return "group_u_FCC.local_gen"

        elif element=='outputDirEos':
            print('The variable <{}> is optional in your analysis.py file, return default empty string'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return ""

        elif element=='eosType':
            print('The variable <{}> is optional in your analysis.py file, return default eospublic'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return "eospublic"

        elif element=='userBatchConfig':
            print('The variable <{}> is optional in your analysis.py file, return default empty string'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return ""

        elif element=='testFile':
            print('The variable <{}> is optional in your analysys.py file, return default file'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_131527278.root"

        elif element=='procDict':
            if isFinal:
                print('The variable <{}> is mandatory in your analysis_final.py file, exit'.format(element))
                sys.exit(3)
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='cutList':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file, return empty dictonary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='defineList':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file, return empty dictonary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='histoList':
            if isFinal:
                print('The variable <{}> is mandatory in your analysis_final.py file, exit'.format(element))
                sys.exit(3)
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='doTree':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file return default value False'.format(element))
                return False
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='procDictAdd':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file return default value {}'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

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
def runPreprocess(df):
    mom_abbrevs = {
    'ReconstructedParticles.momentum.x': 'RP_px',
    'ReconstructedParticles.momentum.y': 'RP_py',
    'ReconstructedParticles.momentum.z': 'RP_pz'
}

    for branch, abbrev in mom_abbrevs.items():
        df.Alias(f'{abbrev}', f'{branch}')

    cols = ROOT.vector('string')()
    cols.push_back("RP_px")
    cols.push_back("RP_py")
    cols.push_back("RP_pz")
    d1 = df.Display(cols)
    d1.Print()
    sys.exit(3)
    return df
#__________________________________________________________
def runRDF(rdfModule, inputlist, outFile, nevt):
    ROOT.ROOT.EnableImplicitMT(getElement(rdfModule, "nCPUS"))
    ROOT.EnableThreadSafety()
    df = ROOT.RDataFrame("events", inputlist)

    preprocess=False
    if preprocess:
        df2 = runPreprocess(df)
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
    logDir   = localDir+"/BatchOutputs/{}".format(process)
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
def runStages(args, rdfModule, preprocess):
    #check if outputDir exist and if not create it
    outputDir = getElement(rdfModule,"outputDir")
    if not os.path.exists(outputDir) and outputDir!='':
        os.system("mkdir -p {}".format(outputDir))

    #check if outputDir exist and if not create it
    outputDirEos = getElement(rdfModule,"outputDirEos")
    if not os.path.exists(outputDirEos) and outputDirEos!='':
        os.system("mkdir -p {}".format(outputDirEos))

    #check if test mode is specified, and if so run the analysis on it (this will exit after)
    if args.test:
        print("----> Running test file mode")
        path, filename = os.path.split(args.output)
        if path!='': os.system("mkdir -p {}".format(path))
        testFile = getElement(rdfModule,"testFile")
        runLocal(rdfModule, [testFile], args.output, True)
        sys.exit(0)

    #check if files are specified, and if so run the analysis on it/them (this will exit after)
    if len(args.files_list)>0:
        print("----> Running with user defined list of files (either locally or from batch)")
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

            if not os.path.exists(outputdir) and outputDir!='':
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


#__________________________________________________________
def testfile(self,f):
    tf=ROOT.TFile.Open(f)
    tt=None
    try :
        tt=tf.Get(self.treename)
        if tt==None:
            print ('file does not contains events, selection was too tight, will skip: ',f)
            return False
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        return False
    except ValueError:
        print ("Could read the file")
        return False
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        print ('file ===%s=== must be deleted'%f)
        return False
    return True

#__________________________________________________________
def runFinal(rdfModule):

    procFile = getElement(rdfModule,"procDict", True)
    procDict = None
    if 'https://fcc-physics-events.web.cern.ch' in procFile:
        print ('----> getting process dictionary from the web')
        import urllib.request
        req = urllib.request.urlopen(procFile).read()
        procDict = json.loads(req.decode('utf-8'))

    else:
        procFile = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + procFile
        if not os.path.isfile(procFile):
            print ('----> No procDict found: ==={}===, exit'.format(procFile))
            sys.exit(3)
        with open(procFile, 'r') as f:
            procDict=json.load(f)


    procDictAdd = getElement(rdfModule,"procDictAdd", True)
    for procAdd in procDictAdd:
        if getElementDict(procDict, procAdd) == None:
            procDict[procAdd] = procDictAdd[procAdd]

    ROOT.ROOT.EnableImplicitMT(getElement(rdfModule,"nCPUS", True))

    nevents_real=0
    start_time = time.time()

    processEvents={}
    eventsTTree={}
    processList={}

    inputDir = getElement(rdfModule,"inputDir", True)
    if inputDir!="":
        if inputDir[-1]!="/":inputDir+="/"

    outputDir = getElement(rdfModule,"outputDir", True)
    if outputDir!="":
        if outputDir[-1]!="/":outputDir+="/"

    if not os.path.exists(outputDir) and outputDir!='':
        os.system("mkdir -p {}".format(outputDir))

    for pr in getElement(rdfModule,"processList", True):
        processEvents[pr]=0
        eventsTTree[pr]=0

        fileListRoot = ROOT.vector('string')()
        fin  = inputDir+pr+'.root' #input file
        if not os.path.isfile(fin):
            print ('----> file ',fin,'  does not exist. Try if it is a directory as it was processed with batch')
        else:
            print ('----> open file ',fin)
            tfin = ROOT.TFile.Open(fin)
            tfin.cd()
            found=False
            for key in tfin.GetListOfKeys():
                if 'eventsProcessed' == key.GetName():
                    events = tfin.eventsProcessed.GetVal()
                    processEvents[pr]=events
                    found=True
            if not found:
                processEvents[pr]=1
            tt=tfin.Get("events")
            eventsTTree[pr]+=tt.GetEntries()

            tfin.Close()
            fileListRoot.push_back(fin)

        if os.path.isdir(inputDir+pr):
            print ('----> open directory ',fin)
            flist=glob.glob(inputDir+pr+"/chunk*.root")
            for f in flist:
                tfin = ROOT.TFile.Open(f)
                print ('  ----> ',f)
                tfin.cd()
                found=False
                for key in tfin.GetListOfKeys():
                    if 'eventsProcessed' == key.GetName():
                        events = tfin.eventsProcessed.GetVal()
                        processEvents[pr]+=events
                        found=True
                if not found:
                    processEvents[pr]=1

                tt=tfin.Get("events")
                eventsTTree[pr]+=tt.GetEntries()
                tfin.Close()
                fileListRoot.push_back(f)
        processList[pr]=fileListRoot

    print('processed events ',processEvents)
    print('events in ttree  ',eventsTTree)

    cutList = getElement(rdfModule,"cutList", True)
    length_cuts_names = max([len(cut) for cut in cutList])

    histoList = getElement(rdfModule,"histoList", True)

    doTree = getElement(rdfModule,"doTree", True)
    for pr in getElement(rdfModule,"processList", True):
        print ('\n---->  Running over process : ',pr)

        RDF = ROOT.ROOT.RDataFrame
        df  = RDF("events", processList[pr])
        defineList = getElement(rdfModule,"defineList", True)
        if len(defineList)>0:
            print ('----> Running extra Define')
            for define in defineList:
                df=df.Define(define, defineList[define])

        fout_list = []
        histos_list = []
        tdf_list = []
        count_list = []

        # Define all histos, snapshots, etc...
        print ('----> Defining snapshots and histograms')
        for cut in cutList:
            fout = outputDir+pr+'_'+cut+'.root' #output file for tree
            fout_list.append(fout)

            df_cut = df.Filter(cutList[cut])
            count_list.append(df_cut.Count())

            histos = []

            for v in histoList:
                model = ROOT.RDF.TH1DModel(v, ";{};".format(histoList[v]["title"]), histoList[v]["bin"], histoList[v]["xmin"], histoList[v]["xmax"])
                histos.append(df_cut.Histo1D(model,histoList[v]["name"]))
            histos_list.append(histos)

            if doTree:
                opts = ROOT.RDF.RSnapshotOptions()
                opts.fLazy = True
                snapshot_tdf = df_cut.Snapshot(self.treename, fout, "", opts)
                # Needed to avoid python garbage collector messing around with the snapshot
                tdf_list.append(snapshot_tdf)

        # Now perform the loop and evaluate everything at once.
        print ('----> Evaluating...')
        all_events = df.Count().GetValue()
        print ('----> Done')

        nevents_real += all_events

        print ('----> Cutflow')
        print ('       {cutname:{width}} : {nevents}'.format(cutname='All events', width=16+length_cuts_names, nevents=all_events))
        for i, cut in enumerate(cutList):
            print ('       After selection {cutname:{width}} : {nevents}'.format(cutname=cut, width=length_cuts_names, nevents=count_list[i].GetValue()))

        # And save everything
        print ('----> Saving outputs')
        for i, cut in enumerate(cutList):
            fhisto = outputDir+pr+'_'+cut+'_histo.root' #output file for histograms
            tf    = ROOT.TFile.Open(fhisto,'RECREATE')
            for h in histos_list[i]:
                try :
                    h.Scale(1.*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]/processEvents[pr])
                except KeyError:
                    print ('----> No value defined for process {} in dictionary'.format(pr))
                    if h.Integral(0,-1)>0:h.Scale(1./h.Integral(0,-1))
                h.Write()
            tf.Close()

            if doTree:
                # test that the snapshot worked well
                validfile = testfile(fout_list[i])
                if not validfile: continue


    elapsed_time = time.time() - start_time
    print  ('==============================SUMMARY==============================')
    print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ('Events Processed/Second  :  ',int(nevents_real/elapsed_time))
    print  ('Total Events Processed   :  ',nevents_real)
    print  ('===================================================================')


#__________________________________________________________
def runPlots(analysisFile):

    import config.doPlots as dp
    dp.run(analysisFile)

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
    publicOptions.add_argument("--output", help="Specify output file name to bypass the processList and or outputList, default output.root", type=str, default="output.root")
    publicOptions.add_argument("--test", action='store_true', help="Run over the test file", default=False)
    publicOptions.add_argument("--final", action='store_true', help="Run final analysis (produces final histograms and trees)", default=False)
    publicOptions.add_argument("--plots", action='store_true', help="Run analysis plots", default=False)
    publicOptions.add_argument("--preprocess", action='store_true', help="Run preprocessing", default=False)

    internalOptions = parser.add_argument_group('\033[4m\033[1m\033[91m Internal options, NOT FOR USERS\033[0m')
    internalOptions.add_argument("--batch", action='store_true', help="Submit on batch", default=False)

    args, _ = parser.parse_known_args()
    #check that the analysis file exists
    analysisFile = sys.argv[1]
    if not os.path.isfile(analysisFile):
        print(sys.argv[1], " does not exist")
        print("syntax should be: ")
        print("python config/FCCAnalysisRun.py analysis.py <options>")
        sys.exit(3)

    #load the analysis
    analysisFile=os.path.abspath(analysisFile)
    rdfSpec   = importlib.util.spec_from_file_location("rdfanalysis", analysisFile)
    rdfModule = importlib.util.module_from_spec(rdfSpec)
    rdfSpec.loader.exec_module(rdfModule)

    #check if this is final analysis
    if args.final:
        if args.plots:
            print ('----> Can not have --plots with --final, exit')
            sys.exit(3)
        if args.preprocess:
            print ('----> Can not have --preprocess with --final, exit')
            sys.exit(3)
        runFinal(rdfModule)

    elif args.plots:
        if args.final:
            print ('----> Can not have --final with --plots, exit')
            sys.exit(3)
        if args.preprocess:
            print ('----> Can not have --preprocess with --plots, exit')
            sys.exit(3)
        runPlots(analysisFile)

    else:
        if args.preprocess:
            if args.plots:
                print ('----> Can not have --plots with --preprocess, exit')
                sys.exit(3)
            if args.final:
                print ('----> Can not have --final with --preprocess, exit')
                sys.exit(3)
        runStages(args, rdfModule, args.preprocess)
