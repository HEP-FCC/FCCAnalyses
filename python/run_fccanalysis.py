'''
Run analysis of style "Analysis", which can be split into several stages.
'''

import os
import sys
import string
import datetime
import logging
import argparse
from typing import Any, Optional, Union

import ROOT  # type: ignore
from anascript import get_element, get_element_dict, get_attribute
from process import get_process_info, get_entries_sow
from frame import generate_graph

LOGGER = logging.getLogger('FCCAnalyses.run')

ROOT.gROOT.SetBatch(True)

LOGGER = logging.getLogger('FCCAnalyses.run_analysis')


# _____________________________________________________________________________
def generate_sample_jobs(config: dict[str, Any]) -> \
        list[dict[str, Union[int, float, str]]]:
    '''
    Generate the jobs to run from samples defined in the analysis class.
    '''
    jobs: list[dict[str, Union[int, float, str]]] = []

    for sample_name, sample_dict in config['samples'].items():
        LOGGER.info('Initializing sample "%s" ...', sample_name)
        info_msg = 'The sample will be processed with the following ' \
                   'parameters:'

        sample_file_list: Optional[list[str]] = None
        file_quantities: Optional[list[dict[str,
                                            Union[int, float, str]]]] = None

        # Check if input directory is provided
        if 'input-dir' in sample_dict:
            if isinstance(sample_dict['input-dir'], str):
                LOGGER.info('Will inspect the sample input directory for the '
                            'sample information.')
                sample_file_list = get_files_in_dir(sample_dict['input-dir'])

        # Check if file list is provided
        if 'input-file-list' in sample_dict:
            if isinstance(sample_dict['input-file-list'], str):
                LOGGER.info('Will inspect the sample input file list for the '
                            'sample information.')
                sample_file_list = \
                    get_file_list(sample_dict['input-file-list'])

        # Check if files are provided
        if 'input-files' in sample_dict:
            if isinstance(sample_dict['input-files'], list):
                if all(isinstance(x, str) for x in sample_dict['input-files']):
                    LOGGER.info('Will inspect directly provided input files '
                                'for the sample information.')
                    sample_file_list = sample_dict['input-files']

        # Using globally set input directory or campaign / production tag
        if sample_file_list is None:
            if config['input-dir'] is not None:
                LOGGER.info('Will inspect the global input directory for the '
                            'sample information.')
                sample_file_list = get_files_in_dir(
                    os.path.join(config['input-dir'], sample_name)
                )
            elif config['campaign'] is not None:
                LOGGER.info('Found the sample information in the campaign: %s',
                            config['campaign'])
                sample_file_list, file_quantities = get_files_in_yaml(
                    sample_name,
                    config['campaign']
                )
            else:
                sample_file_list = None

        if sample_file_list is None:
            LOGGER.error('Could not determine the input file list for the '
                         'sample "%s"!\nAborting...', sample_name)
            sys.exit(3)

        if not sample_file_list:
            LOGGER.warning('The input file list for the sample "%s" is '
                           'empty!\nAborting...', sample_name)
            sys.exit(3)

        info_msg += '\n - total number of files in the sample:  ' \
                    f'{len(sample_file_list):,}'

        # Apply file-path rewrites
        if config['apply-filepath-rewrites']:
            sample_file_list = [apply_filepath_rewrites(fpath) for fpath in
                                sample_file_list]
            if file_quantities is not None:
                file_quantities = [
                    fqs | {'path': apply_filepath_rewrites(fqs['path'])}
                    for fqs in file_quantities
                ]

        # Reduce the sample by a required fraction
        if 'fraction' in sample_dict:
            fraction = 1.
            if isinstance(sample_dict['fraction'], float):
                fraction = sample_dict['fraction']
            else:
                LOGGER.error('Provided sample reduction fraction is not a '
                             'float!\nAborting...')
                sys.exit(3)

            if fraction < 1.:
                if file_quantities is None:
                    file_quantities = get_file_quantities(sample_file_list)
                if not file_quantities:
                    LOGGER.error('Can\'t determine the number of events for '
                                 'the provided input files!\nAborting...')
                    sys.exit(3)
                if len(file_quantities) != len(sample_file_list):
                    LOGGER.warning('For some files the number of events '
                                   'could not be determined!\nThey will be '
                                   'ignored...')
                # print(file_quantities)

                # TODO: Rewrite get_subfile_list() function
                sample_file_list = get_subfile_list(
                    [fqs['path'] for fqs in file_quantities],
                    [fqs['events-in-ttree'] for fqs in file_quantities],
                    fraction
                )
                info_msg += '\n - sample reduction fraction:  ' \
                            f'          {fraction:0,.4g}'
                info_msg += '\n - number of files after reduction:  ' \
                            f'    {len(sample_file_list):,}'

        # Output directory
        output_stem = sample_name
        if 'output' in sample_dict:
            LOGGER.warning('[DEPRECIATED] please use \'output-stem\' instead '
                           'of \'output\' to specify different sample output '
                           'directory.')
            output_stem = sample_dict['output']
            info_msg += '\n - custom output stem set to:  ' \
                        f'          {output_stem}'
        if 'output-stem' in sample_dict:
            output_stem = sample_dict['output-stem']
            info_msg += '\n - custom output stem set to:  ' \
                        f'          {output_stem}'

        # Split into chunks
        n_chunks = 1
        if 'chunks' in sample_dict:
            if isinstance(sample_dict['chunks'], int):
                n_chunks = sample_dict['chunks']
            else:
                LOGGER.error('Provided number of output chunks is not an '
                             'integer!\nAborting...')
                sys.exit(3)

        if n_chunks > len(sample_file_list):
            LOGGER.warning('Can\'t split input sample of %i files into '
                           '%i output chunks!\nAdjusting the number of output '
                           'chunks...',
                           len(sample_file_list), n_chunks)

            n_chunks = len(sample_file_list)

        chunks_list = get_chunk_list(sample_file_list, n_chunks)

        info_msg += '\n - number of output chunks:  ' \
                    f'            {len(chunks_list):,}'

        # Maximum number of events
        n_events_max = None
        if sample_dict['n-events-max'] is not None:
            if n_chunks > 1:
                LOGGER.warning('Specifying maximum number of events is '
                               'not supported in case of multiple output '
                               'chunks.\nIgnoring the setting...')
            else:
                n_events_max = sample_dict['n-events-max']
                info_msg += '\n - Maximum number of events:  ' \
                            f'           {n_events_max}'

        # Stride through the sample
        stride = sample_dict['stride']
        if stride is not None:
            info_msg += '\n - Number of events to stride:  ' \
                        f'         {stride}'

        LOGGER.info(info_msg)

        for idx, chunk_list in enumerate(chunks_list):
            job = {}

            job['name'] = sample_name + f'-{idx}'
            job['input-file-list'] = chunk_list
            job['output-file'] = os.path.join(
                config['output-dir'],
                output_stem,
                output_stem + f'-chunk-{idx}.root'
            )
            job['n-events-max'] = n_events_max
            job['stride'] = stride

            jobs.append(job)
    return jobs


