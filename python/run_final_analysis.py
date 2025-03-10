'''
Run final stage of an analysis
'''

import os
import sys
import time
import glob
import logging
import importlib.util
import pathlib
import json
import math

import ROOT  # type: ignore
import cppyy
from anascript import get_element, get_attribute
from process import get_process_dict, get_entries_sow
from utils import generate_graph

LOGGER = logging.getLogger('FCCAnalyses.run_final')

ROOT.gROOT.SetBatch(True)


# _____________________________________________________________________________
def get_entries(infilepath: str) -> tuple[int, int]:
    '''
    Get number of original entries and number of actual entries in the file
    '''
    events_processed = 0
    events_in_ttree = 0

    with ROOT.TFile(infilepath, 'READ') as infile:
        try:
            events_processed = infile.Get('eventsProcessed').GetVal()
        except AttributeError:
            LOGGER.warning('Input file is missing information about '
                           'original number of events!')

        try:
            events_in_ttree = infile.Get("events").GetEntries()
        except AttributeError:
            LOGGER.error('Input file is missing "events" TTree!\n  - %s'
                         '\nAborting...')
            sys.exit(3)

    return events_processed, events_in_ttree


# _____________________________________________________________________________
def get_processes(rdf_module: object) -> list[str]:
    '''
    Get processes from the analysis script or find them in the input directory.
    TODO: filter out files without .root suffix
    '''
    process_list: list[str] = get_attribute(rdf_module, 'processList', [])
    input_dir: str = get_attribute(rdf_module, 'inputDir', '')
    if not process_list:
        files_or_dirs = glob.glob(f'{input_dir}/*')
        process_list = [pathlib.Path(p).stem for p in files_or_dirs]
        info_msg = f'Found {len(process_list)} processes in the input ' \
                   'directory:'
        for process_name in process_list:
            info_msg += f'\n  - {process_name}'
        LOGGER.info(info_msg)

    return process_list


# _____________________________________________________________________________
def find_sample_files(input_dir: str,
                      sample_name: str) -> list[str]:
    '''
    Find input files for the specified sample name.
    '''
    result: list[str] = []

    full_input_path = os.path.abspath(os.path.join(input_dir, sample_name))

    # Find all input files ending with .root
    if os.path.isdir(full_input_path):
        all_files = os.listdir(full_input_path)
        # Remove files not ending with `.root`
        all_files = [f for f in all_files if f.endswith('.root')]
        # Remove directories
        all_files = [f for f in all_files
                     if os.path.isfile(os.path.join(full_input_path, f))]
        result = [os.path.join(full_input_path, f) for f in all_files]

    # Handle case when there is just one input file
    if len(result) < 1:
        if os.path.isfile(full_input_path + '.root'):
            result.append(full_input_path + '.root')
        else:
            LOGGER.debug('Input file "%s" does not exist!',
                         full_input_path + '.root')

    if len(result) < 1:
        LOGGER.error('Can not find input files for "%s" sample!\nAborting...',
                     sample_name)
        sys.exit(3)

    return result


# _____________________________________________________________________________
def save_results(results: dict[str, dict[str, any]],
                 rdf_module: object) -> None:
    '''
    Save results into various formats, depending on the analysis script.
    '''
    output_dir: str = get_attribute(rdf_module, 'outputDir', '.')

    if get_attribute(rdf_module, 'saveJSON', False):
        json_path: str = os.path.join(output_dir, 'results.json')
        LOGGER.info('Saving results into JSON file:\n%s', json_path)
        save_json(results, json_path)

    if get_attribute(rdf_module, 'saveTabular', False):
        cut_labels: dict[str, str] = get_attribute(rdf_module, 'cutLabels',
                                                   None)
        tables_path: str = os.path.join(output_dir, 'outputTabular.txt')
        LOGGER.info('Saving results in LaTeX tables to:\n%s', tables_path)
        save_tables(results, tables_path, cut_labels)


# _____________________________________________________________________________
def save_json(results: dict[str, dict[str, any]],
              outpath: str) -> None:
    '''
    Save results into a JSON file.
    '''
    with open(outpath, 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile)


