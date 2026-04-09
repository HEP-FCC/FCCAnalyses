'''
Run analysis of style "Analysis", which can be split into several stages.
'''

import os
import sys
import logging
import argparse
from typing import Any, Optional, Union

import ROOT  # type: ignore
from anascript import validate_analysis_class
from sample import get_file_list, get_subfile_list, get_chunk_list
from sample import get_files_in_dir, get_files_in_yaml
from sample import get_file_quantities
from sample import apply_filepath_rewrites
from utils import save_benchmark
from job import Job


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
                sample_file_list = get_files_in_dir(sample_dict['input-dir'])

        # Check if file list is provided
        if 'input-file-list' in sample_dict:
            if isinstance(sample_dict['input-file-list'], str):
                sample_file_list = \
                    get_file_list(sample_dict['input-file-list'])

        # Check if files are provided
        if 'input-files' in sample_dict:
            if isinstance(sample_dict['input-files'], list):
                if all(isinstance(x, str) for x in sample_dict['input-files']):
                    sample_file_list = sample_dict['input-files']

        # Using globally set input directory or campaign / production tag
        if sample_file_list is None:
            if config['input-dir'] is not None:
                sample_file_list = get_files_in_dir(
                    os.path.join(config['input-dir'], sample_name)
                )
            elif config['campaign'] is not None:
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

                # TODO: Rewrite get_subfile_list() function
                sample_file_list = get_subfile_list(
                    [fqs['path'] for fqs in file_quantities],
                    [fqs['events-in-ttree'] for fqs in file_quantities],
                    fraction
                )
                info_msg += '\n - sample reduction fraction:  ' \
                            f'{fraction:0,.4g}'
                info_msg += '\n - number of files after reduction:  ' \
                            f'{len(sample_file_list):,}'

        # Split into chunks
        n_chunks = 1
        if 'chunks' in sample_dict:
            if isinstance(sample_dict['chunks'], int):
                n_chunks = sample_dict['chunks']
            else:
                LOGGER.error('Provided nunmber of output chunks is not an '
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

        LOGGER.info(info_msg)

        for idx, chunk_list in enumerate(chunks_list):
            job = {}

            job['name'] = sample_name + f'-{idx}'
            job['input-file-list'] = chunk_list
            job['output-file'] = os.path.join(
                config['output-dir'],
                sample_name,
                sample_name + f'-chunk-{idx}.root'
            )
            jobs.append(job)
    return jobs


# _____________________________________________________________________________
def generate_jobs(config: dict[str, Any]) -> list[dict[str, Any]]:
    '''
    Generate the jobs to run.
    '''

    # Test job
    if config['test-file'] is not None:
        job: dict[str, Any] = {}
        job['name'] = 'test'
        job['input-file-list'] = config['test-file']
        job['output-file'] = 'test-output.root'
        if config['output-file'] is not None:
            job['output-file'] = config['output-file']

        return [job]

    # Independent sample
    if config['input-file-list'] is not None:
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
            jobs.append(job)

        return jobs

    # Samples defined in samples (process) list
    if config['samples'] is None:
        LOGGER.info('Could not find sample definitions to run!\nAborting...')
        sys.exit(3)

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
        LOGGER.warning('[DEPRECATED] the "process_list" analysis argument '
                       'will be replaced by more general "samples".')

    if hasattr(analysis_class, 'prod_tag'):
        LOGGER.warning('[DEPRECATED] the "prod_tag" analysis argument '
                       'will be replaced by "campaign" argument.')

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
        config['samples'] = analysis_class.process_list
    if hasattr(analysis_class, 'samples'):
        config['samples'] = analysis_class.samples

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
        else:
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
    if hasattr(analysis_class, 'output'):
        config['output-file'] = analysis_class.output
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
    if hasattr(analysis_class, 'n_events_max'):
        config['n-events-max'] = analysis_class.n_events_max
    if args.nevents is not None:
        config['n-events-max'] = args.nevents

    # Check if stride through the sample
    config['stride'] = None
    if hasattr(analysis_class, 'stride'):
        config['stride'] = analysis_class.stride
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
        config['use-data-source'] = True

    # Check if the progress-bar is enabled
    config['enable-progress-bar'] = True
    if args.progress_bar is not None:
        config['enable-progress-bar'] = args.progress_bar

    # Check whether to create the computational graph
    config['generate-graph'] = False
    config['graph-path'] = None
    if args.graph is not None:
        config['generate-graph'] = args.graph

        if config['generate-graph']:
            config['graph-path'] = args.graph_path
            if config['graph-path'] is None:
                config['graph_path'] = os.path.join(os.getcwd(),
                                                    'fccanalysis_graph.dot')

    # Load geometry, needed for the CaloNtupleizer analyzers
    config['geometry-path'] = None
    if hasattr(analysis_class, 'geometry_path'):
        config['geometry-path'] = analysis_class.geometry_path

    config['readout-name'] = None
    if hasattr(analysis_class, 'readout_name'):
        config['readout-name'] = analysis_class.readout_name

    # Check whether to apply file-path rewrites
    config['apply-filepath-rewrites'] = True
    if args.apply_filepath_rewrites is not None:
        config['apply-filepath-rewrites'] = args.apply_filepath_rewrites

    # Check whether to save benchmark results
    config['bench'] = False
    if args.bench is not None:
        config['bench'] = args.bench

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
            success = ROOT.gInterpreter.Declare(
                f'#include "{os.path.join(config["analysis-dir"], path)}"'
            )
            if not success:
                LOGGER.error('Error occurred when JIT compiling "%s" include '
                             'header file!\nAborting...', path)
                sys.exit(3)


# _____________________________________________________________________________
def run_fccanalysis(args, anascript_module) -> None:
    '''
    Run analysis of style "Analysis".
    '''
    config: dict[str, Any] = {}

    # Get analysis class out of the module
    # Also, execute the "constructor" of the analysis class
    LOGGER.info('Initializing analysis class...')
    config |= validate_analysis_class(anascript_module.Analysis(vars(args)))

    LOGGER.info('Setting run parameters...')
    # Merge configuration from command line arguments and analysis class
    config |= merge_config(args, config['analysis-class'])

    # Set number of threads, load header files, ...
    global_setup(config)

    # Generate jobs to be run
    jobs = generate_jobs(config)

    if len(jobs) <= 0:
        LOGGER.error('No jobs to be executed!\nAborting...')
        sys.exit(3)
    elif len(jobs) == 1:
        LOGGER.info('Will execute 1 job...')
    else:
        LOGGER.info('Will execute %i jobs...', len(jobs))

    total_events = 0
    total_elapsed_time = 0.

    for job in jobs:
        LOGGER.info('Starting job: %s ...', job['name'])
        directory, _ = os.path.split(job['output-file'])
        if directory:
            os.system(f'mkdir -p {directory}')

        dframe_job = Job(job['input-file-list'],
                         config['analysis-chain'],
                         config['use-data-source'])

        dframe_job.setup_output(job['output-file'],
                                config['output-variables'])

        if config['enable-progress-bar']:
            dframe_job.enable_progress_bar()

        dframe_job.restrict_events(config['n-events-max'],
                                   config['stride'])

        dframe_job.run()

        dframe_job.finalize()

        if config['generate-graph']:
            dframe_job.generate_analysis_graph(config['graph-path'])

        n_events, elapsed_time = dframe_job.get_benchmark_info()
        total_events += n_events
        total_elapsed_time += elapsed_time

    if config['bench']:
        analysis_name = config['analysis-name'] or config['anascript-path']

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