# _____________________________________________________________________________
def generate_jobs(config: dict[str, Any]) -> list[dict[str, Any]]:
    '''
    Generate the jobs to run.
    '''

    # Test job
    if config['test-file'] is not None:
        LOGGER.info('Generating test job...')

        if config['samples'] is not None:
            LOGGER.warning('Samples/processes defined in your analysis script '
                           'will be ignored...')

        job: dict[str, Any] = {}
        job['name'] = 'test'
        job['input-file-list'] = [config['test-file']]
        job['output-file'] = 'test-output.root'
        if config['output-file'] is not None:
            job['output-file'] = config['output-file']
        job['n-events-max'] = config['n-events-max']
        job['stride'] = config['stride']

        return [job]

    # Independent sample
    if config['input-file-list'] is not None:
        LOGGER.info('Generating jobs for independent sample...')

        if config['samples'] is not None:
            LOGGER.warning('Samples/processes defined in your analysis script '
                           'will be ignored...')

        # Apply file-path rewrites
        if config['apply-filepath-rewrites']:
            input_file_list = [apply_filepath_rewrites(fpath) for fpath in
                               config['input-file-list']]
        else:
            input_file_list = config['input-file-list']

        # Only one output chunk
        if config['n-chunks'] is None:
            job = {}
            if config['sample-name'] is not None:
                sample_name = config['sample-name']
            else:
                sample_name = 'independent-sample'

            job['name'] = sample_name
            job['input-file-list'] = input_file_list
            if config['output-file'] is not None:
                job['output-file'] = config['output-file']
            else:
                job['output-file'] = os.path.join(
                    config['output-dir'],
                    sample_name,
                    sample_name + '.root'
                )
            job['n-events-max'] = config['n-events-max']
            job['stride'] = config['stride']

            return [job]

        # Multiple output chunks
        n_chunks = config['n-chunks']

        if n_chunks > len(input_file_list):
            LOGGER.error('Can\'t split input sample of %i files into '
                         '%i output chunks!\nAborting...',
                         len(input_file_list), n_chunks)
            sys.exit(3)

        chunk_list = get_chunk_list(input_file_list, n_chunks)

        if config['output-file'] is not None:
            LOGGER.warning('When processing an independent sample in '
                           'multiple chunks direct output path is '
                           'ignored!\nOutput path is created from the '
                           'output directory and the sample name '
                           'instead!')
        if config['n-events-max'] is not None:
            LOGGER.warning('Specifying maximum number of events is not '
                           'supported in case of multiple output chunks.'
                           '\nIgnoring the setting...')

        jobs = []
        for idx, chunk in enumerate(chunk_list):
            job = {}
            if config['sample-name'] is not None:
                sample_name = config['sample-name']
            else:
                sample_name = 'independent-sample'

            job['name'] = sample_name + f'-{idx}'
            job['input-file-list'] = chunk
            job['output-file'] = os.path.join(
                config['output-dir'],
                sample_name,
                sample_name + f'-chunk-{idx}.root'
            )
            job['n-events-max'] = None
            job['stride'] = config['stride']

            jobs.append(job)

        return jobs

    # Samples defined in samples (process) list
    if config['samples'] is None:
        LOGGER.info('Could not find sample definitions to run!\nAborting...')
        sys.exit(3)

    if len(config['samples']) == 1:
        LOGGER.info('Found one sample defined in the analysis.')
    else:
        LOGGER.info('Found %i samples defined in the analysis.',
                    len(config['samples']))

    return generate_sample_jobs(config)