# _____________________________________________________________________________
def save_tables(results: dict[str, dict[str, any]],
                outpath: str,
                cut_labels: dict[str, str] = None) -> None:
    '''
    Save results into LaTeX tables.
    '''
    cut_names: list[str] = list(results[next(iter(results))].keys())
    if not cut_names:
        LOGGER.error('No results found!\nAborting...')
        sys.exit(3)

    if cut_labels is None:
        cut_labels = {}
        for name in cut_names:
            cut_labels[name] = f'{name}'

    cut_labels['all_events'] = 'All events'

    with open(outpath, 'w', encoding='utf-8') as outfile:
        # Printing the number of events in format of a LaTeX table
        # Yields
        outfile.write('Yields:\n')
        outfile.write('\\begin{table}[H]\n'
                      '    \\resizebox{\\textwidth}{!}{\n')

        outfile.write('        \\begin{tabular}{|l||')
        outfile.write('c|' * (len(cut_labels) + 2))  # Number of cuts
        outfile.write('} \\hline\n')

        outfile.write(8 * ' ')
        outfile.write(' & ')
        outfile.write(' & '.join(cut_labels.values()))
        outfile.write(' \\\\ \\hline\n')

        for process_name, result in results.items():
            outfile.write(8 * ' ')
            outfile.write(process_name)
            for cut_name in cut_names:
                cut_result: dict[str, any] = result[cut_name]
                outfile.write(' & ')
                if cut_result["n_events_raw"] == 0.:
                    outfile.write('0.')
                else:
                    outfile.write(f'{cut_result["n_events"]:.2e}')
                    outfile.write(' $\\pm$ ')
                    outfile.write(f'{cut_result["uncertainty"]:.2e}')
            outfile.write(' \\\\\n')
        outfile.write('        \\hline\n'
                      '    \\end{tabular}}\n'
                      '    \\caption{Caption}\n'
                      '    \\label{tab:my_label}\n'
                      '\\end{table}')

        # Efficiency:
        outfile.write('\n\nEfficiency:\n')
        outfile.write('\\begin{table}[H] \n'
                      '    \\resizebox{\\textwidth}{!}{ \n')

        outfile.write('    \\begin{tabular}{|l||')
        outfile.write('c|' * len(results))
        outfile.write('} \\hline\n')

        outfile.write(8 * ' ')
        outfile.write(' & ')
        outfile.write(' & '.join(results.keys()))
        outfile.write(' \\hline \\\\\n')

        for cut_name in cut_names:
            if cut_name == 'all_events':
                continue
            outfile.write(8 * ' ')
            outfile.write(f'{cut_name}')
            for result in results.values():
                efficiency = result[cut_name]['n_events'] / \
                             result['all_events']['n_events']
                if efficiency == 0.:
                    outfile.write(' & 0.')
                else:
                    outfile.write(f' & {efficiency:.3g}')
            outfile.write(' \\\\\n')

        outfile.write('        \\hline\n'
                      '    \\end{tabular}}\n'
                      '    \\caption{Caption}\n'
                      '    \\label{tab:my_label}\n'
                      '\\end{table}\n')


