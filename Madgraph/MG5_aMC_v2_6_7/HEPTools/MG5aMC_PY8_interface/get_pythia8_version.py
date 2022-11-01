#! /usr/bin/env python

import sys
import os
import re
import subprocess
pjoin = os.path.join

local_path = os.path.abspath(os.path.dirname(os.path.realpath( __file__ )))

error_exit_code = 9

help_msg = \
"""Usage: python get_pythia8_version.py <Pythia8_installation_root_path>
   Ex:    python get_pythia8_version.py ~/Pythia/pythia8201
"""

if len(sys.argv)!=2:
    print( help_msg)
    sys.exit(error_exit_code)
elif sys.argv[1].lower().startswith('help') or sys.argv[1].lower().startswith('--help'):
    print( help_msg)
    sys.exit(error_exit_code)

pythia8_path = os.path.abspath(os.path.realpath(sys.argv[1]))

# The technique above didn't work, so we will try to obtain the version from the xml doc instead

version = None

def get_version_from_xml():
    if not os.path.exists(pjoin(pythia8_path,'share','Pythia8','xmldoc','Version.xml')):
        print( "Error in 'get_pythia8_version.py': could not get Pyhtia8 file \n  '%s'\n storing the version number"% \
               pjoin(local_path,'share','Pythia8','xmldoc','Version.xml'))
        return None

    versionfinder = re.compile('^\s*\<parmfix\s*name\=\"Pythia:versionNumber\"\s*default=\"(?P<version>[\d\.]+)\"\>')

    for line in open(pjoin(pythia8_path,'share','Pythia8','xmldoc','Version.xml')):
        match = versionfinder.match(line)
        if match:
            version = match.group('version')
            return version
    return None

def get_version_from_cpp():
    if os.path.exists(pjoin(local_path,'pythia8_version')):
        # Make sure to refresh the pythia8_version executable
        os.remove(pjoin(local_path,'pythia8_version'))

    # Try to compile pythia8_version
    try:
        p = subprocess.Popen(['g++','-o','pythia8_version','pythia8_version.cc',
                  '-I%s'%pjoin(pythia8_path,'include'),'-L%s'%pjoin(pythia8_path,'lib'),'-lpythia8'],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=local_path)
        (out, err) = p.communicate()
    except:
        return None

    if os.path.exists(pjoin(local_path,'pythia8_version')) and \
                          os.access(pjoin(local_path, 'pythia8_version'), os.X_OK):
        p = subprocess.Popen('./pythia8_version',
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=local_path)
        (out, err) = p.communicate()
        if re.match('^[\d|\.]+$',out):
            return '%.4f'%float(out.replace('\n',''))
    
    return None

version = get_version_from_xml()
if not version:
    version = get_version_from_cpp()

if not version:
    print( "Error in 'get_pythia8_version.py': could not find pythia8 version number (either from 'Version.xml' or from PYTHIA_VERSION C++ compiler macro).")
    sys.exit(error_exit_code)
else:
    print( version)
    sys.exit(0)
