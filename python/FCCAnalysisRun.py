import ROOT
import os, sys
import time
import yaml
import glob
import json
import subprocess
import importlib.util
from array import array
import datetime
import numpy as np

from anafile import getElement, getElementDict
from process import getProcessInfo, get_process_dict

DATE = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')

#__________________________________________________________
def get_entries(infilepath):
    '''
    Get number of original entries and number of actual entries in the file
    '''
    infile = ROOT.TFile.Open(infilepath)
    infile.cd()

    processEvents = 0
    try:
        processEvents = infile.Get('eventsProcessed').GetVal()
    except AttributeError:
        print('----> Warning: Input file is missing information about '
              'original number of events!')

    eventsTTree = 0
    try:
        eventsTTree = infile.Get("events").GetEntries()
    except AttributeError:
        print('----> Error: Input file is missing events TTree! Aborting...')
        infile.Close()
        sys.exit(3)

    infile.Close()

    return processEvents, eventsTTree


#__________________________________________________________
def getsubfileList(in_file_list, event_list, fraction):
    nevts_total = sum(event_list)
    nevts_target = int(nevts_total * fraction)

    if nevts_target <= 0:
        print(f'----> Error: The reduction fraction {fraction} too stringent, no events left!')
        print('             Aborting...')
        sys.exit(3)

    nevts_real = 0
    out_file_list = []
    for i in range(len(event_list)):
        if nevts_real >= nevts_target:
            break
        nevts_real += event_list[i]
        out_file_list.append(in_file_list[i])

    print(f'----> Info: Reducing the input file list by fraction "{fraction}" of total events:')
    print(f'             - total number of events: {nevts_total:,}')
    print(f'             - targeted number of events: {nevts_target:,}')
    print(f'             - number of events in the resulting file list: {nevts_real:,}')
    print('             - number of files after reduction: {}'.format(len(out_file_list)))

    return out_file_list


#__________________________________________________________
def getchunkList(fileList, chunks):
    chunk_list = list(np.array_split(fileList, chunks))
    chunk_list = [chunk for chunk in chunk_list if chunk.size > 0]

    return chunk_list


#__________________________________________________________
def saveBenchmark(outfile, benchmark):
    benchmarks = []
    try:
        with open(outfile, 'r') as benchin:
            benchmarks = json.load(benchin)
    except OSError:
        pass

    benchmarks = [b for b in benchmarks if b['name'] != benchmark['name']]
    benchmarks.append(benchmark)

    with open(outfile, 'w') as benchout:
        json.dump(benchmarks, benchout, indent=2)


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
def initialize(args, rdfModule, analysisFile):

    # for convenience and compatibility with user code
    ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")
    geometryFile = getElement(rdfModule, "geometryFile")
    readoutName  = getElement(rdfModule, "readoutName")
    if geometryFile!="" and readoutName!="":
        ROOT.CaloNtupleizer.loadGeometry(geometryFile, readoutName)

    # set multithreading (no MT if number of events is specified)
    ncpus = 1
    if args.nevents < 0:
        if isinstance(args.ncpus, int) and args.ncpus >= 1:
            ncpus = args.ncpus
        else:
            ncpus = getElement(rdfModule, "nCPUS")
        if ncpus < 0: # use all available threads
            ROOT.EnableImplicitMT()
            ncpus = ROOT.GetThreadPoolSize()
        ROOT.ROOT.EnableImplicitMT(ncpus)
    ROOT.EnableThreadSafety()

    if ROOT.IsImplicitMTEnabled():
        print(f'----> Info: Multithreading enabled. Running over '
              f'{ROOT.GetThreadPoolSize()} threads')
    else:
        print('----> Info: No multithreading enabled. Running in single '
              'thread...')

    # custom header files
    includePaths = getElement(rdfModule, "includePaths")
    if includePaths:
        ROOT.gInterpreter.ProcessLine(".O3")
        basepath = os.path.dirname(os.path.abspath(analysisFile))+"/"
        for path in includePaths:
            print(f"----> Info: Loading {path}...")
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')

    # check if analyses plugins need to be loaded before anything
    # still in use?
    analysesList = getElement(rdfModule, "analysesList")
    if analysesList and len(analysesList) > 0:
        _ana = []
        for analysis in analysesList:
            print(f'----> Info: Load cxx analyzers from {analysis}...')
            if analysis.startswith('libFCCAnalysis_'):
                ROOT.gSystem.Load(analysis)
            else:
                ROOT.gSystem.Load(f'libFCCAnalysis_{analysis}')
            if not hasattr(ROOT, analysis):
                print(f'----> ERROR: analysis "{analysis}" not properly loaded. Exit')
                sys.exit(4)
            _ana.append(getattr(ROOT, analysis).dictionary)

