'''
The module takes care of building FCCAnalyses
'''

import os
import sys
import subprocess
import pathlib
import shutil


def run_subprocess(command, run_dir):
    '''
    Run subprocess in specified directory.
    Check only the return value, otherwise keep the subprocess connected to
    stdin/stout/stderr.
    '''
    try:
        proc = subprocess.Popen(command, cwd=run_dir)
        status = proc.wait()

        if status != 0:
            print('----> Error encountered!')
            print('      Aborting...')
            sys.exit(3)

    except KeyboardInterrupt:
        print('----> Aborting...')
        sys.exit(0)


def build_analysis(mainparser):
    '''
    Main build steering function
    '''
    args, _ = mainparser.parse_known_args()

    if 'LOCAL_DIR' not in os.environ:
        print('----> FCCAnalyses environment not set up correctly!')
        print('      Aborting...')
        sys.exit(3)

    local_dir = os.environ.get('LOCAL_DIR')
    build_path = pathlib.Path(local_dir + '/build')
    install_path = pathlib.Path(local_dir + '/install')

    print('----> Building analysis located in:')
    print('      ' + local_dir)

    if args.clean_build:
        print('----> Clearing build and install directories...')
        if build_path.is_dir():
            shutil.rmtree(build_path)
        if install_path.is_dir():
            shutil.rmtree(install_path)

    if not build_path.is_dir():
        print('----> Creating build directory...')
        os.makedirs(build_path)

        run_subprocess(['cmake', '-DCMAKE_INSTALL_PREFIX=../install', '..'],
                       local_dir + '/build')

    if not install_path.is_dir():
        print('----> Creating install directory...')
        os.makedirs(install_path)

    run_subprocess(['make', '-j{}'.format(args.build_threads), 'install'],
                   local_dir + '/build')