# __________________________________________________________
def run(rdf_module, args) -> None:
    '''
    Let's start.
    '''
    # Load process dictionary
    proc_dict_location: str = get_attribute(rdf_module, "procDict", '')
    if not proc_dict_location:
        LOGGER.error(
            'Location of the process dictionary not provided!\nAborting...')
        sys.exit(3)

    process_dict: dict[str, any] = get_process_dict(proc_dict_location)

    # Add processes into the dictionary
    process_dict_additions = get_attribute(rdf_module, "procDictAdd", {})
    if process_dict_additions:
        info_msg = 'Adding the following processes to the process dictionary:'
        for process_name, process_info in process_dict_additions.items():
            info_msg += f'\n  - {process_name}'
            if process_name in process_dict:
                LOGGER.debug('Process "%s" already in the dictionary.\n'
                             'Will be overwritten...', process_name)
            process_dict[process_name] = process_info
        LOGGER.info(info_msg)

    # Set multi-threading
    ncpus = get_attribute(rdf_module, "nCPUS", 4)
    if ncpus < 0:  # use all available threads
        ROOT.EnableImplicitMT()
        ncpus = ROOT.GetThreadPoolSize()
    if ncpus != 1:
        ROOT.ROOT.EnableImplicitMT(ncpus)
        ROOT.EnableThreadSafety()

    nevents_real = 0
    start_time = time.time()

    process_events = {}
    events_ttree = {}
    file_list = {}
    results = {}

    # Check if using weighted events is requested
    do_weighted = get_attribute(rdf_module, 'do_weighted', False)

    if do_weighted:
        LOGGER.info('Using generator weights')
        sow_process = process_events.copy()
        sow_ttree = events_ttree.copy()

    # Checking input directory
    input_dir = get_attribute(rdf_module, 'inputDir', '')
    if not input_dir:
        LOGGER.error('The "inputDir" variable is mandatory for the final '
                     'stage of the analysis!\nAborting...')
        sys.exit(3)
    if not os.path.isdir(input_dir):
        LOGGER.error('The specified input directory does not exist!\n'
                     'Aborting...')
        LOGGER.error('Input directory: %s', input_dir)
        sys.exit(3)

    if input_dir[-1] != "/":
        input_dir += "/"

    # Checking output directory
    output_dir = get_attribute(rdf_module, 'outputDir', '.')

    if output_dir[-1] != "/":
        output_dir += "/"

    if not os.path.exists(output_dir):
        LOGGER.debug('Creating output directory:\n  %s', output_dir)
        os.system(f'mkdir -p {output_dir}')

    # Cuts
    cuts: dict[str, str] = get_attribute(rdf_module, "cutList", {})

    # Find processes (samples) to run over
    process_list: list[str] = get_processes(rdf_module)

    # Find number of events per process
    for process_name in process_list:
        process_events[process_name] = 0
        events_ttree[process_name] = 0
        if do_weighted:
            sow_process[process_name] = 0.
            sow_ttree[process_name] = 0.

        file_list[process_name] = ROOT.vector('string')()

        flist = find_sample_files(input_dir, process_name)
        for filepath in flist:
            # TODO: check in `get_entries()` if file is valid and remove it
            #       from the input list if it is not
            if do_weighted:
                chunk_process_events, chunk_events_ttree, \
                    chunk_sow_process, chunk_sow_ttree = \
                    get_entries_sow(filepath, weight_name="weight")
                sow_process[process_name] += chunk_sow_process
                sow_ttree[process_name] += chunk_sow_ttree
            else:
                chunk_process_events, chunk_events_ttree = \
                    get_entries(filepath)
            process_events[process_name] += chunk_process_events
            events_ttree[process_name] += chunk_events_ttree
            file_list[process_name].push_back(filepath)
        if len(file_list[process_name]) < 1:
            LOGGER.error('No valid input files for sample "%s" '
                         'found!\nAborting..', process_name)
            sys.exit(3)
        if len(file_list[process_name]) == 1:
            LOGGER.info('Loading events for sample "%s" from file:\n  - %s',
                        process_name, file_list[process_name][0])
        else:
            info_msg = f'Loading events for sample "{process_name}"'
            info_msg += ' from files:'
            for filepath in file_list[process_name]:
                info_msg += f'\n  - {filepath}'
            LOGGER.info(info_msg)

    info_msg = 'Processed events:'
    for process_name, n_events in process_events.items():
        info_msg += f'\n\t- {process_name}: {n_events:,}'
    LOGGER.info(info_msg)
    info_msg = 'Events in the TTree:'
    for process_name, n_events in events_ttree.items():
        info_msg += f'\n\t- {process_name}: {n_events:,}'
    LOGGER.info(info_msg)

    if do_weighted:
        info_msg = 'Processed sum of weights:'
        for process_name, sow in sow_process.items():
            info_msg += f'\n\t- {process_name}: {sow:,}'
        LOGGER.info(info_msg)
        info_msg = 'Sum of weights in the TTree:'
        for process_name, sow in sow_ttree.items():
            info_msg += f'\n\t- {process_name}: {sow:,}'
        LOGGER.info(info_msg)


    # Check if there are any histograms defined
    histo_list: dict[str, dict[str, any]] = get_attribute(rdf_module,
                                                          "histoList", {})
    if not histo_list:
        LOGGER.error('No histograms defined!\nAborting...')
        sys.exit(3)

    # Check whether to scale the results to the luminosity
    do_scale = get_attribute(rdf_module, "doScale", True)
    if do_scale:
        int_lumi = get_attribute(rdf_module, "intLumi", 1.)
        if int_lumi < 0.:
            LOGGER.error('Integrated luminosity value not valid!\nAborting...')
            sys.exit(3)

    # Check whether to save resulting TTree(s) into a file(s)
    do_tree = get_element(rdf_module, "doTree", True)

    # Main loop
    for process_name in process_list:
        LOGGER.info('Running over process: %s', process_name)

        if process_events[process_name] <= 0:
            LOGGER.error('Can\'t scale histograms, the number of processed '
                         'events for the process "%s" seems to be zero!',
                         process_name)
            sys.exit(3)

        dframe = ROOT.ROOT.RDataFrame("events", file_list[process_name])
        define_list = get_element(rdf_module, "defineList", True)
        if len(define_list) > 0:
            LOGGER.info('Registering extra DataFrame defines...')
            for define in define_list:
                dframe = dframe.Define(define, define_list[define])

        fout_list = []
        histos_list = []
        snapshots = []
        count_list = []
        cuts_list = []
        cuts_list.append(process_name)
        eff_list = []
        eff_list.append(process_name)
        results[process_name] = {}

        if do_scale:
            # Get process information from process directory
            try:
                xsec = process_dict[process_name]["crossSection"]
            except KeyError:
                xsec = 1.0
                LOGGER.warning('Cross-section value not found for process '
                               '"%s"!\nUsing 1.0...', process_name)

            try:
                kfactor = process_dict[process_name]["kfactor"]
            except KeyError:
                kfactor = 1.0
                LOGGER.warning('Kfactor value not found for process "%s"!\n'
                               'Using 1.0...', process_name)

            try:
                matching_efficiency = \
                    process_dict[process_name]["matchingEfficiency"]
            except KeyError:
                matching_efficiency = 1.0
                LOGGER.warning('Matching efficiency value not found for '
                               'process "%s"!\nUsing 1.0...', process_name)

            gen_sf = xsec * kfactor * matching_efficiency
            lpn = len(process_name) + 8
            LOGGER.info('Generator scale factor for "%s": %.4g',
                        process_name, gen_sf)
            LOGGER.info(' - cross-section:      ' + lpn*' ' + '%.4g pb',
                        xsec)
            LOGGER.info(' - kfactor:            ' + lpn*' ' + '%.4g', kfactor)
            LOGGER.info(' - matching efficiency:' + lpn*' ' + '%.4g',
                        matching_efficiency)
            LOGGER.info('Integrated luminosity: %.4g pb-1', int_lumi)

        # Define all histos, snapshots, etc...
        LOGGER.info('Defining cuts and histograms')
        for cut_name, cut_definition in cuts.items():
            try:
                dframe_cut = dframe.Filter(cut_definition)
            except cppyy.gbl.std.runtime_error:
                LOGGER.error('During defining of the cuts an error '
                             'occurred!\nAborting...')
                sys.exit(3)

            count_list.append(dframe_cut.Count())

            histos = []
            for hist_name, hist_definition in histo_list.items():
                # default 1D histogram, looks for the name of the column.
                if "name" in hist_definition:
                    model = ROOT.RDF.TH1DModel(
                        hist_name,
                        f';{hist_definition["title"]};',
                        hist_definition["bin"],
                        hist_definition["xmin"],
                        hist_definition["xmax"])
                    histos.append(dframe_cut.Histo1D(model,
                                                     hist_definition["name"]))
                # multi dim histogram (1, 2 or 3D)
                elif "cols" in hist_definition:
                    cols = hist_definition['cols']
                    bins = hist_definition['bins']
                    if len(bins) != len(cols):
                        LOGGER.error('Amount of columns should be equal to '
                                     'the amount of bin configs!\nAborting...')
                        sys.exit(3)
                    bins_unpacked = tuple(i for sub in bins for i in sub)
                    if len(cols) == 1:
                        histos.append(dframe_cut.Histo1D(
                            (hist_name, '', *bins_unpacked), *cols))
                    elif len(cols) == 2:
                        histos.append(dframe_cut.Histo2D(
                            (hist_name, "", *bins_unpacked), *cols))
                    elif len(cols) == 3:
                        histos.append(dframe_cut.Histo3D(
                            (hist_name, "", *bins_unpacked), *cols))
                    else:
                        LOGGER.error('Only 1, 2 or 3D histograms supported.')
                        sys.exit(3)
                else:
                    LOGGER.error('Error parsing the histogram config. Provide '
                                 'either name or cols.')
                    sys.exit(3)
            histos_list.append(histos)

            if do_tree:
                # output file for the TTree
                fout = os.path.join(output_dir,
                                    process_name + '_' + cut_name + '.root')
                fout_list.append(fout)

                opts = ROOT.RDF.RSnapshotOptions()
                opts.fLazy = True
                # Snapshots need to be kept in memory until the event loop is
                # run
                snapshots.append(dframe_cut.Snapshot("events", fout, "", opts))

        # Now perform the loop and evaluate everything at once.
        LOGGER.info('Evaluating...')
        all_events_raw = dframe.Count().GetValue()
        all_events_weighted = all_events_raw

        if do_weighted:
            # check that the weight column exists, it should always be called "weight" for now
            try:
                all_events_weighted = dframe.Sum("weight").GetValue()
                LOGGER.info(f'Successfully applied event weights, got weighted events = {all_events_weighted:0,.2f}')
            except cppyy.gbl.std.runtime_error:
                LOGGER.error('Error: Event weights requested with do_weighted, '
                                'but input file does not contain weight column. Aborting.')
                sys.exit(3)

        LOGGER.info('Done')

        nevents_real += all_events_raw
        uncertainty = ROOT.Math.sqrt(all_events_raw)

        if do_scale:
            LOGGER.info('Scaling cut yields...')
            if do_weighted:
                    all_events = all_events_weighted * 1. * gen_sf * \
                        int_lumi / sow_process[process_name]
                    uncertainty = ROOT.Math.sqrt(all_events_weighted) * gen_sf * \
                        int_lumi / sow_process[process_name]
            else:
                all_events = all_events_raw * 1. * gen_sf * \
                    int_lumi / process_events[process_name]
                uncertainty = ROOT.Math.sqrt(all_events_raw) * gen_sf * \
                    int_lumi / process_events[process_name]
        else:
            all_events = all_events_raw
            uncertainty = ROOT.Math.sqrt(all_events_raw)

        results[process_name]['all_events'] = {}
        results[process_name]['all_events']['n_events_raw'] = all_events_raw
        results[process_name]['all_events']['n_events'] = all_events
        results[process_name]['all_events']['uncertainty'] = uncertainty

        for i, cut in enumerate(cuts):
            cut_result = {}
            cut_result['n_events_raw'] = count_list[i].GetValue()
            if do_scale:
                cut_result['n_events'] = \
                    cut_result['n_events_raw'] * 1. * gen_sf * \
                    int_lumi / process_events[process_name]
                cut_result['uncertainty'] = \
                    math.sqrt(cut_result['n_events_raw']) * gen_sf * \
                    int_lumi / process_events[process_name]
            else:
                cut_result['n_events'] = cut_result['n_events_raw']
                cut_result['uncertainty'] = \
                    math.sqrt(cut_result['n_events_raw'])
            results[process_name][cut] = cut_result

        # Cut name width
        cn_width = max(len(cn) for cn in results[process_name].keys())
        info_msg = 'Cutflow:\n'
        info_msg += '    ' + cn_width * ' ' + '        Raw events'
        if do_scale:
            info_msg += '    Scaled events'
        for cut_name, cut_result in results[process_name].items():
            if cut_name == 'all_events':
                cut_name = 'All events'
            info_msg += f'\n  - {cut_name:{cn_width}} '
            info_msg += f' {cut_result["n_events_raw"]:>16,}'
            if do_scale:
                if cut_result['n_events_raw'] != 0:
                    info_msg += f' {cut_result["n_events"]:>16.2e}'
                else:
                    info_msg += f' {"0.":>16}'

        LOGGER.info(info_msg)

        if args.graph:
            generate_graph(dframe, args)
            args.graph = False

        # And save everything
        LOGGER.info('Saving the outputs...')
        if do_scale:
            LOGGER.info('Scaling the histograms...')
        for i, cut in enumerate(cuts):
            # output file for histograms
            fhisto = os.path.join(output_dir,
                                  process_name + '_' + cut + '_histo.root')
            with ROOT.TFile(fhisto, 'RECREATE') as outfile:
                for hist in histos_list[i]:
                    hist_name = hist.GetName() + '_raw'
                    outfile.WriteObject(hist.GetValue(), hist_name)
                    if do_scale:
                        if do_weighted:
                            hist.Scale(gen_sf * int_lumi /
                                       sow_process[process_name])         
                        else:
                            hist.Scale(gen_sf * int_lumi /
                                       process_events[process_name])
                        outfile.WriteObject(hist.GetValue())

                # write all metadata info to the output file
                param = ROOT.TParameter(int)("eventsProcessed",
                                             process_events[process_name])
                outfile.WriteObject(param)

                if do_weighted:
                    param = ROOT.TParameter(float)("sumOfWeights",
                                                   sow_process[process_name])
                    outfile.WriteObject(param)

                else:
                    param = ROOT.TParameter(float)("sumOfWeights",
                                                   process_events[process_name])
                    outfile.WriteObject(param) 

                param = ROOT.TParameter(bool)("scaled",
                                              do_scale)
                outfile.WriteObject(param)

                if do_scale:
                    param = ROOT.TParameter(float)("intLumi", int_lumi)
                    outfile.WriteObject(param)

                    param = ROOT.TParameter(float)("crossSection", xsec)
                    outfile.WriteObject(param)

                    param = ROOT.TParameter(float)("kfactor", kfactor)
                    outfile.WriteObject(param)

                    param = ROOT.TParameter(float)("matchingEfficiency",
                                                   matching_efficiency)
                    outfile.WriteObject(param)

                    param = ROOT.TParameter(float)("generatorScaleFactor",
                                                   gen_sf)
                    outfile.WriteObject(param)
            if do_tree:
                # Number of events from a particular cut
                nevt_cut = results[process_name][cut]['n_events_raw']
                # Number of events in file
                try:
                    nevt_infile = snapshots[i].Count().GetValue()
                except cppyy.gbl.std.runtime_error:
                    nevt_infile = 0

                if nevt_cut != nevt_infile:
                    LOGGER.error('Number of events for cut "%s" in sample '
                                 '"%s" does not match with number of saved '
                                 'events!', cut, process_name)
                    sys.exit(3)

                #store also the TParameters for total number of events and sum of weights to the trees
                print("Updating file", fout_list[i])
                outfile = ROOT.TFile(fout_list[i], 'update')
                param = ROOT.TParameter(int)('eventsProcessed', process_events[process_name])
                print("Number of events processed:", process_events[process_name])
                param.Write()
                if do_weighted:
                    param2 = ROOT.TParameter(float)('SumOfWeights', sow_process[process_name])
                    print("Sum of weights:", sow_process[process_name])
                    param2.Write()
                outfile.Write()
                outfile.Close()




    # Save results either to JSON or LaTeX tables
    save_results(results, rdf_module)

    elapsed_time = time.time() - start_time

    info_msg = f"\n{' SUMMARY ':=^80}\n"
    info_msg += 'Elapsed time (H:M:S):    '
    info_msg += time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    info_msg += '\nEvents processed/second: '
    info_msg += f'{int(nevents_real/elapsed_time):,}'
    info_msg += f'\nTotal events processed:  {nevents_real:,}'
    info_msg += '\n'
    info_msg += 80 * '='
    info_msg += '\n'
    LOGGER.info(info_msg)


