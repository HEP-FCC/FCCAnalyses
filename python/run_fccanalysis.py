'''
Run analysis of style "Analysis", which can be split into several stages.
'''

import os
import sys
import time
import shutil
import json
import logging
import subprocess
import datetime
import numpy as np

import ROOT  # type: ignore
from anascript import get_element, get_element_dict, get_attribute
from process import get_process_info
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
                         analysis,
                         process_name: str,
                         chunk_num: int,
                         chunk_list: list[list[str]],
                         anapath: str,
                         cmd_args) -> str:
    '''
    Creates sub-job script to be run.
    '''

    output_dir = get_attribute(analysis, 'output_dir', None)

    scr = '#!/bin/bash\n\n'
    scr += 'source ' + local_dir + '/setup.sh\n\n'

    # add user batch configuration if any
    user_batch_config = get_attribute(analysis, 'user_batch_config', None)
    if user_batch_config is not None:
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
    scr += f'/bin/fccanalysis run {anapath} --batch'
    scr += f' --output {output_path}'
    if cmd_args.ncpus > 0:
        scr += f' --ncpus {cmd_args.ncpus}'
    if len(cmd_args.unknown) > 0:
        scr += ' ' + ' '.join(cmd_args.unknown)
    scr += ' --files-list'
    for file_path in chunk_list[chunk_num]:
        scr += f' {file_path}'
    scr += '\n\n'

    output_dir_eos = get_attribute(analysis, 'output_dir_eos', None)
    if not os.path.isabs(output_dir) and output_dir_eos is None:
        final_dest = os.path.join(local_dir, output_dir, process_name,
                                  f'chunk_{chunk_num}.root')
        scr += f'cp {output_path} {final_dest}\n'

    if output_dir_eos is not None:
        eos_type = get_attribute(analysis, 'eos_type', 'eospublic')

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
def initialize(args, analysis):
    '''
    Common initialization steps.
    '''

    # for convenience and compatibility with user code
    ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")

    # Load geometry, needed for the CaloNtupleizer analyzers
    geometry_file = get_attribute(analysis, 'geometry_path', None)

    readout_name = get_attribute(analysis, 'readout_name', None)

    if geometry_file is not None and readout_name is not None:
        ROOT.CaloNtupleizer.loadGeometry(geometry_file, readout_name)

    # set multithreading (no MT if number of events is specified)
    n_threads = 1
    if args.nevents < 0:
        if isinstance(args.ncpus, int) and args.ncpus >= 1:
            n_threads = args.ncpus
        else:
            n_threads = get_attribute(analysis, "n_threads", 1)
        if n_threads < 0:  # use all available threads
            ROOT.EnableImplicitMT()
            n_threads = ROOT.GetThreadPoolSize()

        if n_threads > 1:
            ROOT.ROOT.EnableImplicitMT(n_threads)

    if ROOT.IsImplicitMTEnabled():
        ROOT.EnableThreadSafety()
        LOGGER.info('Multithreading enabled. Running over %i threads',
                    ROOT.GetThreadPoolSize())
    else:
        LOGGER.info('No multithreading enabled. Running in single thread...')

    # custom header files
    include_paths = get_attribute(analysis, 'include_paths', None)
    if include_paths is not None:
        ROOT.gInterpreter.ProcessLine(".O3")
        basepath = os.path.dirname(os.path.abspath(args.anascript_path)) + "/"
        for path in include_paths:
            LOGGER.info('Loading %s...', path)
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')