# _____________________________________________________________________________
def merge_config(args: argparse.Namespace,
                 analysis_class: Any) -> dict[str, Any]:
    '''
    Merge configuration from command line arguments, analysis class and
    environment variables.
    '''
    config: dict[str, Any] = {}

    # Deprecations
    if args.files_list is not None:
        LOGGER.error('--files-list CLI argument is no longer supported, use '
                     '--i/--input instead!\nAborting...')
        sys.exit(3)
    if hasattr(analysis_class, 'process_list'):
        LOGGER.warning('[DEPRECATED] Please use "samples" instead of '
                       '"process_list"!')

    if hasattr(analysis_class, 'prod_tag'):
        LOGGER.warning('[DEPRECATED] Please use "campaign" instead of '
                       '"prod_tag"!')

    # Determining Key4hep stack and OS
    if 'KEY4HEP_STACK' not in os.environ:
        LOGGER.error('Key4hep stack not setup!\nAborting...')
        sys.exit(3)
    k4h_stack_env = os.environ['KEY4HEP_STACK']
    if 'sw-nightlies.hsf.org' in k4h_stack_env:
        config['key4hep-stack'] = 'nightlies'
    elif 'sw.hsf.org' in k4h_stack_env:
        config['key4hep-stack'] = 'release'
    else:
        LOGGER.error('Key4hep stack not recognized!\nAborting...')
        sys.exit(3)

    if 'almalinux9' in k4h_stack_env:
        config['key4hep-os'] = 'alma9'
    elif 'almalinux10' in k4h_stack_env:
        config['key4hep-os'] = 'alma10'
    elif 'ubuntu22' in k4h_stack_env:
        config['key4hep-os'] = 'ubuntu22'
    elif 'ubuntu24' in k4h_stack_env:
        config['key4hep-os'] = 'ubuntu24'
    else:
        LOGGER.error('Key4hep OS not recognized!\nAborting...')
        sys.exit(3)

    # Determine analysis script path
    config['anascript-path'] = os.path.abspath(args.anascript_path)

    # Determine analysis directory
    config['analysis-dir'] = os.path.dirname(
        os.path.abspath(args.anascript_path)
    )

    # Input file list
    config['input-file-list'] = None
    if args.input_file_list is not None:
        config['input-file-list'] = get_file_list(args.input_file_list)
    if args.input is not None:
        config['input-file-list'] = args.input

    # Check for sample name
    config['sample-name'] = None
    if args.sample_name is not None:
        config['sample-name'] = args.sample_name

    # Check for sample list
    config['samples'] = None
    if hasattr(analysis_class, 'process_list'):
        config['samples'] = validate_sample_list(analysis_class.process_list)
    if hasattr(analysis_class, 'samples'):
        config['samples'] = validate_sample_list(analysis_class.samples)

    if config['samples'] == {}:
        LOGGER.warning('Provided samples dictionary contains no elements!')
        config['samples'] = None

    # Check for campaign / production tag
    config['campaign'] = None
    if hasattr(analysis_class, 'campaign'):
        config['campaign'] = analysis_class.campaign
    if hasattr(analysis_class, 'prod_tag'):
        config['campaign'] = analysis_class.prod_tag

    # Check for input directory
    config['input-dir'] = None
    if hasattr(analysis_class, 'input_dir'):
        config['input-dir'] = analysis_class.input_dir

    # Check whether a test is run
    config['test-file'] = None
    if args.test is not None:
        if hasattr(analysis_class, 'test_file'):
            config['test-file'] = analysis_class.test_file
        if args.test_file is not None:
            config['test-file'] = args.test_file

        if config['test-file'] is None:
            LOGGER.error('Could not find a test file!\nAborting...')
            sys.exit(3)

    # Check include header files
    config['include-paths'] = None
    if hasattr(analysis_class, 'include_paths'):
        config['include-paths'] = analysis_class.include_paths

    # Check for analysis name
    config['analysis-name'] = None
    if hasattr(analysis_class, 'analysis_name'):
        config['analysis-name'] = analysis_class.analysis_name
    if args.analysis_name is not None:
        config['analysis-name'] = args.analysis_name

    # Check for output file
    config['output-file'] = None
    if hasattr(analysis_class, 'output_file'):
        config['output-file'] = analysis_class.output_file
    if args.output is not None:
        config['output-file'] = args.output

    # Check for output directory
    config['output-dir'] = None
    if hasattr(analysis_class, 'output_dir'):
        config['output-dir'] = analysis_class.output_dir
    if args.output_dir is not None:
        config['output-dir'] = args.output_dir

    # Check for number of output chunks
    config['n-chunks'] = None
    if args.n_chunks is not None:
        config['n-chunks'] = args.n_chunks

    # Check number of events to be run over
    config['n-events-max'] = None
    if args.nevents is not None:
        config['n-events-max'] = args.nevents

    # Check if stride through the sample
    config['stride'] = None
    if args.stride is not None:
        config['stride'] = args.stride

    # Check number of requested threads
    config['n-threads'] = 1
    if hasattr(analysis_class, "n_threads"):
        config['n-threads'] = analysis_class.n_threads
    if args.ncpus is not None:
        config['n-threads'] = args.ncpus

    # Check whether to use PODIO DataSource to load the events
    config['use-data-source'] = False
    if hasattr(analysis_class, 'use_data_source'):
        config['use-data-source'] = True
    if args.use_data_source:
        config['use_data_source'] = True
    if get_attribute(analysis, 'use_data_source', False):
        config['use_data_source'] = True
    # Check whether to use event weights (only supported as analysis config file option, not command line!)
    config['do_weighted'] = False
    if get_attribute(analysis, 'do_weighted', False):
        config['do_weighted'] = True

    return config


