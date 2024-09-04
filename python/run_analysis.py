'''
Run analysis in one of the different styles.
'''

import os
import sys
import time
import shutil
import json
import logging
import subprocess
import importlib.util
import datetime
import numpy as np

import ROOT  # type: ignore
from anascript import get_element, get_element_dict
from process import get_process_info, get_process_dict
from frame import generate_graph

LOGGER = logging.getLogger('FCCAnalyses.run')

ROOT.gROOT.SetBatch(True)


# _____________________________________________________________________________
def determine_os(local_dir: str) -> str | None:
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
def create_condor_config(log_dir: str,
                         process_name: str,
                         build_os: str | None,
                         rdf_module,
                         subjob_scripts: list[str]) -> str:
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

    cfg += '+JobFlavour      = "%s"\n' % get_element(rdf_module, 'batchQueue')

    cfg += '+AccountingGroup = "%s"\n' % get_element(rdf_module, 'compGroup')

    cfg += 'RequestCpus      = %i\n' % get_element(rdf_module, "nCPUS")

    cfg += 'queue filename matching files'
    for script in subjob_scripts:
        cfg += ' ' + script
    cfg += '\n'

    return cfg


# _____________________________________________________________________________
def create_subjob_script(local_dir: str,
                         rdf_module,
                         process_name: str,
                         chunk_num: int,
                         chunk_list: list[list[str]],
                         anapath: str) -> str:
    '''
    Creates sub-job script to be run.
    '''

    output_dir = get_element(rdf_module, "outputDir")
    output_dir_eos = get_element(rdf_module, "outputDirEos")
    eos_type = get_element(rdf_module, "eosType")
    user_batch_config = get_element(rdf_module, "userBatchConfig")

    scr = '#!/bin/bash\n\n'
    scr += 'source ' + local_dir + '/setup.sh\n\n'

    # add userBatchConfig if any
    if user_batch_config != '':
        if not os.path.isfile(user_batch_config):
            LOGGER.warning('userBatchConfig file can\'t be found! Will not '
                           'add it to the default config.')
        else:
            with open(user_batch_config, 'r', encoding='utf-8') as cfgfile:
                for line in cfgfile:
                    scr += line + '\n'
        scr += '\n\n'

    scr += f'mkdir job_{process_name}_chunk_{chunk_num}\n'
    scr += f'cd job_{process_name}_chunk_{chunk_num}\n\n'

    if not os.path.isabs(output_dir):
        output_path = os.path.join(output_dir, f'chunk_{chunk_num}.root')
    else:
        output_path = os.path.join(output_dir, process_name,
                                   f'chunk_{chunk_num}.root')

    scr += local_dir
    scr += f'/bin/fccanalysis run {anapath} --batch '
    scr += f'--output {output_path} '
    scr += '--files-list'
    for file_path in chunk_list[chunk_num]:
        scr += f' {file_path}'
    scr += '\n\n'

    if not os.path.isabs(output_dir) and output_dir_eos == '':
        final_dest = os.path.join(local_dir, output_dir, process_name,
                                  f'chunk_{chunk_num}.root')
        scr += f'cp {output_path} {final_dest}\n'

    if output_dir_eos != '':
        final_dest = os.path.join(output_dir_eos,
                                  process_name,
                                  f'chunk_{chunk_num}.root')
        final_dest = f'root://{eos_type}.cern.ch/' + final_dest
        scr += f'xrdcp {output_path} {final_dest}\n'

    return scr


# _____________________________________________________________________________
def get_subfile_list(in_file_list: list[str],
                     event_list: list[int],
                     fraction: float) -> list[str]:
    '''
    Obtain list of files roughly containing the requested fraction of events.
    '''
    nevts_total: int = sum(event_list)
    nevts_target: int = int(nevts_total * fraction)

    if nevts_target <= 0:
        LOGGER.error('The reduction fraction %f too stringent, no events '
                     'left!\nAborting...', fraction)
        sys.exit(3)

    nevts_real: int = 0
    out_file_list: list[str] = []
    for i, nevts in enumerate(event_list):
        if nevts_real >= nevts_target:
            break
        nevts_real += nevts
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
def get_chunk_list(file_list: str, chunks: int):
    '''
    Get list of input file paths arranged into chunks.
    '''
    chunk_list = list(np.array_split(file_list, chunks))
    return [chunk for chunk in chunk_list if chunk.size > 0]


