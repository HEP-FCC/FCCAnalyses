'''
Run regular stage of an analysis
'''

import os
import sys
import time
import json
import shutil
import logging
import subprocess
import importlib.util
import datetime
import numpy as np

import ROOT
from anafile import getElement, getElementDict
from process import get_process_info, get_process_dict

LOGGER = logging.getLogger('FCCAnalyses.run')

ROOT.gROOT.SetBatch(True)


# _____________________________________________________________________________
def determine_os(local_dir):
    '''
    Determines platform on which FCCAnalyses was compiled
    '''
    cmake_config_path = local_dir + '/build/CMakeFiles/CMakeConfigureLog.yaml'
    if not os.path.isfile(cmake_config_path):
        LOGGER.warning('CMake configuration file was not found!\n'
                       'Was FCCAnalyses properly build?')
        return None

    with open(cmake_config_path, 'r', encoding='utf-8') as cmake_config_file:
        cmake_config = cmake_config_file.read()
        if 'centos7' in cmake_config:
            return 'centos7'
        if 'almalinux9' in cmake_config:
            return 'almalinux9'

    return None


# _____________________________________________________________________________
def create_condor_config(log_dir, process_name, build_os, rdf_module,
                         subjob_scripts):
    '''
    Creates contents of condor configuration file.
    '''
    cfg = 'executable       = $(filename)\n'

    cfg += f'Log              = {log_dir}/condor_job.{process_name}.'
    cfg += '$(ClusterId).$(ProcId).log\n'

    cfg += f'Output           = {log_dir}/condor_job.{process_name}.'
    cfg += '$(ClusterId).$(ProcId).out\n'

    cfg += f'Error            = {log_dir}/condor_job.{process_name}.'
    cfg += '$(ClusterId).$(ProcId).error\n'

    cfg += 'getenv           = False\n'

    cfg += 'environment      = "LS_SUBCWD={log_dir}"\n'  # not sure

    cfg += 'requirements     = ( '
    if build_os == 'centos7':
        cfg += '(OpSysAndVer =?= "CentOS7") && '
    if build_os == 'almalinux9':
        cfg += '(OpSysAndVer =?= "AlmaLinux9") && '
    if build_os is None:
        LOGGER.warning('Submitting jobs to default operating system. There '
                       'may be compatibility issues.')
    cfg += '(Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n'

    cfg += 'on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n'

    cfg += 'max_retries      = 3\n'

    cfg += '+JobFlavour      = "%s"\n' % getElement(rdf_module, 'batchQueue')

    cfg += '+AccountingGroup = "%s"\n' % getElement(rdf_module, 'compGroup')

    cfg += 'RequestCpus      = %i\n' % getElement(rdf_module, "nCPUS")

    cfg += 'queue filename matching files'
    for script in subjob_scripts:
        cfg += ' ' + script
    cfg += '\n'

    return cfg


# _____________________________________________________________________________
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


# _____________________________________________________________________________
def getchunkList(fileList, chunks):
    chunk_list = list(np.array_split(fileList, chunks))
    chunk_list = [chunk for chunk in chunk_list if chunk.size > 0]

    return chunk_list


# _____________________________________________________________________________
def saveBenchmark(outfile, benchmark):
    benchmarks = []
    try:
        with open(outfile, 'r') as benchin:
            benchmarks = json.load(benchin)
    except OSError:
        pass

    benchmarks = [b for b in benchmarks if b['name'] != benchmark['name']]
    benchmarks.append(benchmark)

    with open(outfile, 'w', encoding='utf-8') as benchout:
        json.dump(benchmarks, benchout, indent=2)


# _____________________________________________________________________________
def getCommandOutput(command):
    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True)
    (stdout, stderr) = p.communicate()
    return {"stdout": stdout, "stderr": stderr, "returncode": p.returncode}


# _____________________________________________________________________________
def submit_job(cmd, max_trials):
    submissionStatus = 0
    for i in range(max_trials):
        with subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as proc:
            (stdout, stderr) = proc.communicate()

        print('stdout:')
        print(stdout)
        print('stderr:')
        print(stderr)

        outputCMD = getCommandOutput(cmd)
        stderr = outputCMD["stderr"].split('\n')

        if len(stderr) == 1 and stderr[0] == '':
            LOGGER.info('GOOD SUBMISSION')
            submissionStatus = 1
        else:
            LOGGER.warning('Error while submitting, retrying...\n\t'
                           'Trial: %i / %i\n\tError: %s', i, max_trials, stderr)
            time.sleep(10)

        if submissionStatus == 1:
            return 1

        if i == max_trials - 1:
            LOGGER.error('Failed submitting after: %i trials, stop trying to '
                         'submit', max_trials)
            return 0

