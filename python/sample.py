'''
Handle process related information
'''

import os
import sys
import json
import glob
import logging
from typing import Optional, Union
import urllib.request
import yaml  # type: ignore
import ROOT  # type: ignore
import cppyy
import numpy as np
from threading import Thread
from queue import Queue


ROOT.gROOT.SetBatch(True)

LOGGER: logging.Logger = logging.getLogger('FCCAnalyses.process_info')


# _____________________________________________________________________________
def get_entries(inpath: str) -> Optional[int]:
    '''
    Retrieves number of entries in the "events" TTree from the provided ROOT
    file.
    '''
    nevents = None
    with ROOT.TFile(inpath, 'READ') as infile:
        try:
            nevents = infile.Get("events").GetEntries()
        except AttributeError:
            LOGGER.error('Input file is missing "events" TTree!\n  - %s'
                         '\nAborting...', inpath)
            sys.exit(3)

    return nevents


# _____________________________________________________________________________
def get_entries_sow(infilepath: str,
                    nevents_max: Optional[int] = None,
                    get_local: bool = True,
                    weight_name: str = "EventHeader.weight") -> tuple[int, int, float, float]:
    '''
    Get number of original entries and number of actual entries in the file, as
    well as the sum of weights.
    '''

    infile = ROOT.TFile.Open(infilepath)
    infile.cd()

    processEvents = 0
    processSumOfWeights = 0.
    try:
        processEvents = infile.Get('eventsProcessed').GetVal()
    except AttributeError:
        print('----> Warning: Input file is missing information about ' # should these warnings be kept? 
              'original number of events!')
    try:
        processSumOfWeights = infile.Get('SumOfWeights').GetVal()
    except AttributeError:
        print('----> Warning: Input file is missing information about '
              'original sum of weights!')

    if not get_local:
        return processEvents, None, processSumOfWeights, None

    eventsTTree = 0
    sumOfWeightsTTree = 0.

     # check for empty chunk (can this be improved? exception from RDF cannot be caught it seems?)
    tree = infile.Get("events")
    if not tree:
        print("Tree not found in file", infilepath, " possibly empty chunk - continuing with next one.")
        infile.Close()
        return processEvents, eventsTTree, processSumOfWeights, sumOfWeightsTTree

    try:

         # use a RDF here too so the nevents restriction option can be imposed easily for the local events
        rdf_tmp = ROOT.ROOT.RDataFrame("events", infilepath)

        if nevents_max:
            rdf_tmp = rdf_tmp.Range(0, nevents_max)

        eventsTTree = rdf_tmp.Count().GetValue()

        # eventsTTree = infile.Get("events").GetEntries()
        ROOT.gROOT.SetBatch(True)
        try:
            # infile.Get("events").Draw('EventHeader.weight[0]>>histo')
            # histo=ROOT.gDirectory.Get('histo')
            histo = rdf_tmp.Histo1D(weight_name)
            sumOfWeightsTTree = float(eventsTTree) * histo.GetMean()
        except cppyy.gbl.std.runtime_error:
                LOGGER.error('Error: Event weights requested with do_weighted,'
                            'but input file does not contain weight column. Aborting.')
                sys.exit(3)
    except AttributeError:
        print('----> Error: Input file is missing events TTree! Probably empty chunk.')
        infile.Close()

    infile.Close()

    return processEvents, eventsTTree, processSumOfWeights, sumOfWeightsTTree


# _____________________________________________________________________________
def get_process_info(
        process_name: str,
        prod_tag: str,
        input_dir: str,
        process_input_dir: str | None = None) -> tuple[list[str], list[int]]:
    '''
    Decide where to look for the filelist and eventlist.
    '''

    if process_input_dir is not None:
        return get_process_info_files(process_name, process_input_dir)

    if prod_tag is None and input_dir is None:
        LOGGER.error('The variable <prodTag> or <inputDir> is mandatory in '
                     'your analysis script!\nAborting...')
        sys.exit(3)
    elif prod_tag is not None and input_dir is not None:
        LOGGER.error('The variables <prodTag> and <inputDir> can\'t be set '
                     'both at the same time in your analysis script!\n'
                     'Aborting...')
        sys.exit(3)

    if prod_tag is not None:
        return get_process_info_yaml(process_name, prod_tag)

    return get_process_info_files(process_name, input_dir)