def run_final(parser):
    '''
    Run final stage of the analysis.
    '''

    args, _ = parser.parse_known_args()

    if args.command != 'final':
        LOGGER.error('Unknown sub-command "%s"!\nAborting...', args.command)
        sys.exit(3)

    # Check that the analysis file exists
    anapath = args.anascript_path
    if not os.path.isfile(anapath):
        LOGGER.error('Analysis script "%s" not found!\nAborting...',
                     anapath)
        sys.exit(3)

    # Load pre compiled analyzers
    LOGGER.info('Loading analyzers from libFCCAnalyses...')
    ROOT.gSystem.Load("libFCCAnalyses")
    # Is this still needed?? 01/04/2022 still to be the case
    _fcc = ROOT.dummyLoader
    LOGGER.debug(_fcc)

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
    anapath_abs = os.path.abspath(anapath)
    LOGGER.info('Loading analysis script:\n%s', anapath_abs)
    rdf_spec = importlib.util.spec_from_file_location('rdfanalysis',
                                                      anapath_abs)
    rdf_module = importlib.util.module_from_spec(rdf_spec)
    rdf_spec.loader.exec_module(rdf_module)

    # Merge configuration from analysis script file with command line arguments
    if get_element(rdf_module, 'graph'):
        args.graph = True

    if get_element(rdf_module, 'graphPath') != '':
        args.graph_path = get_element(rdf_module, 'graphPath')

    run(rdf_module, args)
