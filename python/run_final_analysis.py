'''
Run final stage of an analysis
'''

import os
import sys
import time
import glob
import logging
import importlib.util

import ROOT
from anafile import getElement, getElementDict
from process import get_process_dict

LOGGER = logging.getLogger('FCCAnalyses.run_final')

ROOT.gROOT.SetBatch(True)


# _____________________________________________________________________________
def get_entries(infilepath):
    '''
    Get number of original entries and number of actual entries in the file
    '''
    infile = ROOT.TFile.Open(infilepath)
    infile.cd()

    events_processed = 0
    try:
        events_processed = infile.Get('eventsProcessed').GetVal()
    except AttributeError:
        LOGGER.warning('Input file is missing information about '
                       'original number of events!')

    events_in_ttree = 0
    try:
        events_in_ttree = infile.Get("events").GetEntries()
    except AttributeError:
        LOGGER.error('Input file is missing "events" TTree!\nAborting...')
        infile.Close()
        sys.exit(3)

    infile.Close()

    return events_processed, events_in_ttree


# _____________________________________________________________________________
def testfile(f):
    '''
    Test input file from previous stages
    '''
    tf = ROOT.TFile.Open(f)
    tt = None
    try:
        tt = tf.Get("events")
        if tt is None:
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
def runFinal(rdf_module):
    proc_dict_location = getElement(rdf_module, "procDict", True)
    if not proc_dict_location:
        LOGGER.error(
            'Location of the process dictionary not provided!\nAborting...')
        sys.exit(3)

    process_dict = get_process_dict(proc_dict_location)

    process_dict_additions = getElement(rdf_module, "procDictAdd", True)
    for addition in process_dict_additions:
        if getElementDict(process_dict, addition) is None:
            process_dict[addition] = process_dict_additions[addition]
        else:
            LOGGER.debug('Process already in the dictionary. Skipping it...')

    ROOT.ROOT.EnableImplicitMT(getElement(rdf_module, "nCPUS", True))

    nevents_real = 0
    start_time = time.time()

    processEvents = {}
    eventsTTree = {}
    file_list = {}
    saveTab = []
    efficiencyList = []

    inputDir = getElement(rdf_module, "inputDir", True)
    if not inputDir:
        LOGGER.error('The inputDir variable is mandatory for the final stage '
                     'of the analysis!\nAborting...')
        sys.exit(3)

    if inputDir[-1] != "/":
        inputDir += "/"

    outputDir = getElement(rdf_module, "outputDir", True)
    if outputDir != "":
        if outputDir[-1] != "/":
            outputDir += "/"

    if not os.path.exists(outputDir) and outputDir != '':
        os.system("mkdir -p {}".format(outputDir))

    cut_list = getElement(rdf_module, "cutList", True)
    length_cuts_names = max([len(cut) for cut in cut_list])
    cutLabels = getElement(rdf_module, "cutLabels", True)

    # save a table in a separate tex file
    save_tabular = getElement(rdf_module, "saveTabular", True)
    if save_tabular:
        # option to rewrite the cuts in a better way for the table. otherwise,
        # take them from the cutList
        if cutLabels:
            cut_names = list(cutLabels.values())
        else:
            cut_names = list(cut_list)

        cut_names.insert(0, ' ')
        saveTab.append(cut_names)
        efficiencyList.append(cut_names)

    process_list = getElement(rdf_module, "processList", True)
    for process_name in process_list:
        processEvents[process_name] = 0
        eventsTTree[process_name] = 0
        file_list[process_name] = ROOT.vector('string')()

        infilepath = inputDir + process_name + '.root'  # input file
        if not os.path.isfile(infilepath):
            LOGGER.debug('File %s does not exist!\nTrying if it is a '
                         'directory as it might have been processed in batch.',
                         infilepath)
        else:
            LOGGER.info('Open file:\n\t%s', infilepath)
            processEvents[process_name], eventsTTree[process_name] = \
                get_entries(infilepath)
            file_list[process_name].push_back(infilepath)

        indirpath = inputDir + process_name
        if os.path.isdir(indirpath):
            info_msg = f'Open directory {indirpath}'
            flist = glob.glob(indirpath + '/chunk*.root')
            for filepath in flist:
                info_msg += '\n\t' + filepath
                chunkProcessEvents, chunkEventsTTree = get_entries(filepath)
                processEvents[process_name] += chunkProcessEvents
                eventsTTree[process_name] += chunkEventsTTree
                file_list[process_name].push_back(filepath)
            LOGGER.info(info_msg)

    info_msg = 'Processed events:'
    for process_name, n_events in processEvents.items():
        info_msg += f'\n\t- {process_name}: {n_events:,}'
    LOGGER.info(info_msg)
    info_msg = 'Events in the TTree:'
    for process_name, n_events in eventsTTree.items():
        info_msg += f'\n\t- {process_name}: {n_events:,}'
    LOGGER.info(info_msg)

    histoList = getElement(rdf_module, "histoList", True)
    doScale = getElement(rdf_module, "doScale", True)
    intLumi = getElement(rdf_module, "intLumi", True)

    doTree = getElement(rdf_module, "doTree", True)
    for process_name in process_list:
        LOGGER.info('Running over process: %s', process_name)

        if processEvents[process_name] == 0:
            LOGGER.error('Can\'t scale histograms, the number of processed '
                         'events for the process "%s" seems to be zero!',
                         process_name)
            sys.exit(3)

        df = ROOT.ROOT.RDataFrame("events", file_list[process_name])
        defineList = getElement(rdf_module, "defineList", True)
        if len(defineList) > 0:
            LOGGER.info('Registering extra DataFrame defines...')
            for define in defineList:
                df = df.Define(define, defineList[define])

        fout_list = []
        histos_list = []
        tdf_list = []
        count_list = []
        cuts_list = []
        cuts_list.append(process_name)
        eff_list = []
        eff_list.append(process_name)

        # Define all histos, snapshots, etc...
        LOGGER.info('Defining snapshots and histograms')
        for cut in cut_list:
            # output file for tree
            fout = outputDir + process_name + '_' + cut + '.root'
            fout_list.append(fout)

            df_cut = df.Filter(cut_list[cut])
            count_list.append(df_cut.Count())

            histos = []

            for v in histoList:
                # default 1D histogram
                if "name" in histoList[v]:
                    model = ROOT.RDF.TH1DModel(
                        v,
                        f';{histoList[v]["title"]};',
                        histoList[v]["bin"],
                        histoList[v]["xmin"],
                        histoList[v]["xmax"])
                    histos.append(df_cut.Histo1D(model, histoList[v]["name"]))
                # multi dim histogram (1, 2 or 3D)
                elif "cols" in histoList[v]:
                    cols = histoList[v]['cols']
                    bins = histoList[v]['bins']
                    bins_unpacked = tuple([i for sub in bins for i in sub])
                    if len(bins) != len(cols):
                        LOGGER.error('Amount of columns should be equal to '
                                     'the amount of bin configs!\nAborting...')
                        sys.exit(3)
                    if len(cols) == 1:
                        histos.append(df_cut.Histo1D((v, "", *bins_unpacked),
                                                     cols[0]))
                    elif len(cols) == 2:
                        histos.append(df_cut.Histo2D((v, "", *bins_unpacked),
                                                     cols[0],
                                                     cols[1]))
                    elif len(cols) == 3:
                        histos.append(df_cut.Histo3D((v, "", *bins_unpacked),
                                                     cols[0],
                                                     cols[1],
                                                     cols[2]))
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
            all_events = all_events * 1. * \
                         process_dict[process_name]["crossSection"] * \
                         process_dict[process_name]["kfactor"] * \
                         process_dict[process_name]["matchingEfficiency"] * \
                         intLumi / processEvents[process_name]
            uncertainty = ROOT.Math.sqrt(all_events) * \
                process_dict[process_name]["crossSection"] * \
                process_dict[process_name]["kfactor"] * \
                process_dict[process_name]["matchingEfficiency"] * \
                intLumi / processEvents[process_name]
            LOGGER.info('Printing scaled number of events!!!')

        cfn_width = 16 + length_cuts_names  # Cutflow name width
        info_msg = 'Cutflow:'
        info_msg += f'\n\t{"All events":{cfn_width}} : {all_events:,}'

        if save_tabular:
            # scientific notation - recomended for backgrounds
            cuts_list.append(f'{all_events:.2e} $\\pm$ {uncertainty:.2e}')
            # float notation - recomended for signals with few events
            # cuts_list.append(f'{all_events:.3f} $\\pm$ {uncertainty:.3f}')
            # ####eff_list.append(1.)  # start with 100% efficiency

        for i, cut in enumerate(cut_list):
            neventsThisCut = count_list[i].GetValue()
            neventsThisCut_raw = neventsThisCut
            uncertainty = ROOT.Math.sqrt(neventsThisCut_raw)
            if doScale:
                neventsThisCut = \
                    neventsThisCut * 1. * \
                    process_dict[process_name]["crossSection"] * \
                    process_dict[process_name]["kfactor"] * \
                    process_dict[process_name]["matchingEfficiency"] * \
                    intLumi / processEvents[process_name]
                uncertainty = \
                    ROOT.Math.sqrt(neventsThisCut_raw) * \
                    process_dict[process_name]["crossSection"] * \
                    process_dict[process_name]["kfactor"] * \
                    process_dict[process_name]["matchingEfficiency"] * \
                    intLumi / processEvents[process_name]
            info_msg += f'\n\t{"After selection " + cut:{cfn_width}} : '
            info_msg += f'{neventsThisCut:,}'

            # Saving the number of events, uncertainty and efficiency for the
            # output-file
            if save_tabular and cut != 'selNone':
                if neventsThisCut != 0:
                    # scientific notation - recomended for backgrounds
                    cuts_list.append(
                        f'{neventsThisCut:.2e} $\\pm$ {uncertainty:.2e}')
                    # float notation - recomended for signals with few events
                    # cuts_list.append(
                    #     f'{neventsThisCut:.3f} $\\pm$ {uncertainty:.3f}')
                    eff_list.append(f'{1.*neventsThisCut/all_events:.3f}')
                # if number of events is zero, the previous uncertainty is
                # saved instead:
                elif '$\\pm$' in cuts_list[-1]:
                    cut = (cuts_list[-1]).split()
                    cuts_list.append(f'$\\leq$ {cut[2]}')
                    eff_list.append('0.')
                else:
                    cuts_list.append(cuts_list[-1])
                    eff_list.append('0.')

        LOGGER.info(info_msg)

        # And save everything
        LOGGER.info('Saving the outputs...')
        for i, cut in enumerate(cut_list):
            # output file for histograms
            fhisto = outputDir + process_name + '_' + cut + '_histo.root'
            tf = ROOT.TFile.Open(fhisto, 'RECREATE')
            for h in histos_list[i]:
                try:
                    h.Scale(1. * process_dict[process_name]["crossSection"] *
                            process_dict[process_name]["kfactor"] *
                            process_dict[process_name]["matchingEfficiency"] /
                            processEvents[process_name])
                except KeyError:
                    LOGGER.warning(
                        'No value defined for process %s in dictionary!',
                        process_name)
                    if h.Integral(0, -1) > 0:
                        h.Scale(1./h.Integral(0, -1))
                h.Write()
            tf.Close()

            if doTree:
                # test that the snapshot worked well
                validfile = testfile(fout_list[i])
                if not validfile:
                    continue

        if save_tabular and cut != 'selNone':
            saveTab.append(cuts_list)
            efficiencyList.append(eff_list)

    if save_tabular:
        tabular_path = outputDir + 'outputTabular.txt'
        LOGGER.info('Saving tabular to:\n%s', tabular_path)
        with open(tabular_path, 'w', encoding='utf-8') as outfile:
            # Printing the number of events in format of a LaTeX table
            outfile.write('\\begin{table}[H]\n'
                          '    \\centering\n'
                          '    \\resizebox{\\textwidth}{!}{\n'
                          '        \\begin{tabular}{|l||')
            outfile.write('c|' * (len(cuts_list)-1))
            outfile.write('} \\hline\n')
            for i, row in enumerate(saveTab):
                outfile.write('        ')
                outfile.write(' & '.join(row))
                outfile.write(' \\\\\n')
                if i == 0:
                    outfile.write('        \\hline\n')
            outfile.write('        \\hline \n'
                          '    \\end{tabular}} \n'
                          '    \\caption{Caption} \n'
                          '    \\label{tab:my_label} \n'
                          '\\end{table}\n')

            # Efficiency:
            outfile.write('\n\nEfficiency:\n')
            outfile.write('\\begin{table}[H] \n'
                          '    \\centering \n'
                          '    \\resizebox{\\textwidth}{!}{ \n'
                          '    \\begin{tabular}{|l||')
            outfile.write('c|' * (len(cuts_list)-1))
            outfile.write('} \\hline\n')
            print(eff_list)
            for i in range(len(eff_list)):
                outfile.write('        ')
                print('i:', i)
                print(efficiencyList)
                v = [row[i] for row in efficiencyList]
                outfile.write(' & '.join(str(v)))
                outfile.write(' \\\\\n')
                if i == 0:
                    outfile.write('        \\hline\n')
            outfile.write('        \\hline \n'
                          '    \\end{tabular}} \n'
                          '    \\caption{Caption} \n'
                          '    \\label{tab:my_label} \n'
                          '\\end{table}\n')

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


def run_final(parser):
    '''
    Run final stage of the analysis.
    '''

    args, _ = parser.parse_known_args()

    if args.command != 'final':
        LOGGER.error('Unknow sub-command "%s"!\nAborting...', args.command)
        sys.exit(3)

    # Check that the analysis file exists
    anapath = args.anafile_path
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

    runFinal(rdf_module)