#__________________________________________________________
def runRDF(rdfModule, inputlist, outFile, nevt, args):
    df = ROOT.RDataFrame("events", inputlist)

    # limit number of events processed
    if args.nevents > 0:
        df = df.Range(0, args.nevents)

    try:
        df2 = getElement(rdfModule.RDFanalysis, "analysers")(df)

        branch_list = ROOT.vector('string')()
        blist = getElement(rdfModule.RDFanalysis, "output")()
        for bname in blist:
            branch_list.push_back(bname)

        df2.Snapshot("events", outFile, branch_list)
    except Exception as excp:
        print('----> Error: During the execution of the analysis file exception occurred:')
        print(excp)

        sys.exit(3)

    return df2.Count()


#__________________________________________________________
def sendToBatch(rdfModule, chunkList, process, analysisFile):
    localDir = os.environ["LOCAL_DIR"]
    logDir   = localDir+"/BatchOutputs/{}/{}".format(DATE, process)
    if not os.path.exists(logDir):
        os.system("mkdir -p {}".format(logDir))

    # Making sure the FCCAnalyses libraries are compiled and installed
    try:
        subprocess.check_output(['make', 'install'],
                                cwd=localDir+'/build',
                                stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        print("----> The FCCanalyses libraries are not properly build and installed!")
        print('----> Aborting job submission...')
        sys.exit(3)

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
        frun.write('source ' + localDir + '/setup.sh\n')

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
            frun.write(localDir + '/bin/fccanalysis run {} --batch --output {}chunk{}.root --files-list '.format(analysisFile, outputDir, ch))
        else:
            frun.write(localDir + '/bin/fccanalysis run {} --batch --output {}{}/chunk{}.root --files-list '.format(analysisFile, outputDir, process,ch))

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
    frun_condor.write('getenv           = False\n')
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
def apply_filepath_rewrites(filepath):
    '''
    Apply path rewrites if applicable.
    '''

    splitpath = filepath.split('/')
    if len(splitpath) > 1 and splitpath[1] == 'eos':
        if splitpath[2] == 'experiment':
            filepath = 'root://eospublic.cern.ch/' + filepath
        elif splitpath[2] == 'user' or 'home-' in splitpath[2]:
            filepath = 'root://eosuser.cern.ch/' + filepath
        else:
            print('----> Warning: Unknown EOS path type!')
            print('      Please check with the developers as this might impact performance of the analysis.')
    return filepath


#__________________________________________________________
def runLocal(rdfModule, infile_list, args):
    # Create list of files to be processed
    print ('----> Info: Creating dataframe object from files: ', )
    file_list = ROOT.vector('string')()
    nevents_orig = 0   # Amount of events processed in previous stage (= 0 if it is the first stage)
    nevents_local = 0  # The amount of events in the input file(s)
    for filepath in infile_list:

        filepath = apply_filepath_rewrites(filepath)

        file_list.push_back(filepath)
        print(f'             - {filepath}')
        infile = ROOT.TFile.Open(filepath, 'READ')
        try:
            nevents_orig += infile.Get('eventsProcessed').GetVal()
        except AttributeError:
            pass

        try:
            nevents_local += infile.Get("events").GetEntries()
        except AttributeError:
            print('----> Error: Input file:')
            print('             ' + filepath)
            print('             is missing events TTree! Aborting...')
            infile.Close()
            sys.exit(3)

    # Adjust number of events in case --nevents was specified
    if args.nevents > 0 and args.nevents < nevents_local:
        nevents_local = args.nevents

    if nevents_orig > 0:
        print('----> Info: Number of events:')
        print(f'             - original: {nevents_orig}')
        print(f'             - local:    {nevents_local}')
    else:
        print(f'----> Info: Number of local events: {nevents_local}')

    outfilepath = getElement(rdfModule, "outputDir")
    if not args.batch:
        outfilepath += '/' + args.output
    else:
        outfilepath = args.output

    #Run RDF
    start_time = time.time()
    outn = runRDF(rdfModule, file_list, outfilepath, nevents_local, args)
    outn = outn.GetValue()

    outfile = ROOT.TFile(outfilepath, 'update')
    param = ROOT.TParameter(int)('eventsProcessed',
                                 nevents_orig if nevents_orig != 0 else nevents_local)
    param.Write()
    outfile.Write()
    outfile.Close()

    elapsed_time = time.time() - start_time
    print('============================= SUMMARY =============================')
    print('Elapsed time (H:M:S):    ', time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
    print('Events processed/second: ', int(nevents_local/elapsed_time))
    print('Total events processed:  ', int(nevents_local))
    print('No. result events:       ', int(outn))
    if nevents_local > 0:
        print('Reduction factor local:  ', outn/nevents_local)
    if nevents_orig > 0:
        print('Reduction factor total:  ', outn/nevents_orig)
    print('===================================================================\n\n')

    if args.bench:
        analysis_name = getElement(rdfModule, 'analysisName')
        if not analysis_name:
            analysis_name = args.anafile_path

        bench_time = {}
        bench_time['name'] = 'Time spent running the analysis: '
        bench_time['name'] += analysis_name
        bench_time['unit'] = 'Seconds'
        bench_time['value'] = elapsed_time
        bench_time['range'] = 10
        bench_time['extra'] = 'Analysis path: ' + args.anafile_path
        saveBenchmark('benchmarks_smaller_better.json', bench_time)

        bench_evt_per_sec = {}
        bench_evt_per_sec['name'] = 'Events processed per second: '
        bench_evt_per_sec['name'] += analysis_name
        bench_evt_per_sec['unit'] = 'Evt/s'
        bench_evt_per_sec['value'] = nevents_local / elapsed_time
        bench_time['range'] = 1000
        bench_time['extra'] = 'Analysis path: ' + args.anafile_path
        saveBenchmark('benchmarks_bigger_better.json', bench_evt_per_sec)


#__________________________________________________________
def runStages(args, rdfModule, preprocess, analysisFile):
    '''
    Run regular stage.
    '''

    # Set ncpus, load header files, custom dicts, ...
    initialize(args, rdfModule, analysisFile)

    # Check if outputDir exist and if not create it
    outputDir = getElement(rdfModule, "outputDir")
    if not os.path.exists(outputDir) and outputDir:
        os.system("mkdir -p {}".format(outputDir))

    # Check if outputDir exist and if not create it
    outputDirEos = getElement(rdfModule,"outputDirEos")
    if not os.path.exists(outputDirEos) and outputDirEos:
        os.system("mkdir -p {}".format(outputDirEos))

    # Check if test mode is specified, and if so run the analysis on it (this
    # will exit after)
    if args.test:
        print('----> Info: Running over test file...')
        testfile_path = getElement(rdfModule, "testFile")
        directory, _ = os.path.split(args.output)
        if directory:
            os.system("mkdir -p {}".format(directory))
        runLocal(rdfModule, [testfile_path], args)
        sys.exit(0)

    # Check if files are specified, and if so run the analysis on it/them (this
    # will exit after)
    if len(args.files_list) > 0:
        print('----> Info: Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system("mkdir -p {}".format(directory))
        runLocal(rdfModule, args.files_list, args)
        sys.exit(0)

    # Check if batch mode and set start and end file from original list
    run_batch = getElement(rdfModule, "runBatch")

    #check if the process list is specified
    process_list = getElement(rdfModule, "processList")

    for process_name in process_list:
        file_list, event_list = getProcessInfo(process_name,
                                               getElement(rdfModule, "prodTag"),
                                               getElement(rdfModule, "inputDir"))

        if len(file_list) <= 0:
            print('----> Error: No files to process!')
            print('             Aborting...')
            sys.exit(3)

        # Determine the fraction of the input to be processed
        fraction = 1
        if getElementDict(process_list[process_name], 'fraction'):
            fraction = getElementDict(process_list[process_name], 'fraction')
        # Put together output path
        output_stem = process_name
        if getElementDict(process_list[process_name], 'output'):
            output_stem = getElementDict(process_list[process_name], 'output')
        # Determine the number of chunks the output will be split into
        chunks = 1
        if getElementDict(process_list[process_name], 'chunks'):
            chunks = getElementDict(process_list[process_name], 'chunks')

        print('----> Info: Adding process "{}" with:'.format(process_name))
        if fraction < 1:
            print('             - fraction:         {}'.format(fraction))
        print('             - number of files:  {}'.format(len(file_list)))
        print('             - output stem:      {}'.format(output_stem))
        if chunks > 1:
            print('             - number of chunks: {}'.format(chunks))

        if fraction < 1:
            file_list = getsubfileList(file_list, event_list, fraction)

        chunk_list = [file_list]
        if chunks > 1:
            chunk_list = getchunkList(file_list, chunks)
        print('----> Info: Number of the output files: {}'.format(len(chunk_list)))

        # Create directory if more than 1 chunk
        if chunks > 1:
            output_directory = os.path.join(outputDir, output_stem)

            if not os.path.exists(output_directory):
                os.system("mkdir -p {}".format(output_directory))

        if run_batch:
            # Sending to the batch system
            print('----> Info: Running on the batch...')
            if len(chunk_list) == 1:
                print('----> \033[4m\033[1m\033[91mWarning: Running on batch '
                      'with only one chunk might not be optimal\033[0m')

            sendToBatch(rdfModule, chunk_list, process_name, analysisFile)

        else:
            # Running locally
            print('----> Running locally...')
            if len(chunk_list) == 1:
                args.output = '{}.root'.format(output_stem)
                runLocal(rdfModule, chunk_list[0], args)
            else:
                for index, chunk in enumerate(chunk_list):
                    args.output = '/{}/chunk{}.root'.format(output_stem, index)
                    runLocal(rdfModule, chunk, args)


#__________________________________________________________
def testfile(f):
    tf=ROOT.TFile.Open(f)
    tt=None
    try :
        tt=tf.Get("events")
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
    proc_dict_location = getElement(rdfModule, "procDict", True)
    if not proc_dict_location:
        print('----> Error: Location of the procDict not provided. Aborting...')
        sys.exit(3)

    procDict = get_process_dict(proc_dict_location)

    procDictAdd = getElement(rdfModule, "procDictAdd", True)
    for procAdd in procDictAdd:
        if getElementDict(procDict, procAdd) == None:
            procDict[procAdd] = procDictAdd[procAdd]

    ROOT.ROOT.EnableImplicitMT(getElement(rdfModule, "nCPUS", True))

    nevents_real=0
    start_time = time.time()

    processEvents={}
    eventsTTree={}
    processList={}
    saveTab=[]
    efficiencyList=[]

    inputDir = getElement(rdfModule,"inputDir", True)
    if not inputDir:
        print('----> Error: The inputDir variable is mandatory for the final '
              'stage of the analysis!')
        print('             Aborting...')
        sys.exit(3)

    if inputDir[-1]!="/":inputDir+="/"

    outputDir = getElement(rdfModule,"outputDir", True)
    if outputDir!="":
        if outputDir[-1]!="/":outputDir+="/"

    if not os.path.exists(outputDir) and outputDir!='':
        os.system("mkdir -p {}".format(outputDir))

    cutList = getElement(rdfModule,"cutList", True)
    length_cuts_names = max([len(cut) for cut in cutList])
    cutLabels = getElement(rdfModule,"cutLabels", True)

    # save a table in a separate tex file
    saveTabular = getElement(rdfModule,"saveTabular", True)
    if saveTabular:
        # option to rewrite the cuts in a better way for the table. otherwise, take them from the cutList
        if cutLabels:
            cutNames = list(cutLabels.values())
        else:
            cutNames = [cut for cut in cutList]

        cutNames.insert(0, ' ')
        saveTab.append(cutNames)
        efficiencyList.append(cutNames)

    for process_id in getElement(rdfModule, "processList", True):
        processEvents[process_id] = 0
        eventsTTree[process_id] = 0

        fileListRoot = ROOT.vector('string')()
        infilepath = inputDir + process_id + '.root' #input file
        if not os.path.isfile(infilepath):
            print('----> File ', infilepath, '  does not exist. Try if it is a directory as it was processed with batch')
        else:
            print('----> Open file ', infilepath)
            processEvents[process_id], eventsTTree[process_id] = get_entries(infilepath)
            fileListRoot.push_back(infilepath)

        indirpath = inputDir + process_id
        if os.path.isdir(indirpath):
            print('----> Open directory ' + indirpath)
            flist = glob.glob(indirpath + '/chunk*.root')
            for filepath in flist:
                print('        ' + filepath)
                processEvents[process_id], eventsTTree[process_id] = get_entries(filepath)
                fileListRoot.push_back(filepath)
        processList[process_id] = fileListRoot

    print('----> Processed events: {}'.format(processEvents))
    print('----> Events in ttree:  {}'.format(eventsTTree))

    histoList = getElement(rdfModule, "histoList", True)
    doScale = getElement(rdfModule, "doScale", True)
    intLumi = getElement(rdfModule, "intLumi", True)

    doTree = getElement(rdfModule, "doTree", True)
    for pr in getElement(rdfModule, "processList", True):
        print ('\n----> Running over process: ', pr)

        if processEvents[pr] == 0:
            print('----> Error: Can\'t scale histograms, the number of '
                  'processed events for the process {} seems to be '
                  'zero!'.format(pr))
            sys.exit(3)

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
        cuts_list = []
        cuts_list.append(pr)
        eff_list=[]
        eff_list.append(pr)

        # Define all histos, snapshots, etc...
        print ('----> Defining snapshots and histograms')
        for cut in cutList:
            fout = outputDir+pr+'_'+cut+'.root' #output file for tree
            fout_list.append(fout)

            df_cut = df.Filter(cutList[cut])
            count_list.append(df_cut.Count())

            histos = []

            for v in histoList:
                if "name" in histoList[v]: # default 1D histogram
                    model = ROOT.RDF.TH1DModel(v, ";{};".format(histoList[v]["title"]), histoList[v]["bin"], histoList[v]["xmin"], histoList[v]["xmax"])
                    histos.append(df_cut.Histo1D(model,histoList[v]["name"]))
                elif "cols" in histoList[v]: # multi dim histogram (1, 2 or 3D)
                    cols = histoList[v]['cols']
                    bins = histoList[v]['bins']
                    bins_unpacked = tuple([i for sub in bins for i in sub])
                    if len(bins) != len(cols):
                        print ('----> Amount of columns should be equal to the amount of bin configs.')
                        sys.exit(3)
                    if len(cols) == 1:
                        histos.append(df_cut.Histo1D((v, "", *bins_unpacked), cols[0]))
                    elif len(cols) == 2:
                        histos.append(df_cut.Histo2D((v, "", *bins_unpacked), cols[0], cols[1]))
                    elif len(cols) == 3:
                        histos.append(df_cut.Histo3D((v, "", *bins_unpacked), cols[0], cols[1], cols[2]))
                    else:
                        print ('----> Only 1, 2 or 3D histograms supported.')
                        sys.exit(3)
                else:
                    print ('----> Error parsing the histogram config. Provide either name or cols.')
                    sys.exit(3)
            histos_list.append(histos)

            if doTree:
                opts = ROOT.RDF.RSnapshotOptions()
                opts.fLazy = True
                try:
                    snapshot_tdf = df_cut.Snapshot("events", fout, "", opts)
                except Exception as excp:
                    print('----> Error: During the execution of the final stage exception occurred:')

                # Needed to avoid python garbage collector messing around with the snapshot
                tdf_list.append(snapshot_tdf)

        # Now perform the loop and evaluate everything at once.
        print ('----> Evaluating...')
        all_events = df.Count().GetValue()
        print ('----> Done')

        nevents_real += all_events
        uncertainty = ROOT.Math.sqrt(all_events)

        if doScale:
            all_events = all_events*1.*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]*intLumi/processEvents[pr]
            uncertainty = ROOT.Math.sqrt(all_events)*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]*intLumi/processEvents[pr]
            print('  Printing scaled number of events!!! ')

        print ('----> Cutflow')
        print ('       {cutname:{width}} : {nevents}'.format(cutname='All events', width=16+length_cuts_names, nevents=all_events))

        if saveTabular:
            cuts_list.append('{nevents:.2e} $\\pm$ {uncertainty:.2e}'.format(nevents=all_events,uncertainty=uncertainty)) # scientific notation - recomended for backgrounds
            # cuts_list.append('{nevents:.3f} $\\pm$ {uncertainty:.3f}'.format(nevents=all_events,uncertainty=uncertainty)) # float notation - recomended for signals with few events
            eff_list.append(1.) #start with 100% efficiency

        for i, cut in enumerate(cutList):
            neventsThisCut = count_list[i].GetValue()
            neventsThisCut_raw = neventsThisCut
            uncertainty = ROOT.Math.sqrt(neventsThisCut_raw)
            if doScale:
                neventsThisCut = neventsThisCut*1.*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]*intLumi/processEvents[pr]
                uncertainty = ROOT.Math.sqrt(neventsThisCut_raw)*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]*intLumi/processEvents[pr]
            print ('       After selection {cutname:{width}} : {nevents}'.format(cutname=cut, width=length_cuts_names, nevents=neventsThisCut))

            # Saving the number of events, uncertainty and efficiency for the output-file
            if saveTabular and cut != 'selNone':
                if neventsThisCut != 0:
                    cuts_list.append('{nevents:.2e} $\\pm$ {uncertainty:.2e}'.format(nevents=neventsThisCut,uncertainty=uncertainty)) # scientific notation - recomended for backgrounds
                    # cuts_list.append('{nevents:.3f} $\\pm$ {uncertainty:.3f}'.format(nevents=neventsThisCut,uncertainty=uncertainty)) # # float notation - recomended for signals with few events
                    prevNevents = cuts_list[-2].split()
                    eff_list.append('{eff:.3f}'.format(eff=1.*neventsThisCut/all_events))
                # if number of events is zero, the previous uncertainty is saved instead:
                elif '$\\pm$' in cuts_list[-1]:
                    cut = (cuts_list[-1]).split()
                    cuts_list.append('$\\leq$ {uncertainty}'.format(uncertainty=cut[2]))
                    eff_list.append('0.')
                else:
                    cuts_list.append(cuts_list[-1])
                    eff_list.append('0.')

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

        if saveTabular and cut != 'selNone':
            saveTab.append(cuts_list)
            efficiencyList.append(eff_list)

    if saveTabular:
        f = open(outputDir+"outputTabular.txt","w")
        # Printing the number of events in format of a LaTeX table
        print('\\begin{table}[H] \n    \\centering \n    \\resizebox{\\textwidth}{!}{ \n    \\begin{tabular}{|l||',end='',file=f)
        print('c|' * (len(cuts_list)-1),end='',file=f)
        print('} \hline',file=f)
        for i, row in enumerate(saveTab):
            print('        ', end='', file=f)
            print(*row, sep = ' & ', end='', file=f)
            print(' \\\\ ', file=f)
            if (i == 0):
                print('        \\hline',file=f)
        print('        \\hline \n    \\end{tabular}} \n    \\caption{Caption} \n    \\label{tab:my_label} \n\\end{table}', file=f)

        # Efficiency:
        print('\n\nEfficiency: ', file=f)
        print('\\begin{table}[H] \n    \\centering \n    \\resizebox{\\textwidth}{!}{ \n    \\begin{tabular}{|l||',end='',file=f)
        print('c|' * (len(cuts_list)-1),end='',file=f)
        print('} \hline',file=f)
        for i in range(len(eff_list)):
            print('        ', end='', file=f)
            v = [row[i] for row in efficiencyList]
            print(*v, sep = ' & ', end='', file=f)
            print(' \\\\ ', file=f)
            if (i == 0):
                print('        \\hline',file=f)
        print('        \\hline \n    \\end{tabular}} \n    \\caption{Caption} \n    \\label{tab:my_label} \n\\end{table}', file=f)
        f.close()

    elapsed_time = time.time() - start_time
    print  ('==============================SUMMARY==============================')
    print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ('Events Processed/Second  :  ',int(nevents_real/elapsed_time))
    print  ('Total Events Processed   :  ',nevents_real)
    print  ('===================================================================')


