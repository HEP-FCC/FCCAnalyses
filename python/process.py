'''
Handle process related information
'''

import os
import sys
import json
import glob
import logging
import urllib.request
import yaml  # type: ignore
import ROOT  # type: ignore

ROOT.gROOT.SetBatch(True)

LOGGER: logging.Logger = logging.getLogger('FCCAnalyses.process_info')


def get_entries(inpath: str) -> int:
    '''
    Get number of entries in the TTree named "events".
    '''
    nevents = None
    with ROOT.TFile(inpath, 'READ') as infile:
        tt = infile.Get("events")
        nevents = tt.GetEntries()
    return nevents


def get_process_info(process: str,
                     prod_tag: str,
                     input_dir: str) -> tuple[list[str], list[int]]:
    '''
    Decide where to look for the filelist and eventlist.
    '''
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
        return get_process_info_yaml(process, prod_tag)

    return get_process_info_files(process, input_dir)


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
