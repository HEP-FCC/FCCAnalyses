import os
import sys
import time
import yaml
import glob
import json
import logging
import subprocess
import importlib.util
import datetime
import numpy as np

import ROOT
from anafile import getElement, getElementDict
from process import getProcessInfo, get_process_dict

LOGGER = logging.getLogger('FCCAnalyses.run')

ROOT.gROOT.SetBatch(True)

# __________________________________________________________
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
        LOGGER.warning('Input file is missing information about '
                       'original number of events!')

    eventsTTree = 0
    try:
        eventsTTree = infile.Get("events").GetEntries()
    except AttributeError:
        LOGGER.error('Input file is missing "events" TTree!\nAborting...')
        infile.Close()
        sys.exit(3)

    infile.Close()

    return processEvents, eventsTTree


# __________________________________________________________
def getsubfileList(in_file_list, event_list, fraction):
    nevts_total = sum(event_list)
    nevts_target = int(nevts_total * fraction)

    if nevts_target <= 0:
        LOGGER.error('The reduction fraction %f too stringent, no events '
                     'left!\nAborting...', fraction)
        sys.exit(3)

    nevts_real = 0
    out_file_list = []
    for i in range(len(event_list)):
        if nevts_real >= nevts_target:
            break
        nevts_real += event_list[i]
        out_file_list.append(in_file_list[i])

    info_msg = f'Reducing the input file list by fraction "{fraction}" of '
    info_msg += 'total events:\n\t'
    info_msg += f'- total number of events: {nevts_total:,}\n\t'
    info_msg += f'- targeted number of events: {nevts_target:,}\n\t'
    info_msg += '- number of events in the resulting file list: '
    info_msg += f'{nevts_real:,}\n\t'
    info_msg += '- number of files after reduction: '
    info_msg += str((len(out_file_list)))
    LOGGER.info(info_msg)

    return out_file_list


# __________________________________________________________
def getchunkList(fileList, chunks):
    chunk_list = list(np.array_split(fileList, chunks))
    chunk_list = [chunk for chunk in chunk_list if chunk.size > 0]

    return chunk_list


# __________________________________________________________
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


# __________________________________________________________
def SubmitToCondor(cmd,nbtrials):
    submissionStatus=0
    cmd=cmd.replace('//','/') # -> dav : is it needed?
    for i in range(nbtrials):
        outputCMD = getCommandOutput(cmd)
        stderr=outputCMD["stderr"].split('\n')
        stdout=outputCMD["stdout"].split('\n') # -> dav : is it needed?

        if len(stderr)==1 and stderr[0]=='' :
            LOGGER.info('GOOD SUBMISSION')
            submissionStatus=1
        else:
            LOGGER.warning('Error while submitting, retrying...\n\t'
                           'Trial: %i / %i\n\tError: %s', i, nbtrials, stderr)
            time.sleep(10)

        if submissionStatus == 1:
            return 1

        if i == nbtrials-1:
            LOGGER.error('Failed submitting after: %i trials, stop trying to '
                         'submit', nbtrials)
            return 0

# __________________________________________________________
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
        if ncpus < 0:  # use all available threads
            ROOT.EnableImplicitMT()
            ncpus = ROOT.GetThreadPoolSize()
        ROOT.ROOT.EnableImplicitMT(ncpus)
    ROOT.EnableThreadSafety()

    if ROOT.IsImplicitMTEnabled():
        LOGGER.info('Multithreading enabled. Running over %i threads',
                    ROOT.GetThreadPoolSize())
    else:
        LOGGER.info('No multithreading enabled. Running in single thread...')

    # custom header files
    includePaths = getElement(rdfModule, "includePaths")
    if includePaths:
        ROOT.gInterpreter.ProcessLine(".O3")
        basepath = os.path.dirname(os.path.abspath(analysisFile))+"/"
        for path in includePaths:
            LOGGER.info('Loading %s...', path)
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')

    # check if analyses plugins need to be loaded before anything
    # still in use?
    analysesList = getElement(rdfModule, "analysesList")
    if analysesList and len(analysesList) > 0:
        _ana = []
        for analysis in analysesList:
            LOGGER.info('Load cxx analyzers from %s...', analysis)
            if analysis.startswith('libFCCAnalysis_'):
                ROOT.gSystem.Load(analysis)
            else:
                ROOT.gSystem.Load(f'libFCCAnalysis_{analysis}')
            if not hasattr(ROOT, analysis):
                ROOT.error('Analysis %s not properly loaded!\nAborting...',
                           analysis)
                sys.exit(4)
            _ana.append(getattr(ROOT, analysis).dictionary)