# __________________________________________________________
def initialize(args, rdf_module, anascript_path):
    '''
    Common initialization steps.
    '''

    # for convenience and compatibility with user code
    ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")
    geometryFile = getElement(rdf_module, "geometryFile")
    readout_name = getElement(rdf_module, "readoutName")
    if geometryFile != "" and readout_name != "":
        ROOT.CaloNtupleizer.loadGeometry(geometryFile, readout_name)

    # set multithreading (no MT if number of events is specified)
    ncpus = 1
    if args.nevents < 0:
        if isinstance(args.ncpus, int) and args.ncpus >= 1:
            ncpus = args.ncpus
        else:
            ncpus = getElement(rdf_module, "nCPUS")
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
    include_paths = getElement(rdf_module, "includePaths")
    if include_paths:
        ROOT.gInterpreter.ProcessLine(".O3")
        basepath = os.path.dirname(os.path.abspath(anascript_path)) + "/"
        for path in include_paths:
            LOGGER.info('Loading %s...', path)
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')

    # check if analyses plugins need to be loaded before anything
    # still in use?
    analyses_list = getElement(rdf_module, "analysesList")
    if analyses_list and len(analyses_list) > 0:
        _ana = []
        for analysis in analyses_list:
            LOGGER.info('Load cxx analyzers from %s...', analysis)
            if analysis.startswith('libFCCAnalysis_'):
                ROOT.gSystem.Load(analysis)
            else:
                ROOT.gSystem.Load(f'libFCCAnalysis_{analysis}')
            if not hasattr(ROOT, analysis):
                ROOT.error('Analysis %s not properly loaded!\nAborting...',
                           analysis)
                sys.exit(3)
            _ana.append(getattr(ROOT, analysis).dictionary)

# _____________________________________________________________________________
def runRDF(rdf_module, inputlist, outFile, nevt, args):
    df = ROOT.RDataFrame("events", inputlist)

    # limit number of events processed
    if args.nevents > 0:
        df = df.Range(0, args.nevents)

    try:
        df2 = getElement(rdf_module.RDFanalysis, "analysers")(df)

        branch_list = ROOT.vector('string')()
        blist = getElement(rdf_module.RDFanalysis, "output")()
        for bname in blist:
            branch_list.push_back(bname)

        df2.Snapshot("events", outFile, branch_list)
    except Exception as excp:
        LOGGER.error('During the execution of the analysis file exception '
                     'occurred:\n%s', excp)
        sys.exit(3)

    return df2.Count()


# _____________________________________________________________________________
def sendToBatch(rdf_module, chunkList, process, analysisFile):
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
    except subprocess.CalledProcessError:
        LOGGER.error('The FCCanalyses libraries are not properly build and '
                     'installed!\nAborting job submission...')
        sys.exit(3)

    outputDir = getElement(rdf_module, "outputDir")
    outputDirEos = getElement(rdf_module, "outputDirEos")
    eosType = getElement(rdf_module, "eosType")
    userBatchConfig = getElement(rdf_module, "userBatchConfig")

    if outputDir!="" and outputDir[-1]!="/": outputDir+="/"

    subjob_scripts = []
    for ch in range(len(chunkList)):
        frunname = '{}/job{}_chunk{}.sh'.format(logDir, process, ch)
        LOGGER.info('Script to run %s: ', frunname)
        subjob_scripts.append(frunname)

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
            if outputDirEos == "":
                frun.write('cp {}chunk{}.root  {}/{}/{}/chunk{}.root\n'.format(outputDir,ch,localDir,outputDir,process,ch))
            else:
                frun.write('xrdcp {}chunk{}.root  root://{}.cern.ch/{}/{}/chunk{}.root\n'.format(outputDir,ch,eosType,outputDirEos,process,ch))
        else:
            if outputDirEos != "":
                frun.write('xrdcp {}chunk{}.root  root://{}.cern.ch/{}/{}/chunk{}.root\n'.format(outputDir,ch,eosType,outputDirEos,process,ch))

        frun.close()

    condor_config_path = f'{logDir}/job_desc_{process}.cfg'

    for _ in range(3):
        try:
            with open(condor_config_path, 'w', encoding='utf-8') as cfgfile:
                condor_config = create_condor_config(logDir,
                                                     process,
                                                     determine_os(localDir),
                                                     rdf_module,
                                                     subjob_scripts)
                cfgfile.write(condor_config)
        except IOError as e:
            LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
        else:
            break
        time.sleep(10)
    subprocess.getstatusoutput(f'chmod 777 {condor_config_path}')

    batch_cmd = f'condor_submit {condor_config_path}'
    LOGGER.info('Batch command: %s', batch_cmd)
    ntry = SubmitToCondor(batch_cmd, 10)
    LOGGER.debug('Batch command submitted on %i try.', ntry)