# _____________________________________________________________________________
def global_setup(config):
    '''
    Initialization steps.
    '''

    # For convenience and compatibility with user code
    if config['use-data-source']:
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses::PodioSource;")
    else:
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")

    if config['geometry-path'] is not None and \
            config['readout-name'] is not None:
        ROOT.CaloNtupleizer.loadGeometry(config['geometry-path'],
                                         config['readout-name'])

    if config['n-threads'] < 0:  # use all available threads
        ROOT.EnableImplicitMT()
        config['n-threads'] = ROOT.GetThreadPoolSize()

    if config['n-threads'] > 1:
        ROOT.ROOT.EnableImplicitMT(config['n-threads'])

    if ROOT.IsImplicitMTEnabled():
        ROOT.EnableThreadSafety()
        LOGGER.info('Multithreading enabled. Running over %i threads',
                    ROOT.GetThreadPoolSize())
    else:
        LOGGER.info('No multithreading enabled. Running in a single thread...')

    # Additional include header files
    if config['include-paths'] is not None:
        # Check if the include paths exist
        for path in config['include-paths']:
            if not os.path.isfile(os.path.join(config['analysis-dir'], path)):
                LOGGER.error('Include header file "%s" not found!'
                             '\nAborting...', path)
                sys.exit(3)

        ROOT.gInterpreter.ProcessLine(".O2")
        for path in config['include-paths']:
            LOGGER.info('Loading %s...', path)
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')