# __________________________________________________________
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
        LOGGER.error('During the execution of the analysis file exception '
                     'occurred:\n%s', excp)
        sys.exit(3)

    return df2.Count()


# __________________________________________________________
def sendToBatch(rdfModule, chunkList, process, analysisFile):
    localDir = os.environ["LOCAL_DIR"]
    current_date = datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')
    logDir = localDir + "/BatchOutputs/{}/{}".format(current_date, process)
    if not os.path.exists(logDir):
        os.system("mkdir -p {}".format(logDir))

    # Making sure the FCCAnalyses libraries are compiled and installed
    try:
        subprocess.check_output(['make', 'install'],
                                cwd=localDir+'/build',
                                stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        LOGGER.error('The FCCanalyses libraries are not properly build and '
                     'installed!\nAborting job submission...')
        sys.exit(3)

    outputDir       = getElement(rdfModule, "outputDir")
    outputDirEos    = getElement(rdfModule, "outputDirEos")
    eosType         = getElement(rdfModule, "eosType")
    userBatchConfig = getElement(rdfModule, "userBatchConfig")

    if outputDir!="" and outputDir[-1]!="/": outputDir+="/"

    condor_file_str = ''
    for ch in range(len(chunkList)):
        frunname = '{}/job{}_chunk{}.sh'.format(logDir, process, ch)
        LOGGER.info('Script to run %s: ', frunname)
        condor_file_str += frunname + " "

        frun = None
        try:
            frun = open(frunname, 'w')
        except IOError as e:
            LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
            time.sleep(10)
            frun = open(frunname, 'w')

        subprocess.getstatusoutput('chmod 777 %s'%(frunname))
        frun.write('#!/bin/bash\n')
        frun.write('source ' + localDir + '/setup.sh\n')

        # add userBatchConfig if any
        if userBatchConfig != "":
            if not os.path.isfile(userBatchConfig):
                LOGGER.warning('userBatchConfig file does not exist, will not '
                               'add it to default config, please check')
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
        LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
        time.sleep(10)
        frun_condor = open(frunfull_condor, 'w')
    sysVer_str = ''
    try:
        f_make = open(localDir+'/build/CMakeFiles/CMakeConfigureLog.yaml', 'r')
    except IOError as e:
        LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
        LOGGER.warning('File not found: ' + localDir+'/build/CMakeFiles/CMakeConfigureLog.yaml')
    else:
        with open(localDir+'/build/CMakeFiles/CMakeConfigureLog.yaml', 'r') as makeConfig:
            make_content = makeConfig.read()
            if 'centos7' in make_content:
                sysVer_str = '(OpSysAndVer =?= "CentOS7")' + ' &&'
            if 'almalinux9' in make_content:
                sysVer_str = '(OpSysAndVer =?= "AlmaLinux9")' + ' &&'
    if sysVer_str == '':
        LOGGER.warning('FCCAnalysis was compiled in an environment not available in lxplus HTcondor. Please check.'
                       'Submitting jobs to default operating system. There may be compatibility issues.')
    subprocess.getstatusoutput('chmod 777 {}'.format(frunfull_condor))
    frun_condor.write('executable       = $(filename)\n')
    frun_condor.write('Log              = {}/condor_job.{}.$(ClusterId).$(ProcId).log\n'.format(logDir,process))
    frun_condor.write('Output           = {}/condor_job.{}.$(ClusterId).$(ProcId).out\n'.format(logDir,process))
    frun_condor.write('Error            = {}/condor_job.{}.$(ClusterId).$(ProcId).error\n'.format(logDir,process))
    frun_condor.write('getenv           = False\n')
    frun_condor.write('environment      = "LS_SUBCWD={}"\n'.format(logDir)) # not sure
    frun_condor.write('requirements     = ({} (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n'.format(sysVer_str))
    frun_condor.write('on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n')
    frun_condor.write('max_retries      = 3\n')
    frun_condor.write('+JobFlavour      = "{}"\n'.format(getElement(rdfModule, "batchQueue")))
    frun_condor.write('+AccountingGroup = "{}"\n'.format(getElement(rdfModule, "compGroup")))
    frun_condor.write('RequestCpus      = {}\n'.format(getElement(rdfModule, "nCPUS")))
    frun_condor.write('queue filename matching files {}\n'.format(condor_file_str))
    frun_condor.close()

    cmdBatch="condor_submit {}".format(frunfull_condor)
    LOGGER.info('Batch command: %s', cmdBatch)
    job=SubmitToCondor(cmdBatch, 10)


#__________________________________________________________
def apply_filepath_rewrites(filepath):
    '''
    Apply path rewrites if applicable.
    '''
    # Stripping leading and trailing white spaces
    filepath_stripped = filepath.strip()
    # Stripping leading and trailing slashes
    filepath_stripped = filepath_stripped.strip('/')

    # Splitting the path along slashes
    filepath_splitted = filepath_stripped.split('/')

    if len(filepath_splitted) > 1 and filepath_splitted[0] == 'eos':
        if filepath_splitted[1] == 'experiment':
            filepath = 'root://eospublic.cern.ch//' + filepath_stripped
        elif filepath_splitted[1] == 'user':
            filepath = 'root://eosuser.cern.ch//' + filepath_stripped
        elif 'home-' in filepath_splitted[1]:
            filepath = 'root://eosuser.cern.ch//eos/user/' + \
                       filepath_stripped.replace('eos/home-', '')
        else:
            LOGGER.warning('Unknown EOS path type!\nPlease check with the '
                           'developers as this might impact performance of '
                           'the analysis.')
    return filepath


# __________________________________________________________
def runLocal(rdfModule, infile_list, args):
    # Create list of files to be processed
    info_msg = 'Creating dataframe object from files:\n\t'
    file_list = ROOT.vector('string')()
    nevents_orig = 0   # Amount of events processed in previous stage (= 0 if it is the first stage)
    nevents_local = 0  # The amount of events in the input file(s)
    for filepath in infile_list:

        filepath = apply_filepath_rewrites(filepath)

        file_list.push_back(filepath)
        info_msg += f'- {filepath}\t\n'
        infile = ROOT.TFile.Open(filepath, 'READ')
        try:
            nevents_orig += infile.Get('eventsProcessed').GetVal()
        except AttributeError:
            pass

        try:
            nevents_local += infile.Get("events").GetEntries()
        except AttributeError:
            LOGGER.error('Input file:\n%s\nis missing events TTree!\n'
                         'Aborting...', filepath)
            infile.Close()
            sys.exit(3)

    LOGGER.info(info_msg)

    # Adjust number of events in case --nevents was specified
    if args.nevents > 0 and args.nevents < nevents_local:
        nevents_local = args.nevents

    if nevents_orig > 0:
        LOGGER.info('Number of events:\n\t- original: %s\n\t- local:    %s',
                    f'{nevents_orig:,}', f'{nevents_local:,}')
    else:
        LOGGER.info('Number of local events: %s', f'{nevents_local:,}')

    output_dir = getElement(rdfModule, "outputDir")
    if not args.batch:
        if os.path.isabs(args.output):
            LOGGER.warning('Provided output path is absolute, "outputDir" '
                           'from analysis script will be ignored!')
        outfile_path = os.path.join(output_dir, args.output)
    else:
        outfile_path = args.output
    LOGGER.info('Output file path:\n%s', outfile_path)

    # Run RDF
    start_time = time.time()
    outn = runRDF(rdfModule, file_list, outfile_path, nevents_local, args)
    outn = outn.GetValue()

    outfile = ROOT.TFile(outfile_path, 'update')
    param = ROOT.TParameter(int)(
            'eventsProcessed',
            nevents_orig if nevents_orig != 0 else nevents_local)
    param.Write()
    outfile.Write()
    outfile.Close()

    elapsed_time = time.time() - start_time
    info_msg = f"{' SUMMARY ':=^80}\n"
    info_msg += 'Elapsed time (H:M:S):    '
    info_msg += time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    info_msg += '\nEvents processed/second: '
    info_msg += f'{int(nevents_local/elapsed_time):,}'
    info_msg += f'\nTotal events processed:  {int(nevents_local):,}'
    info_msg += f'\nNo. result events:       {int(outn):,}'
    if nevents_local > 0:
        info_msg += f'\nReduction factor local:  {outn/nevents_local}'
    if nevents_orig > 0:
        info_msg += f'\nReduction factor total:  {outn/nevents_orig}'
    info_msg += '\n'
    info_msg += 80 * '='
    info_msg += '\n'
    LOGGER.info(info_msg)

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
        LOGGER.info('Running over test file...')
        testfile_path = getElement(rdfModule, "testFile")
        directory, _ = os.path.split(args.output)
        if directory:
            os.system("mkdir -p {}".format(directory))
        runLocal(rdfModule, [testfile_path], args)
        sys.exit(0)

    # Check if files are specified, and if so run the analysis on it/them (this
    # will exit after)
    if len(args.files_list) > 0:
        LOGGER.info('Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        runLocal(rdfModule, args.files_list, args)
        sys.exit(0)

    # Check if batch mode and set start and end file from original list
    run_batch = getElement(rdfModule, "runBatch")

    # Check if the process list is specified
    process_list = getElement(rdfModule, "processList")

    for process_name in process_list:
        file_list, event_list = getProcessInfo(
            process_name,
            getElement(rdfModule, "prodTag"),
            getElement(rdfModule, "inputDir"))

        if len(file_list) <= 0:
            LOGGER.error('No files to process!\nAborting...')
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

        info_msg = f'Adding process "{process_name}" with:'
        if fraction < 1:
            info_msg += f'\n\t- fraction:         {fraction}'
        info_msg += f'\n\t- number of files:  {len(file_list):,}'
        info_msg += f'\n\t- output stem:      {output_stem}'
        if chunks > 1:
            info_msg += f'\n\t- number of chunks: {chunks}'

        if fraction < 1:
            file_list = getsubfileList(file_list, event_list, fraction)

        chunk_list = [file_list]
        if chunks > 1:
            chunk_list = getchunkList(file_list, chunks)
        LOGGER.info('Number of the output files: %s', f'{len(chunk_list):,}')

        # Create directory if more than 1 chunk
        if chunks > 1:
            output_directory = os.path.join(outputDir, output_stem)

            if not os.path.exists(output_directory):
                os.system("mkdir -p {}".format(output_directory))

        if run_batch:
            # Sending to the batch system
            LOGGER.info('Running on the batch...')
            if len(chunk_list) == 1:
                LOGGER.warning('\033[4m\033[1m\033[91mRunning on batch with '
                               'only one chunk might not be optimal\033[0m')

            sendToBatch(rdfModule, chunk_list, process_name, analysisFile)

        else:
            # Running locally
            LOGGER.info('Running locally...')
            if len(chunk_list) == 1:
                args.output = '{}.root'.format(output_stem)
                runLocal(rdfModule, chunk_list[0], args)
            else:
                for index, chunk in enumerate(chunk_list):
                    args.output = '{}/chunk{}.root'.format(output_stem, index)
                    runLocal(rdfModule, chunk, args)


# __________________________________________________________
def testfile(f):
    tf=ROOT.TFile.Open(f)
    tt=None
    try:
        tt=tf.Get("events")
        if tt == None:
            LOGGER.warning('File does not contains events, selection was too '
                           'tight, skipping it: %s', f)
            return False
    except IOError as e:
        LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
        return False
    except ValueError:
        LOGGER.warning('Could read the file')
        return False
    except:
        LOGGER.warning('Unexpected error: %s\nfile ===%s=== must be deleted',
                       sys.exc_info()[0], f)
        return False
    return True


# __________________________________________________________
def runFinal(rdfModule):
    proc_dict_location = getElement(rdfModule, "procDict", True)
    if not proc_dict_location:
        LOGGER.error('Location of the procDict not provided!\nAborting...')
        sys.exit(3)

    procDict = get_process_dict(proc_dict_location)

    procDictAdd = getElement(rdfModule, "procDictAdd", True)
    for procAdd in procDictAdd:
        if getElementDict(procDict, procAdd) == None:
            procDict[procAdd] = procDictAdd[procAdd]

    ROOT.ROOT.EnableImplicitMT(getElement(rdfModule, "nCPUS", True))

    nevents_real = 0
    start_time = time.time()

    processEvents={}
    eventsTTree={}
    processList={}
    saveTab=[]
    efficiencyList=[]

    inputDir = getElement(rdfModule,"inputDir", True)
    if not inputDir:
        LOGGER.error('The inputDir variable is mandatory for the final stage '
                     'of the analysis!\nAborting...')
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
        infilepath = inputDir + process_id + '.root'  # input file
        if not os.path.isfile(infilepath):
            LOGGER.warning('File %s does not exist!\nTrying if it is a '
                           'directory as it was processed with batch.',
                           infilepath)
        else:
            LOGGER.info('Open file:\n\t%s', infilepath)
            processEvents[process_id], eventsTTree[process_id] = get_entries(infilepath)
            fileListRoot.push_back(infilepath)

        indirpath = inputDir + process_id
        if os.path.isdir(indirpath):
            info_msg = f'Open directory {indirpath}'
            flist = glob.glob(indirpath + '/chunk*.root')
            for filepath in flist:
                info_msg += '\n\t' + filepath
                chunkProcessEvents, chunkEventsTTree = get_entries(filepath)
                processEvents[process_id] += chunkProcessEvents
                eventsTTree[process_id] += chunkEventsTTree
                fileListRoot.push_back(filepath)
            LOGGER.info(info_msg)
        processList[process_id] = fileListRoot

    info_msg = 'Processed events:'
    for process_id, n_events in processEvents.items():
        info_msg += f'\n\t- {process_id}: {n_events:,}'
    LOGGER.info(info_msg)
    info_msg = 'Events in the TTree:'
    for process_id, n_events in eventsTTree.items():
        info_msg += f'\n\t- {process_id}: {n_events:,}'
    LOGGER.info(info_msg)

    histoList = getElement(rdfModule, "histoList", True)
    doScale = getElement(rdfModule, "doScale", True)
    intLumi = getElement(rdfModule, "intLumi", True)

    doTree = getElement(rdfModule, "doTree", True)
    for pr in getElement(rdfModule, "processList", True):
        LOGGER.info('Running over process: %s', pr)

        if processEvents[pr] == 0:
            LOGGER.error('Can\'t scale histograms, the number of processed '
                         'events for the process "%s" seems to be zero!', pr)
            sys.exit(3)

        RDF = ROOT.ROOT.RDataFrame
        df  = RDF("events", processList[pr])
        defineList = getElement(rdfModule,"defineList", True)
        if len(defineList) > 0:
            LOGGER.info('Registering extra DataFrame defines...')
            for define in defineList:
                df = df.Define(define, defineList[define])

        fout_list = []
        histos_list = []
        tdf_list = []
        count_list = []
        cuts_list = []
        cuts_list.append(pr)
        eff_list = []
        eff_list.append(pr)

        # Define all histos, snapshots, etc...
        LOGGER.info('Defining snapshots and histograms')
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
                        LOGGER.error('Amount of columns should be equal to '
                                     'the amount of bin configs!\nAborting...')
                        sys.exit(3)
                    if len(cols) == 1:
                        histos.append(df_cut.Histo1D((v, "", *bins_unpacked), cols[0]))
                    elif len(cols) == 2:
                        histos.append(df_cut.Histo2D((v, "", *bins_unpacked), cols[0], cols[1]))
                    elif len(cols) == 3:
                        histos.append(df_cut.Histo3D((v, "", *bins_unpacked), cols[0], cols[1], cols[2]))
                    else:
                        LOGGER.error('Only 1, 2 or 3D histograms supported.')
                        sys.exit(3)
                else:
                    LOGGER.error('Error parsing the histogram config. Provide '
                                 'either name or cols.')
                    sys.exit(3)
            histos_list.append(histos)

            if doTree:
                opts = ROOT.RDF.RSnapshotOptions()
                opts.fLazy = True
                try:
                    snapshot_tdf = df_cut.Snapshot("events", fout, "", opts)
                except Exception as excp:
                    LOGGER.error('During the execution of the final stage '
                                 'exception occurred:\n%s', excp)
                    sys.exit(3)

                # Needed to avoid python garbage collector messing around with
                # the snapshot
                tdf_list.append(snapshot_tdf)

        # Now perform the loop and evaluate everything at once.
        LOGGER.info('Evaluating...')
        all_events = df.Count().GetValue()
        LOGGER.info('Done')

        nevents_real += all_events
        uncertainty = ROOT.Math.sqrt(all_events)

        if doScale:
            all_events = all_events*1.*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]*intLumi/processEvents[pr]
            uncertainty = ROOT.Math.sqrt(all_events)*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]*intLumi/processEvents[pr]
            LOGGER.info('Printing scaled number of events!!!')

        cfn_width = 16 + length_cuts_names  # Cutflow name width
        info_msg = 'Cutflow:'
        info_msg += f'\n\t{"All events":{cfn_width}} : {all_events:,}'

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
            info_msg += f'\n\t{"After selection " + cut:{cfn_width}} : '
            info_msg += f'{neventsThisCut:,}'

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

        LOGGER.info(info_msg)

        # And save everything
        LOGGER.info('Saving the outputs...')
        for i, cut in enumerate(cutList):
            fhisto = outputDir+pr+'_'+cut+'_histo.root' #output file for histograms
            tf    = ROOT.TFile.Open(fhisto,'RECREATE')
            for h in histos_list[i]:
                try :
                    h.Scale(1.*procDict[pr]["crossSection"]*procDict[pr]["kfactor"]*procDict[pr]["matchingEfficiency"]/processEvents[pr])
                except KeyError:
                    LOGGER.warning(
                        'No value defined for process %s in dictionary!', pr)
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

    info_msg = f"{' SUMMARY ':=^80}\n"
    info_msg += 'Elapsed time (H:M:S):    '
    info_msg += time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    info_msg += '\nEvents processed/second: '
    info_msg += f'{int(nevents_real/elapsed_time):,}'
    info_msg += f'\nTotal events processed:  {nevents_real:,}'
    info_msg += '\n'
    info_msg += 80 * '='
    info_msg += '\n'
    LOGGER.info(info_msg)