# _____________________________________________________________________________
def save_benchmark(outfile, benchmark):
    '''
    Save benchmark results to a JSON file.
    '''
    benchmarks = []
    try:
        with open(outfile, 'r', encoding='utf-8') as benchin:
            benchmarks = json.load(benchin)
    except OSError:
        pass

    benchmarks = [b for b in benchmarks if b['name'] != benchmark['name']]
    benchmarks.append(benchmark)

    with open(outfile, 'w', encoding='utf-8') as benchout:
        json.dump(benchmarks, benchout, indent=2)


# _____________________________________________________________________________
def submit_job(cmd: str, max_trials: int) -> bool:
    '''
    Submit job to condor, retry `max_trials` times.
    '''
    for i in range(max_trials):
        with subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as proc:
            (stdout, stderr) = proc.communicate()

            if proc.returncode == 0 and len(stderr) == 0:
                LOGGER.info(stdout)
                LOGGER.info('GOOD SUBMISSION')
                return True

            LOGGER.warning('Error while submitting, retrying...\n  '
                           'Trial: %i / %i\n  Error: %s',
                           i, max_trials, stderr)
            time.sleep(10)

    LOGGER.error('Failed submitting after: %i trials!', max_trials)
    return False


# _____________________________________________________________________________
def initialize(args, rdf_module, anapath: str):
    '''
    Common initialization steps.
    '''

    # for convenience and compatibility with user code
    ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")
    geometry_file = get_element(rdf_module, "geometryFile")
    readout_name = get_element(rdf_module, "readoutName")
    if geometry_file != "" and readout_name != "":
        ROOT.CaloNtupleizer.loadGeometry(geometry_file, readout_name)

    # set multithreading (no MT if number of events is specified)
    ncpus = 1
    if args.nevents < 0:
        if isinstance(args.ncpus, int) and args.ncpus >= 1:
            ncpus = args.ncpus
        else:
            ncpus = get_element(rdf_module, "nCPUS")
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
    include_paths = get_element(rdf_module, "includePaths")
    if include_paths:
        ROOT.gInterpreter.ProcessLine(".O3")
        basepath = os.path.dirname(os.path.abspath(anapath)) + "/"
        for path in include_paths:
            LOGGER.info('Loading %s...', path)
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')

    # check if analyses plugins need to be loaded before anything
    # still in use?
    analyses_list = get_element(rdf_module, "analysesList")
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
def run_rdf(rdf_module,
            input_list: list[str],
            out_file: str,
            args) -> int:
    '''
    Create RDataFrame and snapshot it.
    '''
    dframe = ROOT.RDataFrame("events", input_list)

    # limit number of events processed
    if args.nevents > 0:
        dframe2 = dframe.Range(0, args.nevents)
    else:
        dframe2 = dframe

    try:
        evtcount_init = dframe2.Count()
        dframe3 = get_element(rdf_module.RDFanalysis, "analysers")(dframe2)

        branch_list = ROOT.vector('string')()
        blist = get_element(rdf_module.RDFanalysis, "output")()
        for bname in blist:
            branch_list.push_back(bname)

        evtcount_final = dframe3.Count()

        # Generate computational graph of the analysis
        if args.graph:
            generate_graph(dframe, args)

        dframe3.Snapshot("events", out_file, branch_list)
    except Exception as excp:
        LOGGER.error('During the execution of the analysis file exception '
                     'occurred:\n%s', excp)
        sys.exit(3)

    return evtcount_init.GetValue(), evtcount_final.GetValue()


