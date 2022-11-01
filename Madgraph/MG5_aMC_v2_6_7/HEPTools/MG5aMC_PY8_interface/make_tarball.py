#! /usr/bin/env python

import tarfile
import os
import glob

pjoin = os.path.join

local_path = os.path.abspath(os.path.dirname(os.path.realpath( __file__ )))

vetoed_files = ['MG5AMC_VERSION_ON_INSTALL','PYTHIA8_VERSION_ON_INSTALL','MG5aMC_PY8_interface_example_input_ckkwl.dat',
                'MG5aMC_PY8_interface_example_input_mlm.dat','pythia8_version','MG5aMC_PY8_interface']

files_to_add = [filepath for filepath in glob.glob(pjoin(local_path,'*')) if not os.path.basename(filepath) in vetoed_files]

tarball_name = 'MG5aMC_PY8_interface.tar.gz'
tarball_path = pjoin(local_path, tarball_name)

if os.path.exists(tarball_path):
    print( "Cleaning up existing archive at:\n  %s"%tarball_path)
    os.remove(pjoin(local_path, tarball_name))

tarball = tarfile.open(tarball_path,'w:gz')

for f in files_to_add:
    tarball.add(f,arcname=os.path.basename(f))

tarball.close()

print( "Tarball created at:\n   %s"%tarball_path)
