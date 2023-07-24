'''
Handle process related information
'''

import os
import sys
import json
import yaml
import glob
import ROOT


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
    if prodTag==None and inputDir==None:
        print('The variable <prodTag> or <inputDir> is mandatory your analysis.py file, will exit')
        sys.exit(3)
    elif prodTag!=None and inputDir!=None:
        print('The variable <prodTag> and <inputDir> can not be set both at the same time in your analysis.py file, will exit')
        sys.exit(3)

    if prodTag!=None:
        return getProcessInfoYaml(process, prodTag)
    elif inputDir!=None:
        return getProcessInfoFiles(process, inputDir)
    else:
        print('problem, why are you here???, exit')
        sys.exist(3)


def getProcessInfoFiles(process, inputDir):
    '''
    Get list of files and events from the specified location
    '''
    filelist=[]
    eventlist=[]
    filetest='{}/{}.root'.format(inputDir, process)
    dirtest='{}/{}'.format(inputDir, process)

    if os.path.isfile(filetest) and os.path.isdir(dirtest):
        print ("----> For process {} both a file {} and a directory {} exist".format(process,filetest,dirtest))
        print ("----> Exactly one should be used, please check. Exit")
        sys.exit(3)

    if not os.path.isfile(filetest) and not os.path.isdir(dirtest):
        print ("----> For process {} neither a file {} nor a directory {} exist".format(process,filetest,dirtest))
        print ("----> Exactly one should be used, please check. Exit")
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
        print('----> Error: Can\'t find the YAML file with process info!')
        print('             Aborting...')
        sys.exit(3)

    with open(yamlfilepath) as ftmp:
        try:
            doc = yaml.load(ftmp, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
        except IOError as exc:
            print("----> Error: I/O error({0}): {1}".format(exc.errno, exc.strerror))
            print("             yamlfile: ", yamlfilepath)
        finally:
            print('----> Info: YAML file with process information successfully loaded:')
            print('            {}'.format(yamlfilepath))

    filelist = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
    eventlist = [f[1] for f in doc['merge']['outfiles']]
    return filelist, eventlist


def get_process_dict(proc_dict_location):
    '''
    Pick up the dictionary with process information
    '''
    if 'http://' in proc_dict_location or 'https://' in proc_dict_location:
        print('----> Info: Getting process dictionary from the web:')
        print('            {}'.format(proc_dict_location))
        import urllib.request
        req = urllib.request.urlopen(proc_dict_location).read()
        try:
            proc_dict = json.loads(req.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print('----> Error: Failed to parse process dictionary correctly!')
            print('             Aborting...')
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

            print('----> Info: Loading process dictionary from:')
            print('            {}'.format(proc_dict_path))

            with open(proc_dict_path, 'r') as infile:
                try:
                    proc_dict = json.load(infile)
                except json.decoder.JSONDecodeError:
                    print('----> Error: Failed to parse process dictionary '
                          'correctly!')
                    print('             Aborting...')
                    sys.exit(3)

        if not proc_dict:
            print('----> Error: Process dictionary not found!')
            print('             Aborting...')

    return proc_dict


def get_process_dict_dirs():
    '''
    Get search directories for the process dictionaries
    '''
    dirs = os.getenv('FCCDICTSDIR')
    if not dirs:
        print('----> Error: Evironment variable FCCDICTSDIR not defined.')
        print('             Was the setup.sh file sourced properly?')
        print('             Aborting...')
    dirs = dirs.split(':')
    dirs = [d for d in dirs if d]

    return dirs