# _____________________________________________________________________________
def send_to_batch(rdf_module, chunk_list, process, anapath: str):
    '''
    Send jobs to HTCondor batch system.
    '''
    local_dir = os.environ['LOCAL_DIR']
    current_date = datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = os.path.join(local_dir, 'BatchOutputs', current_date, process)
    if not os.path.exists(log_dir):
        os.system(f'mkdir -p {log_dir}')

    # Making sure the FCCAnalyses libraries are compiled and installed
    try:
        subprocess.check_output(['make', 'install'],
                                cwd=local_dir+'/build',
                                stderr=subprocess.DEVNULL
                                )
    except subprocess.CalledProcessError:
        LOGGER.error('The FCCanalyses libraries are not properly build and '
                     'installed!\nAborting job submission...')
        sys.exit(3)

    subjob_scripts = []
    for ch in range(len(chunk_list)):
        subjob_script_path = os.path.join(log_dir,
                                          f'job_{process}_chunk_{ch}.sh')
        subjob_scripts.append(subjob_script_path)

        for i in range(3):
            try:
                with open(subjob_script_path, 'w', encoding='utf-8') as ofile:
                    subjob_script = create_subjob_script(local_dir,
                                                         rdf_module,
                                                         process,
                                                         ch,
                                                         chunk_list,
                                                         anapath)
                    ofile.write(subjob_script)
            except IOError as e:
                if i < 2:
                    LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
                else:
                    LOGGER.error('I/O error(%i): %s', e.errno, e.strerror)
                    sys.exit(3)
            else:
                break
            time.sleep(10)
        subprocess.getstatusoutput(f'chmod 777 {subjob_script_path}')

    LOGGER.debug('Sub-job scripts to be run:\n - %s',
                 '\n - '.join(subjob_scripts))

    condor_config_path = f'{log_dir}/job_desc_{process}.cfg'

    for i in range(3):
        try:
            with open(condor_config_path, 'w', encoding='utf-8') as cfgfile:
                condor_config = create_condor_config(log_dir,
                                                     process,
                                                     determine_os(local_dir),
                                                     rdf_module,
                                                     subjob_scripts)
                cfgfile.write(condor_config)
        except IOError as e:
            LOGGER.warning('I/O error(%i): %s', e.errno, e.strerror)
            if i == 2:
                sys.exit(3)
        else:
            break
        time.sleep(10)
    subprocess.getstatusoutput(f'chmod 777 {condor_config_path}')

    batch_cmd = f'condor_submit {condor_config_path}'
    LOGGER.info('Batch command:\n  %s', batch_cmd)
    success = submit_job(batch_cmd, 10)
    if not success:
        sys.exit(3)


# _____________________________________________________________________________
def apply_filepath_rewrites(filepath: str) -> str:
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
def run_local(rdf_module, infile_list, args):
    '''
    Run analysis locally.
    '''
    # Create list of files to be processed
    info_msg = 'Creating dataframe object from files:\n'
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
        infile.Close()

    LOGGER.info(info_msg)

    # Adjust number of events in case --nevents was specified
    if args.nevents > 0 and args.nevents < nevents_local:
        nevents_local = args.nevents

    if nevents_orig > 0:
        LOGGER.info('Number of events:\n\t- original: %s\n\t- local:    %s',
                    f'{nevents_orig:,}', f'{nevents_local:,}')
    else:
        LOGGER.info('Number of local events: %s', f'{nevents_local:,}')

    output_dir = get_element(rdf_module, "outputDir")
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
    inn, outn = run_rdf(rdf_module, file_list, outfile_path, args)
    elapsed_time = time.time() - start_time
    
    # replace nevents_local by inn = the amount of processed events

    info_msg = f"{' SUMMARY ':=^80}\n"
    info_msg += 'Elapsed time (H:M:S):    '
    info_msg += time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    info_msg += '\nEvents processed/second: '
    info_msg += f'{int(inn/elapsed_time):,}'
    info_msg += f'\nTotal events processed:  {int(inn):,}'
    info_msg += f'\nNo. result events:       {int(outn):,}'
    if inn > 0:
        info_msg += f'\nReduction factor local:  {outn/inn}'
    if nevents_orig > 0:
        info_msg += f'\nReduction factor total:  {outn/nevents_orig}'
    info_msg += '\n'
    info_msg += 80 * '='
    info_msg += '\n'
    LOGGER.info(info_msg)

    # Update resulting root file with number of processed events
    # and number of selected events
    with ROOT.TFile(outfile_path, 'update') as outfile:
        param = ROOT.TParameter(int)(
                'eventsProcessed',
                nevents_orig if nevents_orig != 0 else inn)
        param.Write()
        param = ROOT.TParameter(int)('eventsSelected', outn)
        param.Write()
        outfile.Write()

    if args.bench:
        analysis_name = get_element(rdf_module, 'analysisName')
        if not analysis_name:
            analysis_name = args.anascript_path

        bench_time = {}
        bench_time['name'] = 'Time spent running the analysis: '
        bench_time['name'] += analysis_name
        bench_time['unit'] = 'Seconds'
        bench_time['value'] = elapsed_time
        bench_time['range'] = 10
        bench_time['extra'] = 'Analysis path: ' + args.anascript_path
        save_benchmark('benchmarks_smaller_better.json', bench_time)

        bench_evt_per_sec = {}
        bench_evt_per_sec['name'] = 'Events processed per second: '
        bench_evt_per_sec['name'] += analysis_name
        bench_evt_per_sec['unit'] = 'Evt/s'
        bench_evt_per_sec['value'] = nevents_local / elapsed_time
        bench_time['range'] = 1000
        bench_time['extra'] = 'Analysis path: ' + args.anascript_path
        save_benchmark('benchmarks_bigger_better.json', bench_evt_per_sec)