def runHistmaker(args, rdfModule, analysisFile):

    # set ncpus, load header files, custom dicts, ...
    initialize(args, rdfModule, analysisFile)

    # load process dictionary
    proc_dict_location = getElement(rdfModule, "procDict", True)
    if not proc_dict_location:
        print('----> Error: Location of the procDict not provided. Aborting...')
        sys.exit(3)

    # check if outputDir exist and if not create it
    outputDir = getElement(rdfModule,"outputDir")
    if not os.path.exists(outputDir) and outputDir!='':
        os.system("mkdir -p {}".format(outputDir))

    doScale = getElement(rdfModule,"doScale", True)
    intLumi = getElement(rdfModule,"intLumi", True)

    # check if the process list is specified, and create graphs for them
    processList = getElement(rdfModule,"processList")
    graph_function = getattr(rdfModule, "build_graph")
    results = [] # all the histograms
    hweights = [] # all the weights
    evtcounts = [] # event count of the input file
    eventsProcessedDict = {} # number of events processed per process, in a potential previous step

    for process in processList:
        fileList, eventList = getProcessInfo(process, getElement(rdfModule,"prodTag"), getElement(rdfModule, "inputDir"))
        if len(fileList)==0:
            print('----> ERROR: No files to process. Exit')
            sys.exit(3)

        # get the number of events processed, in a potential previous step
        fileListRoot = ROOT.vector('string')()
        nevents_meta = 0 # amount of events processed in previous stage (= 0 if it is the first stage)
        for fileName in fileList:
            fsplit = fileName.split('/')
            if len(fsplit) > 1 and fsplit[1]=='eos':
                fileName=addeosType(fileName)
            fileListRoot.push_back(fileName)
            tf=ROOT.TFile.Open(str(fileName),"READ")
            tf.cd()
            for key in tf.GetListOfKeys():
                if 'eventsProcessed' == key.GetName():
                    nevents_meta += tf.eventsProcessed.GetVal()
                    break
        eventsProcessedDict[process] = nevents_meta

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

        if fraction<1:fileList = getsubfileList(fileList, eventList, fraction)
        print ('----> Info: Add process {} with fraction={}, nfiles={}, output={}, chunks={}'.format(process, fraction, len(fileList), output, chunks))

        df = ROOT.ROOT.RDataFrame("events", fileListRoot)
        evtcount = df.Count()
        res, hweight = graph_function(df, process)
        results.append(res)
        hweights.append(hweight)
        evtcounts.append(evtcount)

    print('----> Info: Begin event loop')
    start_time = time.time()
    ROOT.ROOT.RDF.RunGraphs(evtcounts)
    print('----> Info: Done event loop')
    elapsed_time = time.time() - start_time

    print('----> Info: Write output files')
    nevents_tot = 0
    for process, res, hweight, evtcount in zip(processList, results, hweights, evtcounts):
        print(f"----> Info: Write process {process}, nevents processed {evtcount.GetValue()}")
        fOut = ROOT.TFile(f"{outputDir}/{process}.root", "RECREATE")

        # get the cross-sections etc. First try locally, then the procDict
        if 'crossSection' in processList[process]:
            crossSection = processList[process]['crossSection']
        elif process in procDict and 'crossSection' in procDict[process]:
            crossSection = procDict[process]['crossSection']
        else:
            print(f"WARNING: cannot find crossSection for {process} in processList or procDict, use default value of 1")
            crossSection = 1

        if 'kfactor' in processList[process]:
            kfactor = processList[process]['kfactor']
        elif process in procDict and 'kfactor' in procDict[process]:
            kfactor = procDict[process]['kfactor']
        else:
            kfactor = 1

        if 'matchingEfficiency' in processList[process]:
            matchingEfficiency = processList[process]['matchingEfficiency']
        elif process in procDict and 'matchingEfficiency' in procDict[process]:
            matchingEfficiency = procDict[process]['matchingEfficiency']
        else:
            matchingEfficiency = 1

        eventsProcessed = eventsProcessedDict[process] if eventsProcessedDict[process] != 0 else evtcount.GetValue()
        scale = crossSection*kfactor*matchingEfficiency/eventsProcessed

        histsToWrite = {}
        for r in res:
            hist = r.GetValue()
            hName = hist.GetName()
            if hist.GetName() in histsToWrite: # merge histograms in case histogram exists
                histsToWrite[hName].Add(hist)
            else:
                histsToWrite[hName] = hist

        for hist in histsToWrite.values():
            if doScale:
                hist.Scale(scale*intLumi)
            hist.Write()

        # write all meta info to the output file
        p = ROOT.TParameter(int)("eventsProcessed", eventsProcessed)
        p.Write()
        p = ROOT.TParameter(float)("sumOfWeights", hweight.GetValue())
        p.Write()
        p = ROOT.TParameter(float)("intLumi", intLumi)
        p.Write()
        p = ROOT.TParameter(float)("crossSection", crossSection)
        p.Write()
        p = ROOT.TParameter(float)("kfactor", kfactor)
        p.Write()
        p = ROOT.TParameter(float)("matchingEfficiency", matchingEfficiency)
        p.Write()
        nevents_tot += evtcount.GetValue()

    print  ("==============================SUMMARY==============================")
    print  ("Elapsed time (H:M:S)     :  ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ("Events Processed/Second  :  ",int(nevents_tot/elapsed_time))
    print  ("Total Events Processed   :  ",int(nevents_tot))
    print  ("===================================================================")


#__________________________________________________________
def runPlots(analysisFile):
    import doPlots as dp
    dp.run(analysisFile)

#__________________________________________________________
def runValidate(jobdir):
    listdir=os.listdir(jobdir)
    if jobdir[-1]!="/":jobdir+="/"
    for dir in listdir:
        if not os.path.isdir(jobdir+dir): continue
        listfile=glob.glob(jobdir+dir+"/*.sh")
        for file in listfile:
            with open(file) as f:
                for line in f:
                    pass
                lastLine = line
            print(line)


#__________________________________________________________
def setup_run_parser(parser):
    publicOptions = parser.add_argument_group('User options')
    publicOptions.add_argument('anafile_path', help="path to analysis script")
    publicOptions.add_argument("--files-list", help="Specify input file to bypass the processList", default=[], nargs='+')
    publicOptions.add_argument("--output", help="Specify output file name to bypass the processList and or outputList, default output.root", type=str, default="output.root")
    publicOptions.add_argument("--nevents", help="Specify max number of events to process", type=int, default=-1)
    publicOptions.add_argument("--test", action='store_true', help="Run over the test file", default=False)
    publicOptions.add_argument('--bench', action='store_true', help='Output benchmark results to a JSON file', default=False)
    publicOptions.add_argument("--ncpus", help="Set number of threads", type=int)
    publicOptions.add_argument("--final", action='store_true', help="Run final analysis (produces final histograms and trees)", default=False)
    publicOptions.add_argument("--plots", action='store_true', help="Run analysis plots", default=False)
    publicOptions.add_argument("--preprocess", action='store_true', help="Run preprocessing", default=False)
    publicOptions.add_argument("--validate", action='store_true', help="Validate a given production", default=False)
    publicOptions.add_argument("--rerunfailed", action='store_true', help="Rerun failed jobs", default=False)
    publicOptions.add_argument("--jobdir", help="Specify the batch job directory", type=str, default="output.root")
    publicOptions.add_argument("--eloglevel", help="Specify the RDataFrame ELogLevel", type=str, default="kUnset", choices = ['kUnset','kFatal','kError','kWarning','kInfo','kDebug'])
    
    internalOptions = parser.add_argument_group('\033[4m\033[1m\033[91m Internal options, NOT FOR USERS\033[0m')
    internalOptions.add_argument("--batch", action='store_true', help="Submit on batch", default=False)


#__________________________________________________________
def run(mainparser, subparser=None):
    """
    Set things in motion.
    The two parser arguments are a hack to allow running this
    both as `fccanalysis run` and `python config/FCCAnalysisRun.py`
    For the latter case, both are the same (see below).
    """

    if subparser:
        setup_run_parser(subparser)
    args, _ = mainparser.parse_known_args()
    #check that the analysis file exists
    analysisFile = args.anafile_path
    if not os.path.isfile(analysisFile):
        print("Script ", analysisFile, " does not exist")
        print("specify a valid analysis script in the command line arguments")
        sys.exit(3)

    print ("----> Info: Loading analyzers from libFCCAnalyses... ",)
    ROOT.gSystem.Load("libFCCAnalyses")
    ROOT.gErrorIgnoreLevel = ROOT.kFatal
    #Is this still needed?? 01/04/2022 still to be the case
    _fcc = ROOT.dummyLoader

    #set the RDF ELogLevel
    try:
        verbosity = ROOT.Experimental.RLogScopedVerbosity(ROOT.Detail.RDF.RDFLogChannel(), getattr(ROOT.Experimental.ELogLevel,args.eloglevel))
    except AttributeError:
        pass
    #load the analysis
    analysisFile = os.path.abspath(analysisFile)
    print('----> Info: Loading analysis file:')
    print('            ' + analysisFile)
    rdfSpec   = importlib.util.spec_from_file_location("rdfanalysis", analysisFile)
    rdfModule = importlib.util.module_from_spec(rdfSpec)
    rdfSpec.loader.exec_module(rdfModule)

    if hasattr(args, 'command'):
        if args.command == "run":
            if hasattr(rdfModule, "build_graph") and hasattr(rdfModule, "RDFanalysis"):
                print('----> Error: Analysis file ambiguous!')
                print('             Both "RDFanalysis" class and "build_graph" function defined.')
                sys.exit(3)
            elif hasattr(rdfModule, "build_graph") and not hasattr(rdfModule, "RDFanalysis"):
                runHistmaker(args, rdfModule, analysisFile)
            elif not hasattr(rdfModule, "build_graph") and hasattr(rdfModule, "RDFanalysis"):
                runStages(args, rdfModule, args.preprocess, analysisFile)
            else:
                print('----> Error: Analysis file does not contain required objects!')
                print('             Provide either "RDFanalysis" class or "build_graph" function.')
                sys.exit(3)
        elif args.command == "final":
            runFinal(rdfModule)
        elif args.command == "plots":
            runPlots(analysisFile)
        return

    print('----> Info: Running the old way...')
    print('      This way of running the analysis is deprecated and will')
    print('      be removed in the next release!')

    # below is legacy using the old way of runnig with options in
    # "python config/FCCAnalysisRun.py analysis.py --options check if this is
    # final analysis
    if args.final:
        if args.plots:
            print('----> Can not have --plots with --final, exit')
            sys.exit(3)
        if args.preprocess:
            print('----> Can not have --preprocess with --final, exit')
            sys.exit(3)
        runFinal(rdfModule)

    elif args.plots:
        if args.final:
            print('----> Can not have --final with --plots, exit')
            sys.exit(3)
        if args.preprocess:
            print('----> Can not have --preprocess with --plots, exit')
            sys.exit(3)
        runPlots(analysisFile)

    elif args.validate:
        runValidate(args.jobdir)

    else:
        if args.preprocess:
            if args.plots:
                print('----> Can not have --plots with --preprocess, exit')
                sys.exit(3)
            if args.final:
                print('----> Can not have --final with --preprocess, exit')
                sys.exit(3)
        runStages(args, rdfModule, args.preprocess, analysisFile)


#__________________________________________________________
if __name__ == "__main__":
    print("Running this script directly is deprecated, use `fccanalysis run` instead.")
    # legacy behavior: allow running this script directly
    # with python config/FCCAnalysis.py
    # and the same behavior as `fccanalysis run`
    import argparse
    parser = argparse.ArgumentParser()
    run(parser, parser)