def runHistmaker(args, rdfModule, analysisFile):

    # set ncpus, load header files, custom dicts, ...
    initialize(args, rdfModule, analysisFile)

    # load process dictionary
    proc_dict_location = getElement(rdfModule, "procDict", True)
    if not proc_dict_location:
        LOGGER.error('Location of the procDict not provided.\nAborting...')
        sys.exit(3)

    procDict = get_process_dict(proc_dict_location) 

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
        if len(fileList) == 0:
            LOGGER.error('No files to process!\nAborting...')
            sys.exit(3)
        processDict={}
        fraction = 1
        output = process
        chunks = 1
        try:
            processDict = processList[process]
            if getElementDict(processList[process], 'fraction') != None: fraction = getElementDict(processList[process], 'fraction')
            if getElementDict(processList[process], 'output')   != None: output   = getElementDict(processList[process], 'output')
            if getElementDict(processList[process], 'chunks')   != None: chunks   = getElementDict(processList[process], 'chunks')
        except TypeError:
            LOGGER.warning('No values set for process %s will use default '
                           'values!', process)
        if fraction < 1:fileList = getsubfileList(fileList, eventList, fraction)

        # get the number of events processed, in a potential previous step
        fileListRoot = ROOT.vector('string')()
        nevents_meta = 0 # amount of events processed in previous stage (= 0 if it is the first stage)
        for fileName in fileList:
            fileName = apply_filepath_rewrites(fileName)
            fileListRoot.push_back(fileName)
            if getElement(rdfModule,"prodTag") == None: # skip check for processed events in case of first stage
                tf=ROOT.TFile.Open(str(fileName),"READ")
                tf.cd()
                for key in tf.GetListOfKeys():
                    if 'eventsProcessed' == key.GetName():
                        nevents_meta += tf.eventsProcessed.GetVal()
                        break
            if args.test:
                break
        eventsProcessedDict[process] = nevents_meta
        info_msg = f'Add process "{process}" with:'
        info_msg += f'\n\tfraction = {fraction}'
        info_msg += f'\n\tnFiles = {len(fileListRoot):,}'
        info_msg += f'\n\toutput = {output}\n\tchunks = {chunks}'
        LOGGER.info(info_msg)

        df = ROOT.ROOT.RDataFrame("events", fileListRoot)
        evtcount = df.Count()
        res, hweight = graph_function(df, process)
        results.append(res)
        hweights.append(hweight)
        evtcounts.append(evtcount)

    LOGGER.info('Starting the event loop...')
    start_time = time.time()
    ROOT.ROOT.RDF.RunGraphs(evtcounts)
    LOGGER.info('Event loop done!')
    elapsed_time = time.time() - start_time

    LOGGER.info('Writing out output files...')
    nevents_tot = 0
    for process, res, hweight, evtcount in zip(processList, results, hweights, evtcounts):
        LOGGER.info('Writing out process %s, nEvents processed %s',
                    process, f'{evtcount.GetValue():,}')
        fOut = ROOT.TFile(f"{outputDir}/{process}.root", "RECREATE")

        # get the cross-sections etc. First try locally, then the procDict
        if 'crossSection' in processList[process]:
            crossSection = processList[process]['crossSection']
        elif process in procDict and 'crossSection' in procDict[process]:
            crossSection = procDict[process]['crossSection']
        else:
            LOGGER.warning('Can\'t find cross-section for process %s in '
                           'processList or procDict!\nUsing default value of 1'
                           , process)
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

    info_msg = f"{' SUMMARY ':=^80}\n"
    info_msg += 'Elapsed time (H:M:S):    '
    info_msg += time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    info_msg += '\nEvents processed/second: '
    info_msg += f'{int(nevents_tot/elapsed_time):,}'
    info_msg += f'\nTotal events processed:  {nevents_tot:,}'
    info_msg += '\n'
    info_msg += 80 * '='
    info_msg += '\n'
    LOGGER.info(info_msg)