# _____________________________________________________________________________
def get_process_info_files(process: str, input_dir: str) -> tuple[list[str],
                                                                  list[int]]:
    '''
    Get list of files and events from the specified location
    '''
    filelist = []
    eventlist = []
    filetest = f'{input_dir}/{process}.root'
    dirtest = f'{input_dir}/{process}'

    if os.path.isfile(filetest) and os.path.isdir(dirtest):
        LOGGER.error('For process "%s" both a file %s and a directory %s '
                     'exist!\nExactly one should be used, please '
                     'check.\nAborting...', process, filetest, dirtest)
        sys.exit(3)

    if not os.path.isfile(filetest) and not os.path.isdir(dirtest):
        LOGGER.error('For process "%s" neither a file %s nor a directory %s '
                     'exist!\nExactly one should be used, please check.\n'
                     'Aborting...', process, filetest, dirtest)
        sys.exit(3)

    if os.path.isfile(filetest):
        filelist.append(filetest)
        eventlist.append(get_entries(filetest))

    if os.path.isdir(dirtest):
        flist = glob.glob(dirtest+"/*.root")
        for f in flist:
            filelist.append(f)
            eventlist.append(get_entries(f))

    return filelist, eventlist


def get_process_info_yaml(process_name: str,
                          prod_tag: str) -> tuple[list[str],
                                                  list[int]]:
    '''
    Get list of files and events from the YAML file
    '''
    doc = None
    proc_dict_dirs = get_process_dict_dirs()
    yamlfilepath = None
    for path in proc_dict_dirs:
        yamlfilepath = os.path.join(path, 'yaml', prod_tag, process_name,
                                    'merge.yaml')
        if not os.path.isfile(yamlfilepath):
            continue
    if not os.path.isfile(yamlfilepath):
        LOGGER.error('Can\'t find the YAML file with process info for process '
                     '"%s"!\nAborting...', process_name)
        sys.exit(3)

    with open(yamlfilepath, 'r', encoding='utf-8') as ftmp:
        try:
            doc = yaml.load(ftmp, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            LOGGER.error(exc)
            sys.exit(3)
        except IOError as exc:
            LOGGER.error('I/O error(%i): %s\nYAML file: %s',
                         exc.errno, exc.strerror, yamlfilepath)
            sys.exit(3)
        finally:
            LOGGER.debug('YAML file with process information successfully '
                         'loaded:\n%s', yamlfilepath)

    filelist = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
    eventlist = [f[1] for f in doc['merge']['outfiles']]

    return filelist, eventlist


# _____________________________________________________________________________
def get_process_dict(proc_dict_location: str) -> dict:
    '''
    Pick up the dictionary with process information
    '''
    if 'http://' in proc_dict_location or 'https://' in proc_dict_location:
        LOGGER.info('Getting process dictionary from the web:\n%s',
                    proc_dict_location)
        with urllib.request.urlopen(proc_dict_location).read() as response:
            try:
                proc_dict = json.loads(response.read())
            except json.decoder.JSONDecodeError:
                LOGGER.error('Failed to parse process dictionary correctly!\n'
                             'Aborting...')
                sys.exit(3)

    else:
        proc_dict_dirs = get_process_dict_dirs()
        # Add empty directory to handle local files or files with absolute path
        proc_dict_dirs = [''] + proc_dict_dirs
        proc_dict = None
        for path in proc_dict_dirs:
            proc_dict_path = os.path.join(path, proc_dict_location)
            if not os.path.isfile(proc_dict_path):
                continue

            LOGGER.info('Loading process dictionary from:\n%s', proc_dict_path)

            with open(proc_dict_path, 'r', encoding='utf-8') as infile:
                try:
                    proc_dict = json.load(infile)
                except json.decoder.JSONDecodeError:
                    LOGGER.error('Failed to parse process dictionary '
                                 'correctly!\nAborting...')
                    sys.exit(3)

            if proc_dict:
                break

        if not proc_dict:
            LOGGER.error('Process dictionary not found!\nAborting...')
            sys.exit(3)

    return proc_dict


# _____________________________________________________________________________
def get_process_dict_dirs() -> list[str]:
    '''
    Get search directories for the process dictionaries
    '''
    dirs_var = os.getenv('FCCDICTSDIR')
    if dirs_var is None:
        LOGGER.error('Environment variable FCCDICTSDIR not defined!\n'
                     'Was the setup.sh file sourced properly?\n'
                     'Aborting...')
        sys.exit(3)
    dirs = dirs_var.split(':')
    dirs[:] = [d for d in dirs if d]

    return dirs


# _____________________________________________________________________________
def get_file_list(file_list_path: str) -> list[str]:
    '''
    Loads file list from the provided file.
    '''
    if not os.path.isfile(file_list_path):
        LOGGER.error('Provided file containing list of ROOT files could not '
                     'be found!\nAborting...')
        sys.exit(3)

    with open(file_list_path, 'r', encoding='utf-8') as lstfile:
        file_list = [line.strip() for line in lstfile]

    # remove empty lines
    file_list = [line for line in file_list if line]

    # remove commented out lines
    file_list = [line for line in file_list if line[0] != '#']

    if not file_list:
        LOGGER.error('Provided file containing list of ROOT files is empty or '
                     'does not contain valid lines!\nAborting...')
        sys.exit(3)

    return file_list


# _____________________________________________________________________________
def get_files_in_dir(dir_path: str) -> Optional[list[str]]:
    '''
    Finds ROOT files in the provided directory.
    '''

    if not os.path.isdir(dir_path):
        LOGGER.error('Can\'t access the sample directory!\n - %s\nAborting...',
                     dir_path)
        sys.exit(3)

    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if
             os.path.isfile(os.path.join(dir_path, f)) and
             f.endswith('.root')]

    if not files:
        return None

    return files


