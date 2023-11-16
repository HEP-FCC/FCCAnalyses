'''
Handle process related information
'''

import os
import sys
import json
import glob
import logging
import yaml
import ROOT

ROOT.gROOT.SetBatch(True)

LOGGER = logging.getLogger('FCCAnalyses.process_info')

def getEntries(f):
    tf=ROOT.TFile.Open(f,"READ")
    tf.cd()
    tt=tf.Get("events")
    nevents=tt.GetEntries()
    tf.Close()
    return nevents


def getProcessInfo(process, prodTag, inputDir):
    '''
    Decide where to look for the filelist and eventlist.
    '''
    if prodTag is None and inputDir is None:
        LOGGER.error('The variable <prodTag> or <inputDir> is mandatory in '
                     'your analysis script!\nAborting...')
        sys.exit(3)
    elif prodTag is not None and inputDir is not None:
        LOGGER.error('The variables <prodTag> and <inputDir> can\'t be set '
                     'both at the same time in your analysis script!\n'
                     'Aborting...')
        sys.exit(3)

    if prodTag!=None:
        return getProcessInfoYaml(process, prodTag)
    elif inputDir!=None:
        return getProcessInfoFiles(process, inputDir)
    else:
        LOGGER.error('Problem, why are you here???\nAborting...')
        sys.exit(3)


def getProcessInfoFiles(process, inputDir):
    '''
    Get list of files and events from the specified location
    '''
    filelist=[]
    eventlist=[]
    filetest='{}/{}.root'.format(inputDir, process)
    dirtest='{}/{}'.format(inputDir, process)

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
        eventlist.append(getEntries(filetest))

    if os.path.isdir(dirtest):
        flist=glob.glob(dirtest+"/*.root")
        for f in flist:
            filelist.append(f)
            eventlist.append(getEntries(f))


    return filelist, eventlist


def getProcessInfoYaml(process, prodTag):
    '''
    Get list of files and events from the YAML file
    '''
    doc = None
    proc_dict_dirs = get_process_dict_dirs()
    yamlfilepath = None
    for path in proc_dict_dirs:
        yamlfilepath = os.path.join(path, 'yaml', prodTag, process, 'merge.yaml')
        if not os.path.isfile(yamlfilepath):
            continue
    if not yamlfilepath:
        LOGGER.error('Can\'t find the YAML file with process info!\n'
                     'Aborting...')
        sys.exit(3)

    with open(yamlfilepath) as ftmp:
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
            LOGGER.info('YAML file with process information successfully '
                        'loaded:\n%s', yamlfilepath)

    filelist = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
    eventlist = [f[1] for f in doc['merge']['outfiles']]
    return filelist, eventlist


def get_process_dict(proc_dict_location):
    '''
    Pick up the dictionary with process information
    '''
    if 'http://' in proc_dict_location or 'https://' in proc_dict_location:
        LOGGER.info('Getting process dictionary from the web:\n%s',
                    proc_dict_location)
        import urllib.request
        req = urllib.request.urlopen(proc_dict_location).read()
        try:
            proc_dict = json.loads(req.decode('utf-8'))
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

            with open(proc_dict_path, 'r') as infile:
                try:
                    proc_dict = json.load(infile)
                except json.decoder.JSONDecodeError:
                    LOGGER.error('Failed to parse process dictionary '
                                 'correctly!\nAborting...')
                    sys.exit(3)

        if not proc_dict:
            LOGGER.error('Process dictionary not found!\nAborting...')
            sys.exit(3)

    return proc_dict


def get_process_dict_dirs():
    '''
    Get search directories for the process dictionaries
    '''
    dirs = os.getenv('FCCDICTSDIR')
    if not dirs:
        LOGGER.error('Environment variable FCCDICTSDIR not defined!\n'
                     'Was the setup.sh file sourced properly?\n'
                     'Aborting...')
        sys.exit(3)
    dirs = dirs.split(':')
    dirs = [d for d in dirs if d]

    return dirs