# _____________________________________________________________________________
def run_rdf(args,
            analysis,
            input_list: list[str],
            out_file: str) -> int:
    '''
    Run the analysis ROOTDataFrame and snapshot it.
    '''
    # Create initial dataframe
    dframe = ROOT.RDataFrame("events", input_list)

    # Limit number of events processed
    if args.nevents > 0:
        dframe2 = dframe.Range(0, args.nevents)
    else:
        dframe2 = dframe

    try:
        evtcount_init = dframe2.Count()

        dframe3 = analysis.analyzers(dframe2)

        branch_list = ROOT.vector('string')()
        blist = analysis.output()
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
def send_to_batch(args, analysis, chunk_list, sample_name, anapath: str):
    '''
    Send jobs to HTCondor batch system.
    '''
    local_dir = os.environ['LOCAL_DIR']
    current_date = datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = os.path.join(local_dir, 'BatchOutputs', current_date,
                           sample_name)
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
    for ch_num in range(len(chunk_list)):
        subjob_script_path = os.path.join(
            log_dir,
            f'job_{sample_name}_chunk_{ch_num}.sh')
        subjob_scripts.append(subjob_script_path)

        for i in range(3):
            try:
                with open(subjob_script_path, 'w', encoding='utf-8') as ofile:
                    subjob_script = create_subjob_script(local_dir,
                                                         analysis,
                                                         sample_name,
                                                         ch_num,
                                                         chunk_list,
                                                         anapath,
                                                         args)
                    ofile.write(subjob_script)
            except IOError as err:
                if i < 2:
                    LOGGER.warning('I/O error(%i): %s',
                                   err.errno, err.strerror)
                else:
                    LOGGER.error('I/O error(%i): %s', err.errno, err.strerror)
                    sys.exit(3)
            else:
                break
            time.sleep(10)
        subprocess.getstatusoutput(f'chmod 777 {subjob_script_path}')

    LOGGER.debug('Sub-job scripts to be run:\n - %s',
                 '\n - '.join(subjob_scripts))

    condor_config_path = f'{log_dir}/job_desc_{sample_name}.cfg'

    for i in range(3):
        try:
            with open(condor_config_path, 'w', encoding='utf-8') as cfgfile:
                condor_config = create_condor_config(log_dir,
                                                     sample_name,
                                                     determine_os(local_dir),
                                                     analysis,
                                                     subjob_scripts)
                cfgfile.write(condor_config)
        except IOError as err:
            LOGGER.warning('I/O error(%i): %s', err.errno, err.strerror)
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
def run_local(args, analysis, infile_list):
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

    output_dir = get_attribute(analysis, 'output_dir', '')
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
    inn, outn = run_rdf(args, analysis, file_list, outfile_path)
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
        analysis_name = get_attribute(analysis,
                                      'analysis_name', args.anascript_path)

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
def run_fccanalysis(args, analysis_module):
    '''
    Run analysis of style "Analysis".
    '''

    # Get analysis class out of the module
    analysis_args = vars(args)
    analysis = analysis_module.Analysis(analysis_args)

    # Set number of threads, load header files, custom dicts, ...
    initialize(args, analysis_module)

    # Check if output directory exist and if not create it
    output_dir = get_attribute(analysis, 'output_dir', None)
    if output_dir is not None and not os.path.exists(output_dir):
        os.system(f'mkdir -p {output_dir}')

    # Check if eos output directory exist and if not create it
    output_dir_eos = get_attribute(analysis, 'output_dir_eos', None)
    if output_dir_eos is not None and not os.path.exists(output_dir_eos):
        os.system(f'mkdir -p {output_dir_eos}')

    # Check if test mode is specified, and if so run the analysis on it (this
    # will exit after)
    if args.test:
        LOGGER.info('Running over test file...')
        testfile_path = getattr(analysis, "test_file")
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(args, analysis, [testfile_path])
        sys.exit(0)

    # Check if files are specified, and if so run the analysis on it/them (this
    # will exit after)
    if len(args.files_list) > 0:
        LOGGER.info('Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(args, analysis, args.files_list)
        sys.exit(0)

    # Check if batch mode is available
    run_batch = get_attribute(analysis, 'run_batch', False)
    if run_batch and shutil.which('condor_q') is None:
        LOGGER.error('HTCondor tools can\'t be found!\nAborting...')
        sys.exit(3)

    # Check if the process list is specified
    process_list = get_attribute(analysis, 'process_list', [])

    prod_tag = get_attribute(analysis, 'prod_tag', None)

    input_dir = get_attribute(analysis, 'input_dir', None)

    if prod_tag is None and input_dir is None:
        LOGGER.error('No input directory or production tag specified in the '
                     'analysis script!\nAborting...')
        sys.exit(3)

    for process_name in process_list:
        LOGGER.info('Started processing sample "%s" ...', process_name)
        file_list, event_list = get_process_info(process_name,
                                                 prod_tag,
                                                 input_dir)

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
            output_directory = os.path.join(output_dir if output_dir else '',
                                            output_stem)

            if not os.path.exists(output_directory):
                os.system(f'mkdir -p {output_directory}')

        if run_batch:
            # Sending to the batch system
            LOGGER.info('Running on the batch...')
            if len(chunk_list) == 1:
                LOGGER.warning('\033[4m\033[1m\033[91mRunning on batch with '
                               'only one chunk might not be optimal\033[0m')

            anapath = os.path.abspath(args.anascript_path)

            send_to_batch(args, analysis, chunk_list, process_name, anapath)

        else:
            # Running locally
            LOGGER.info('Running locally...')
            if len(chunk_list) == 1:
                args.output = f'{output_stem}.root'
                run_local(args, analysis, chunk_list[0])
            else:
                for index, chunk in enumerate(chunk_list):
                    args.output = f'{output_stem}/chunk{index}.root'
                    run_local(args, analysis, chunk)

    if len(process_list) == 0:
        LOGGER.warning('No files processed (process_list not found)!\n'
                       'Exiting...')
