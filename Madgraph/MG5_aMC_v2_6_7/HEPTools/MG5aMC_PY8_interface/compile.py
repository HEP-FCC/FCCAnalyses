#! /usr/bin/env python

import subprocess
import sys
import os
import shutil
import re

pjoin = os.path.join

local_path = os.path.abspath(os.path.dirname(os.path.realpath( __file__ )))

error_exit_code = 9

help_msg = \
"""Usage: python compile.py <Pythia8_installation_root_path>
   Ex:    python compile.py ~/Pythia/pythia8201
"""

def edit_makefile(path):
    text = []
    for line in open(path,'r'):
        if line.strip().startswith(('PREFIX_LIB=','PREFIX_INCLUDE=')):
            text.append(line.replace('PREFIX_', 'PREFIX_DO_NOT_USE_'))
        else:
            text.append(line)

    fsock = open(path, 'w')
    fsock.writelines(text)
    return
    
    


# When using only original PY8 makefiles, HEPMC2 will be linked dynamically.
# By default, the interface's makefile (which include PY8's ones) will link HEPMC2 statically.
_use_original_PY8_makefile = False

# Get tools versions requirement
min_mg5amc_version  = None
min_pythia8_version = None
for line in open(pjoin(local_path,'COMPATIBILITY')):
    mgamc_match   = re.match('^MIN_MGAMC_VERSION\s*(?P<version>[\d\.]+)\s*$',line)
    pythia8_match = re.match('^MIN_PYTHIA8_VERSION\s*(?P<version>[\d\.]+)\s*$',line)
    if mgamc_match:
        min_mg5amc_version = mgamc_match.group('version')
    if pythia8_match:
        min_pythia8_version = pythia8_match.group('version')

if min_mg5amc_version is None or min_pythia8_version is None:
    print( "Error, minimum required pythia8 and MG5_aMC version could not be retrieved"+\
          " from the file 'COMPATIBILITY', check it.")
    sys.exit(error_exit_code)

if '--pythia8_makefile' in sys.argv:
    sys.argv.remove('--pythia8_makefile')
    _use_original_PY8_makefile = True

if not len(sys.argv) in [2,3] :
    print( help_msg)
    sys.exit(error_exit_code)
elif sys.argv[1].lower().startswith('help') or sys.argv[1].lower().startswith('--help'):
    print( help_msg)
    sys.exit(error_exit_code)

pythia8_path = os.path.abspath(os.path.realpath(sys.argv[1]))

# Get Pythia_Version
p = subprocess.Popen([sys.executable,'get_pythia8_version.py', pythia8_path], stdout=subprocess.PIPE, 
                                             stderr=subprocess.STDOUT, cwd=local_path)
(out, err) = p.communicate()
out = out.decode().replace('\n','')

if not re.match('^[\d|\.]+$',out):
    print( "Error, could not retrieve Pythia8 version using script 'get_pythia8_version.py'. Check it.")
    sys.exit(error_exit_code)

pythia8_version = out

if float(out)<float(min_pythia8_version):
    print( "Error, the pythia8 version specified at:\n  %s\nseems older (%s) than the minimum requirement (>=%s) for this interface."%\
            (pythia8_path,pythia8_version,min_pythia8_version))
    sys.exit(error_exit_code)

# Guess
mg5amc_path = os.path.abspath(pjoin(local_path,os.pardir,os.pardir))
# If specified when invoking compile.py
if len(sys.argv) == 3:
    mg5amc_path = os.path.abspath(os.path.realpath(sys.argv[2]))

# Optional specification of the MG5_aMC version it is installed from
mg5amc_version_finder = re.compile('^\s*version\s*\=\s*(?P<version>[\d\.]+)\s*$')
mg5amc_version = None
if os.path.exists(pjoin(mg5amc_path,'VERSION')):
    for line in open(pjoin(mg5amc_path,'VERSION')):
        mgamc_version_match =  mg5amc_version_finder.match(line)
        if mgamc_version_match:
            mg5amc_version = mgamc_version_match.group('version')
            break
    if mg5amc_version is None:
        print( "Warning, could not find MG5_aMC version in '%s'."%pjoin(mg5amc_path,'VERSION'))

# Check that the minimum MG5 required version is met. 
if not mg5amc_version is None:
    for i, target_req in enumerate(min_mg5amc_version.split('.')):
        if i>=len(mg5amc_version.split('.')):
            break
        try:
            if int(mg5amc_version.split('.')[i])<int(target_req): 
                print( "Error, the MG5_aMC version specified at:\n  %s\nseems older (%s) than the minimum requirement (>=%s) for this interface."%\
                        (mg5amc_path,mg5amc_version,min_mg5amc_version))
                sys.exit(error_exit_code)
            elif int(mg5amc_version.split('.')[i])>int(target_req):
                break
        except ValueError:
            # Sometimes the MG version is not numerical in development versions
            pass

# Now proceed with the installation

if not os.path.exists(pjoin(pythia8_path,'share','Pythia8','examples','Makefile.inc')):
    print( "Error in MG5aMC_PY8_interface installer. Could not find file:\n   %s"%\
                       pjoin(pythia8_path,'share','Pythia8','examples','Makefile.inc'))
    sys.exit(error_exit_code)