# _____________________________________________________________________________
def get_files_in_yaml(sample_name: str,
                      campaign: str) -> Optional[list[str]]:
    '''
    Get list of files of a sample from the YAML file.
    '''
    file_counts = get_file_counts_yaml(sample_name, campaign)

    filelist = [fc['path'] for fc in file_counts]

    return filelist, file_counts


# _____________________________________________________________________________
def get_file_counts_yaml(
        sample_name: str,
        campaign: str) -> \
            Optional[list[dict[str, Union[str, int, Optional[float]]]]]:
    '''
    Get list of files of a sample from the YAML file
    campaign_name: "<accelerator>/<season-and-year>/<detector>"
    sample_name: "<generator>_<process>_<energy>"
    '''
    doc = None
    proc_dict_dirs = get_process_dict_dirs()

    # Select first valid YAML file found
    yamlfilepath = None
    for path in proc_dict_dirs:
        yamlfilepath = os.path.join(path, 'yaml', campaign, sample_name,
                                    'merge.yaml')
        if not os.path.isfile(yamlfilepath):
            continue
    if not os.path.isfile(yamlfilepath):
        LOGGER.error('Can\'t find the YAML file with information for sample '
                     '"%s"!\nSample will be ignored...', sample_name)
        return None

    with open(yamlfilepath, 'r', encoding='utf-8') as ftmp:
        try:
            doc = yaml.load(ftmp, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            LOGGER.error(exc)
            return None
        except IOError as exc:
            LOGGER.error('I/O error(%i): %s\nYAML file: %s',
                         exc.errno, exc.strerror, yamlfilepath)
            return None
        finally:
            LOGGER.debug('YAML file with process information successfully '
                         'loaded:\n%s', yamlfilepath)

    file_counts: list[dict[str, Union[str, int, Optional[float]]]] = []
    for file_info in doc['merge']['outfiles']:
        file_count = {}
        file_count['path'] = doc['merge']['outdir'] + file_info[0]
        file_count['n-events'] = file_info[1]
        file_count['sum-of-weights'] = None

        file_counts.append(file_count)

    if not file_counts:
        return None

    return file_counts


# _____________________________________________________________________________
def get_one_file_quantities(infilepath: str,
                            results: Queue) -> None:
    '''
    Get number of original entries and sum of weights together with number of
    current entries in the "events" TTree.
    '''

    result: dict[str, Union[None, str, int, float]] = {}
    result['path'] = infilepath
    result['events-processed'] = None
    result['sow-processed'] = None
    result['events-in-ttree'] = None

    error_ignore_level = ROOT.gErrorIgnoreLevel
    try:
        # Suppress Info and Warning messages, only show Error and Fatal
        ROOT.gErrorIgnoreLevel = ROOT.kError

        # ROOT 6.38 does not support "in" for dictionary style of access
        with ROOT.TFile.Open(infilepath) as infile:
            try:
                result['events-processed'] = infile['eventsProcessed'].GetVal()
            except KeyError:
                pass

            try:
                result['sow-processed'] = infile['SumOfWeights'].GetVal()
            except KeyError:
                pass

            try:
                fccana_dir = infile['fccana']
                if 'n-events-original' in fccana_dir:
                    result['events-processed'] = \
                        fccana_dir['n-events-original']
                if 'sow-original' in fccana_dir:
                    result['sow-processed'] = fccana_dir['sow-original']
            except KeyError:
                pass

            try:
                result['events-in-ttree'] = infile['events'].GetEntries()
            except KeyError:
                pass

            # TODO: Pick up also sum of weights somehow (avoid running over all
            #       events)

        ROOT.gErrorIgnoreLevel = error_ignore_level

        results.put(result)
    except OSError:
        ROOT.gErrorIgnoreLevel = error_ignore_level

        results.put(result)


# _____________________________________________________________________________
def get_file_quantities(file_list: list[str]) -> \
        list[dict[str, Union[None, str, int, float]]]:
    '''
    Get event counts and sum of weights for each file in the file list.
    '''

    threads = []
    results: Queue = Queue()
    for filepath in file_list:
        filepath = apply_filepath_rewrites(filepath)

        thread = Thread(target=get_one_file_quantities,
                        args=(filepath, results))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return [result for result in results.queue
            if result['events-in-ttree'] is not None]


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
    info_msg += 'total events:\n'
    info_msg += f' - total number of events: {nevts_total:,}\n'
    info_msg += f' - targeted number of events: {nevts_target:,}\n'
    info_msg += ' - number of events in the resulting file list: ' \
                f'{nevts_real:,}\n'
    info_msg += ' - number of files after reduction: '
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