# _____________________________________________________________________________
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


# _____________________________________________________________________________
def runLocal(rdf_module, infile_list, args):
    '''
    Run analysis locally.
    '''
    # Create list of files to be processed
    info_msg = 'Creating dataframe object from files:\n\t'
    file_list = ROOT.vector('string')()
    # Amount of events processed in previous stage (= 0 if it is the first
    # stage)
    nevents_orig = 0
    # The amount of events in the input file(s)
    nevents_local = 0
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

    output_dir = getElement(rdf_module, "outputDir")
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
    outn = runRDF(rdf_module, file_list, outfile_path, nevents_local, args)
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
        analysis_name = getElement(rdf_module, 'analysisName')
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


# _____________________________________________________________________________
def runStages(args, rdf_module, preprocess, analysisFile):
    '''
    Run regular stage.
    '''

    # Set ncpus, load header files, custom dicts, ...
    initialize(args, rdf_module, analysisFile)

    # Check if outputDir exist and if not create it
    outputDir = getElement(rdf_module, "outputDir")
    if not os.path.exists(outputDir) and outputDir:
        os.system("mkdir -p {}".format(outputDir))

    # Check if outputDir exist and if not create it
    outputDirEos = getElement(rdf_module, "outputDirEos")
    if not os.path.exists(outputDirEos) and outputDirEos:
        os.system("mkdir -p {}".format(outputDirEos))

    # Check if test mode is specified, and if so run the analysis on it (this
    # will exit after)
    if args.test:
        LOGGER.info('Running over test file...')
        testfile_path = getElement(rdf_module, "testFile")
        directory, _ = os.path.split(args.output)
        if directory:
            os.system("mkdir -p {}".format(directory))
        runLocal(rdf_module, [testfile_path], args)
        sys.exit(0)

    # Check if files are specified, and if so run the analysis on it/them (this
    # will exit after)
    if len(args.files_list) > 0:
        LOGGER.info('Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        runLocal(rdf_module, args.files_list, args)
        sys.exit(0)

    # Check if batch mode and set start and end file from original list
    run_batch = getElement(rdf_module, "runBatch")
    if run_batch and shutil.which('condor_q') is None:
        LOGGER.error('HTCondor tools can\'t be found!\nAborting...')
        sys.exit(3)

    # Check if the process list is specified
    process_list = getElement(rdf_module, "processList")

    for process_name in process_list:
        file_list, event_list = get_process_info(
            process_name,
            getElement(rdf_module, "prodTag"),
            getElement(rdf_module, "inputDir"))

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

            sendToBatch(rdf_module, chunk_list, process_name, analysisFile)

        else:
            # Running locally
            LOGGER.info('Running locally...')
            if len(chunk_list) == 1:
                args.output = '{}.root'.format(output_stem)
                runLocal(rdf_module, chunk_list[0], args)
            else:
                for index, chunk in enumerate(chunk_list):
                    args.output = '{}/chunk{}.root'.format(output_stem, index)
                    runLocal(rdf_module, chunk, args)


def runHistmaker(args, rdf_module, analysisFile):

    # set ncpus, load header files, custom dicts, ...
    initialize(args, rdf_module, analysisFile)

    # load process dictionary
    proc_dict_location = getElement(rdf_module, "procDict", True)
    if not proc_dict_location:
        LOGGER.error('Location of the procDict not provided.\nAborting...')
        sys.exit(3)

    procDict = get_process_dict(proc_dict_location)

    # check if outputDir exist and if not create it
    outputDir = getElement(rdf_module, "outputDir")
    if not os.path.exists(outputDir) and outputDir != '':
        os.system(f'mkdir -p {outputDir}')

    doScale = getElement(rdf_module, "doScale", True)
    intLumi = getElement(rdf_module, "intLumi", True)

    # check if the process list is specified, and create graphs for them
    processList = getElement(rdf_module, "processList")
    graph_function = getattr(rdf_module, "build_graph")
    results = []  # all the histograms
    hweights = []  # all the weights
    evtcounts = []  # event count of the input file
    eventsProcessedDict = {}  # number of events processed per process, in a potential previous step
    for process in processList:
        fileList, eventList = get_process_info(
            process,
            getElement(rdf_module, "prodTag"),
            getElement(rdf_module, "inputDir"))
        if len(fileList) == 0:
            LOGGER.error('No files to process!\nAborting...')
            sys.exit(3)
        fraction = 1
        output = process
        chunks = 1
        try:
            if getElementDict(processList[process], 'fraction') is not None:
                fraction = getElementDict(processList[process], 'fraction')
            if getElementDict(processList[process], 'output') is not None:
                output = getElementDict(processList[process], 'output')
            if getElementDict(processList[process], 'chunks') is not None:
                chunks = getElementDict(processList[process], 'chunks')
        except TypeError:
            LOGGER.warning('No values set for process %s will use default '
                           'values!', process)
        if fraction < 1:
            fileList = getsubfileList(fileList, eventList, fraction)

        # get the number of events processed, in a potential previous step
        fileListRoot = ROOT.vector('string')()
        # amount of events processed in previous stage (= 0 if it is the first
        # stage)
        nevents_meta = 0
        for fileName in fileList:
            fileName = apply_filepath_rewrites(fileName)
            fileListRoot.push_back(fileName)
            # Skip check for processed events in case of first stage
            if getElement(rdf_module, "prodTag") is None:
                tf = ROOT.TFile.Open(str(fileName), "READ")
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
            # merge histograms in case histogram exists
            if hist.GetName() in histsToWrite:
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


def run(parser):
    '''
    Set things in motion.
    '''

    args, _ = parser.parse_known_args()

    if not hasattr(args, 'command'):
        LOGGER.error('Error occurred during subcommand routing!\nAborting...')
        sys.exit(3)

    if args.command != 'run':
        LOGGER.error('Unknow sub-command "%s"!\nAborting...')
        sys.exit(3)

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
    fcc_loaded = ROOT.dummyLoader()
    if fcc_loaded:
        LOGGER.debug('Succesfuly loaded main FCCanalyses analyzers.')

    # Set verbosity level
    if args.verbose:
        # ROOT.Experimental.ELogLevel.kInfo verbosity level is more
        # equivalent to DEBUG in other log systems
        LOGGER.debug('Setting verbosity level "kInfo" for RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kInfo)
        LOGGER.debug(verbosity)
    if args.more_verbose:
        LOGGER.debug('Setting verbosity level "kDebug" for RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kDebug)
        LOGGER.debug(verbosity)
    if args.most_verbose:
        LOGGER.debug('Setting verbosity level "kDebug+10" for '
                     'RDataFrame...')
        verbosity = ROOT.Experimental.RLogScopedVerbosity(
            ROOT.Detail.RDF.RDFLogChannel(),
            ROOT.Experimental.ELogLevel.kDebug+10)
        LOGGER.debug(verbosity)

    # Load the analysis
    analysisFile = os.path.abspath(analysisFile)
    LOGGER.info('Loading analysis file:\n%s', analysisFile)
    rdf_spec = importlib.util.spec_from_file_location("rdfanalysis",
                                                      analysisFile)
    rdf_module = importlib.util.module_from_spec(rdf_spec)
    rdf_spec.loader.exec_module(rdf_module)

    if hasattr(rdf_module, "build_graph") and \
            hasattr(rdf_module, "RDFanalysis"):
        LOGGER.error('Analysis file ambiguous!\nBoth "RDFanalysis" '
                     'class and "build_graph" function are defined.')
        sys.exit(3)
    elif hasattr(rdf_module, "build_graph") and \
            not hasattr(rdf_module, "RDFanalysis"):
        runHistmaker(args, rdf_module, analysisFile)
    elif not hasattr(rdf_module, "build_graph") and \
            hasattr(rdf_module, "RDFanalysis"):
        runStages(args, rdf_module, args.preprocess, analysisFile)
    else:
        LOGGER.error('Analysis file does not contain required '
                     'objects!\nProvide either "RDFanalysis" class or '
                     '"build_graph" function.')
        sys.exit(3)
