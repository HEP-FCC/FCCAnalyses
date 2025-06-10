'''
Run analysis in one of the different styles.
'''

import os
import sys
import time
import logging
import importlib.util
import string

import ROOT  # type: ignore
import cppyy
from anascript import get_element, get_element_dict, get_attribute
from process import get_process_info, get_process_dict
from process import get_subfile_list, get_chunk_list
from utils import generate_graph, save_benchmark
from run_fccanalysis import run_fccanalysis


ROOT.gROOT.SetBatch(True)

LOGGER = logging.getLogger('FCCAnalyses.run')


# _____________________________________________________________________________
def initialize(args, rdf_module, anapath: str):
    '''
    Common initialization steps.
    '''

    # Put runBatch deprecation warning
    if hasattr(rdf_module, 'runBatch'):
        if rdf_module.runBatch:
            LOGGER.error('runBatch script attribute is no longer supported, '
                         'use "fccanalysis submit" instead!\nAborting...')
            sys.exit(3)

    # for convenience and compatibility with user code
    if args.use_data_source:
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses::PodioSource;")
    else:
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
            outfile_path: str,
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

        # Registering Count before Snapshot to avoid additional event loops
        evtcount_final = dframe3.Count()

        # Generate computational graph of the analysis
        if args.graph:
            generate_graph(dframe, args)

        dframe3.Snapshot("events", outfile_path, branch_list)
    except cppyy.gbl.std.runtime_error as err:
        LOGGER.error('%s\nDuring the execution of the analysis script an '
                     'exception occurred!\nAborting...', err)
        sys.exit(3)

    return evtcount_init.GetValue(), evtcount_final.GetValue()


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
        info_msg += f'\t- {filepath}\n'
        try:
            infile = ROOT.TFile.Open(filepath, 'READ')
        except OSError as excp:
            LOGGER.error('While opening input file:\n%s\nan error '
                         'occurred:\n%s\nAborting...', filepath, excp)
            sys.exit(3)

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

    # Check if EOS outputDir exist and if not create it
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

    # Check if the process list is specified
    process_list = get_element(rdf_module, 'processList')

    for process_name in process_list:
        try:
            process_input_dir = process_list[process_name]['inputDir']
        except KeyError:
            process_input_dir = None
        file_list, event_list = get_process_info(
            process_name,
            get_element(rdf_module, "prodTag"),
            get_element(rdf_module, "inputDir"),
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
        chunks = 1
        if get_element_dict(process_list[process_name], 'chunks'):
            chunks = get_element_dict(process_list[process_name], 'chunks')

        chunk_list = [file_list]
        if chunks > 1:
            chunk_list = get_chunk_list(file_list, chunks)
        LOGGER.info('Number of the output files: %s', f'{len(chunk_list):,}')

        # Put together output path
        output_stem = process_name
        if get_element_dict(process_list[process_name], 'output'):
            output_stem = get_element_dict(process_list[process_name],
                                           'output')
        output_dir = get_attribute(rdf_module, 'outputDir', '')

        if chunks == 1:
            output_filepath = os.path.join(output_dir, output_stem+'.root')
            output_dir = None
        else:
            output_filepath = None
            output_dir = os.path.join(output_dir, output_stem)

        info_msg = f'Adding process "{process_name}" with:'
        if fraction < 1:
            info_msg += f'\n\t- fraction:         {fraction}'
        info_msg += f'\n\t- number of files:  {len(file_list):,}'
        if output_dir:
            info_msg += f'\n\t- output directory:      {output_dir}'
        if output_filepath:
            info_msg += f'\n\t- output file path:      {output_dir}'
        if chunks > 1:
            info_msg += f'\n\t- number of chunks: {chunks}'

        # Create directory if more than 1 chunk
        if chunks > 1:
            output_directory = os.path.join(output_dir, output_stem)

            if not os.path.exists(output_directory):
                os.system(f'mkdir -p {output_directory}')

        # Running locally
        LOGGER.info('Running locally...')
        if len(chunk_list) == 1:
            args.output = output_filepath
            run_local(rdf_module, chunk_list[0], args)
        else:
            for index, chunk in enumerate(chunk_list):
                args.output = os.path.join(output_dir, f'chunk{index}.root')
                run_local(rdf_module, chunk, args)


def run_histmaker(args, rdf_module, anapath):
    '''
    Run the analysis using histmaker (all stages integrated into one).
    '''

    # Check whether to use PODIO ROOT DataSource to load the events
    if get_element(rdf_module, "useDataSource", False):
        args.use_data_source = True

    # set ncpus, load header files, custom dicts, ...
    initialize(args, rdf_module, anapath)

    # Determining Key4hep stack and OS
    if 'KEY4HEP_STACK' not in os.environ:
        LOGGER.error('Key4hep stack not setup!\nAborting...')
        sys.exit(3)
    k4h_stack_env = os.environ['KEY4HEP_STACK']
    if 'sw-nightlies.hsf.org' in k4h_stack_env:
        key4hep_stack = 'nightlies'
    elif 'sw.hsf.org' in k4h_stack_env:
        key4hep_stack = 'release'
    else:
        LOGGER.error('Key4hep stack not recognized!\nAborting...')
        sys.exit(3)

    if 'almalinux9' in k4h_stack_env:
        key4hep_os = 'alma9'
    elif 'ubuntu22' in k4h_stack_env:
        key4hep_os = 'ubuntu22'
    elif 'ubuntu24' in k4h_stack_env:
        key4hep_os = 'ubuntu24'
    else:
        LOGGER.error('Key4hep OS not recognized!\nAborting...')
        sys.exit(3)

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
    for process_name, process_dict in process_list.items():
        try:
            process_input_dir = process_list[process_name]['inputDir']
        except KeyError:
            process_input_dir = None

        if args.test:
            try:
                if get_element_dict(process_dict, 'testfile') is not None:
                    testfile_path = get_element_dict(process_dict, 'testfile')
                    if isinstance(testfile_path, string.Template):
                        testfile_path = testfile_path.substitute(
                            key4hep_os=key4hep_os,
                            key4hep_stack=key4hep_stack
                        )
                    file_list = [testfile_path]
            except TypeError:
                LOGGER.warning('No test file for process %s found!\n'
                               'Aborting...')
                sys.exit(3)
            fraction = 1
            output = process_name
            chunks = 1
        else:
            file_list, event_list = get_process_info(
                process_name,
                get_element(rdf_module, "prodTag"),
                get_element(rdf_module, "inputDir"),
                process_input_dir)
            if len(file_list) == 0:
                LOGGER.error('No files to process!\nAborting...')
                sys.exit(3)
            fraction = 1
            output = process_name
            chunks = 1
            try:
                if get_element_dict(process_dict, 'fraction') is not None:
                    fraction = get_element_dict(process_dict, 'fraction')
                if get_element_dict(process_dict, 'output') is not None:
                    output = get_element_dict(process_dict, 'output')
                if get_element_dict(process_dict, 'chunks') is not None:
                    chunks = get_element_dict(process_dict, 'chunks')
            except TypeError:
                LOGGER.warning('No values set for process %s will use default '
                               'values!', process_name)
            if fraction < 1:
                file_list = get_subfile_list(file_list, event_list, fraction)

        # get the number of events processed, in a potential previous step
        file_list_root = ROOT.vector('string')()
        # amount of events processed in previous stage (= 0 if it is the first
        # stage)
        nevents_meta = 0
        for file_name in file_list:
            if not args.use_data_source:
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
        events_processed_dict[process_name] = nevents_meta
        info_msg = f'Add process "{process_name}" with:'
        info_msg += f'\n\tfraction = {fraction}'
        info_msg += f'\n\tnFiles = {len(file_list_root):,}'
        info_msg += f'\n\toutput = {output}\n\tchunks = {chunks}'
        LOGGER.info(info_msg)

        if args.use_data_source:
            if ROOT.podio.DataSource:
                LOGGER.debug('Found Podio ROOT DataSource.')
            else:
                LOGGER.error('Podio ROOT DataSource library not found!'
                             '\nAborting...')
                sys.exit(3)
            LOGGER.info('Loading events through podio::DataSource...')

            try:
                dframe = ROOT.podio.CreateDataFrame(file_list_root)
            except TypeError as excp:
                LOGGER.error('Unable to build dataframe using '
                             'podio::DataSource!\n%s', excp)
                sys.exit(3)
        else:
            dframe = ROOT.ROOT.RDataFrame("events", file_list_root)
        evtcount = dframe.Count()

        try:
            res, hweight = graph_function(dframe, process_name)
        except cppyy.gbl.std.runtime_error as err:
            LOGGER.error(err)
            LOGGER.error('During loading of the analysis an error occurred!'
                         '\nAborting...')
            sys.exit(3)

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
        with ROOT.TFile(os.path.join(output_dir, f'{process}.root'),
                        'RECREATE'):
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

    try:
        dash_dash_index = sys.argv.index('--')
        args = parser.parse_args(sys.argv[1:dash_dash_index])
        args.remaining = sys.argv[dash_dash_index+1:]
    except ValueError:
        args = parser.parse_args()
        args.remaining = []

    if not hasattr(args, 'command'):
        LOGGER.error('Error occurred during subcommand routing!\nAborting...')
        sys.exit(3)

    if args.command != 'run':
        LOGGER.error('Unknow sub-command "%s"!\nAborting...')
        sys.exit(3)

    # Work with absolute path of the analysis script
    anapath = os.path.abspath(args.anascript_path)

    # Check that the analysis file exists
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
    LOGGER.info('Loading analysis script:\n%s', anapath)
    try:
        rdf_spec = importlib.util.spec_from_file_location('rdfanalysis',
                                                          anapath)
        rdf_module = importlib.util.module_from_spec(rdf_spec)
        rdf_spec.loader.exec_module(rdf_module)
    except SyntaxError as err:
        LOGGER.error('Syntax error encountered in the analysis script:\n%s',
                     err)
        sys.exit(3)

    # Merge configuration from analysis script file with command line arguments
    if get_element(rdf_module, 'graph', False):
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
        run_fccanalysis(args, rdf_module)
    if hasattr(rdf_module, "RDFanalysis"):
        run_stages(args, rdf_module, anapath)
    if hasattr(rdf_module, "build_graph"):
        run_histmaker(args, rdf_module, anapath)