# _____________________________________________________________________________
def run_rdf(config: dict[str, any],
            args,
            analysis,
            input_list: list[str],
            out_file: str) -> int:
    '''
    Run the analysis ROOTDataFrame and snapshot it.
    '''
    # Create initial dataframe
    if config['use_data_source']:
        if ROOT.podio.DataSource:
            LOGGER.debug('Found podio::DataSource.')
        else:
            LOGGER.error('podio::DataSource library not found!\nAborting...')
            sys.exit(3)
        LOGGER.info('Loading events through podio::DataSource...')

        try:
            dframe = ROOT.podio.CreateDataFrame(input_list)
        except TypeError as excp:
            LOGGER.error('Unable to build dataframe using '
                         'podio::DataSource!\n%s', excp)
            sys.exit(3)
    else:
        dframe = ROOT.RDataFrame("events", input_list)

    # Limit number of events processed
    if args.nevents > 0:
        dframe2 = dframe.Range(0, args.nevents)
    else:
        dframe2 = dframe

    try:
        evtcount_init = dframe2.Count()
        sow_init = evtcount_init
        if config['do_weighted']:
            sow_init = dframe2.Sum("EventHeader.weight")

        dframe3 = analysis.analyzers(dframe2)

        branch_list = ROOT.vector('string')()
        blist = analysis.output()
        for bname in blist:
            branch_list.push_back(bname)

        evtcount_final = dframe3.Count()
        sow_final = evtcount_final
        if config['do_weighted']:
            sow_final = dframe3.Sum("EventHeader.weight")

        # Generate computational graph of the analysis
        if args.graph:
            generate_graph(dframe, args)

        dframe3.Snapshot("events", out_file, branch_list)
    except Exception as excp:
        LOGGER.error('During the execution of the analysis file exception '
                     'occurred:\n%s', excp)
        sys.exit(3)

    return evtcount_init.GetValue(), evtcount_final.GetValue(), sow_init.GetValue(), sow_final.GetValue()


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

    # Resolve test-file template if needed
    if config.get('test-file') is not None and \
            isinstance(config['test-file'], string.Template):
        config['test-file'] = config['test-file'].substitute(
            key4hep_os=config['key4hep-os'],
            key4hep_stack=config['key4hep-stack'],
            date=datetime.date.today().strftime('%Y-%m-%d')
        )