# __________________________________________________________
def runPlots(analysisFile):
    import doPlots as dp
    dp.run(analysisFile)


def run(parser):
    '''
    Set things in motion.
    '''

    args, _ = parser.parse_known_args()

    # Check that the analysis file exists
    analysisFile = args.anafile_path
    if not os.path.isfile(analysisFile):
        LOGGER.error('Analysis script %s not found!\nAborting...',
                     analysisFile)
        sys.exit(3)

    # Load pre compiled analyzers
    LOGGER.info('Loading analyzers from libFCCAnalyses...')
    ROOT.gSystem.Load("libFCCAnalyses")
    # Is this still needed?? 01/04/2022 still to be the case
    _fcc = ROOT.dummyLoader

    # Set verbosity level
    if args.verbose:
        # ROOT.Experimental.ELogLevel.kInfo verbosity level is more
        # equivalent to DEBUG in other log systems
        LOGGER.debug('Setting verbosity level "kInfo" for RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kInfo)
    if args.more_verbose:
        LOGGER.debug('Setting verbosity level "kDebug" for RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kDebug)
    if args.most_verbose:
        LOGGER.debug('Setting verbosity level "kDebug+10" for '
                     'RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kDebug+10)

    # Load the analysis
    analysisFile = os.path.abspath(analysisFile)
    LOGGER.info('Loading analysis file:\n%s', analysisFile)
    rdfSpec   = importlib.util.spec_from_file_location("rdfanalysis", analysisFile)
    rdfModule = importlib.util.module_from_spec(rdfSpec)
    rdfSpec.loader.exec_module(rdfModule)

    if not hasattr(args, 'command'):
        LOGGER.error('Unknow sub-command "%s"!\nAborting...')
        sys.exit(3)

    if args.command == "run":
        if hasattr(rdfModule, "build_graph") and hasattr(rdfModule, "RDFanalysis"):
            LOGGER.error('Analysis file ambiguous!\nBoth "RDFanalysis" '
                         'class and "build_graph" function are defined.')
            sys.exit(3)
        elif hasattr(rdfModule, "build_graph") and not hasattr(rdfModule, "RDFanalysis"):
            runHistmaker(args, rdfModule, analysisFile)
        elif not hasattr(rdfModule, "build_graph") and hasattr(rdfModule, "RDFanalysis"):
            runStages(args, rdfModule, args.preprocess, analysisFile)
        else:
            LOGGER.error('Analysis file does not contain required '
                         'objects!\nProvide either "RDFanalysis" class or '
                         '"build_graph" function.')
            sys.exit(3)
    elif args.command == "final":
        runFinal(rdfModule)
    elif args.command == "plots":
        runPlots(analysisFile)