# _____________________________________________________________________________
def run_stages(args, rdf_module, anapath):
    '''
    Run regular stage.
    '''

    # Set ncpus, load header files, custom dicts, ...
    initialize(args, rdf_module, anapath)

    # Check if outputDir exist and if not create it
    output_dir = get_element(rdf_module, "outputDir")
    if not os.path.exists(output_dir) and output_dir:
        os.system(f'mkdir -p {output_dir}')

    # Check if outputDir exist and if not create it
    output_dir_eos = get_element(rdf_module, "outputDirEos")
    if not os.path.exists(output_dir_eos) and output_dir_eos:
        os.system(f'mkdir -p {output_dir_eos}')

    # Check if test mode is specified, and if so run the analysis on it (this
    # will exit after)
    if args.test:
        LOGGER.info('Running over test file...')
        testfile_path = get_element(rdf_module, "testFile")
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(rdf_module, [testfile_path], args)
        sys.exit(0)

    # Check if files are specified, and if so run the analysis on it/them (this
    # will exit after)
    if len(args.files_list) > 0:
        LOGGER.info('Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(rdf_module, args.files_list, args)
        sys.exit(0)

    # Check if batch mode is available
    run_batch = get_element(rdf_module, 'runBatch')
    if run_batch and shutil.which('condor_q') is None:
        LOGGER.error('HTCondor tools can\'t be found!\nAborting...')
        sys.exit(3)

    # Check if the process list is specified
    process_list = get_element(rdf_module, 'processList')

    for process_name in process_list:
        file_list, event_list = get_process_info(
            process_name,
            get_element(rdf_module, "prodTag"),
            get_element(rdf_module, "inputDir"))

        if len(file_list) <= 0:
            LOGGER.error('No files to process!\nAborting...')
            sys.exit(3)

        # Determine the fraction of the input to be processed
        fraction = 1
        if get_element_dict(process_list[process_name], 'fraction'):
            fraction = get_element_dict(process_list[process_name], 'fraction')
        # Put together output path
        output_stem = process_name
        if get_element_dict(process_list[process_name], 'output'):
            output_stem = get_element_dict(process_list[process_name],
                                           'output')
        # Determine the number of chunks the output will be split into
        chunks = 1
        if get_element_dict(process_list[process_name], 'chunks'):
            chunks = get_element_dict(process_list[process_name], 'chunks')

        info_msg = f'Adding process "{process_name}" with:'
        if fraction < 1:
            info_msg += f'\n\t- fraction:         {fraction}'
        info_msg += f'\n\t- number of files:  {len(file_list):,}'
        info_msg += f'\n\t- output stem:      {output_stem}'
        if chunks > 1:
            info_msg += f'\n\t- number of chunks: {chunks}'

        if fraction < 1:
            file_list = get_subfile_list(file_list, event_list, fraction)

        chunk_list = [file_list]
        if chunks > 1:
            chunk_list = get_chunk_list(file_list, chunks)
        LOGGER.info('Number of the output files: %s', f'{len(chunk_list):,}')

        # Create directory if more than 1 chunk
        if chunks > 1:
            output_directory = os.path.join(output_dir, output_stem)

            if not os.path.exists(output_directory):
                os.system(f'mkdir -p {output_directory}')

        if run_batch:
            # Sending to the batch system
            LOGGER.info('Running on the batch...')
            if len(chunk_list) == 1:
                LOGGER.warning('\033[4m\033[1m\033[91mRunning on batch with '
                               'only one chunk might not be optimal\033[0m')

            send_to_batch(rdf_module, chunk_list, process_name, anapath)

        else:
            # Running locally
            LOGGER.info('Running locally...')
            if len(chunk_list) == 1:
                args.output = f'{output_stem}.root'
                run_local(rdf_module, chunk_list[0], args)
            else:
                for index, chunk in enumerate(chunk_list):
                    args.output = f'{output_stem}/chunk{index}.root'
                    run_local(rdf_module, chunk, args)


def run_histmaker(args, rdf_module, anapath):
    '''
    Run the analysis using histmaker (all stages integrated into one).
    '''

    # set ncpus, load header files, custom dicts, ...
    initialize(args, rdf_module, anapath)

    # load process dictionary
    proc_dict_location = get_element(rdf_module, "procDict", True)
    if not proc_dict_location:
        LOGGER.error('Location of the procDict not provided.\nAborting...')
        sys.exit(3)

    proc_dict = get_process_dict(proc_dict_location)

    # check if outputDir exist and if not create it
    output_dir = get_element(rdf_module, "outputDir")
    if not os.path.exists(output_dir) and output_dir != '':
        os.system(f'mkdir -p {output_dir}')

    do_scale = get_element(rdf_module, "doScale", True)
    int_lumi = get_element(rdf_module, "intLumi", True)

    # check if the process list is specified, and create graphs for them
    process_list = get_element(rdf_module, "processList")
    graph_function = getattr(rdf_module, "build_graph")
    results = []  # all the histograms
    hweights = []  # all the weights
    evtcounts = []  # event count of the input file
    # number of events processed per process, in a potential previous step
    events_processed_dict = {}
    for process in process_list:
        file_list, event_list = get_process_info(
            process,
            get_element(rdf_module, "prodTag"),
            get_element(rdf_module, "inputDir"))
        if len(file_list) == 0:
            LOGGER.error('No files to process!\nAborting...')
            sys.exit(3)
        fraction = 1
        output = process
        chunks = 1
        try:
            if get_element_dict(process_list[process], 'fraction') is not None:
                fraction = get_element_dict(process_list[process], 'fraction')
            if get_element_dict(process_list[process], 'output') is not None:
                output = get_element_dict(process_list[process], 'output')
            if get_element_dict(process_list[process], 'chunks') is not None:
                chunks = get_element_dict(process_list[process], 'chunks')
        except TypeError:
            LOGGER.warning('No values set for process %s will use default '
                           'values!', process)
        if fraction < 1:
            file_list = get_subfile_list(file_list, event_list, fraction)

        # get the number of events processed, in a potential previous step
        file_list_root = ROOT.vector('string')()
        # amount of events processed in previous stage (= 0 if it is the first
        # stage)
        nevents_meta = 0
        for file_name in file_list:
            file_name = apply_filepath_rewrites(file_name)
            file_list_root.push_back(file_name)
            # Skip check for processed events in case of first stage
            if get_element(rdf_module, "prodTag") is None:
                infile = ROOT.TFile.Open(str(file_name), 'READ')
                for key in infile.GetListOfKeys():
                    if 'eventsProcessed' == key.GetName():
                        nevents_meta += infile.eventsProcessed.GetVal()
                        break
                infile.Close()
            if args.test:
                break
        events_processed_dict[process] = nevents_meta
        info_msg = f'Add process "{process}" with:'
        info_msg += f'\n\tfraction = {fraction}'
        info_msg += f'\n\tnFiles = {len(file_list_root):,}'
        info_msg += f'\n\toutput = {output}\n\tchunks = {chunks}'
        LOGGER.info(info_msg)

        dframe = ROOT.ROOT.RDataFrame("events", file_list_root)
        evtcount = dframe.Count()

        res, hweight = graph_function(dframe, process)
        results.append(res)
        hweights.append(hweight)
        evtcounts.append(evtcount)

    # Generate computational graph of the analysis
    if args.graph:
        generate_graph(dframe, args)

    LOGGER.info('Starting the event loop...')
    start_time = time.time()
    ROOT.ROOT.RDF.RunGraphs(evtcounts)
    LOGGER.info('Event loop done!')
    elapsed_time = time.time() - start_time

    LOGGER.info('Writing out output files...')
    nevents_tot = 0
    for process, res, hweight, evtcount in zip(process_list,
                                               results,
                                               hweights,
                                               evtcounts):
        # get the cross-sections etc. First try locally, then the procDict
        if 'crossSection' in process_list[process]:
            cross_section = process_list[process]['crossSection']
        elif process in proc_dict and 'crossSection' in proc_dict[process]:
            cross_section = proc_dict[process]['crossSection']
        else:
            LOGGER.warning('Can\'t find cross-section for process %s in '
                           'processList or procDict!\nUsing default value '
                           'of 1', process)
            cross_section = 1

        if 'kfactor' in process_list[process]:
            kfactor = process_list[process]['kfactor']
        elif process in proc_dict and 'kfactor' in proc_dict[process]:
            kfactor = proc_dict[process]['kfactor']
        else:
            kfactor = 1

        if 'matchingEfficiency' in process_list[process]:
            matching_efficiency = process_list[process]['matchingEfficiency']
        elif process in proc_dict \
                and 'matchingEfficiency' in proc_dict[process]:
            matching_efficiency = proc_dict[process]['matchingEfficiency']
        else:
            matching_efficiency = 1

        events_processed = events_processed_dict[process] \
            if events_processed_dict[process] != 0 else evtcount.GetValue()
        scale = cross_section*kfactor*matching_efficiency/events_processed

        nevents_tot += evtcount.GetValue()

        hists_to_write = {}
        for r in res:
            hist = r.GetValue()
            hname = hist.GetName()
            # merge histograms in case histogram exists
            if hist.GetName() in hists_to_write:
                hists_to_write[hname].Add(hist)
            else:
                hists_to_write[hname] = hist

        LOGGER.info('Writing out process %s, nEvents processed %s',
                    process, f'{evtcount.GetValue():,}')
        with ROOT.TFile(f'{output_dir}/{process}.root', 'RECREATE'):
            for hist in hists_to_write.values():
                if do_scale:
                    hist.Scale(scale * int_lumi)
                hist.Write()

            # write all meta info to the output file
            p = ROOT.TParameter(int)("eventsProcessed", events_processed)
            p.Write()
            p = ROOT.TParameter(float)("sumOfWeights", hweight.GetValue())
            p.Write()
            p = ROOT.TParameter(float)("intLumi", int_lumi)
            p.Write()
            p = ROOT.TParameter(float)("crossSection", cross_section)
            p.Write()
            p = ROOT.TParameter(float)("kfactor", kfactor)
            p.Write()
            p = ROOT.TParameter(float)("matchingEfficiency",
                                       matching_efficiency)
            p.Write()

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

    args, unknown_args = parser.parse_known_args()
    # Add unknown arguments including unknown input files
    unknown_args += [x for x in args.files_list if not x.endswith('.root')]
    args.unknown = unknown_args
    args.files_list = [x for x in args.files_list if x.endswith('.root')]

    if not hasattr(args, 'command'):
        LOGGER.error('Error occurred during subcommand routing!\nAborting...')
        sys.exit(3)

    if args.command != 'run':
        LOGGER.error('Unknow sub-command "%s"!\nAborting...')
        sys.exit(3)

    # Check that the analysis file exists
    anapath = args.anascript_path
    if not os.path.isfile(anapath):
        LOGGER.error('Analysis script %s not found!\nAborting...',
                     anapath)
        sys.exit(3)

    # Set verbosity level of the RDataFrame
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

    # Load pre compiled analyzers
    LOGGER.info('Loading analyzers from libFCCAnalyses...')
    ROOT.gSystem.Load("libFCCAnalyses")
    # Is this still needed?? 01/04/2022 still to be the case
    fcc_loaded = ROOT.dummyLoader()
    if fcc_loaded:
        LOGGER.debug('Succesfuly loaded main FCCanalyses analyzers.')

    # Load the analysis script as a module
    anapath = os.path.abspath(anapath)
    LOGGER.info('Loading analysis file:\n%s', anapath)
    rdf_spec = importlib.util.spec_from_file_location("fcc_analysis_module",
                                                      anapath)
    rdf_module = importlib.util.module_from_spec(rdf_spec)
    rdf_spec.loader.exec_module(rdf_module)

    # Merge configuration from analysis script file with command line arguments
    if get_element(rdf_module, 'graph'):
        args.graph = True

    if get_element(rdf_module, 'graphPath') != '':
        args.graph_path = get_element(rdf_module, 'graphPath')

    n_ana_styles = 0
    for analysis_style in ["build_graph", "RDFanalysis", "Analysis"]:
        if hasattr(rdf_module, analysis_style):
            LOGGER.debug("Analysis style found: %s", analysis_style)
            n_ana_styles += 1

    if n_ana_styles == 0:
        LOGGER.error('Analysis file does not contain required objects!\n'
                     'Provide either RDFanalysis class, Analysis class, or '
                     'build_graph function.')
        sys.exit(3)

    if n_ana_styles > 1:
        LOGGER.error('Analysis file ambiguous!\n'
                     'Multiple analysis styles used!\n'
                     'Provide only one out of "RDFanalysis", "Analysis", '
                     'or "build_graph".')
        sys.exit(3)

    if hasattr(rdf_module, "Analysis"):
        from run_fccanalysis import run_fccanalysis
        run_fccanalysis(args, rdf_module)
    if hasattr(rdf_module, "RDFanalysis"):
        run_stages(args, rdf_module, anapath)
    if hasattr(rdf_module, "build_graph"):
        run_histmaker(args, rdf_module, anapath)