# _____________________________________________________________________________
def run_fccanalysis(args, anascript_module) -> None:
    '''
    Run analysis of style "Analysis".
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
def run_local(config: dict[str, any],
              args: object,
              analysis: object,
              infile_list):
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

    # Same for the sum of weights
    if config['do_weighted']:
        sow_orig = 0.
        sow_local = 0.

    for filepath in infile_list:

        if not config['use_data_source']:
            filepath = apply_filepath_rewrites(filepath)

        file_list.push_back(filepath)
        info_msg += f'- {filepath}\t\n'

        if config['do_weighted']:
             # Adjust number of events in case --nevents was specified
            if args.nevents > 0:
                nevts_param, nevts_tree, sow_param, sow_tree = get_entries_sow(filepath, args.nevents)
            else:
                nevts_param, nevts_tree, sow_param, sow_tree = get_entries_sow(filepath)

            nevents_orig += nevts_param
            nevents_local += nevts_tree
            sow_orig += sow_param
            sow_local += sow_tree

        else:
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

             # Adjust number of events in case --nevents was specified
            if args.nevents > 0 and args.nevents < nevents_local:
                nevents_local = args.nevents


    LOGGER.info(info_msg)

   
    if nevents_orig > 0:
        LOGGER.info('Number of events:\n\t- original: %s\n\t- local:    %s',
                    f'{nevents_orig:,}', f'{nevents_local:,}')
        if config['do_weighted']:
            LOGGER.info('Sum of weights:\n\t- original: %s\n\t- local:    %s',
                        f'{sow_orig:,}', f'{sow_local:,}')
    else:
        LOGGER.info('Number of local events: %s', f'{nevents_local:,}')
        if config['do_weighted']:
            LOGGER.info('Local sum of weights: %s', f'{sow_local:0,.2f}')


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
    inn, outn, in_sow, out_sow = run_rdf(config, args, analysis, file_list, outfile_path)
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
    if config['do_weighted']:
        info_msg += f'\nTotal sum of weights processed:  {float(in_sow):0,.2f}'
        info_msg += f'\nNo. result weighted events :       {float(out_sow):0,.2f}'
        if in_sow > 0:
            info_msg += f'\nReduction factor local, weighted:  {float(out_sow/in_sow):0,.4f}'
        if sow_orig > 0:
            info_msg += f'\nReduction factor total, weighted:  {float(out_sow/sow_orig):0,.4f}'
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

        if config['do_weighted']:
            param_sow = ROOT.TParameter(float)( 
                        'SumOfWeights', 
                        sow_orig if sow_orig != 0 else in_sow )
            param_sow.Write()
            param_sow = ROOT.TParameter(float)('SumOfWeightsSelected', out_sow) # No of weighted, selected events
            param_sow.Write()
        outfile.Write()

    if args.bench:
        analysis_name = get_attribute(analysis,
                                      'analysis_name', args.anascript_path)

        bench_time = {}
        bench_time['name'] = 'Time spent running the analysis: ' + \
                             analysis_name
        bench_time['unit'] = 'Seconds'
        bench_time['value'] = total_elapsed_time
        bench_time['range'] = 10
        bench_time['extra'] = 'Analysis path: ' + config['anascript-path']
        save_benchmark('benchmarks_smaller_better.json', bench_time)

        bench_evt_per_sec = {}
        bench_evt_per_sec['name'] = 'Events processed per second: ' + \
                                    analysis_name
        bench_evt_per_sec['unit'] = 'Evt/s'
        bench_evt_per_sec['value'] = total_events / total_elapsed_time
        bench_evt_per_sec['range'] = 1000
        bench_evt_per_sec['extra'] = 'Analysis path: ' + \
                                     config['anascript-path']
        save_benchmark('benchmarks_bigger_better.json', bench_evt_per_sec)


# _____________________________________________________________________________
def run_fccanalysis(args, analysis_module):
    '''
    Run analysis of style "Analysis".
    '''

    # Get analysis class out of the module
    analysis_args = vars(args)
    analysis = analysis_module.Analysis(analysis_args)

    # Merge configuration from command line arguments and analysis class
    config: dict[str, any] = merge_config(args, analysis)

    # Set number of threads, load header files, custom dicts, ...
    initialize(config, args, analysis_module)

    # Check if output directory exist and if not create it
    output_dir = get_attribute(analysis, 'output_dir', None)
    if output_dir is not None and not os.path.exists(output_dir):
        os.system(f'mkdir -p {output_dir}')

    # Check if eos output directory exist and if not create it
    output_dir_eos = get_attribute(analysis, 'output_dir_eos', None)
    if output_dir_eos is not None and not os.path.exists(output_dir_eos):
        os.system(f'mkdir -p {output_dir_eos}')

    if config['do_weighted']:
        LOGGER.info('Using generator weights')

    # Check if test mode is specified, and if so run the analysis on it (this
    # will exit after)
    if args.test:
        LOGGER.info('Running over test file...')
        testfile_path = getattr(analysis, "test_file")
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(config, args, analysis, [testfile_path])
        sys.exit(0)

    # Check if files are specified, and if so run the analysis on it/them (this
    # will exit after)
    if len(args.files_list) > 0:
        LOGGER.info('Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(config, args, analysis, args.files_list)
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
        if len(chunk_list) > 1:
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
                run_local(config, args, analysis, chunk_list[0])
            else:
                for index, chunk in enumerate(chunk_list):
                    args.output = f'{output_stem}/chunk{index}.root'
                    run_local(config, args, analysis, chunk)

    if len(process_list) == 0:
        LOGGER.warning('No files processed (process_list not found)!\n'
                       'Exiting...')