shutil.copy(pjoin(pythia8_path,'share','Pythia8','examples','Makefile.inc'),
                                                 pjoin(local_path,'Makefile.inc'))
if not os.path.exists(pjoin(pythia8_path,'share','Pythia8','examples','Makefile')):
    print( "Error in MG5aMC_PY8_interface installer. Could not find file:\n   %s"%\
                           pjoin(pythia8_path,'share','Pythia8','examples','Makefile'))
    sys.exit(error_exit_code)
shutil.copy(pjoin(pythia8_path,'share','Pythia8','examples','Makefile'),
                                                     pjoin(local_path,'Makefile'))

edit_makefile(pjoin(local_path,'Makefile'))

if _use_original_PY8_makefile:
    shutil.move(pjoin(local_path,'MG5aMC_PY8_interface.cc'),pjoin(local_path,'main89.cc'))
    p = subprocess.Popen(['make','main89'], stdout=subprocess.PIPE, 
                                             stderr=subprocess.STDOUT, cwd=local_path)
else:
    # Make sure to refresh the executable
    if os.path.exists(pjoin(local_path,'MG5aMC_PY8_interface')):
        os.remove(pjoin(local_path,'MG5aMC_PY8_interface'))

    # First obtain the location of the HEPMC libraries
    Makefile_paths = dict(tuple(tok.strip() for tok in line.split('=')[:2]) for line in 
                    open(pjoin(local_path,'Makefile.inc'),'r') if len(line.split('='))>=2)
    try:
        HEPMC2LibPath = Makefile_paths['HEPMC2_LIB'].split("-Wl")[0].strip()
        if HEPMC2LibPath.startswith("-L"): HEPMC2LibPath = HEPMC2LibPath[2:]
    except KeyError:
        print( "The specified Pythia8 version does not seem to be installed with HEPMC2 support.")
        print( "This is required for the compilation of MG5aMC_PY8_interface.")
        sys.exit(error_exit_code)
    # Now copy the static HEPMC library locally so we are guaranteed that it will be compiled
    # statically
    if not os.path.isfile(pjoin(HEPMC2LibPath,'libHepMC.a')):
        print( "The version of HEPMC2 linked to Pythia8 seems not to include a static library.")
        print( "This is necessary for the default compilation of MG5aMC_PY8_interface.")
        print( "You can try again with the option --pythia8_makefile but HEPMC2 will need"+\
              " to be available at runtime.")
        sys.exit(error_exit_code)
    if not os.path.isdir(pjoin(local_path,'static_library_dependencies')):
        os.mkdir(pjoin(local_path,'static_library_dependencies'))
    shutil.copy(pjoin(HEPMC2LibPath,'libHepMC.a'),pjoin(local_path,'static_library_dependencies'))
    p = subprocess.Popen(['make','-f','Makefile_mg5amc_py8_interface_static','MG5aMC_PY8_interface',
            'CUSTOM_STATIC_HEPMC2_LIB=%s'%pjoin(local_path,'static_library_dependencies')], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=local_path)

(out, err) = p.communicate()

print( "------------------------------------------------")
print( "MG5aMC_PY8_interface compilation output log:\n%s"%out)
if err:
    print( "------------------------------------------------")
    print( "MG5aMC_PY8_interface compilation error log:\n%s"%err)
print( "------------------------------------------------")

if (_use_original_PY8_makefile and \
                   (not os.path.exists(pjoin(local_path, 'main89')) or \
                    not os.access(pjoin(local_path, 'main89'), os.X_OK))) or\
   (not _use_original_PY8_makefile and \
                   (not os.path.exists(pjoin(local_path, 'MG5aMC_PY8_interface')) or \
                    not os.access(pjoin(local_path, 'MG5aMC_PY8_interface'), os.X_OK))):
    print( "Error during the compilation of MG5aMC_PY8_interface:\n%s"%out)
    os.remove(pjoin(local_path,'Makefile'))
    os.remove(pjoin(local_path,'Makefile.inc'))
    if _use_original_PY8_makefile:
        shutil.move(pjoin(local_path,'main89.cc'),pjoin(local_path,'MG5aMC_PY8_interface.cc'))    
    sys.exit(error_exit_code)
else:
    print( "Successful compilation of the MG5aMC_PY8_interface.")
    if _use_original_PY8_makefile:
        shutil.move(pjoin(local_path,'main89'),pjoin(local_path,'MG5aMC_PY8_interface'))

os.remove(pjoin(local_path,'Makefile'))
os.remove(pjoin(local_path,'Makefile.inc'))
if _use_original_PY8_makefile:
    shutil.move(pjoin(local_path,'main89.cc'),pjoin(local_path,'MG5aMC_PY8_interface.cc'))
else:
    shutil.rmtree(pjoin(local_path,'static_library_dependencies'))

# Installation successful, register what version of Pythia8 and MG5 where used when installing this interface
open(pjoin(local_path,'MG5AMC_VERSION_ON_INSTALL'),'w').write('UNSPECIFIED' if mg5amc_version is None else mg5amc_version)
open(pjoin(local_path,'PYTHIA8_VERSION_ON_INSTALL'),'w').write(pythia8_version)

if p.returncode:
    sys.exit(p.returncode)
else:
    sys.exit(0)
