'''
Run analysis of style "Analysis", which can be split into several stages.
'''

import os
import sys
import time
import logging
import argparse
import string
from typing import Any

import ROOT  # type: ignore
from anascript import get_element_dict, get_attribute
from process import get_process_info, get_entries_sow
from process import get_subfile_list, get_chunk_list
from utils import generate_graph, save_benchmark


ROOT.gROOT.SetBatch(True)

LOGGER = logging.getLogger('FCCAnalyses.run')


# _____________________________________________________________________________
def merge_config(args: argparse.Namespace, analysis: Any) -> dict[str, Any]:
    '''
    Merge configuration from command line arguments and analysis class.
    '''
    config: dict[str, Any] = {}

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

    # Put runBatch deprecation warning
    if hasattr(analysis, 'run_batch'):
        if analysis.run_batch:
            LOGGER.error('run_batch analysis attribute is no longer '
                         'supported, use "fccanalysis submit" instead!\n'
                         'Aborting...')
            sys.exit(3)

    # Check whether to use PODIO DataSource to load the events
    config['use_data_source'] = False
    if args.use_data_source:
        config['use_data_source'] = True
    if get_attribute(analysis, 'use_data_source', False):
        config['use_data_source'] = True
    # Check whether to use event weights (only supported as analysis config
    # file option, not command line!)
    config['do_weighted'] = False
    if get_attribute(analysis, 'do_weighted', False):
        config['do_weighted'] = True

    # Check the output path
    # config['output_file_path'] = None
    # if args.output

    return config


# _____________________________________________________________________________
def initialize(config, args, analysis):
    '''
    Common initialization steps.
    '''

    # For convenience and compatibility with user code
    if config['use_data_source']:
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses::PodioSource;")
    else:
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
        ROOT.gInterpreter.ProcessLine(".O2")
        basepath = os.path.dirname(os.path.abspath(args.anascript_path)) + "/"
        for path in include_paths:
            LOGGER.info('Loading %s...', path)
            ROOT.gInterpreter.Declare(f'#include "{basepath}/{path}"')


# _____________________________________________________________________________
def run_rdf(config: dict[str, Any],
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
def run_local(config: dict[str, Any],
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
                nevts_param, nevts_tree, sow_param, sow_tree = \
                    get_entries_sow(filepath, args.nevents)
            else:
                nevts_param, nevts_tree, sow_param, sow_tree = \
                    get_entries_sow(filepath)

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

    outfile_path = args.output
    LOGGER.info('Output file path:\n%s', outfile_path)

    # Run RDF
    start_time = time.time()
    inn, outn, in_sow, out_sow = run_rdf(config, args, analysis, file_list,
                                         outfile_path)
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
                        sow_orig if sow_orig != 0 else in_sow)
            param_sow.Write()
            # No of weighted, selected events
            param_sow = ROOT.TParameter(float)('SumOfWeightsSelected', out_sow)
            param_sow.Write()
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
    analysis = analysis_module.Analysis(vars(args))

    # Merge configuration from command line arguments and analysis class
    config: dict[str, Any] = merge_config(args, analysis)

    # Set number of threads, load header files, custom dicts, ...
    initialize(config, args, analysis_module)

    # Check if output directory exist and if not create it
    output_dir = get_attribute(analysis, 'output_dir', None)
    if output_dir is not None and not os.path.exists(output_dir):
        os.system(f'mkdir -p {output_dir}')

    # Check if EOS output directory exist and if not create it
    output_dir_eos = get_attribute(analysis, 'output_dir_eos', None)
    if output_dir_eos is not None and not os.path.exists(output_dir_eos):
        os.system(f'mkdir -p {output_dir_eos}')

    if config['do_weighted']:
        LOGGER.info('Using generator weights')

    # Check if test mode is specified, and if so run the analysis on it (this
    # will exit afterwards)
    if args.test:
        LOGGER.info('Running over test file...')
        testfile_path = getattr(analysis, "test_file")
        if isinstance(testfile_path, string.Template):
            testfile_path = testfile_path.substitute(
                key4hep_os=config['key4hep-os'],
                key4hep_stack=config['key4hep-stack']
            )

        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(config, args, analysis, [testfile_path])
        sys.exit(0)

    # Check if input file(s) are specified, and if so run the analysis on
    # it/them (this will exit afterwards)
    if len(args.files_list) > 0:
        LOGGER.info('Running over files provided in command line argument...')
        directory, _ = os.path.split(args.output)
        if directory:
            os.system(f'mkdir -p {directory}')
        run_local(config, args, analysis, args.files_list)
        sys.exit(0)

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
        try:
            process_input_dir = process_list[process_name]['input_dir']
        except KeyError:
            process_input_dir = None
        file_list, event_list = get_process_info(process_name,
                                                 prod_tag,
                                                 input_dir,
                                                 process_input_dir)

        if len(file_list) <= 0:
            LOGGER.error('No files to process!\nAborting...')
            sys.exit(3)

        # Determine the fraction of the input to be processed
        fraction = 1.
        if get_element_dict(process_list[process_name], 'fraction'):
            fraction = get_element_dict(process_list[process_name], 'fraction')

        if fraction < 1:
            file_list = get_subfile_list(file_list, event_list, fraction)

        # Determine the number of chunks the output will be split into
        n_chunks = 1
        if get_element_dict(process_list[process_name], 'chunks'):
            n_chunks = get_element_dict(process_list[process_name], 'chunks')

        chunk_list = [file_list]
        if n_chunks > 1:
            chunk_list = get_chunk_list(file_list, n_chunks)
            n_chunks = len(chunk_list)

        # Put together output path
        output_stem = process_name
        if get_element_dict(process_list[process_name], 'output'):
            output_stem = get_element_dict(process_list[process_name],
                                           'output')
        output_dir = get_attribute(analysis, 'output_dir', '')

        if n_chunks == 1:
            output_filepath = os.path.join(output_dir, output_stem+'.root')
            output_dir = None
        else:
            output_filepath = None
            output_dir = os.path.join(output_dir, output_stem)

        info_msg = 'Will proceed with:'
        if fraction < 1:
            info_msg += f'\n    - input reduction fraction: {fraction}'
        info_msg += f'\n    - number of input files: {len(file_list):,}'
        if output_dir is not None:
            info_msg += f'\n    - output directory: {output_dir}'
        if n_chunks > 1:
            info_msg += f'\n    - number of output chunks: {n_chunks:,}'
        if output_filepath is not None:
            info_msg += f'\n    - output file path: {output_filepath}'
        LOGGER.info(info_msg)

        # Create directory if more than 1 chunk
        if n_chunks > 1:
            if not os.path.exists(output_dir):
                os.system(f'mkdir -p {output_dir}')

        # Running locally
        LOGGER.info('Running locally...')
        if n_chunks == 1:
            args.output = output_filepath
            run_local(config, args, analysis, chunk_list[0])
        else:
            for index, chunk in enumerate(chunk_list):
                args.output = f'{output_dir}/chunk{index}.root'
                run_local(config, args, analysis, chunk)

    if len(process_list) == 0:
        LOGGER.warning('No files processed (process_list not found)!\n'
                       'Exiting...')
