'''
The module takes care of building FCCAnalyses
'''

import os
import sys
import subprocess
import pathlib
import shutil
import logging


LOGGER = logging.getLogger('FCCAnalyses.build')


def run_subprocess(command: str, run_dir: str) -> None:
    '''
    Run subprocess in specified directory.
    Check only the return value, otherwise keep the subprocess connected to
    stdin/stout/stderr.
    '''
    try:
        with subprocess.Popen(command, cwd=run_dir) as proc:
            status: int = proc.wait()

            if status != 0:
                LOGGER.error('Error encountered!\nAborting...')
                sys.exit(3)

    except KeyboardInterrupt:
        LOGGER.error('Aborting...')
        sys.exit(0)


def build_analysis(mainparser) -> None:
    '''
    Main build steering function
    '''
    args = mainparser.parse_args()

    if 'LOCAL_DIR' not in os.environ:
        LOGGER.error('FCCAnalyses environment not set up correctly!\n'
                     'Aborting...')
        sys.exit(3)

    local_dir = os.environ.get('LOCAL_DIR')
    build_path = pathlib.Path(local_dir + '/build')
    install_path = pathlib.Path(local_dir + '/install')
    cmake_args = ['-DCMAKE_INSTALL_PREFIX=../install']

    LOGGER.info('Building analysis located in:\n%s', local_dir)

    if args.acts_on:
        LOGGER.info('Building also ACTS based analyzers...')
        cmake_args += ['-DWITH_ACTS=ON']

    if args.clean_build:
        LOGGER.info('Clearing build and install directories...')
        if build_path.is_dir():
            shutil.rmtree(build_path)
        if install_path.is_dir():
            shutil.rmtree(install_path)

    if not build_path.is_dir():
        LOGGER.info('Creating build directory...')
        os.makedirs(build_path)

        run_subprocess(['cmake'] + cmake_args + ['..'],
                       local_dir + '/build')

    if not install_path.is_dir():
        LOGGER.info('Creating install directory...')
        os.makedirs(install_path)

    run_subprocess(['make', f'-j{args.build_threads}', 'install'],
                   local_dir + '/build')
